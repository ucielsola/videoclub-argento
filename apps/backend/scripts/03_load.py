#!/usr/bin/env python3
"""
Gold Layer: Load to PostgreSQL
Reads processed data from Silver layer and batch upserts to PostgreSQL
using on_conflict_do_update on the slug field.
"""

import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Movie, SessionLocal, settings, EnrichmentStatus

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
BATCH_SIZE = settings.BATCH_SIZE


def load_processed_movies() -> list[dict]:
    path = PROCESSED_DIR / "movies.json"
    if not path.exists():
        logger.error("Run 02_transform.py first - no processed data found")
        sys.exit(1)
    return json.loads(path.read_text())


def create_upsert_stmt(movie_dict: dict):
    from sqlalchemy.dialects.postgresql import insert
    from sqlalchemy import insert as sql_insert

    stmt = insert(Movie).values(**movie_dict)
    stmt = stmt.on_conflict_do_update(
        index_elements=["slug"],
        set_={
            "title": stmt.excluded.title,
            "director": stmt.excluded.director,
            "year": stmt.excluded.year,
            "official_media": stmt.excluded.official_media,
            "watch_link": stmt.excluded.watch_link,
            "tmdb_id": stmt.excluded.tmdb_id,
            "original_title": stmt.excluded.original_title,
            "poster_url": stmt.excluded.poster_url,
            "backdrop_url": stmt.excluded.backdrop_url,
            "tmdb_synopsis": stmt.excluded.tmdb_synopsis,
            "rating": stmt.excluded.rating,
            "vote_count": stmt.excluded.vote_count,
            "runtime": stmt.excluded.runtime,
            "genres": stmt.excluded.genres,
            "imdb_rating": stmt.excluded.imdb_rating,
            "imdb_votes": stmt.excluded.imdb_votes,
            "wiki_summary": stmt.excluded.wiki_summary,
            "wikipedia_url": stmt.excluded.wikipedia_url,
            "search_title": stmt.excluded.search_title,
            "enrichment_status": EnrichmentStatus.COMPLETE,
        },
    )
    return stmt


def batch_upsert(movies: list[dict], db, batch_size: int = BATCH_SIZE):
    total = len(movies)
    inserted = 0
    updated = 0

    for i in range(0, total, batch_size):
        batch = movies[i : i + batch_size]
        logger.info(
            f"Processing batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size} ({len(batch)} records)"
        )

        for movie in batch:
            movie["enrichment_status"] = EnrichmentStatus.COMPLETE
            stmt = create_upsert_stmt(movie)
            try:
                db.execute(stmt)
            except Exception as e:
                logger.error(f"Error upserting {movie.get('title')}: {e}")

        try:
            db.commit()
            inserted += len(batch)
            logger.info(f"Committed {len(batch)} records")
        except Exception as e:
            db.rollback()
            logger.error(f"Batch commit error: {e}")

    return inserted, updated


def main():
    movies = load_processed_movies()
    logger.info(f"Loading {len(movies)} movies to PostgreSQL...")

    db = SessionLocal()
    try:
        inserted, updated = batch_upsert(movies, db)
        logger.info(f"Load complete! {inserted} records upserted.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
