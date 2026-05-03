<script lang="ts">
import { Badge, Tooltip } from "flowbite-svelte";
import { Bookmark, Eye, Film, Trophy } from "lucide-svelte";
import { resolvePosterUrl } from "$lib/poster";
import { watchlist } from "$lib/state";
import type { MovieListItem } from "$lib/types";

interface Props {
	movie: MovieListItem;
}

let { movie }: Props = $props();

const posterUrl = $derived(resolvePosterUrl(movie.poster_url));
const status = $derived(watchlist.getStatus(movie.slug));
</script>

<a
	href={`/movies/${movie.slug}`}
	class="block overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-200 dark:bg-gray-700 hover:shadow-lg hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-200 h-[420px] relative group"
>
	{#if posterUrl}
		<img
			src={posterUrl}
			alt={movie.title}
			class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
			loading="lazy"
		/>
	{:else}
		<div class="w-full h-full flex items-center justify-center text-gray-400">
			<Film class="w-8 h-8" />
		</div>
	{/if}

	<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent">
		{#if status}
			<div class="absolute bottom-3 right-3 w-2.5 h-2.5 rounded-full {status === 'quiero-ver' ? 'bg-blue-500' : 'bg-green-500'}"></div>
		{/if}

		<div class="absolute top-2 right-2 flex flex-col gap-1">
			<button
				id="quiero-{movie.slug}"
				onclick={(e) => { e.preventDefault(); e.stopPropagation(); watchlist.toggleQuieroVer(movie.slug); }}
				class="p-1 rounded-full border border-white/30 transition-colors {status === 'quiero-ver' ? 'bg-blue-500/80 text-white' : 'bg-black/30 text-white/60 hover:text-white hover:bg-black/50'}"
			>
				<Bookmark class="w-3.5 h-3.5" fill={status === 'quiero-ver' ? 'currentColor' : 'none'} />
			</button>
			<Tooltip triggeredBy="#quiero-{movie.slug}" type="light" class="text-xs">Quiero ver</Tooltip>
			<button
				id="visto-{movie.slug}"
				onclick={(e) => { e.preventDefault(); e.stopPropagation(); watchlist.toggleYaLaVi(movie.slug); }}
				class="p-1 rounded-full border border-white/30 transition-colors {status === 'ya-la-vi' ? 'bg-green-500/80 text-white' : 'bg-black/30 text-white/60 hover:text-white hover:bg-black/50'}"
			>
				<Eye class="w-3.5 h-3.5" fill={status === 'ya-la-vi' ? 'currentColor' : 'none'} />
			</button>
			<Tooltip triggeredBy="#visto-{movie.slug}" type="light" class="text-xs">Ya la vi</Tooltip>
		</div>

		<div class="absolute bottom-0 left-0 right-0 p-3 text-white">
			<h5 class="text-sm font-bold tracking-tight line-clamp-1">
				{movie.title}
			</h5>
			<p class="text-xs text-gray-300 mt-0.5">
				{movie.year || "N/A"} •
				{#if movie.director}
					{#if movie.director.includes(",")}
						{@const directors = movie.director.split(",")}
						{#each directors as director, index}
							{@const isLast = index === directors.length - 1}
							<a
								href="/directors/{encodeURIComponent(director.trim())}"
								class="hover:text-indigo-400 transition-colors"
								onclick={(e) => e.stopPropagation()}
							>
								{director.trim()}{`${isLast ? "" : ", "}`}
							</a>
						{/each}
					{:else}
						<a
							href="/directors/{encodeURIComponent(movie.director)}"
							class="hover:text-indigo-400 transition-colors"
							onclick={(e) => e.stopPropagation()}
						>
							{movie.director}
						</a>
					{/if}
				{:else}
					Unknown
				{/if}
			</p>
			{#if (movie.categories ?? []).length > 0}
				<div class="flex flex-wrap gap-1 mt-1.5">
					{#each (movie.categories ?? []) as category}
						<a
							href="/categories/{encodeURIComponent(category)}"
							onclick={(e) => e.stopPropagation()}
						>
							<Badge color="indigo" class="text-[10px] px-1.5 py-0">
								{category}
							</Badge>
						</a>
					{/each}
				</div>
			{/if}
		</div>
	</div>

	{#if movie.is_top_100}
		<Badge
			color="yellow"
			class="absolute top-2 left-2 flex items-center gap-1 text-xs"
		>
			<Trophy class="w-3 h-3" />
			Top 100
		</Badge>
	{/if}
</a>
