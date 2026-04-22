import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import SessionLocal, Movie, settings
from utils import normalize_for_search, get_unique_slug
import logging
import httpx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 200
OMDB_URL = "https://www.omdbapi.com/"


async def enrich_with_omdb(client: httpx.AsyncClient, movie: Movie):
    if not settings.OMDB_API_KEY:
        return None

    if movie.tmdb_id and movie.rating and movie.rating >= 7.0 and movie.synopsis:
        return None

    omdb_params = {
        "apikey": settings.OMDB_API_KEY,
        "t": movie.title,
    }
    if movie.year:
        omdb_params["y"] = movie.year

    try:
        omdb_res = await client.get(OMDB_URL, params=omdb_params)
        omdb_res.raise_for_status()
        return omdb_res.json()
    except Exception as e:
        logger.error(f"  OMDb error for {movie.title}: {e}")
        return None


def migrate():
    db = SessionLocal()
    total = 0
    updated = 0

    try:
        movies = db.query(Movie).all()
        total = len(movies)
        logger.info(f"Found {total} movies to migrate.")

        batch = []
        for movie in movies:
            movie.search_title = normalize_for_search(movie.title)
            movie.slug = get_unique_slug(db, movie.title, movie.year)
            batch.append(movie)

            if len(batch) >= BATCH_SIZE:
                db.commit()
                updated += len(batch)
                logger.info(f"  Committed batch: {updated}/{total}")
                batch = []

        if batch:
            db.commit()
            updated += len(batch)
            logger.info(f"  Committed final batch: {updated}/{total}")

        logger.info(f"Migration complete. Updated {updated}/{total} movies.")

    except Exception as e:
        db.rollback()
        logger.error(f"Migration failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
