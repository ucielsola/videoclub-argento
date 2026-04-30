import { env } from "$env/dynamic/private";
import { env as pubEnv } from "$env/dynamic/public";
import type { MovieListItem, MovieResponse } from "$lib/types";

function baseUrl(): string {
	return (
		(typeof window === "undefined"
			? env.PRIVATE_API_BASE_URL
			: pubEnv.PUBLIC_API_BASE_URL) ?? "http://localhost:8000"
	);
}

async function get<T>(
	path: string,
	fetch?: typeof globalThis.fetch,
): Promise<T> {
	const res = await (fetch ?? globalThis.fetch)(`${baseUrl()}${path}`);
	if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
	return res.json();
}

export const api = {
	getMovies: (fetch?: typeof globalThis.fetch) =>
		get<MovieListItem[]>("/movies", fetch),
	getMoviesByDirector: (director: string, fetch?: typeof globalThis.fetch) =>
		get<MovieListItem[]>(
			`/movies/director/${encodeURIComponent(director)}`,
			fetch,
		),
	getMovieBySlug: (slug: string, fetch?: typeof globalThis.fetch) =>
		get<MovieResponse>(`/movies/slug/${slug}`, fetch),
};
