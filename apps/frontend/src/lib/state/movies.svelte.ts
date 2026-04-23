import Fuse from 'fuse.js';
import type { MovieListItem } from '$lib/types';

const API_BASE = 'http://localhost:8000';

export type FilterMode = 'all' | 'title' | 'director' | 'year';

class MoviesStore {
	#list = $state<MovieListItem[]>([]);
	#loading = $state(false);
	#syncing = $state(false);
	#error = $state<string | null>(null);
	#syncMessage = $state<string | null>(null);
	#searchQuery = $state('');
	#activeFilter = $state<FilterMode>('all');

	constructor() {
		this.loadMovies();
	}

	get list(): MovieListItem[] { return this.#list; }
	get loading(): boolean { return this.#loading; }
	get syncing(): boolean { return this.#syncing; }
	get error(): string | null { return this.#error; }
	get syncMessage(): string | null { return this.#syncMessage; }
	get searchQuery(): string { return this.#searchQuery; }
	set searchQuery(v: string) { this.#searchQuery = v; }

	get activeFilter(): FilterMode { return this.#activeFilter; }
	set activeFilter(v: FilterMode) { this.#activeFilter = v; }

	get #fuseInstance(): Fuse<MovieListItem> {
		return new Fuse(this.#list, {
			keys: [
				{ name: 'search_title', weight: 0.7 },
				{ name: 'title', weight: 0.7 },
				{ name: 'director', weight: 0.3 },
			],
			threshold: 0.3,
			includeScore: true,
		});
	}

	get filteredList(): MovieListItem[] {
		if (!this.#searchQuery.trim()) return this.#list;

		const results = this.#fuseInstance.search(this.#searchQuery);

		if (this.#activeFilter === 'title') {
			return results
				.filter(r => r.item.title?.toLowerCase().includes(this.#searchQuery.toLowerCase()))
				.map(r => r.item);
		}

		if (this.#activeFilter === 'director') {
			return results
				.filter(r => r.item.director?.toLowerCase().includes(this.#searchQuery.toLowerCase()))
				.map(r => r.item);
		}

		if (this.#activeFilter === 'year') {
			const year = parseInt(this.#searchQuery);
			if (isNaN(year)) return results.map(r => r.item);
			return results
				.filter(r => r.item.year === year || r.item.year?.toString().includes(this.#searchQuery))
				.map(r => r.item);
		}

		return results.map(r => r.item);
	}

	get directors(): string[] {
		const set = new Set(
			this.#list
				.map(m => m.director)
				.filter((d): d is string => typeof d === 'string')
		);
		return Array.from(set).sort();
	}

	get years(): number[] {
		const set = new Set(this.#list.map(m => m.year).filter(Boolean) as number[]);
		return Array.from(set).sort((a, b) => b - a);
	}

	setSearchQuery(query: string): void {
		this.#searchQuery = query;
	}

	setFilter(filter: FilterMode): void {
		this.#activeFilter = filter;
	}

	async loadMovies(): Promise<void> {
		this.#loading = true;
		this.#error = null;
		this.#syncMessage = null;
		try {
			const res = await fetch(`${API_BASE}/movies`);
			if (!res.ok) throw new Error('Failed to fetch movies');
			this.#list = await res.json();
		} catch (e: unknown) {
			this.#error = e instanceof Error ? e.message : 'Unknown error';
		} finally {
			this.#loading = false;
		}
	}

	async syncDatabase(): Promise<void> {
		this.#syncing = true;
		this.#error = null;
		this.#syncMessage = null;
		try {
			const res = await fetch(`${API_BASE}/sheets/sync`, { method: 'POST' });
			const data = await res.json();
			if (!res.ok) throw new Error(data.detail || 'Sync failed');
			this.#syncMessage = data.message;
			await this.loadMovies();
		} catch (e: unknown) {
			this.#error = e instanceof Error ? e.message : 'Unknown error';
		} finally {
			this.#syncing = false;
		}
	}

	clearMessages(): void {
		this.#error = null;
		this.#syncMessage = null;
	}
}

export const movies = new MoviesStore();