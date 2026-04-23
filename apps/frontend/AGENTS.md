# Frontend Agent Guide

## 🎯 Purpose
A modern SvelteKit web interface for browsing and managing the movie collection.

## 🛠️ Tech Stack
- **Svelte 5**: Uses Runes (`$state`, `$derived`) and Snippets.
- **Tailwind CSS v4**: High-performance styling via the Vite plugin.
- **Flowbite Svelte v2**: UI component library built for Svelte 5.

## 🧩 Key Logic
- `src/routes/+page.ts`: Fetches movie data from the backend during SSR.
- `src/routes/+page.svelte`: Displays the movie grid and handles the "Sync" action.
- `src/app.css`: Central Tailwind v4 configuration.

## 🚀 How to Run
```bash
npm run dev
```

## 🏗️ Store Pattern (Svelte 5 Runes)

Use class-based stores with private `$state` fields and public getters:

```typescript
class MoviesStore {
  #loading = $state<boolean>(false);
  #error = $state<string | null>(null);
  #list = $state<Movie[]>([]);

  constructor() {
    this.loadMovies();
  }

  public async loadMovies(): Promise<void> {
    this.#loading = true;
    try {
      this.#list = await api.getMovies();
    } catch (e) {
      this.#error = "Failed to load movies";
    } finally {
      this.#loading = false;
    }
  }

  get loading(): boolean { return this.#loading; }
  get error(): string | null { return this.#error; }
  get list(): Movie[] { return this.#list; }
}

export const movies = new MoviesStore();
```

Then use in Svelte components:
```svelte
{#if movies.loading}
  <Spinner />
{:else}
  {#each movies.list as movie}
    <MovieCard {movie} />
  {/each}
{/if}
```
