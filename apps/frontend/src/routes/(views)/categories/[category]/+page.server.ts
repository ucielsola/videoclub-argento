import { api } from "$lib/api-client";

export const load = async ({ fetch, params }) => {
	const category = decodeURIComponent(params.category);
	const movies = await api.getMovies(fetch, { categories: category });
	return { category, movies };
};
