from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import EnrichmentStatus


class MovieBase(BaseModel):
    title: str
    director: Optional[str] = None
    year: Optional[int] = None
    official_media: Optional[str] = None
    watch_link: Optional[str] = None

    tmdb_id: Optional[int] = None
    original_title: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    tmdb_synopsis: Optional[str] = None
    rating: Optional[float] = None
    vote_count: Optional[int] = None
    runtime: Optional[int] = None
    genres: Optional[str] = None

    imdb_rating: Optional[float] = None
    imdb_votes: Optional[int] = None

    wiki_summary: Optional[str] = None
    wikipedia_url: Optional[str] = None

    search_title: Optional[str] = None
    slug: Optional[str] = None

    enrichment_status: Optional[EnrichmentStatus] = None


class MovieListItem(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    poster_url: Optional[str] = None
    search_title: Optional[str] = None
    slug: Optional[str] = None
    director: Optional[str] = None
    rating: Optional[float] = None
    watch_link: Optional[str] = None

    class Config:
        from_attributes = True


class MovieResponse(MovieBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
