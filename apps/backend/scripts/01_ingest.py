#!/usr/bin/env python3
"""
Bronze Layer: Raw Ingestion
Fetches data from external sources (Google Sheets, TMDB, OMDb, Wikipedia)
and saves raw JSON to local cache.
"""

import asyncio
import csv
import httpx
import io
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
CACHE_DIRS = {
    "sheets": DATA_DIR / "sheets",
    "tmdb": DATA_DIR / "tmdb",
    "omdb": DATA_DIR / "omdb",
    "wikipedia": DATA_DIR / "wikipedia",
}


def ensure_dirs():
    for d in CACHE_DIRS.values():
        d.mkdir(parents=True, exist_ok=True)


def get_cache_path(source: str, slug: str) -> Path:
    return CACHE_DIRS[source] / f"{slug}.json"


def load_cached(source: str, slug: str) -> dict | None:
    path = get_cache_path(source, slug)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None


def save_cache(source: str, slug: str, data: dict):
    path = get_cache_path(source, slug)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def generate_slug(title: str, year: int | None) -> str:
    import unicodedata
    import re

    normalized = unicodedata.normalize("NFD", title)
    cleaned = "".join(
        c for c in normalized if not unicodedata.category(c).startswith("M")
    )
    cleaned = cleaned.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    cleaned = re.sub(r"\s+", "-", cleaned).strip("-")
    if year:
        cleaned = f"{cleaned}-{year}"
    return cleaned


async def fetch_csv() -> list[dict]:
    slug = "google-sheets"
    cached = load_cached("sheets", slug)
    if cached:
        logger.info("Using cached Google Sheets data")
        return cached["movies"]

    logger.info(f"Fetching CSV from {settings.CSV_URL}")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(settings.CSV_URL)
        response.raise_for_status()

    lines = response.text.splitlines()
    csv_data = "\n".join(lines[10:])
    reader = csv.DictReader(io.StringIO(csv_data))

    movies = []
    for row in reader:
        title = row.get("Nombre", "").strip()
        if not title:
            continue

        try:
            year = (
                int(row.get("Año", "").strip()) if row.get("Año", "").strip() else None
            )
        except ValueError:
            year = None

        slug = generate_slug(title, year)
        movies.append(
            {
                "title": title,
                "director": row.get("Director", "").strip(),
                "year": year,
                "official_media": row.get("Medios oficiales", ""),
                "watch_link": row.get("Link", ""),
                "slug": slug,
            }
        )

    save_cache(
        "sheets", slug, {"fetched_at": datetime.now().isoformat(), "movies": movies}
    )
    logger.info(f"Fetched {len(movies)} movies from CSV")
    return movies


async def fetch_tmdb(
    client: httpx.AsyncClient, title: str, year: int | None, slug: str
) -> dict | None:
    cached = load_cached("tmdb", slug)
    if cached:
        return cached

    if not settings.TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not set")
        return None

    params = {"query": title, "language": "es-AR", "api_key": settings.TMDB_API_KEY}
    if year:
        params["year"] = year

    try:
        res = await client.get(settings.TMDB_SEARCH_URL, params=params)
        res.raise_for_status()
        results = res.json().get("results", [])

        if not results:
            logger.warning(f"No TMDB results for: {title}")
            save_cache("tmdb", slug, {"not_found": True})
            return None

        movie_id = results[0]["id"]
        details_res = await client.get(
            f"{settings.TMDB_DETAILS_URL}{movie_id}",
            params={"language": "es-AR", "api_key": settings.TMDB_API_KEY},
        )
        details_res.raise_for_status()
        data = details_res.json()

        save_cache("tmdb", slug, data)
        logger.info(f"Enriched TMDB: {title}")
        return data

    except Exception as e:
        logger.error(f"TMDB error for {title}: {e}")
        return None


async def fetch_omdb(
    client: httpx.AsyncClient,
    imdb_id: str | None,
    title: str,
    year: int | None,
    slug: str,
) -> dict | None:
    if not imdb_id:
        slug_fallback = f"{slug}-omdb"
        cached = load_cached("omdb", slug_fallback)
        if cached:
            return cached
    else:
        cached = load_cached("omdb", imdb_id)
        if cached:
            return cached

    if not settings.OMDB_API_KEY:
        logger.warning("OMDB_API_KEY not set")
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

        if data.get("Response") != "True":
            return None

        if imdb_id:
            save_cache("omdb", imdb_id, data)
        else:
            save_cache("omdb", f"{slug}-omdb", data)
        logger.info(f"Enriched OMDb: {title}")
        return data

    except Exception as e:
        logger.error(f"OMDb error for {title}: {e}")
        return None


async def fetch_wikipedia(
    client: httpx.AsyncClient, title: str, year: int | None, slug: str
) -> dict | None:
    cached = load_cached("wikipedia", slug)
    if cached:
        return cached

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
            logger.warning(f"No Wikipedia results for: {title}")
            save_cache("wikipedia", slug, {"not_found": True})
            return None

        page_title = pages[0]["title"]

        summary_res = await client.get(
            f"{settings.WIKI_SUMMARY_API}/{page_title.replace(' ', '_')}",
            headers={"User-Agent": "VideoClubArgento/1.0 (contact@example.com)"},
        )
        summary_res.raise_for_status()
        summary_data = summary_res.json()

        result = {
            "title": summary_data.get("title"),
            "extract": summary_data.get("extract"),
            "content_urls": summary_data.get("content_urls", {}).get("desktop", {}),
        }

        save_cache("wikipedia", slug, result)
        logger.info(f"Enriched Wikipedia: {title}")
        return result

    except Exception as e:
        logger.error(f"Wikipedia error for {title}: {e}")
        return None


async def ingest_movie(client: httpx.AsyncClient, movie: dict):
    slug = movie["slug"]
    title = movie["title"]
    year = movie["year"]

    tmdb_data = await fetch_tmdb(client, title, year, slug)

    imdb_id = tmdb_data.get("imdb_id") if tmdb_data else None
    omdb_data = await fetch_omdb(client, imdb_id, title, year, slug)

    wiki_data = await fetch_wikipedia(client, title, year, slug)

    return {
        "source": movie,
        "tmdb": tmdb_data,
        "omdb": omdb_data,
        "wikipedia": wiki_data,
    }


async def main():
    ensure_dirs()

    movies = await fetch_csv()
    logger.info(f"Starting ingestion for {len(movies)} movies...")

    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        for i, movie in enumerate(movies):
            logger.info(f"[{i + 1}/{len(movies)}] Ingesting: {movie['title']}")
            await ingest_movie(client, movie)
            await asyncio.sleep(0.2)

    logger.info("Bronze ingestion complete!")


if __name__ == "__main__":
    asyncio.run(main())
