# Frontend Agent Guide

## Purpose
SvelteKit web interface for browsing and managing the Argentine cinema collection.

## Tech Stack
- **Svelte 5** — Runes (`$state`, `$derived`, `$effect`) + Snippets
- **SvelteKit** — SSR load functions, adapter-auto
- **Tailwind CSS v4** — via `@tailwindcss/vite` plugin (CSS-first config, no `tailwind.config.js`)
- **Flowbite Svelte v2** — UI components (Card, Badge, Button, Spinner, Alert, ButtonToggleGroup)
- **Lucide Svelte** — icons
- **Fuse.js** — client-side fuzzy search (weighted: search_title 0.7, title 0.7, director 0.3)
- **Biome** — linting + formatting (replaces ESLint + Prettier)

## Commands
```bash
pnpm dev:fe                        # Start dev server (port 5173)
pnpm --filter frontend biome check .       # Lint
pnpm --filter frontend biome format --write .  # Format
pnpm --filter frontend check       # Typecheck (svelte-check)
pnpm generate-client               # Generate OpenAPI client (unused currently)
```

## Directory Structure
```
src/
  app.css              # Tailwind v4 config (imports, plugins, custom variants, utilities)
  app.html             # HTML shell with inline dark-mode flash prevention
  lib/
    types.ts           # Movie type definitions
    components/
      PageHeader       # Sticky header with scroll-based compaction animation
      MovieGrid        # Main browse area: search, filter, sort, VirtualList
      MovieCard        # Clickable card: poster, title, year, director link
      VirtualList      # Custom virtual-scrolled grid (Svelte 5 generics, ResizeObserver)
      SearchBar        # Debounced search input (500ms) → Fuse.js
      FilterButtons    # Toggle: Todo/Titulo/Director/Ano
      SyncButton       # Triggers POST /sheets/sync
      AlertMessage     # Error/success alerts from store
      Footer           # Fixed footer with backdrop blur
      ScrollToTop      # Appears after 400px scroll
    state/
      movies.svelte.ts # MoviesStore: list, search, filter, sort, sync, Fuse.js
      theme.svelte.ts  # ThemeStore: dark/light toggle, localStorage persistence
  routes/
    +page.svelte       # Home: movie grid with search/filter/sort
    +page.ts           # SSR: fetch all movies
    movies/[slug]/     # Movie detail page
    directors/[director]/ # Director filmography page
    +layout.svelte     # Root layout: CSS import, bg-grid-pattern, ScrollToTop
```

## State Pattern (Svelte 5 Runes)
Class-based stores with private `#field = $state()` and public getters. Singletons exported from `src/lib/state/index.ts`.

## API Calls
Currently uses raw `fetch` to `http://localhost:8000` (or `127.0.0.1:8000` for SSR). OpenAPI client is generated but not wired up.

## Biome Config (`biome.json`)
- Tabs for indentation, double quotes for JS
- Recommended rules + `noUnusedImports`/`noUnusedVariables` as warnings
- Svelte overrides: relaxed rules in `.svelte` files
- CSS linting/formatting disabled (Tailwind v4 directives)
- Excludes `src/app.css`
- Auto-organize imports enabled

## Svelte Config (`svelte.config.js`)
- Forces Runes mode globally (except `node_modules`)
- Uses `adapter-auto`

## Conventions
- Spanish-language UI
- No comments in code unless requested
- Tabs, double quotes, Biome formatting
