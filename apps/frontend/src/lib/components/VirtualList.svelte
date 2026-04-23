<script lang="ts" generics="T">
	import type { Snippet } from 'svelte';

	interface Props {
		items: T[];
		itemHeight: number;
		minColWidth?: number;
		gap?: number;
		overscan?: number;
		contained?: boolean;
		row: Snippet<[{ item: T; index: number }]>;
		children?: Snippet;
	}

	let {
		items,
		itemHeight,
		minColWidth = 340,
		gap = 8,
		overscan = 3,
		contained = true, // Defaulting to true because it's a huge performance win
		row,
		children
	}: Props = $props();

	let scrollTop = $state(0);
	let containerHeight = $state(0);
	let containerWidth = $state(0);
	let containerRef: HTMLDivElement | undefined = $state();

	const columnsCount = $derived(
		Math.max(1, Math.floor(containerWidth / minColWidth))
	);

	const rowHeight = $derived(itemHeight + gap);
	const totalRows = $derived(Math.ceil(items.length / columnsCount));
	const totalHeight = $derived(totalRows * rowHeight);

	export function scrollToIndex(index: number, behavior: ScrollBehavior = 'auto') {
		if (!containerRef || index < 0 || index >= items.length) return;

		// Calculate which row this index lives on
		const rowIndex = Math.floor(index / columnsCount);
		// Calculate exactly where that row sits vertically
		const targetScrollTop = rowIndex * rowHeight;

		containerRef.scrollTo({ top: targetScrollTop, behavior });
	}

	export function scrollTo(options?: ScrollToOptions) {
		containerRef?.scrollTo(options);
	}

	const startRow = $derived(Math.max(0, Math.floor(scrollTop / rowHeight) - overscan));
	const visibleRows = $derived(Math.ceil(containerHeight / rowHeight) + overscan * 2);
	const endRow = $derived(Math.min(totalRows, startRow + visibleRows));

	const visibleItems = $derived.by(() => {
		const result: { item: T; index: number }[] = [];
		for (let rowIdx = startRow; rowIdx < endRow; rowIdx++) {
			const startIdx = rowIdx * columnsCount;
			const endIdx = Math.min(startIdx + columnsCount, items.length);
			for (let i = startIdx; i < endIdx; i++) {
				result.push({ item: items[i], index: i });
			}
		}
		return result;
	});

	const offsetY = $derived(startRow * rowHeight);

	function handleScroll(e: Event) {
		scrollTop = (e.currentTarget as HTMLElement).scrollTop;
	}
</script>

<div
	bind:this={containerRef}
	bind:clientHeight={containerHeight}
	bind:clientWidth={containerWidth}
	onscroll={handleScroll}
	role="list"
	aria-label="Virtual grid"
	class="relative h-full overflow-y-auto [-webkit-overflow-scrolling:touch]"
>
	<div class="relative w-full" style="height: {totalHeight}px;">
		<div class="absolute left-0 top-0 w-full" style="transform: translateY({offsetY}px);">
			<div
				class="grid"
				style="grid-template-columns: repeat({columnsCount}, minmax(0, 1fr)); gap: {gap}px;"
			>
				{#each visibleItems as { item, index } (index)}
					<div
						class="w-full {contained ? 'contain-[layout_style_paint]' : ''}"
						style="height: {itemHeight}px;"
					>
						{@render row({ item, index })}
					</div>
				{/each}
			</div>
		</div>
	</div>

	{@render children?.()}
</div>
