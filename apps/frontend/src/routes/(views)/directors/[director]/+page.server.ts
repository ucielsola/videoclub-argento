import { api } from "$lib/api-client";

export const load = async ({ fetch, params }) => {
	const director = decodeURIComponent(params.director);
	const movies = await api.getMovies(fetch, { director });
	return { director, movies };
};
