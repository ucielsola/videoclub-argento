import csv
import httpx
import io
import logging
from sqlalchemy.orm import Session
from database import Movie
from utils import normalize_for_search, generate_slug

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/158Jjw_BMEcVgqeVwjGFwLtbnQm2EPg20P2Z5SDUBW_c/export?format=csv&gid=0"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"


async def sync_movies(db: Session, tmdb_api_key: str):
    logger.info("Starting sync process...")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # 1. Download CSV
        logger.info(f"Downloading CSV from {CSV_URL}")
        try:
            response = await client.get(CSV_URL, follow_redirects=True)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to download CSV: {e}")
            return 0

        # 2. Skip first 10 lines and parse CSV
        lines = response.text.splitlines()
        logger.info(f"Fetched {len(lines)} lines from CSV.")
        csv_data = "\n".join(lines[10:])
        reader = csv.DictReader(io.StringIO(csv_data))

        # 3. Delta Sync: Get existing movies
        logger.info("Checking existing movies in database...")
        existing_movies = db.query(Movie).all()
        existing_set = {
            f"{m.title}_{m.director}_{m.year}".lower().strip() for m in existing_movies
        }

        movies_to_process = []
        for row in reader:
            title = row.get("Nombre", "").strip()
            director = row.get("Director", "").strip()
            year_str = row.get("Año", "").strip()

            if not title:
                continue

            try:
                year = int(year_str) if year_str else None
            except ValueError:
                year = None

            key = f"{title}_{director}_{year}".lower().strip()
            if key not in existing_set:
                movies_to_process.append(
                    {
                        "title": title,
                        "director": director,
                        "year": year,
                        "official_media": row.get("Medios oficiales", ""),
                        "watch_link": row.get("Link", ""),
                    }
                )

        logger.info(f"Found {len(movies_to_process)} new movies to process.")

        # 4. Enrich with TMDB and insert
        count = 0
        for i, item in enumerate(movies_to_process):
            logger.info(
                f"[{i + 1}/{len(movies_to_process)}] Processing: {item['title']}"
            )

            # Check for duplicate in DB
            existing = (
                db.query(Movie).filter(Movie.watch_link == item["watch_link"]).first()
            )
            if existing:
                logger.info(
                    f"  Skipping: {item['title']} (already in DB via watch_link)"
                )
                continue

            tmdb_data = None

            if tmdb_api_key:
                params = {
                    "query": item["title"],
                    "language": "es-AR",
                    "api_key": tmdb_api_key,
                }
                if item["year"]:
                    params["year"] = item["year"]

                try:
                    tmdb_res = await client.get(TMDB_SEARCH_URL, params=params)
                    tmdb_res.raise_for_status()
                    results = tmdb_res.json().get("results", [])

                    if results:
                        movie_id = results[0].get("id")
                        details_res = await client.get(
                            f"{TMDB_DETAILS_URL}{movie_id}",
                            params={"language": "es-AR", "api_key": tmdb_api_key},
                        )
                        details_res.raise_for_status()
                        tmdb_data = details_res.json()
                        logger.info(f"  Enriched with TMDB: {item['title']}")
                    else:
                        logger.warning(f"  No TMDB results for: {item['title']}")
                except Exception as e:
                    logger.error(f"  Error fetching TMDB data for {item['title']}: {e}")

            new_movie = Movie(
                title=item["title"],
                director=item["director"],
                year=item["year"],
                official_media=item["official_media"],
                watch_link=item["watch_link"],
                search_title=normalize_for_search(item["title"]),
                slug=generate_slug(item["title"], item["year"]),
            )

            if tmdb_data:
                new_movie.tmdb_id = tmdb_data.get("id")
                new_movie.original_title = tmdb_data.get("original_title")
                new_movie.synopsis = tmdb_data.get("overview")
                new_movie.rating = tmdb_data.get("vote_average")
                new_movie.vote_count = tmdb_data.get("vote_count")
                new_movie.runtime = tmdb_data.get("runtime")

                if tmdb_data.get("poster_path"):
                    new_movie.poster_url = (
                        f"{TMDB_IMAGE_BASE}{tmdb_data.get('poster_path')}"
                    )
                if tmdb_data.get("backdrop_path"):
                    new_movie.backdrop_url = (
                        f"{TMDB_BACKDROP_BASE}{tmdb_data.get('backdrop_path')}"
                    )
                if tmdb_data.get("genres"):
                    new_movie.genres = ", ".join(
                        [g["name"] for g in tmdb_data.get("genres")]
                    )

            db.add(new_movie)
            try:
                db.commit()
                count += 1
                logger.info(f"  Successfully saved: {item['title']}")
            except Exception as e:
                db.rollback()
                logger.error(f"  Database error saving {item['title']}: {e}")

        logger.info(f"Sync complete. Processed {count} new movies.")
        return count
