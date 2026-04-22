import unicodedata
import re


def normalize_for_search(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    cleaned = "".join(
        char for char in normalized if not unicodedata.category(char).startswith("M")
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
