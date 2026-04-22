# Backend Agent Guide

## 🎯 Purpose
A FastAPI-based REST API and ETL engine for the movie database.

## 🛠️ Tech Stack
- **Python 3.14+** (Managed by `uv`)
- **FastAPI**: Serves the movie data.
- **SQLAlchemy**: ORM for the PostgreSQL database.
- **httpx**: Tool for TMDB API.

## 🧩 Key Logic
- `database.py`: Defines the `Movie` model and handles DB connections.
- `etl.py`: Core logic for fetching metadata from TMDB.
- `main.py`: Entry point for the API (`/movies`).

## 🚀 How to Run
```bash
uv run fastapi dev main.py
```
