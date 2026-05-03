<script lang="ts">
import { movies, watchlist } from "$lib/state";

const quieroCount = $derived(watchlist.quieroVerList.length);
const vistoCount = $derived(watchlist.yaLaViList.length);

const activeFilter = $derived(movies.watchlistFilter);
</script>

<div class="flex gap-2">
	<button
		onclick={() => movies.watchlistFilter = activeFilter === 'quiero' ? null : 'quiero'}
		class="px-4 py-2 text-sm rounded-full transition-colors {activeFilter === 'quiero' ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
	>
		Quiero ver ({quieroCount})
	</button>
	<button
		onclick={() => movies.watchlistFilter = activeFilter === 'visto' ? null : 'visto'}
		class="px-4 py-2 text-sm rounded-full transition-colors {activeFilter === 'visto' ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
	>
		Ya la vi ({vistoCount})
	</button>
</div>
