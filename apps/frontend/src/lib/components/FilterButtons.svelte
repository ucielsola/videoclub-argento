<script lang="ts">
import { ButtonToggle, ButtonToggleGroup } from "flowbite-svelte";
import { movies } from "$lib/state";
</script>

<div class="mt-4 flex justify-center">
    <ButtonToggleGroup
        color="gray"
        class="overflow-hidden rounded-full"
        value={movies.activeFilter}
        onSelect={(v) => {
            if (v) {
                movies.setFilter(v as "all" | "director" | "year");
            }
        }}
        ctxBtnClass="border border-gray-300 dark:border-gray-600 first:rounded-l-full last:rounded-r-full"
    >
        <ButtonToggle value="all">Todo</ButtonToggle>
        <ButtonToggle value="title">Título</ButtonToggle>
        <ButtonToggle value="director">Director</ButtonToggle>
        <ButtonToggle value="year">Año</ButtonToggle>
    </ButtonToggleGroup>
</div>
