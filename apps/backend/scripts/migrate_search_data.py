import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import SessionLocal, Movie
from utils import normalize_for_search, generate_slug
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 500


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
            movie.slug = generate_slug(movie.title, movie.year)
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
