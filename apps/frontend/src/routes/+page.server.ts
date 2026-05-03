import { api } from "$lib/api-client";

export const load = async ({ fetch }) => {
	try {
		const [movies, categoriesList] = await Promise.all([
			api.getMovies(fetch),
			api.getCategories(fetch),
		]);
		return { movies, categories: categoriesList };
	} catch (e) {
		console.error("[+page.server.ts]", e);
		return { movies: [], categories: [] };
	}
};
