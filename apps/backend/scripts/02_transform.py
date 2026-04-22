#!/usr/bin/env python3
"""
Silver Layer: Transform & Normalize
Reads raw JSON from Bronze layer, merges sources, applies normalization,
and saves processed data to data/processed/.
"""

import json
import logging
import os
import sys
import unicodedata
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"


def ensure_dirs():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_for_search(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    cleaned = "".join(
        c for c in normalized if not unicodedata.category(c).startswith("M")
    )
    cleaned = cleaned.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def generate_slug(title: str, year: int | None) -> str:
    slug = normalize_for_search(title)
    if year:
        slug = f"{slug}-{year}"
    return slug


def load_raw_movies() -> list[dict]:
    sheets_path = RAW_DIR / "sheets" / "google-sheets.json"
    if not sheets_path.exists():
        logger.error("Run 01_ingest.py first - no sheets data found")
        sys.exit(1)

    data = json.loads(sheets_path.read_text())
    return data.get("movies", [])


def load_source_data(slug: str, source: str) -> dict | None:
    path = RAW_DIR / source / f"{slug}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def transform_movie(raw_movie: dict) -> dict:
    slug = raw_movie["slug"]
    title = raw_movie["title"]
    year = raw_movie.get("year")

    tmdb = load_source_data(slug, "tmdb")
    omdb = load_source_data(slug, "omdb") or load_source_data(f"{slug}-omdb", "omdb")
    wiki = load_source_data(slug, "wikipedia")

    search_title = normalize_for_search(title)
    final_slug = generate_slug(title, year)

    transformed = {
        "title": title,
        "director": raw_movie.get("director"),
        "year": year,
        "official_media": raw_movie.get("official_media"),
        "watch_link": raw_movie.get("watch_link"),
        "search_title": search_title,
        "slug": final_slug,
    }

    if tmdb and not tmdb.get("not_found"):
        transformed.update(
            {
                "tmdb_id": tmdb.get("id"),
                "original_title": tmdb.get("original_title"),
                "poster_url": f"{TMDB_IMAGE_BASE}{tmdb.get('poster_path')}"
                if tmdb.get("poster_path")
                else None,
                "backdrop_url": f"{TMDB_BACKDROP_BASE}{tmdb.get('backdrop_path')}"
                if tmdb.get("backdrop_path")
                else None,
                "tmdb_synopsis": tmdb.get("overview"),
                "rating": tmdb.get("vote_average"),
                "vote_count": tmdb.get("vote_count"),
                "runtime": tmdb.get("runtime"),
                "genres": ", ".join([g["name"] for g in tmdb.get("genres", [])])
                if tmdb.get("genres")
                else None,
            }
        )

    if omdb and omdb.get("Response") == "True":
        imdb_rating = omdb.get("imdbRating")
        imdb_votes = omdb.get("imdbVotes")
        transformed.update(
            {
                "imdb_rating": float(imdb_rating)
                if imdb_rating and imdb_rating != "N/A"
                else None,
                "imdb_votes": int(imdb_votes.replace(",", ""))
                if imdb_votes and imdb_votes != "N/A"
                else None,
            }
        )
        if not transformed.get("tmdb_synopsis") and omdb.get("Plot") != "N/A":
            transformed["tmdb_synopsis"] = omdb.get("Plot")

    if wiki and not wiki.get("not_found"):
        transformed.update(
            {
                "wiki_summary": wiki.get("extract"),
                "wikipedia_url": wiki.get("content_urls", {}).get("page"),
            }
        )

    return transformed


def handle_slug_collision(
    processed_movies: list[dict], slug: str, base_slug: str
) -> str:
    existing_slugs = {m["slug"] for m in processed_movies}
    if slug not in existing_slugs:
        return slug

    counter = 1
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1
    return f"{base_slug}-{counter}"


def main():
    ensure_dirs()

    raw_movies = load_raw_movies()
    logger.info(f"Transforming {len(raw_movies)} movies...")

    processed = []
    for i, raw in enumerate(raw_movies):
        logger.info(f"[{i + 1}/{len(raw_movies)}] Transforming: {raw['title']}")

        transformed = transform_movie(raw)

        transformed["slug"] = handle_slug_collision(
            processed,
            transformed["slug"],
            generate_slug(transformed["title"], transformed.get("year")),
        )

        processed.append(transformed)

    output_path = PROCESSED_DIR / "movies.json"
    output_path.write_text(json.dumps(processed, ensure_ascii=False, indent=2))
    logger.info(
        f"Silver transformation complete! Saved {len(processed)} movies to {output_path}"
    )


if __name__ == "__main__":
    main()
