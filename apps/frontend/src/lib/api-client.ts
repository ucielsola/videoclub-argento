import { env } from "$env/dynamic/public";
import type { Category, MovieDetail, MovieListItem } from "$lib/types";

const API_PREFIX = "/api/videoclub-argento";

function baseUrl(): string {
	return env.PUBLIC_UCIEL_API ?? "http://localhost:8000";
}

interface MoviesParams {
	search?: string;
	director?: string;
	categories?: string;
}

async function get<T>(
	path: string,
	fetch?: typeof globalThis.fetch,
): Promise<T> {
	const res = await (fetch ?? globalThis.fetch)(`${baseUrl()}${path}`);
	if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
	return res.json();
}

function buildQuery(params?: MoviesParams): string {
	if (!params) return "";
	const parts: string[] = [];
	if (params.search) parts.push(`search=${encodeURIComponent(params.search)}`);
	if (params.director)
		parts.push(`director=${encodeURIComponent(params.director)}`);
	if (params.categories)
		parts.push(`categories=${encodeURIComponent(params.categories)}`);
	return parts.length > 0 ? `?${parts.join("&")}` : "";
}

export const api = {
	getMovies: async (fetch?: typeof globalThis.fetch, params?: MoviesParams) => {
		const res = await get<{ movies: MovieListItem[] }>(
			`${API_PREFIX}/movies${buildQuery(params)}`,
			fetch,
		);
		return res.movies;
	},
	getMovieBySlug: (slug: string, fetch?: typeof globalThis.fetch) =>
		get<MovieDetail>(`${API_PREFIX}/movies/${slug}`, fetch),
	getCategories: async (fetch?: typeof globalThis.fetch) => {
		const res = await get<{ categories: Category[]; total: number }>(
			`${API_PREFIX}/categories`,
			fetch,
		);
		return res.categories;
	},
};
