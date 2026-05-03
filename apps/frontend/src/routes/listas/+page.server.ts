import { apiClient } from "$lib/api-client";
import type { MovieListItem } from "$lib/types";

export async function load() {
	const movies = await apiClient<MovieListItem[]>("/movies");
	return { movies };
}
