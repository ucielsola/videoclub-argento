import Fuse from "fuse.js";
import type { MovieListItem, SortDirection, SortMode } from "$lib/types";

const API_BASE = "http://localhost:8000";
const DEFAULT_FILTER = "all";

export type FilterMode = "all" | "title" | "director" | "year";

class MoviesStore {
  #list = $state<MovieListItem[]>([]);
  #loading = $state(false);
  #syncing = $state(false);
  #error = $state<string | null>(null);
  #syncMessage = $state<string | null>(null);
  #searchQuery = $state("");
  #activeFilter = $state<FilterMode>("all");
  #sortBy = $state<SortMode>("title");
  #sortDirection = $state<SortDirection>("asc");

  constructor() {
    this.loadMovies();
  }

  get list(): MovieListItem[] {
    return this.#list;
  }
  get loading(): boolean {
    return this.#loading;
  }
  get syncing(): boolean {
    return this.#syncing;
  }
  get error(): string | null {
    return this.#error;
  }
  get syncMessage(): string | null {
    return this.#syncMessage;
  }
  get searchQuery(): string {
    return this.#searchQuery;
  }
  set searchQuery(v: string) {
    this.#searchQuery = v;
  }

  get activeFilter(): FilterMode {
    return this.#activeFilter;
  }
  set activeFilter(v: FilterMode) {
    this.#activeFilter = v;
  }

  get sortBy(): SortMode {
    return this.#sortBy;
  }
  set sortBy(v: SortMode) {
    this.#sortBy = v;
  }

  get sortDirection(): SortDirection {
    return this.#sortDirection;
  }
  set sortDirection(v: SortDirection) {
    this.#sortDirection = v;
  }

  #fuseInstance: Fuse<MovieListItem> | null = null;

  get #fuse(): Fuse<MovieListItem> {
    if (!this.#fuseInstance) {
      this.#fuseInstance = new Fuse(this.#list, {
        keys: [
          { name: "search_title", weight: 0.7 },
          { name: "title", weight: 0.7 },
          { name: "director", weight: 0.3 },
          { name: "year", weight: 0.5 }, // <-- Add this
        ],
        threshold: 0.3,
        includeScore: true,
      });
    }
    return this.#fuseInstance;
  }

  get filteredList(): MovieListItem[] {
    let results: MovieListItem[];

    if (!this.#searchQuery.trim()) {
      results = [...this.#list];
    } else {
      const fuseResults = this.#fuse.search(this.#searchQuery);

      if (this.#activeFilter === "title") {
        results = fuseResults
          .filter((r) =>
            r.item.title
              ?.toLowerCase()
              .includes(this.#searchQuery.toLowerCase()),
          )
          .map((r) => r.item);
      } else if (this.#activeFilter === "director") {
        results = fuseResults
          .filter((r) =>
            r.item.director
              ?.toLowerCase()
              .includes(this.#searchQuery.toLowerCase()),
          )
          .map((r) => r.item);
      } else if (this.#activeFilter === "year") {
        const year = parseInt(this.#searchQuery);
        if (isNaN(year)) {
          results = fuseResults.map((r) => r.item);
        } else {
          results = fuseResults
            .filter(
              (r) =>
                r.item.year === year ||
                r.item.year?.toString().includes(this.#searchQuery),
            )
            .map((r) => r.item);
        }
      } else {
        results = fuseResults.map((r) => r.item);
      }
    }

    if (this.#sortBy === "title") {
      results.sort(
        (a, b) =>
          a.title.localeCompare(b.title) *
          (this.#sortDirection === "asc" ? 1 : -1),
      );
    } else {
      results.sort(
        (a, b) =>
          ((a.year ?? 0) - (b.year ?? 0)) *
          (this.#sortDirection === "asc" ? 1 : -1),
      );
    }

    return results;
  }

  get directors(): string[] {
    const set = new Set(
      this.#list
        .map((m) => m.director)
        .filter((d): d is string => typeof d === "string"),
    );
    return Array.from(set).sort();
  }

  get years(): number[] {
    const set = new Set(
      this.#list.map((m) => m.year).filter(Boolean) as number[],
    );
    return Array.from(set).sort((a, b) => b - a);
  }

  setSearchQuery(query: string): void {
    this.#searchQuery = query;
  }

  setFilter(filter: FilterMode): void {
    this.#activeFilter = filter ?? DEFAULT_FILTER;
  }

  async loadMovies(): Promise<void> {
    this.#loading = true;
    this.#error = null;
    this.#syncMessage = null;
    try {
      const res = await fetch(`${API_BASE}/movies`);
      if (!res.ok) throw new Error("Failed to fetch movies");
      this.#list = await res.json();
      this.#fuseInstance = null;
    } catch (e: unknown) {
      this.#error = e instanceof Error ? e.message : "Unknown error";
    } finally {
      this.#loading = false;
    }
  }

  async syncDatabase(): Promise<void> {
    this.#syncing = true;
    this.#error = null;
    this.#syncMessage = null;
    try {
      const res = await fetch(`${API_BASE}/sheets/sync`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Sync failed");
      this.#syncMessage = data.message;
      await this.loadMovies();
    } catch (e: unknown) {
      this.#error = e instanceof Error ? e.message : "Unknown error";
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
