<script lang="ts">
	import { onMount } from 'svelte';
	import { Button, Card, Spinner, Alert } from 'flowbite-svelte';
	import { RefreshCw } from 'lucide-svelte';
	import { goto } from '$app/navigation';
	import type { MovieListItem } from '$lib/types';

	let movies: MovieListItem[] = $state([]);
	let loading = $state(true);
	let syncing = $state(false);
	let error = $state('');
	let syncMessage = $state('');

	async function fetchMovies() {
		loading = true;
		try {
			const res = await fetch('http://localhost:8000/movies');
			if (!res.ok) throw new Error('Failed to fetch movies');
			movies = await res.json();
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function syncDatabase() {
		syncing = true;
		syncMessage = '';
		error = '';
		try {
			const res = await fetch('http://localhost:8000/sheets/sync', {
				method: 'POST'
			});
			const data = await res.json();
			if (!res.ok) throw new Error(data.detail || 'Sync failed');
			syncMessage = data.message;
			await fetchMovies();
		} catch (e: any) {
			error = e.message;
		} finally {
			syncing = false;
		}
	}

	function openMovie(slug: string | undefined) {
		if (!slug) return;
		goto(`/movies/${slug}`);
	}

	onMount(fetchMovies);
</script>

<div class="container mx-auto p-4">
	<div class="flex justify-between items-center mb-8">
		<h1 class="text-3xl font-bold text-gray-900 dark:text-white">Video Club Argento</h1>
		<Button color="dark" onclick={syncDatabase} disabled={syncing}>
			{#if syncing}
				<Spinner class="mr-2" size="4" />
				Syncing...
			{:else}
				<RefreshCw class="mr-2 h-4 w-4" />
				Sync Database
			{/if}
		</Button>
	</div>

	{#if error}
		<Alert color="red" class="mb-6">
			<span class="font-medium">Error!</span> {error}
		</Alert>
	{/if}

	{#if syncMessage}
		<Alert color="green" class="mb-6">
			<span class="font-medium">Success!</span> {syncMessage}
		</Alert>
	{/if}

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<Spinner size="12" />
		</div>
	{:else if movies.length === 0}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">No movies found. Click "Sync Database" to load them.</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
			{#each movies as movie}
				<button
					onclick={() => openMovie(movie.slug)}
					class="block w-full text-left cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg"
				>
				<Card>
					<div class="aspect-[2/3] bg-gray-200 dark:bg-gray-700 overflow-hidden">
						{#if movie.poster_url}
							<img
								src={movie.poster_url}
								alt={movie.title}
								class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
							/>
						{:else}
							<div class="w-full h-full flex items-center justify-center text-gray-400">
								No Poster
							</div>
						{/if}
					</div>
					<div class="p-4">
						<h5 class="text-lg font-bold tracking-tight text-gray-900 dark:text-white line-clamp-1">
							{movie.title}
						</h5>
						<p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
							{movie.year || 'N/A'} • {movie.director || 'Unknown'}
						</p>
						<div class="flex justify-between items-center">
							<span class="text-xs font-medium px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
								★ {movie.rating || 'N/A'}
							</span>
							{#if movie.watch_link}
								<a
									href={movie.watch_link}
									target="_blank"
									rel="noopener noreferrer"
									onclick={(e) => e.stopPropagation()}
									class="text-blue-600 hover:underline text-sm font-medium"
								>
									Watch Now
								</a>
							{/if}
						</div>
					</div>
				</Card>
				</button>
			{/each}
		</div>
	{/if}
</div>
