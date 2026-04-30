import { api } from "$lib/api-client";

export const load = async ({ fetch, params }) => {
	try {
		const movie = await api.getMovieBySlug(params.slug, fetch);
		return { movie };
	} catch {
		return { movie: null };
	}
};
