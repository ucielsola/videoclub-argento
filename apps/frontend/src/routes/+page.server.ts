import { api } from "$lib/api-client";

export const load = async ({ fetch }) => {
	try {
		const movies = await api.getMovies(fetch);
		return { movies };
	} catch (e) {
		console.error("[+page.server.ts]", e);
		return { movies: [] };
	}
};
