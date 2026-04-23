from datetime import datetime

from pydantic import BaseModel

from database import EnrichmentStatus


class MovieBase(BaseModel):
    title: str
    director: str | None = None
    year: int | None = None
    official_media: str | None = None
    watch_link: str | None = None

    tmdb_id: int | None = None
    original_title: str | None = None
    poster_url: str | None = None
    backdrop_url: str | None = None
    tmdb_synopsis: str | None = None
    rating: float | None = None
    vote_count: int | None = None
    runtime: int | None = None
    genres: str | None = None

    imdb_rating: float | None = None
    imdb_votes: int | None = None

    wiki_summary: str | None = None
    wikipedia_url: str | None = None

    search_title: str | None = None
    slug: str | None = None

    enrichment_status: EnrichmentStatus | None = None


class MovieListItem(BaseModel):
    id: int
    title: str
    year: int | None = None
    poster_url: str | None = None
    search_title: str | None = None
    slug: str | None = None
    director: str | None = None
    rating: float | None = None
    watch_link: str | None = None

    class Config:
        from_attributes = True


class MovieResponse(MovieBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
