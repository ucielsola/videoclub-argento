import re
import unicodedata

from sqlalchemy.orm import Session


def normalize_for_search(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    cleaned = "".join(char for char in normalized if not unicodedata.category(char).startswith("M"))
    cleaned = cleaned.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def generate_slug(title: str, year: int | None) -> str:
    slug = normalize_for_search(title)
    if year:
        slug = f"{slug}-{year}"
    return slug


def get_unique_slug(db: Session, title: str, year: int | None) -> str:
    from database import Movie

    base_slug = generate_slug(title, year)
    slug = base_slug

    counter = 1
    while db.query(Movie).filter(Movie.slug == slug).first():
        counter += 1
        slug = f"{base_slug}-{counter}"

    return slug
