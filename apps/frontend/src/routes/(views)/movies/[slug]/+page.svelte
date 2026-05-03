<script lang="ts">
import { Badge, Button, Tooltip } from "flowbite-svelte";
import {
	Clock,
	ExternalLink,
	Film,
	Image,
	Play,
	Star,
	Trophy,
	Users,
} from "lucide-svelte";
import SynopsisTabs from "$lib/components/SynopsisTabs.svelte";
import { resolvePosterUrl } from "$lib/poster";
import type { MovieDetail } from "$lib/types";

interface Props {
	data: { movie: MovieDetail | null };
}

let { data }: Props = $props();
let movie = $derived(data.movie);

const genres = $derived(movie?.genres ?? []);
const categories = $derived(movie?.categories ?? []);
const cast = $derived(movie?.cast ?? []);
const enrichment = $derived(movie?.enrichment ?? []);

const posterUrl = $derived(movie ? resolvePosterUrl(movie.poster_url) : null);
const backdropUrl = $derived(
	movie ? resolvePosterUrl(movie.backdrop_url) : null,
);
const stillUrls = $derived(
	movie?.still_urls?.map((url) => resolvePosterUrl(url)).filter(Boolean) ?? [],
);
</script>

<svelte:head>
    <title>{movie?.title || "Movie"} - Video Club Argento</title>
</svelte:head>

{#if !movie}
    <div class="container mx-auto p-8 text-center">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Película no encontrada
        </h1>
    </div>
{:else}
    {#if backdropUrl}
        <div class="relative w-full h-64 md:h-80 overflow-hidden">
            <img
                src={backdropUrl}
                alt=""
                class="w-full h-full object-cover"
            />
            <div
                class="absolute inset-0 bg-gradient-to-t from-white dark:from-gray-900 to-transparent"
            ></div>
        </div>
    {/if}

    <div class="container mx-auto p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1">
                <div
                    class="aspect-2/3 bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden shadow-lg relative"
                >
                    {#if posterUrl}
                        <img
                            src={posterUrl}
                            alt={movie.title}
                            class="w-full h-full object-cover"
                        />
                    {:else}
                        <div
                            class="w-full h-full flex items-center justify-center text-gray-400"
                        >
                            <Film class="w-12 h-12" />
                        </div>
                    {/if}
                    {#if movie.is_top_100}
                        <Badge
                            color="yellow"
                            class="absolute top-3 left-3 flex items-center gap-1"
                        >
                            <Trophy class="w-3.5 h-3.5" />
                            Top 100
                        </Badge>
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
                        <Badge color="yellow" class="text-lg px-3 py-1 flex items-center gap-1">
                            <Star class="w-4 h-4" />
                            {movie.rating}
                        </Badge>
                    {/if}
                </div>

                <div
                    class="flex flex-wrap gap-4 text-gray-600 dark:text-gray-400 mb-6"
                >
                    {#if movie.year}
                        <span>{movie.year}</span>
                    {/if}
                    <span>•
                        {#if movie.director}
                            {#if movie.director.includes(",")}
                                {@const directors = movie.director.split(",")}
                                {#each directors as d, index}
                                    {@const isLast = index === directors.length - 1}
                                    <a
                                        href="/directors/{encodeURIComponent(d.trim())}"
                                        class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                                    >
                                        {d.trim()}{`${isLast ? "" : ", "}`}
                                    </a>
                                {/each}
                            {:else}
                                <a
                                    href="/directors/{encodeURIComponent(movie.director)}"
                                    class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                                >
                                    {movie.director}
                                </a>
                            {/if}
                        {/if}
                    </span>
                    {#if movie.runtime}
                        <span class="flex items-center gap-1">
                            • <Clock class="w-3.5 h-3.5" /> {movie.runtime} min
                        </span>
                    {/if}
                </div>

                {#if genres.length > 0}
                    <div class="flex flex-wrap gap-2 mb-4">
                        {#each genres as genre}
                            <Badge color="gray">{genre}</Badge>
                        {/each}
                    </div>
                {/if}

                {#if categories.length > 0}
                    <div class="flex flex-wrap gap-1.5 mb-6">
                        {#each categories as category}
                            <a href="/categories/{encodeURIComponent(category)}">
                                <Badge color="indigo" class="text-xs">{category}</Badge>
                            </a>
                        {/each}
                    </div>
                {/if}

                <SynopsisTabs {enrichment} />

                {#if cast.length > 0}
                    <div class="mb-6">
                        <h2
                            class="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2"
                        >
                            <Users class="w-5 h-5" />
                            Reparto
                        </h2>
                        <div class="flex flex-wrap gap-2">
                            {#each cast as actor, i}
                                <a
                                    id="cast-{i}"
                                    href="https://cinenacional.com/persona/{actor.toLowerCase().replace(/\s+/g, '-')}"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    <Badge color="gray">{actor}</Badge>
                                </a>
                                <Tooltip triggeredBy="#cast-{i}" placement="top">Ver en Cinenacional</Tooltip>
                            {/each}
                        </div>
                    </div>
                {/if}

                {#if movie.color_type || movie.sound_type}
                    <div class="flex gap-3 mb-6 text-sm text-gray-500 dark:text-gray-400">
                        {#if movie.color_type}
                            <Badge color="gray">{movie.color_type}</Badge>
                        {/if}
                        {#if movie.sound_type}
                            <Badge color="gray">{movie.sound_type}</Badge>
                        {/if}
                    </div>
                {/if}

                {#if movie.imdb_rating}
                    <div class="mb-6 flex items-center gap-2">
                        <Badge color="yellow" class="flex items-center gap-1">
                            IMDb
                        </Badge>
                        <span class="text-sm text-gray-700 dark:text-gray-300">
                            {movie.imdb_rating}/10
                            {#if movie.imdb_votes}
                                <span class="text-gray-400">({movie.imdb_votes.toLocaleString()} votos)</span>
                            {/if}
                        </span>
                    </div>
                {/if}

                {#if stillUrls.length > 0}
                    <div class="mb-6">
                        <h2
                            class="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2"
                        >
                            <Image class="w-5 h-5" />
                            Imágenes
                        </h2>
                        <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                            {#each stillUrls as url}
                                <img
                                    src={url!}
                                    alt="{movie.title} still"
                                    class="w-full rounded-lg aspect-video object-cover"
                                    loading="lazy"
                                />
                            {/each}
                        </div>
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
