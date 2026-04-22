<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		items: unknown[];
		itemHeight: number;
		columns?: number;
		overscan?: number;
		row: Snippet<[{ item: unknown; index: number }]>;
		children?: Snippet;
	}

	let { items, itemHeight, columns = 6, overscan = 3, row, children }: Props = $props();

	let scrollTop = $state(0);
	let containerHeight = $state(0);
	let containerRef: HTMLDivElement | undefined = $state();
	let containerWidth = $state(0);

	export function scrollTo(options?: ScrollToOptions) {
		containerRef?.scrollTo(options);
	}

	const columnsCount = $derived(
		Math.floor(containerWidth / 180) || columns
	);

	const rowHeight = $derived(itemHeight + 8);
	const totalRows = $derived(Math.ceil(items.length / columnsCount));
	const totalHeight = $derived(totalRows * rowHeight);

	const startRow = $derived(Math.max(0, Math.floor(scrollTop / rowHeight) - overscan));
	const visibleRows = $derived(Math.ceil(containerHeight / rowHeight) + overscan * 2);
	const endRow = $derived(Math.min(totalRows, startRow + visibleRows));

	const visibleItems = $derived.by(() => {
		const result: { item: unknown; index: number }[] = [];
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

	function handleResize(e: Event) {
		containerWidth = (e.currentTarget as HTMLElement).clientWidth;
	}
</script>

<div
	class="virtual-list-container"
	bind:this={containerRef}
	bind:clientHeight={containerHeight}
	bind:clientWidth={containerWidth}
	onscroll={handleScroll}
	onresize={handleResize}
	role="list"
	aria-label="Virtual list"
>
	<div class="virtual-list-ghost" style="height: {totalHeight}px;">
		<div class="virtual-list-window" style="transform: translateY({offsetY}px);">
			<div class="virtual-list-grid" style="--cols: {columnsCount}">
				{#each visibleItems as { item, index } (index)}
					<div class="virtual-list-item">
						{@render row({ item, index })}
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.virtual-list-container {
		height: 100%;
		overflow-y: auto;
		position: relative;
		-webkit-overflow-scrolling: touch;
	}

	.virtual-list-ghost {
		position: relative;
		width: 100%;
	}

	.virtual-list-window {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
	}

	.virtual-list-grid {
		display: grid;
		grid-template-columns: repeat(var(--cols, 6), 1fr);
		gap: 8px;
	}

	.virtual-list-item {
		width: 100%;
	}
</style>