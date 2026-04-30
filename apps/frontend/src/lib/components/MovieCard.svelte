<script lang="ts">
import { Card } from "flowbite-svelte";
import { Film } from "lucide-svelte";
import type { MovieListItem } from "$lib/types";

interface Props {
	movie: MovieListItem;
}

let { movie }: Props = $props();
</script>

<Card
    hoverable
    class="p-0 overflow-hidden h-full flex flex-col"
    href={`/movies/${movie.slug}`}
>
    <div class="bg-gray-200 dark:bg-gray-700 relative flex-1 min-h-0">
        {#if movie.poster_url}
            <img
                src={movie.poster_url}
                alt={movie.title}
                class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                loading="lazy"
            />
        {:else}
            <div
                class="w-full h-full flex items-center justify-center text-gray-400"
            >
                <Film class="w-8 h-8" />
            </div>
        {/if}
    </div>

    <div class="p-3 shrink-0">
        <h5
            class="text-sm font-bold tracking-tight text-gray-900 dark:text-white line-clamp-1"
        >
            {movie.title}
        </h5>
        <p class="text-xs text-gray-600 dark:text-gray-400">
            {movie.year || "N/A"} •
            {#if movie.director}
                {#if movie.director.includes(",")}
                    {@const directors = movie.director.split(",")}
                    {#each directors as director, index}
                        {@const isLast = index === directors.length - 1}
                        <a
                            href="/directors/{encodeURIComponent(director)}"
                            class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                            onclick={(e) => e.stopPropagation()}
                        >
                            {director}{`${isLast ? "" : ", "}`}
                        </a>
                    {/each}
                {:else}
                    <a
                        href="/directors/{encodeURIComponent(movie.director)}"
                        class="hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"
                        onclick={(e) => e.stopPropagation()}
                    >
                        {movie.director}
                    </a>
                {/if}
            {:else}
                Unknown
            {/if}
        </p>
    </div>
</Card>
