export const load = async ({ fetch }) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/movies');
        if (response.ok) {
            const movies = await response.json();
            return { movies };
        }
    } catch (e) {
        console.error("Could not fetch movies", e);
    }
    return { movies: [] };
};
