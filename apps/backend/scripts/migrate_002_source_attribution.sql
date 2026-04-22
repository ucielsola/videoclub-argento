-- Migration 002: Source Attribution + Self-Healing Fields
-- Run with: psql -d videoclub -f scripts/migrate_002_source_attribution.sql
-- Or: python -c "import psycopg2; conn = psycopg2.connect('postgresql://videouser:videopassword@localhost:5432/videoclub'); cur = conn.cursor(); cur.execute(open('scripts/migrate_002_source_attribution.sql').read()); conn.commit()"

BEGIN;

-- 1. Add new source-attributed columns
ALTER TABLE movies ADD COLUMN IF NOT EXISTS tmdb_synopsis TEXT;
ALTER TABLE movies ADD COLUMN IF NOT EXISTS imdb_rating FLOAT;
ALTER TABLE movies ADD COLUMN IF NOT EXISTS imdb_votes INTEGER;
ALTER TABLE movies ADD COLUMN IF NOT EXISTS wiki_summary TEXT;
ALTER TABLE movies ADD COLUMN IF NOT EXISTS wikipedia_url VARCHAR(500);

-- 2. Add enrichment_status enum column
CREATE TYPE enrichment_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETE', 'FAILED');
ALTER TABLE movies ADD COLUMN IF NOT EXISTS enrichment_status enrichment_status DEFAULT 'PENDING';

-- 3. Create index on enrichment_status for worker queries
CREATE INDEX IF NOT EXISTS idx_movies_enrichment_status ON movies(enrichment_status);

-- 4. Drop unique constraint on slug (we handle collisions in app code)
ALTER TABLE movies DROP CONSTRAINT IF EXISTS movies_slug_key;

-- 5. Create non-unique index on slug for lookups
CREATE INDEX IF NOT EXISTS idx_movies_slug ON movies(slug);

-- 6. Rename old synopsis to tmdb_synopsis if it has data
UPDATE movies SET tmdb_synopsis = synopsis WHERE tmdb_synopsis IS NULL AND synopsis IS NOT NULL;

-- 7. Migrate rating to imdb_rating
UPDATE movies SET imdb_rating = rating WHERE imdb_rating IS NULL AND rating IS NOT NULL;

-- 8. Set all existing movies to PENDING (re-process through new pipeline)
UPDATE movies SET enrichment_status = 'PENDING';

COMMIT;