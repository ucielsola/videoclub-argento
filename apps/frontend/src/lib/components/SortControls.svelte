<script lang="ts">
import { Badge } from "flowbite-svelte";
import { ArrowDownNarrowWide, ArrowUpNarrowWide } from "lucide-svelte";
import { movies } from "$lib/state";
import type { SortMode } from "$lib/types";

function setSort(mode: SortMode) {
	if (mode === movies.sortBy) {
		movies.sortDirection = movies.sortDirection === "asc" ? "desc" : "asc";
		return;
	}
	movies.sortBy = mode;
	movies.sortDirection = "asc";
}
</script>

<div class="flex items-center gap-2">
	<span class="text-xs font-medium text-gray-500 dark:text-gray-400">Ordenar:</span>
	<Badge
		color={movies.sortBy === "title" ? "brand" : "gray"}
		rounded
		onclick={() => setSort("title")}
		class="cursor-pointer select-none text-xs"
	>
		Título
	</Badge>
	<Badge
		color={movies.sortBy === "year" ? "brand" : "gray"}
		rounded
		onclick={() => setSort("year")}
		class="cursor-pointer select-none text-xs"
	>
		Año
	</Badge>
	<button
		type="button"
		onclick={() => (movies.sortDirection = movies.sortDirection === "asc" ? "desc" : "asc")}
		class="inline-flex items-center justify-center rounded-full p-1.5 text-gray-500 hover:bg-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors cursor-pointer"
		aria-label="Cambiar dirección de ordenamiento"
	>
		{#if movies.sortDirection === "asc"}
			<ArrowUpNarrowWide class="h-3.5 w-3.5" />
		{:else}
			<ArrowDownNarrowWide class="h-3.5 w-3.5" />
		{/if}
	</button>
</div>
