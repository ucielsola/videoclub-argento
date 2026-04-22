from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MovieBase(BaseModel):
    title: str
    director: Optional[str] = None
    year: Optional[int] = None
    official_media: Optional[str] = None
    watch_link: Optional[str] = None

    # TMDB Data
    tmdb_id: Optional[int] = None
    original_title: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    synopsis: Optional[str] = None
    rating: Optional[float] = None
    vote_count: Optional[int] = None
    runtime: Optional[int] = None
    genres: Optional[str] = None

    # Search & URL helpers
    search_title: Optional[str] = None
    slug: Optional[str] = None


class MovieListItem(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    poster_url: Optional[str] = None
    search_title: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        from_attributes = True


class MovieResponse(MovieBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
