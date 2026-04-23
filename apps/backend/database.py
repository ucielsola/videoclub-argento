from enum import StrEnum

from pydantic_settings import BaseSettings
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


class EnrichmentStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://videouser:videopassword@localhost:5432/videoclub"
    TMDB_API_KEY: str = ""
    OMDB_API_KEY: str = ""

    CSV_URL: str = (
        "https://docs.google.com/spreadsheets/d/158Jjw_BMEcVgqeVwjGFwLtbnQm2EPg20P2Z5SDUBW_c/export?format=csv&gid=0"
    )
    TMDB_SEARCH_URL: str = "https://api.themoviedb.org/3/search/movie"
    TMDB_DETAILS_URL: str = "https://api.themoviedb.org/3/movie/"
    TMDB_IMAGE_BASE: str = "https://image.tmdb.org/t/p/w500"
    TMDB_BACKDROP_BASE: str = "https://image.tmdb.org/t/p/w1280"
    OMDB_URL: str = "https://www.omdbapi.com/"
    WIKI_ACTION_API: str = "https://es.wikipedia.org/w/api.php"
    WIKI_SUMMARY_API: str = "https://es.wikipedia.org/api/rest_v1/page/summary"

    CORS_ORIGINS: str = "*"
    BATCH_SIZE: int = 200

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)

    # CSV Data
    title = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    official_media = Column(String)
    watch_link = Column(String, unique=True, index=True)

    # TMDB Data
    tmdb_id = Column(Integer, unique=True, index=True)
    original_title = Column(String)
    poster_url = Column(String)
    backdrop_url = Column(String)
    tmdb_synopsis = Column(Text)
    rating = Column(Float)
    vote_count = Column(Integer)
    runtime = Column(Integer)
    genres = Column(String)

    # OMDb Data
    imdb_rating = Column(Float)
    imdb_votes = Column(Integer)

    # Wikipedia Data
    wiki_summary = Column(Text)
    wikipedia_url = Column(String)

    # Search & URL helpers
    search_title = Column(String, index=True)
    slug = Column(String, index=True)

    # Self-Healing
    enrichment_status = Column(SQLEnum(EnrichmentStatus), default=EnrichmentStatus.PENDING, index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
