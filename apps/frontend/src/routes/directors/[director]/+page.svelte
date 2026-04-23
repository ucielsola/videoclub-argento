<script lang="ts">
    import { ArrowLeft } from 'lucide-svelte';
    import MovieCard from '$lib/components/MovieCard.svelte';
    import type { MovieListItem } from '$lib/types';

    interface Props {
        data: { director: string; movies: MovieListItem[] };
    }

    let { data }: Props = $props();
</script>

<svelte:head>
    <title>{data.director} - Video Club Argento</title>
</svelte:head>

<div class="container mx-auto p-4">
    <a href="/" class="inline-flex items-center text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-6">
        <ArrowLeft class="mr-2 h-4 w-4" />
        Back to movies
    </a>

    <h1 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
        {data.director}
    </h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">
        {data.movies.length} {data.movies.length === 1 ? 'película' : 'películas'}
    </p>

    {#if data.movies.length === 0}
        <div class="text-center py-12">
            <p class="text-gray-500 dark:text-gray-400">No se encontraron películas para este director.</p>
        </div>
    {:else}
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {#each data.movies as movie}
                <MovieCard {movie} />
            {/each}
        </div>
    {/if}
</div>
