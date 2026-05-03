<script lang="ts">
import { ArrowLeft } from "lucide-svelte";
import MovieCard from "$lib/components/MovieCard.svelte";
import type { MovieListItem } from "$lib/types";

interface Props {
	data: { director: string; movies: MovieListItem[] };
}

let { data }: Props = $props();
</script>

<svelte:head>
    <title>{data.director} - Video Club Argento</title>
</svelte:head>

<div class="container mx-auto p-4">
    <h1
        class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2"
    >
        {data.director}
    </h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">
        {data.movies.length}
        {data.movies.length === 1 ? "película" : "películas"}
    </p>

    {#if data.movies.length === 0}
        <div class="text-center py-12">
            <p class="text-gray-500 dark:text-gray-400">
                No se encontraron películas para este director.
            </p>
        </div>
    {:else}
        <div
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
        >
            {#each data.movies as movie}
                <MovieCard {movie} />
            {/each}
        </div>
    {/if}
</div>
