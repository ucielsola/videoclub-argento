<script lang="ts">
import type { Enrichment } from "$lib/types";

interface SynopsisSource {
	label: string;
	synopsis: string;
}

interface Props {
	synopsis: string | null;
	enrichment: Enrichment[];
}

let { synopsis, enrichment }: Props = $props();

const sources = $derived.by(() => {
	const result: SynopsisSource[] = [];
	for (const e of enrichment) {
		const text = e.data.synopsis;
		if (text?.trim()) {
			const label = {
				cinenacional: "Cinenacional",
				tmdb: "TMDB",
				omdb: "OMDb",
				wikipedia: "Wikipedia",
			}[e.source];
			result.push({ label, synopsis: text });
		}
	}
	return result;
});

const hasMultipleSources = $derived(sources.length > 1);

let activeTab = $state<number>(0);
</script>

{#if synopsis || sources.length > 0}
    <div class="mb-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Sinopsis
        </h2>

        {#if hasMultipleSources}
            <div
                class="flex border-b border-gray-200 dark:border-gray-700 mb-3 overflow-x-auto"
            >
                <button
                    class="px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors {activeTab === 0
                        ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400'
                        : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
                    onclick={() => (activeTab = 0)}
                >
                    Sinopsis
                </button>
                {#each sources as source, i}
                    <button
                        class="px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors {activeTab ===
                        i + 1
                            ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
                        onclick={() => (activeTab = i + 1)}
                    >
                        {source.label}
                    </button>
                {/each}
            </div>

            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
                {activeTab === 0
                    ? synopsis || sources[0].synopsis
                    : sources[activeTab - 1].synopsis}
            </p>
        {:else}
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
                {synopsis || sources[0]?.synopsis || ""}
            </p>
        {/if}
    </div>
{/if}
