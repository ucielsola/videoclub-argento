# Frontend Plan: Classic Movie Library & Smart Search

## Objective
Implement a stable, user-friendly search interface for 3,000+ movies using Svelte 5 runes and Flowbite Svelte v2 components.

---

## Step 1: Install Fuse.js

```bash
cd apps/frontend && npm install fuse.js
```

---

## Step 2: Backend - Remove Pagination Limit

**File:** `apps/backend/main.py`

- **Line 44:** Change `limit: int = 100` → `limit: int = 10000`

---

## Step 3: Frontend - Implement Search (`+page.svelte`)

### A. Imports

```typescript
import Fuse from 'fuse.js';
import { SearchOutline, Film } from 'lucide-svelte';
import { Input, ButtonGroup, ButtonGroupItem, Badge, Alert } from 'flowbite-svelte';
```

### B. State (Svelte 5 Runes)

```typescript
let searchQuery = $state('');
let activeFilter = $state<'all' | 'director' | 'year'>('all');

// Fuse.js instance - $derived so it rebuilds when movies change
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

// Filtered & sorted results - $derived auto-calculates
let filteredMovies = $derived.by(() => {
  if (!searchQuery.trim()) return movies;
  
  const results = fuseInstance.search(searchQuery);
  
  // Apply filter-specific logic
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
  
  // 'all' - sort by score (title matches first)
  return results.map(r => r.item);
});
```

### C. Search Hero UI

```svelte
<div class="bg-gray-50 dark:bg-gray-800 py-8 mb-8">
  <div class="container mx-auto px-4">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 text-center">
      Video Club Argento
    </h1>
    
    <div class="max-w-2xl mx-auto">
      <Input
        type="text"
        placeholder="Buscar películas..."
        bind:value={searchQuery}
        aria-label="Buscar películas"
        size="lg"
      >
        <SearchOutline slot="left" class="w-5 h-5" />
      </Input>
      
      <div class="mt-4 flex justify-center">
        <ButtonGroup>
          <ButtonGroupItem
            onclick={() => activeFilter = 'all'}
            active={activeFilter === 'all'}
          >
            Todo
          </ButtonGroupItem>
          <ButtonGroupItem
            onclick={() => activeFilter = 'director'}
            active={activeFilter === 'director'}
          >
            Director
          </ButtonGroupItem>
          <ButtonGroupItem
            onclick={() => activeFilter = 'year'}
            active={activeFilter === 'year'}
          >
            Año
          </ButtonGroupItem>
        </ButtonGroup>
      </div>
    </div>
  </div>
</div>
```

### D. Results Gallery

```svelte
<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
  {#each filteredMovies as movie (movie.id)}
    <a href="/movies/{movie.slug}" class="block">
      <Card class="h-full overflow-hidden">
        <div class="aspect-[2/3] bg-gray-200 dark:bg-gray-700 overflow-hidden">
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
            <Badge color="indigo" class="absolute top-2 right-2">
              Pendiente
            </Badge>
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
    </a>
  {/each}
</div>
```

### E. Empty State

```svelte
{#if filteredMovies.length === 0}
  <Alert color="yellow" class="mt-8">
    <Film slot="icon" class="w-5 h-5" />
    <span class="font-medium">No se encontraron películas.</span>
    <span>Intenta con otro término de búsqueda.</span>
  </Alert>
{/if}
```

### F. Scroll to Top on Filter Change

```typescript
function setFilter(filter: 'all' | 'director' | 'year') {
  activeFilter = filter;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
```

---

## Step 4: Accessibility Checklist

- [ ] Input has `aria-label="Buscar películas"`
- [ ] ButtonToggleGroup (ButtonGroup) is keyboard navigable
- [ ] Movie cards use `<a>` tags for proper focus order
- [ ] Posters have `alt` text
- [ ] Proper heading hierarchy: `h1` → `h5`

---

## Questions Resolved

1. **Limit**: 10,000 movies
2. **Types**: Already updated in `src/lib/types.ts`
3. **Fuzzy matching**: Using Fuse.js with weighted keys
4. **Sorting**: Title matches (weight 0.7) prioritized over Director (weight 0.3)