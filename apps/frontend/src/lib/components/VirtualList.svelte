<script lang="ts" generics="T">
import type { Snippet } from "svelte";
import { fade } from "svelte/transition";

interface Props {
	items: T[];
	itemHeight: number;
	minColWidth?: number;
	gap?: number;
	overscan?: number;
	useWindowScroll?: boolean;
	row: Snippet<[{ item: T; index: number }]>;
	children?: Snippet;
}

let {
	items,
	itemHeight,
	minColWidth = 320,
	maxCols = 4,
	gap = 8,
	overscan = 3,
	useWindowScroll = false,
	row,
	children,
}: Props = $props();

let scrollTop = $state(0);
let containerHeight = $state(0);
let containerWidth = $state(0);
let containerRef: HTMLDivElement | undefined = $state();

let containerTop = 0;
let rafId = 0;

const columnsCount = $derived(
	Math.max(1, Math.min(maxCols, Math.floor(containerWidth / minColWidth))),
);

const rowHeight = $derived(itemHeight + gap);
const totalRows = $derived(Math.ceil(items.length / columnsCount));
const totalHeight = $derived(totalRows * rowHeight);

export function scrollToIndex(
	index: number,
	behavior: ScrollBehavior = "auto",
) {
	if (index < 0 || index >= items.length) return;

	const rowIndex = Math.floor(index / columnsCount);
	const targetScrollTop = rowIndex * rowHeight;

	if (useWindowScroll) {
		const top = containerRef ? containerTop + targetScrollTop : targetScrollTop;
		window.scrollTo({ top, behavior });
	} else {
		containerRef?.scrollTo({ top: targetScrollTop, behavior });
	}
}

export function scrollTo(options?: ScrollToOptions) {
	if (useWindowScroll) {
		window.scrollTo(options);
	} else {
		containerRef?.scrollTo(options);
	}
}

const startRow = $derived(
	Math.max(0, Math.floor(scrollTop / rowHeight) - overscan),
);
const visibleRows = $derived(
	Math.ceil(containerHeight / rowHeight) + overscan * 2,
);
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

function handleContainerScroll(e: Event) {
	scrollTop = (e.currentTarget as HTMLElement).scrollTop;
}

function recalcTop() {
	if (!containerRef) return;
	containerTop = containerRef.offsetTop;
}

function scheduleWindowUpdate() {
	cancelAnimationFrame(rafId);
	rafId = requestAnimationFrame(() => {
		if (!containerRef) return;
		const rect = containerRef.getBoundingClientRect();
		scrollTop = Math.max(0, -rect.top);
		containerHeight = Math.max(0, window.innerHeight - Math.max(0, rect.top));
	});
}

$effect(() => {
	if (containerRef === undefined) return;

	const observer = new ResizeObserver(() => {
		if (containerRef === undefined) return;
		containerWidth = containerRef.clientWidth;
		if (!useWindowScroll) {
			containerHeight = containerRef.clientHeight;
		}
	});
	observer.observe(containerRef);
	return () => observer.disconnect();
});

$effect(() => {
	if (!useWindowScroll || !containerRef) return;

	recalcTop();

	scheduleWindowUpdate();

	window.addEventListener("scroll", scheduleWindowUpdate, {
		passive: true,
	});
	window.addEventListener("resize", scheduleWindowUpdate, {
		passive: true,
	});
	return () => {
		window.removeEventListener("scroll", scheduleWindowUpdate);
		window.removeEventListener("resize", scheduleWindowUpdate);
		cancelAnimationFrame(rafId);
	};
});
</script>

<div
    bind:this={containerRef}
    onscroll={useWindowScroll ? undefined : handleContainerScroll}
    role="list"
    aria-label="Virtual grid"
    class="relative {useWindowScroll
        ? ''
        : 'h-full overflow-y-auto [-webkit-overflow-scrolling:touch]'}"
    style="contain: layout style;"
>
    <div class="w-full" style="height: {totalHeight}px; contain: size layout;">
        <div
            class="will-change-transform"
            style="transform: translateY({offsetY}px);"
        >
            <div
                class="grid justify-center"
                style="
                        grid-template-columns: repeat({columnsCount}, minmax(0, {columnsCount ===
                1
                    ? 'max-content'
                    : '1fr'}));
                        gap: {gap}px;
                    "
            >
                {#each visibleItems as { item, index } (index)}
                    <div
                        class="w-full"
                        style="height: {itemHeight}px; content-visibility: auto; contain-intrinsic-size: 0 {itemHeight}px;"
                        transition:fade
                    >
                        {@render row({ item, index })}
                    </div>
                {/each}
            </div>
        </div>
    </div>

    {@render children?.()}
</div>
