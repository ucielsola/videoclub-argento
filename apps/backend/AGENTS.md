# Backend Agent Guide

## Purpose
FastAPI REST API + ETL engine for the Argentine cinema movie database.

## Tech Stack
- **Python 3.14+** (managed by `uv`)
- **FastAPI** with `uvicorn[standard]`
- **SQLAlchemy** ORM → PostgreSQL 15
- **httpx** for external API calls (TMDB, OMDb, Wikipedia)
- **pydantic-settings** for env config

## Commands
```bash
pnpm dev:be              # Start dev server (port 8000)
uv run ruff check .      # Lint
uv run ruff format .     # Format
uv run ruff check --fix . # Lint + autofix
```

## Docker (Production)
```bash
docker compose up -d             # Start db + backend + worker
docker compose build backend     # Rebuild image after code changes
docker compose logs -f backend   # View logs
docker compose logs -f worker    # View worker logs
docker compose down              # Stop all
```

- **Backend** serves API on port 8000 (`restart: unless-stopped`)
- **Worker** runs `worker.py` as a separate container from the same image
- Both load `apps/backend/.env` and override `DATABASE_URL` to `db:5432` (Docker network)
- Served externally via Cloudflare tunnel → `localhost:8000`

## Key Files
| File | Purpose |
|---|---|
| `main.py` | FastAPI app, 6 endpoints, CORS, lifespan |
| `database.py` | `Movie` model, `Settings` (env), `get_db()`, `init_db()` |
| `schemas.py` | Pydantic response models: `MovieListItem`, `MovieResponse` |
| `etl.py` | In-process sync: CSV → TMDB/OMDb → DB (triggered by `POST /sheets/sync`) |
| `worker.py` | Background process: enriches PENDING movies (TMDB + OMDb + Wikipedia) |
| `utils.py` | `generate_slug()`, `normalize_for_search()` |
| `Dockerfile` | Production image: python:3.14-slim + uv, uvicorn entrypoint |
| `.dockerignore` | Excludes .venv, .env, data/, cache dirs |

## Medallion Scripts (`scripts/`)
- `01_ingest.py` — Bronze: raw API ingestion with local JSON caching to `data/raw/`
- `02_transform.py` — Silver: merge + normalize TMDB/OMDb/Wikipedia → `data/processed/movies.json`
- `03_load.py` — Gold: batch upsert to PostgreSQL (conflict on `slug`)
- `migrate_search_data.py` — Backfill `search_title` + `slug`
- `migrate_002_source_attribution.sql` — Add enrichment fields + status enum

## API Endpoints
| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/movies` | List all movies (paginated, returns `MovieListItem[]`) |
| `GET` | `/movies/director/{director}` | Filter by director (case-insensitive) |
| `GET` | `/movies/slug/{slug}` | Movie detail by slug |
| `GET` | `/movies/{movie_id}` | Movie detail by ID |
| `POST` | `/sheets/sync` | Trigger ETL sync from Google Sheets |

## Database Model (`movies` table)
Key columns: `id`, `title`, `director`, `year`, `slug`, `search_title`, `poster_url`, `backdrop_url`, `rating`, `genres`, `runtime`, `tmdb_synopsis`, `wiki_summary`, `enrichment_status` (PENDING/PROCESSING/COMPLETE/FAILED), `watch_link`, `official_media`

## Configuration (`.env`)
```
DATABASE_URL=postgresql://videouser:videopassword@localhost:5432/videoclub
TMDB_API_KEY=...
OMDB_API_KEY=...
CORS_ORIGINS=*
BATCH_SIZE=200
```

Note: `DATABASE_URL` is overridden in `docker-compose.yml` to `postgresql://videouser:videopassword@db:5432/videoclub` for containers.

## Ruff Config (in `pyproject.toml`)
- Target: py314, line-length: 120
- Rules: E, F, I, UP, B, SIM, RUF (ignore B008)
