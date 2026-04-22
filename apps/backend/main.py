from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, init_db, Movie, settings
from schemas import MovieResponse
from etl import sync_movies
from fastapi.middleware.cors import CORSMiddleware

# Create tables on startup
init_db()

app = FastAPI(title="Video Club Argento API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Video Club Argento API"}

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/sheets/sync")
async def trigger_sync(db: Session = Depends(get_db)):
    try:
        count = await sync_movies(db, settings.TMDB_API_KEY)
        return {"message": f"Sync completed successfully. {count} new movies added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
