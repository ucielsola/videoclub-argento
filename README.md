# Video Club Argento: Movie ETL & API

A monorepo for managing a movie database synced from Google Sheets with enriched metadata from TMDB.

## Structure

- `apps/backend`: FastAPI + SQLAlchemy + uv (Python 3.14+)
- `apps/frontend`: SvelteKit + Tailwind CSS v4 + Flowbite Svelte
- `docker-compose.yml`: PostgreSQL 15, pgAdmin, backend API, background worker

## Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Node.js & pnpm
- [uv](https://github.com/astral-sh/uv) (Python package manager, for local dev only)

### 2. Production (Docker)
Spin up everything — database, API, and worker:
```bash
docker compose up -d
```

All services auto-restart after power outage (`restart: unless-stopped`).

- **API**: [http://localhost:8000](http://localhost:8000)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)

### 3. Backend Configuration
Create `apps/backend/.env` and provide:
- `TMDB_API_KEY`: Get one from [TMDB](https://www.themoviedb.org/documentation/api)
- `OMDB_API_KEY`: Get one from [OMDb](https://www.omdbapi.com/apikey.aspx)

The `DATABASE_URL` is automatically overridden in Docker to point to the `db` service.

### 4. Local Development
Run backend and frontend separately:
```bash
pnpm dev:be       # Backend (port 8000, requires running DB)
pnpm dev:fe       # Frontend (port 5173)
```

Database must be running first: `docker compose up -d db`

### 5. Frontend Deployment (Vercel)
Frontend deploys to Vercel. Set environment variables in the Vercel dashboard:
```
PRIVATE_API_BASE_URL=https://<your-cloudflare-tunnel-domain>
PUBLIC_API_BASE_URL=https://<your-cloudflare-tunnel-domain>
```

Expose the backend via a Cloudflare tunnel pointing to `localhost:8000`.
