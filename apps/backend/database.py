import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://videouser:videopassword@localhost:5432/videoclub"
    TMDB_API_KEY: str = ""

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
    synopsis = Column(Text)
    rating = Column(Float)
    vote_count = Column(Integer)
    runtime = Column(Integer)
    genres = Column(String)

    # Search & URL helpers
    search_title = Column(String, index=True)
    slug = Column(String, index=True, unique=True)

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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
