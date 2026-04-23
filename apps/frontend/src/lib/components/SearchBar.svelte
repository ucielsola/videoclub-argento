<script lang="ts">
	import { Search, X } from 'lucide-svelte';
	import { movies } from '$lib/state';

	let inputValue = $state('');
	let debounceTimer: ReturnType<typeof setTimeout> | undefined = $state();

	function handleInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		inputValue = value;
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			movies.setSearchQuery(value);
		}, 500);
	}

	function handleClear() {
		inputValue = '';
		clearTimeout(debounceTimer);
		movies.setSearchQuery('');
	}
</script>

<div class="relative">
	<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
	<input
		type="text"
		placeholder="Buscar películas..."
		value={inputValue}
		oninput={handleInput}
		aria-label="Buscar películas"
		class="w-full pl-10 {inputValue ? 'pr-10' : 'pr-4'} py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-800 dark:text-white"
	/>
	{#if inputValue}
		<button
			type="button"
			onclick={handleClear}
			class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
			aria-label="Limpiar búsqueda"
		>
			<X class="w-5 h-5" />
		</button>
	{/if}
</div>