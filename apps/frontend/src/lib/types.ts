export type SortMode = "title" | "year" | "director";
export type SortDirection = "asc" | "desc";

export interface Category {
	name: string;
	movie_count: number;
}

export interface MovieListItem {
	hash: string;
	slug: string;
	title: string;
	year: number;
	director: string;
	poster_url: string;
	rating: number | null;
	watch_link: string | null;
	is_top_100: boolean;
	categories: string[];
}

export interface MovieDetail extends MovieListItem {
	backdrop_url: string | null;
	official_media: string | null;
	synopsis: string | null;
	runtime: number | null;
	genres: string[];
	cast: string[];
	imdb_rating: number | null;
	imdb_votes: number | null;
	color_type: string | null;
	sound_type: string | null;
	still_urls: string[];
	enrichment: Enrichment[];
}

export type Enrichment =
	| TmdbEnrichment
	| OmdbEnrichment
	| WikipediaEnrichment
	| CinenacionalEnrichment;

export interface TmdbEnrichment {
	source: "tmdb";
	data: {
		genres: string[];
		rating: number;
		runtime: number;
		tmdb_id: number;
		synopsis: string;
		vote_count: number;
		backdrop_url: string;
		original_title: string;
		primary_poster: string;
		alternate_posters: string[] | null;
	};
}

export interface OmdbEnrichment {
	source: "omdb";
	data: {
		genres: string[];
		imdb_id: string;
		runtime: number | null;
		synopsis: string | null;
		imdb_votes: string | number | null;
		imdb_rating: string | number | null;
	};
}

export interface WikipediaEnrichment {
	source: "wikipedia";
	data: {
		synopsis: string;
		page_title: string;
		wikipedia_url: string;
	};
}

export interface CinenacionalEnrichment {
	source: "cinenacional";
	data: {
		cast: string[];
		rating: string;
		writer: string;
		imdb_id: string;
		tmdb_id: number;
		director: string;
		duration: number;
		synopsis: string;
		movie_url: string;
		color_type: string;
		sound_type: string;
		still_urls: string[];
		release_date: string;
		primary_poster: string;
		cinenacional_id: number;
		alternate_posters: string[] | null;
	};
}
