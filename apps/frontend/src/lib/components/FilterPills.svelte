<script lang="ts">
import { movies } from "$lib/state";
import type { FilterMode } from "$lib/state/movies.svelte";

const filters: { value: FilterMode; label: string }[] = [
	{ value: "all", label: "Todo" },
	{ value: "title", label: "Título" },
	{ value: "director", label: "Director" },
	{ value: "year", label: "Año" },
];

function select(value: FilterMode) {
	movies.setFilter(value === movies.activeFilter ? "all" : value);
}
</script>

<div class="flex items-center gap-2">
    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">
        Filtrar:
    </span>
    <div
        class="flex rounded-full overflow-hidden border border-gray-300 dark:border-gray-600"
    >
        {#each filters as f, i}
            <button
                type="button"
                onclick={() => select(f.value)}
                class="px-3 py-1 text-xs font-medium transition-colors cursor-pointer
				{movies.activeFilter === f.value
                    ? 'bg-gray-700 text-white dark:bg-gray-100 dark:text-gray-900'
                    : 'bg-white text-gray-700 hover:bg-gray-100 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800'}
				{i > 0 ? 'border-l border-gray-300 dark:border-gray-600' : ''}"
            >
                {f.label}
            </button>
        {/each}
    </div>
</div>
