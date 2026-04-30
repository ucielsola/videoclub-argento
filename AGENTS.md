# AGENTS.md

## Project Overview

**Video Club Argento** — a monorepo for managing an Argentine cinema movie database synced from Google Sheets, enriched with metadata from TMDB, OMDb, and Wikipedia.

## Structure

```
apps/backend/   FastAPI + SQLAlchemy + PostgreSQL (Python 3.14+, uv)
apps/frontend/  SvelteKit + Tailwind CSS v4 + Flowbite Svelte
```

Root `package.json` uses pnpm workspaces to orchestrate. No Turborepo.

## Commands

```bash
pnpm dev:fe       # Frontend only (port 5173)
pnpm dev:be       # Backend only (port 8000, native uv)
pnpm build        # Build frontend (for Vercel)
pnpm check        # Typecheck frontend
pnpm lint         # Lint both apps
```

## Backend (apps/backend/)

- **Stack**: Python 3.14+, FastAPI, SQLAlchemy, httpx, uv
- **Lint**: `uv run ruff check .` | **Format**: `uv run ruff format .`
- **Config**: Ruff in `pyproject.toml` — target py314, line-length 120, rules E/F/I/UP/B/SIM/RUF
- **DB**: PostgreSQL 15 (Docker), model in `database.py`
- **API**: 6 endpoints in `main.py` (movies CRUD + sheets sync)
- **ETL**: Google Sheets → TMDB/OMDb → DB (in-process via `etl.py` + medallion scripts in `scripts/`)
- **Worker**: `worker.py` — background enrichment for PENDING movies
- **Docker**: `Dockerfile` + `docker-compose.yml` — production deployment via Docker containers

### Production (Docker)

```bash
docker compose up -d            # Start db + backend + worker
docker compose up -d backend    # Start/rebuild backend only
docker compose logs -f backend  # View backend logs
docker compose down             # Stop all services
```

All services use `restart: unless-stopped` — auto-recover after power outage.

The `backend` and `worker` services use the same Docker image (different CMD). Both load env vars from `apps/backend/.env` and override `DATABASE_URL` to point to the `db` service on the Docker network.

## Frontend (apps/frontend/)

- **Stack**: Svelte 5 (Runes + Snippets), SvelteKit, Tailwind CSS v4, Flowbite Svelte v2
- **Lint**: `biome check .` | **Format**: `biome format --write .`
- **Config**: Biome in `biome.json` — tabs, double quotes, recommended rules
- **Search**: Fuse.js for client-side fuzzy search
- **State**: Svelte 5 class-based stores in `src/lib/state/` (MoviesStore, ThemeStore)
- **API**: Hand-written client in `src/lib/api-client.ts` — raw fetch to backend
- **VirtualList**: Custom virtual-scrolled grid for large movie lists
- **Deploy**: Vercel (adapter-auto)

### Frontend Environment Variables (for Vercel)

Set these in Vercel dashboard pointing to your Cloudflare tunnel domain:
```
PRIVATE_API_BASE_URL=https://<tunnel-domain>   # SSR fetch from Vercel servers
PUBLIC_API_BASE_URL=https://<tunnel-domain>    # Client-side fetch from browser
```

## Conventions

- No comments in code unless requested
- Spanish-language UI, English codebase
- Backend: snake_case, Ruff formatting
- Frontend: tabs, double quotes, Biome formatting

## Plan Mode

- Make plans extremely concise. Sacrifice grammar for concision.
- End each plan with a list of unresolved questions, if any.
