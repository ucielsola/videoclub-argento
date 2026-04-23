export const load = async ({ fetch, params }) => {
	const director = decodeURIComponent(params.director);
	try {
		const response = await fetch(
			`http://127.0.0.1:8000/movies/director/${encodeURIComponent(director)}`,
		);
		if (response.ok) {
			const movies = await response.json();
			return { director, movies };
		}
	} catch (e) {
		console.error("Could not fetch movies by director", e);
	}
	return { director, movies: [] };
};
