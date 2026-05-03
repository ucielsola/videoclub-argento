<script lang="ts">
import type { Snippet } from "svelte";
import { watchlist } from "$lib/state";

interface Props {
	activeTab: "quiero" | "visto";
	onchange?: (tab: "quiero" | "visto") => void;
	children?: Snippet<[{ count: number }]>;
}

let { activeTab, onchange, children }: Props = $props();

const quieroCount = $derived(watchlist.quieroVerList.length);
const vistoCount = $derived(watchlist.yaLaViList.length);
</script>

<div class="flex gap-2">
	<button
		onclick={() => onchange?.("quiero")}
		class="px-3 py-1.5 text-xs rounded-full transition-colors {activeTab === 'quiero' ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
	>
		Quiero ver ({quieroCount})
	</button>
	<button
		onclick={() => onchange?.("visto")}
		class="px-3 py-1.5 text-xs rounded-full transition-colors {activeTab === 'visto' ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
	>
		Ya la vi ({vistoCount})
	</button>
	{#if children}
		{@render children({ count: quieroCount + vistoCount })}
	{/if}
</div>
