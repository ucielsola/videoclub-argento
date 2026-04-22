-- Migration: Add search_title and slug columns
-- Safe: only adds columns, does not delete or modify existing data

ALTER TABLE movies
ADD COLUMN IF NOT EXISTS search_title VARCHAR,
ADD COLUMN IF NOT EXISTS slug VARCHAR;

-- Create indexes (optional but recommended for performance)
CREATE INDEX IF NOT EXISTS idx_movies_search_title ON movies(search_title);
CREATE UNIQUE INDEX IF NOT EXISTS idx_movies_slug ON movies(slug);