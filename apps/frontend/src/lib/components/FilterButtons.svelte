<script lang="ts">
	import { ButtonToggleGroup, ButtonToggle } from 'flowbite-svelte';
	import { movies } from '$lib/state';
</script>

<div class="mt-4 flex justify-center">
	<ButtonToggleGroup
		color="gray"
		value={movies.activeFilter}
		onSelect={(v) => {
			if (typeof v === 'string') {
				movies.setFilter(v as 'all' | 'director' | 'year');
			}
		}}
		ctxBtnClass="border-gray-300 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-600 first:rounded-l-full last:rounded-r-full"
	>
		<ButtonToggle value="all">Todo</ButtonToggle>
		<ButtonToggle value="director">Director</ButtonToggle>
		<ButtonToggle value="year">Año</ButtonToggle>
	</ButtonToggleGroup>
</div>