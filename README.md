# 🎥 Video Club Argento: Movie ETL & API

A monorepo for managing a movie database synced from Google Sheets with enriched metadata from TMDB.

## 📁 Structure

- `apps/backend`: FastAPI + SQLAlchemy + UV (Python 3.14+)
- `apps/frontend`: SvelteKit + Tailwind CSS v4 + Flowbite Svelte
- `docker-compose.yml`: PostgreSQL 15 and pgAdmin setup

## 🚀 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Node.js & npm
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### 2. Infrastructure
Spin up the database:
```bash
docker-compose up -d
```

### 3. Backend Configuration
Create `apps/backend/.env` (already scaffolded) and provide:
- `TMDB_API_KEY`: Get one from [TMDB](https://www.themoviedb.org/documentation/api)

### 4. Development
Run both backend and frontend simultaneously from the root:
```bash
npm run dev
```

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **API**: [http://localhost:8000](http://localhost:8000)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)
