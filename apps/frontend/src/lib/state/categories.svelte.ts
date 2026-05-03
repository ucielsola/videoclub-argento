import type { Category } from "$lib/types";

class CategoriesStore {
	#list = $state<Category[]>([]);

	get list(): Category[] {
		return this.#list;
	}

	initialize(list: Category[]): void {
		this.#list = list;
	}
}

export const categories = new CategoriesStore();
