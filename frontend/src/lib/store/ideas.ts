import { writable, type Writable } from "svelte/store";
import type { IdeaGet } from "$lib/models/ideaModels";

/**
 * A writable Svelte store holding the current authentication tokens.
 */
export const ideasStore: Writable<IdeaGet[]> = writable([]);