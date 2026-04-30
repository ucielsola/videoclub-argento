<script lang="ts">
import { Badge, Button } from "flowbite-svelte";
import { ArrowLeft, ExternalLink, Play } from "lucide-svelte";
import type { MovieResponse } from "$lib/types";

interface Props {
	data: { movie: MovieResponse | null };
}

let { data }: Props = $props();
let movie = $derived(data.movie);
</script>

<svelte:head>
    <title>{movie?.title || "Movie"} - Video Club Argento</title>
</svelte:head>

{#if !movie}
    <div class="container mx-auto p-8 text-center">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Movie not found
        </h1>
    </div>
{:else}
    <div class="container mx-auto p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1">
                <div
                    class="aspect-2/3 bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden shadow-lg"
                >
                    {#if movie.poster_url}
                        <img
                            src={movie.poster_url}
                            alt={movie.title}
                            class="w-full h-full object-cover"
                        />
                    {:else}
                        <div
                            class="w-full h-full flex items-center justify-center text-gray-400"
                        >
                            Sin Poster
                        </div>
                    {/if}
                </div>
            </div>

            <div class="md:col-span-2">
                <div class="flex items-start justify-between mb-4">
                    <h1
                        class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white"
                    >
                        {movie.title}
                    </h1>
                    {#if movie.rating}
                        <Badge color="yellow" class="text-lg px-3 py-1">
                            ★ {movie.rating}
                        </Badge>
                    {/if}
                </div>

                <div
                    class="flex flex-wrap gap-4 text-gray-600 dark:text-gray-400 mb-6"
                >
                    {#if movie.year}
                        <span>{movie.year}</span>
                    {/if}
                    <span
                        >•
                        {#if movie.director}
                            {#if movie.director.includes(",")}
                                {@const directors = movie.director.split(",")}
                                {#each directors as director, index}
                                    {@const isLast =
                                        index === directors.length - 1}
                                    <a
                                        href="/directors/{encodeURIComponent(
                                            director,
                                        )}"
                                        class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                                        onclick={(e) => e.stopPropagation()}
                                    >
                                        {director}{`${isLast ? "" : ", "}`}
                                    </a>
                                {/each}
                            {:else}
                                <a
                                    href="/directors/{encodeURIComponent(
                                        movie.director,
                                    )}"
                                    class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                                    onclick={(e) => e.stopPropagation()}
                                >
                                    {movie.director}
                                </a>
                            {/if}
                        {/if}
                    </span>
                    {#if movie.runtime}
                        <span>• {movie.runtime} min</span>
                    {/if}
                </div>

                {#if movie.genres}
                    <div class="flex flex-wrap gap-2 mb-6">
                        {#each movie.genres.split(", ") as genre}
                            <Badge color="gray">{genre}</Badge>
                        {/each}
                    </div>
                {/if}

			{#if movie.tmdb_synopsis}
					<div class="mb-6">
						<h2
							class="text-lg font-semibold text-gray-900 dark:text-white mb-2"
						>
							Sinopsis
						</h2>
						<p
							class="text-gray-700 dark:text-gray-300 leading-relaxed"
						>
							{movie.tmdb_synopsis}
						</p>
					</div>
				{/if}

                {#if movie.watch_link || movie.official_media}
                    <div class="flex flex-wrap gap-4">
                        {#if movie.watch_link}
                            <a
                                href={movie.watch_link}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Button color="dark">
                                    <Play class="mr-2 h-4 w-4" />
                                    Ver Película
                                </Button>
                            </a>
                        {/if}
                        {#if movie.official_media}
                            <a
                                href={movie.official_media}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Button outline color="dark">
                                    <ExternalLink class="mr-2 h-4 w-4" />
                                    Fuente Oficial
                                </Button>
                            </a>
                        {/if}
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}
