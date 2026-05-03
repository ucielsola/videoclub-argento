import Fuse from "fuse.js";
import type { MovieListItem, SortDirection, SortMode } from "$lib/types";

const DEFAULT_FILTER = "all";

export type FilterMode = "all" | "title" | "director" | "year";

class MoviesStore {
  #list = $state<MovieListItem[]>([]);
  #searchQuery = $state("");
  #activeFilter = $state<FilterMode>("all");
  #sortBy = $state<SortMode>("year");
  #sortDirection = $state<SortDirection>("desc");

  get list(): MovieListItem[] {
    return this.#list;
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

  initialize(list: MovieListItem[]): void {
    this.#list = list;
    this.#fuseInstance = null;
  }

  #fuseInstance: Fuse<MovieListItem> | null = null;

  get #fuse(): Fuse<MovieListItem> {
    if (!this.#fuseInstance) {
      this.#fuseInstance = new Fuse(this.#list, {
        keys: [
          { name: "title", weight: 0.7 },
          { name: "director", weight: 0.3 },
          { name: "year", weight: 0.5 },
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
        const year = parseInt(this.#searchQuery, 10);
        if (Number.isNaN(year)) {
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

  setSearchQuery(query: string): void {
    this.#searchQuery = query;
  }

  setFilter(filter: FilterMode): void {
    this.#activeFilter = filter ?? DEFAULT_FILTER;
  }
}

export const movies = new MoviesStore();
