<script lang="ts">
    import { Button, Spinner, Badge } from 'flowbite-svelte';
    import { ArrowLeft, ExternalLink, Play } from 'lucide-svelte';

    interface Props {
        data: { movie: any };
    }

    let { data }: Props = $props();
    let movie = $derived(data.movie);
</script>

<svelte:head>
    <title>{movie?.title || 'Movie'} - Video Club Argento</title>
</svelte:head>

{#if !movie}
    <div class="container mx-auto p-8 text-center">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Movie not found</h1>
        <a href="/">
            <Button>
                <ArrowLeft class="mr-2 h-4 w-4" />
                Back to movies
            </Button>
        </a>
    </div>
{:else}
    <div class="container mx-auto p-4">
        <a href="/" class="inline-flex items-center text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-6">
            <ArrowLeft class="mr-2 h-4 w-4" />
            Back to movies
        </a>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1">
                <div class="aspect-[2/3] bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden shadow-lg">
                    {#if movie.poster_url}
                        <img
                            src={movie.poster_url}
                            alt={movie.title}
                            class="w-full h-full object-cover"
                        />
                    {:else}
                        <div class="w-full h-full flex items-center justify-center text-gray-400">
                            No Poster
                        </div>
                    {/if}
                </div>
            </div>

            <div class="md:col-span-2">
                <div class="flex items-start justify-between mb-4">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">
                        {movie.title}
                    </h1>
                    {#if movie.rating}
                        <Badge color="yellow" class="text-lg px-3 py-1">
                            ★ {movie.rating}
                        </Badge>
                    {/if}
                </div>

                <div class="flex flex-wrap gap-4 text-gray-600 dark:text-gray-400 mb-6">
                    {#if movie.year}
                        <span>{movie.year}</span>
                    {/if}
                    {#if movie.director}
                        <span>• {movie.director}</span>
                    {/if}
                    {#if movie.runtime}
                        <span>• {movie.runtime} min</span>
                    {/if}
                </div>

                {#if movie.genres}
                    <div class="flex flex-wrap gap-2 mb-6">
                        {#each movie.genres.split(', ') as genre}
                            <Badge color="gray">{genre}</Badge>
                        {/each}
                    </div>
                {/if}

                {#if movie.synopsis}
                    <div class="mb-6">
                        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Synopsis</h2>
                        <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
                            {movie.synopsis}
                        </p>
                    </div>
                {/if}

                {#if movie.watch_link || movie.official_media}
                    <div class="flex flex-wrap gap-4">
                        {#if movie.watch_link}
                            <a href={movie.watch_link} target="_blank" rel="noopener noreferrer">
                                <Button color="dark">
                                    <Play class="mr-2 h-4 w-4" />
                                    Watch Movie
                                </Button>
                            </a>
                        {/if}
                        {#if movie.official_media}
                            <a href={movie.official_media} target="_blank" rel="noopener noreferrer">
                                <Button outline color="dark">
                                    <ExternalLink class="mr-2 h-4 w-4" />
                                    Official Media
                                </Button>
                            </a>
                        {/if}
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}