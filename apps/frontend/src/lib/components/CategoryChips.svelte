<script lang="ts">
import { Tag } from "lucide-svelte";
import { categories } from "$lib/state";
</script>

{#if categories.list.length > 0}
    <div class="flex items-center gap-2 overflow-x-auto pb-1 [-webkit-overflow-scrolling:touch] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        <Tag class="w-3.5 h-3.5 shrink-0 text-gray-400" />
        {#each categories.list as cat}
            <a
                href="/categories/{encodeURIComponent(cat.name)}"
                class="shrink-0 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-full transition-colors
                bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-indigo-900/40 dark:hover:text-indigo-300"
            >
                {cat.name}
                <span class="text-[10px] opacity-60">{cat.movie_count}</span>
            </a>
        {/each}
    </div>
{/if}
