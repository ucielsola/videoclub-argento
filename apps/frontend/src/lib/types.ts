export type SortMode = "title" | "year" | "director";
export type SortDirection = "asc" | "desc";

export type EnrichmentStatus = "PENDING" | "PROCESSING" | "COMPLETE" | "FAILED";

export interface MovieListItem {
	id: number;
	title: string;
	year?: number | null;
	poster_url?: string | null;
	search_title?: string | null;
	slug?: string | null;
	director?: string | null;
	rating?: number | null;
	watch_link?: string | null;
}

export interface MovieResponse {
	id: number;
	title: string;
	director?: string | null;
	year?: number | null;
	official_media?: string | null;
	watch_link?: string | null;
	tmdb_id?: number | null;
	original_title?: string | null;
	poster_url?: string | null;
	backdrop_url?: string | null;
	tmdb_synopsis?: string | null;
	rating?: number | null;
	vote_count?: number | null;
	runtime?: number | null;
	genres?: string | null;
	imdb_rating?: number | null;
	imdb_votes?: number | null;
	wiki_summary?: string | null;
	wikipedia_url?: string | null;
	search_title?: string | null;
	slug?: string | null;
	enrichment_status?: EnrichmentStatus | null;
	created_at?: string | null;
	updated_at?: string | null;
}
