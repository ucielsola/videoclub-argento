export const load = async ({ fetch, params }) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/movies/slug/${params.slug}`);
        if (response.ok) {
            const movie = await response.json();
            return { movie };
        }
    } catch (e) {
        console.error("Could not fetch movie", e);
    }
    return { movie: null };
};