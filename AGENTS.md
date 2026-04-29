# AGENTS.md

## Project Overview

**Video Club Argento** — a monorepo for managing an Argentine cinema movie database synced from Google Sheets, enriched with metadata from TMDB, OMDb, and Wikipedia.

## Structure

```
apps/backend/   FastAPI + SQLAlchemy + PostgreSQL (Python 3.14+, uv)
apps/frontend/  SvelteKit + Tailwind CSS v4 + Flowbite Svelte
```

Root `package.json` uses pnpm + Turborepo to orchestrate.

## Commands

```bash
pnpm dev          # Run both apps
pnpm dev:fe       # Frontend only (port 5173)
pnpm dev:be       # Backend only (port 8000)
pnpm build        # Build both
pnpm check        # Typecheck both
pnpm lint         # Lint both
pnpm generate-client  # Generate OpenAPI client from backend spec
```

## Backend (apps/backend/)

- **Stack**: Python 3.14+, FastAPI, SQLAlchemy, httpx, uv
- **Lint**: `uv run ruff check .` | **Format**: `uv run ruff format .`
- **Config**: Ruff in `pyproject.toml` — target py314, line-length 120, rules E/F/I/UP/B/SIM/RUF
- **DB**: PostgreSQL 15 (Docker), model in `database.py`
- **API**: 6 endpoints in `main.py` (movies CRUD + sheets sync)
- **ETL**: Google Sheets → TMDB/OMDb → DB (in-process via `etl.py` + medallion scripts in `scripts/`)
- **Worker**: `worker.py` — background enrichment for PENDING movies

## Frontend (apps/frontend/)

- **Stack**: Svelte 5 (Runes + Snippets), SvelteKit, Tailwind CSS v4, Flowbite Svelte v2
- **Lint**: `biome check .` | **Format**: `biome format --write .`
- **Config**: Biome in `biome.json` — tabs, double quotes, recommended rules
- **Search**: Fuse.js for client-side fuzzy search
- **State**: Svelte 5 class-based stores in `src/lib/state/` (MoviesStore, ThemeStore)
- **API**: Raw fetch to `http://localhost:8000` (OpenAPI client generated but unused)
- **VirtualList**: Custom virtual-scrolled grid for large movie lists

## Conventions

- No comments in code unless requested
- Spanish-language UI, English codebase
- Backend: snake_case, Ruff formatting
- Frontend: tabs, double quotes, Biome formatting

## Plan Mode

- Make plans extremely concise. Sacrifice grammar for concision.
- End each plan with a list of unresolved questions, if any.
