#!/usr/bin/env python3
"""
Self-Healing Background Worker
Runs as a separate process to resolve "Enrichment Debt".
Queries DB for PENDING movies, fetches/enriches them, and updates status.
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import EnrichmentStatus, Movie, SessionLocal, settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BATCH_SIZE = 10
THROTTLE_SECONDS = 5


async def fetch_tmdb(client, title: str, year: int | None):
    if not settings.TMDB_API_KEY:
        return None

    params = {"query": title, "language": "es-AR", "api_key": settings.TMDB_API_KEY}
    if year:
        params["year"] = year

    try:
        res = await client.get(settings.TMDB_SEARCH_URL, params=params)
        res.raise_for_status()
        results = res.json().get("results", [])
        if not results:
            return None

        movie_id = results[0]["id"]
        details = await client.get(
            f"{settings.TMDB_DETAILS_URL}{movie_id}",
            params={"language": "es-AR", "api_key": settings.TMDB_API_KEY},
        )
        details.raise_for_status()
        return details.json()
    except Exception as e:
        logger.error(f"TMDB error for {title}: {e}")
        return None


async def fetch_omdb(client, imdb_id: str | None, title: str, year: int | None):
    if not settings.OMDB_API_KEY:
        return None

    params = {"apikey": settings.OMDB_API_KEY, "t": title}
    if year:
        params["y"] = year

    try:
        res = await client.get(
            settings.OMDB_URL,
            params=params,
            headers={"User-Agent": "VideoClubArgento/1.0"},
        )
        res.raise_for_status()
        data = res.json()
        return data if data.get("Response") == "True" else None
    except Exception as e:
        logger.error(f"OMDb error for {title}: {e}")
        return None


async def fetch_wikipedia(client, title: str, year: int | None):
    search_query = f"{title} {year} película" if year else f"{title} película"

    try:
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": search_query,
            "format": "json",
            "utf8": 1,
            "srlimit": 1,
        }
        search_res = await client.get(
            settings.WIKI_ACTION_API,
            params=search_params,
            headers={"User-Agent": "VideoClubArgento/1.0 (contact@example.com)"},
        )
        search_res.raise_for_status()
        search_data = search_res.json()

        pages = search_data.get("query", {}).get("search", [])
        if not pages:
            return None

        page_title = pages[0]["title"]
        summary_res = await client.get(
            f"{settings.WIKI_SUMMARY_API}/{page_title.replace(' ', '_')}",
            headers={"User-Agent": "VideoClubArgento/1.0 (contact@example.com)"},
        )
        summary_res.raise_for_status()
        return summary_res.json()
    except Exception as e:
        logger.error(f"Wikipedia error for {title}: {e}")
        return None


async def enrich_movie(movie_id: int, title: str, year: int | None):
    async with asyncio.timeout(30):
        async with asyncio.ClientSession() as client:
            tmdb_data = await fetch_tmdb(client, title, year)

            imdb_id = tmdb_data.get("imdb_id") if tmdb_data else None
            omdb_data = await fetch_omdb(client, imdb_id, title, year)
            wiki_data = await fetch_wikipedia(client, title, year)

            db = SessionLocal()
            try:
                movie = db.query(Movie).filter(Movie.id == movie_id).first()
                if not movie:
                    logger.error(f"Movie {movie_id} not found")
                    return False

                if tmdb_data:
                    movie.tmdb_id = tmdb_data.get("id")
                    movie.original_title = tmdb_data.get("original_title")
                    if tmdb_data.get("poster_path"):
                        movie.poster_url = f"{settings.TMDB_IMAGE_BASE}{tmdb_data.get('poster_path')}"
                    if tmdb_data.get("backdrop_path"):
                        movie.backdrop_url = f"{settings.TMDB_BACKDROP_BASE}{tmdb_data.get('backdrop_path')}"
                    if not movie.tmdb_synopsis and tmdb_data.get("overview"):
                        movie.tmdb_synopsis = tmdb_data.get("overview")
                    if not movie.rating and tmdb_data.get("vote_average"):
                        movie.rating = tmdb_data.get("vote_average")
                    if not movie.vote_count and tmdb_data.get("vote_count"):
                        movie.vote_count = tmdb_data.get("vote_count")
                    if not movie.runtime and tmdb_data.get("runtime"):
                        movie.runtime = tmdb_data.get("runtime")
                    if not movie.genres and tmdb_data.get("genres"):
                        movie.genres = ", ".join([g["name"] for g in tmdb_data.get("genres", [])])

                if omdb_data:
                    if omdb_data.get("imdbRating") and omdb_data.get("imdbRating") != "N/A":
                        movie.imdb_rating = float(omdb_data.get("imdbRating"))
                    if omdb_data.get("imdbVotes") and omdb_data.get("imdbVotes") != "N/A":
                        movie.imdb_votes = int(omdb_data.get("imdbVotes").replace(",", ""))
                    if not movie.tmdb_synopsis and omdb_data.get("Plot") != "N/A":
                        movie.tmdb_synopsis = omdb_data.get("Plot")

                if wiki_data:
                    movie.wiki_summary = wiki_data.get("extract")
                    movie.wikipedia_url = wiki_data.get("content_urls", {}).get("desktop", {}).get("page")

                movie.enrichment_status = EnrichmentStatus.COMPLETE
                db.commit()
                logger.info(f"Enriched: {title}")
                return True

            except Exception as e:
                db.rollback()
                logger.error(f"Error enriching {title}: {e}")
                movie = db.query(Movie).filter(Movie.id == movie_id).first()
                if movie:
                    movie.enrichment_status = EnrichmentStatus.FAILED
                    db.commit()
                return False
            finally:
                db.close()


async def worker_loop():
    logger.info("Starting self-healing worker...")

    while True:
        db = SessionLocal()
        try:
            movies = (
                db.query(Movie)
                .filter(Movie.enrichment_status == EnrichmentStatus.PENDING)
                .order_by(Movie.id)
                .limit(BATCH_SIZE)
                .all()
            )

            if not movies:
                logger.info("No pending movies. Sleeping 30s...")
                await asyncio.sleep(30)
                continue

            logger.info(f"Found {len(movies)} pending movies to process")

            for movie in movies:
                db.query(Movie).filter(Movie.id == movie.id).update({"enrichment_status": EnrichmentStatus.PROCESSING})
                db.commit()

                success = await enrich_movie(movie.id, movie.title, movie.year)

                if not success:
                    logger.warning(f"Failed to enrich: {movie.title}")

                await asyncio.sleep(THROTTLE_SECONDS)

        except Exception as e:
            logger.error(f"Worker error: {e}")
            await asyncio.sleep(10)
        finally:
            db.close()


if __name__ == "__main__":
    asyncio.run(worker_loop())
