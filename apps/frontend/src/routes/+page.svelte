<script lang="ts">
	import Fuse from 'fuse.js';
	import { Film, RefreshCw, Search } from 'lucide-svelte';
	import { Alert, Card, Spinner } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import type { MovieListItem } from '$lib/types';
	import VirtualList from '$lib/components/VirtualList.svelte';

	let movies: MovieListItem[] = $state([]);
	let loading = $state(true);
	let syncing = $state(false);
	let error = $state('');
	let syncMessage = $state('');

	let searchQuery = $state('');
	let activeFilter = $state<'all' | 'director' | 'year'>('all');

	let fuseInstance = $derived(
		new Fuse(movies, {
			keys: [
				{ name: 'search_title', weight: 0.7 },
				{ name: 'title', weight: 0.7 },
				{ name: 'director', weight: 0.3 },
			],
			threshold: 0.3,
			includeScore: true,
		})
	);

	let filteredMovies = $derived.by(() => {
		if (!searchQuery.trim()) return movies;

		const results = fuseInstance.search(searchQuery);

		if (activeFilter === 'director') {
			return results
				.filter(r => r.item.director?.toLowerCase().includes(searchQuery.toLowerCase()))
				.map(r => r.item);
		}

		if (activeFilter === 'year') {
			const year = parseInt(searchQuery);
			if (isNaN(year)) return results.map(r => r.item);
			return results
				.filter(r => r.item.year === year || r.item.year?.toString().includes(searchQuery))
				.map(r => r.item);
		}

		return results.map(r => r.item);
	});

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

	let virtualList: { scrollTo: (options: ScrollToOptions) => void } | undefined = $state();

	function setFilter(filter: 'all' | 'director' | 'year') {
		activeFilter = filter;
		if (virtualList) {
			virtualList.scrollTo({ top: 0, behavior: 'smooth' });
		}
	}

	function openMovie(slug: string | undefined) {
		if (!slug) return;
		goto(`/movies/${slug}`);
	}

	fetchMovies();
</script>

<div class="bg-gray-50 dark:bg-gray-800 py-8 mb-8">
	<div class="container mx-auto px-4">
		<div class="flex flex-col sm:flex-row justify-between items-center mb-6">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white">
				Video Club Argento
			</h1>
			<button
				onclick={syncDatabase}
				disabled={syncing}
				class="mt-4 sm:mt-0 px-4 py-2 bg-gray-800 dark:bg-gray-700 text-white rounded-lg hover:bg-gray-700 dark:hover:bg-gray-600 disabled:opacity-50 flex items-center gap-2"
			>
				{#if syncing}
					<Spinner size="4" />
					Syncing...
				{:else}
					<RefreshCw class="w-4 h-4" />
					Sync Database
				{/if}
			</button>
		</div>

		<div class="max-w-2xl mx-auto">
			<div class="relative">
				<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
				<input
					type="text"
					placeholder="Buscar películas..."
					bind:value={searchQuery}
					aria-label="Buscar películas"
					class="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
				/>
			</div>

			<div class="mt-4 flex justify-center gap-2">
				<button
					onclick={() => setFilter('all')}
					class="px-4 py-2 rounded-lg transition-colors {activeFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
				>
					Todo
				</button>
				<button
					onclick={() => setFilter('director')}
					class="px-4 py-2 rounded-lg transition-colors {activeFilter === 'director' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
				>
					Director
				</button>
				<button
					onclick={() => setFilter('year')}
					class="px-4 py-2 rounded-lg transition-colors {activeFilter === 'year' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
				>
					Año
				</button>
			</div>
		</div>
	</div>
</div>

<div class="container mx-auto px-4">
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
		<div class="flex-1 overflow-hidden">
			<div class="h-[calc(100vh-300px)]">
				<VirtualList bind:this={virtualList} items={filteredMovies} itemHeight={280} columns={6} overscan={3}>
					{#snippet row({ item, index }: { item: unknown; index: number })}
						{@const movie = item as MovieListItem}
						<button
							onclick={() => openMovie(movie.slug)}
							class="block w-full text-left cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg"
						>
							<Card class="h-full overflow-hidden">
								<div class="aspect-[2/3] bg-gray-200 dark:bg-gray-700 overflow-hidden relative">
										{#if movie.poster_url}
											<img
												src={movie.poster_url}
												alt={movie.title}
												class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
												loading="lazy"
											/>
										{:else}
											<div class="w-full h-full flex items-center justify-center text-gray-400">
												<Film class="w-8 h-8" />
											</div>
										{/if}

										{#if movie.enrichment_status === 'PENDING'}
											<span class="absolute top-2 right-2 px-2 py-1 text-xs font-medium bg-indigo-100 text-indigo-800 rounded dark:bg-indigo-900 dark:text-indigo-300">
												Pendiente
											</span>
										{/if}
									</div>
									<div class="p-3">
										<h5 class="text-sm font-bold tracking-tight text-gray-900 dark:text-white line-clamp-1">
											{movie.title}
										</h5>
										<p class="text-xs text-gray-600 dark:text-gray-400">
											{movie.year || 'N/A'} • {movie.director || 'Unknown'}
										</p>
									</div>
								</Card>
							</button>
						{/snippet}
				</VirtualList>
			</div>
		</div>

		{#if filteredMovies.length === 0}
			<Alert color="yellow" class="mt-8">
				<span class="font-medium">No se encontraron películas.</span>
				<span>Intenta con otro término de búsqueda.</span>
			</Alert>
		{/if}
	{/if}
</div>