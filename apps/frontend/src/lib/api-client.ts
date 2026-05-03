import { env } from "$env/dynamic/private";
import { env as pubEnv } from "$env/dynamic/public";
import type { MovieDetail, MovieListItem } from "$lib/types";

const API_PREFIX = "/api/videoclub-argento";

function baseUrl(): string {
	return (
		(typeof window === "undefined"
			? env.PRIVATE_API_BASE_URL
			: pubEnv.PUBLIC_API_BASE_URL) ?? "http://localhost:8000"
	);
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
	getMovies: (fetch?: typeof globalThis.fetch, params?: MoviesParams) =>
		get<MovieListItem[]>(`${API_PREFIX}/movies${buildQuery(params)}`, fetch),
	getMovieBySlug: (slug: string, fetch?: typeof globalThis.fetch) =>
		get<MovieDetail>(`${API_PREFIX}/movies/${slug}`, fetch),
};
