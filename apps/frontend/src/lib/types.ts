export type SortMode = "title" | "year" | "director";
export type SortDirection = "asc" | "desc";

export enum EnrichmentStatus {
  Pending = "PENDING",
  Processing = "PROCESSING",
  Complete = "COMPLETE",
  Failed = "FAILED",
}

export interface MovieListItem {
  id: number;
  title: string;
  year?: number;
  poster_url?: string;
  search_title?: string;
  slug?: string;
  director?: string;
  rating?: number;
  watch_link?: string;
  enrichment_status?: EnrichmentStatus;
}

export interface MovieBase {
  title: string;
  director?: string;
  year?: number;
  official_media?: string;
  watch_link?: string;

  tmdb_id?: number;
  original_title?: string;
  poster_url?: string;
  backdrop_url?: string;
  tmdb_synopsis?: string;
  rating?: number;
  vote_count?: number;
  runtime?: number;
  genres?: string;

  imdb_rating?: number;
  imdb_votes?: number;

  wiki_summary?: string;
  wikipedia_url?: string;

  search_title?: string;
  slug?: string;

  enrichment_status?: EnrichmentStatus;
}

export interface MovieResponse extends MovieBase {
  id: number;
  created_at?: string;
  updated_at?: string;
}
