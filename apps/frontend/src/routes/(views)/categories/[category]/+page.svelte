<script lang="ts">
import MovieCard from "$lib/components/MovieCard.svelte";
import type { MovieListItem } from "$lib/types";

interface Props {
	data: { category: string; movies: MovieListItem[] };
}

let { data }: Props = $props();
</script>

<svelte:head>
    <title>{data.category} - Video Club Argento</title>
</svelte:head>

<div class="container mx-auto p-4">
    <h1
        class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2"
    >
        {data.category}
    </h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">
        {data.movies.length}
        {data.movies.length === 1 ? "película" : "películas"}
    </p>

    {#if data.movies.length === 0}
        <div class="text-center py-12">
            <p class="text-gray-500 dark:text-gray-400">
                No se encontraron películas en esta categoría.
            </p>
        </div>
    {:else}
        <div
            class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4"
        >
            {#each data.movies as movie}
                <MovieCard {movie} />
            {/each}
        </div>
    {/if}
</div>
