from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session, load_only

from database import Movie, get_db, init_db, settings
from etl import sync_movies
from schemas import MovieListItem, MovieResponse

init_db()


def get_cors_origins() -> list[str]:
    origins = settings.CORS_ORIGINS
    if origins == "*":
        return ["*"]
    return [o.strip() for o in origins.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Video Club Argento API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Video Club Argento API"}


@app.get("/movies", response_model=list[MovieListItem])
def get_movies(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    movies = (
        db.query(Movie)
        .options(
            load_only(
                Movie.id,
                Movie.title,
                Movie.year,
                Movie.poster_url,
                Movie.search_title,
                Movie.slug,
                Movie.director,
                Movie.rating,
                Movie.watch_link,
                Movie.enrichment_status,
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return movies


@app.get("/movies/director/{director}", response_model=list[MovieListItem])
def get_movies_by_director(director: str, db: Session = Depends(get_db)):
    movies = (
        db.query(Movie)
        .options(
            load_only(
                Movie.id,
                Movie.title,
                Movie.year,
                Movie.poster_url,
                Movie.search_title,
                Movie.slug,
                Movie.director,
                Movie.rating,
                Movie.watch_link,
                Movie.enrichment_status,
            )
        )
        .filter(sa_func.lower(Movie.director) == director.lower())
        .all()
    )
    return movies


@app.get("/movies/slug/{slug}", response_model=MovieResponse)
def get_movie_by_slug(slug: str, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.slug == slug).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/sheets/sync")
async def trigger_sync(db: Session = Depends(get_db)):
    try:
        count = await sync_movies(db, settings.TMDB_API_KEY, settings.OMDB_API_KEY)
        return {"message": f"Sync completed successfully. {count} new movies added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
