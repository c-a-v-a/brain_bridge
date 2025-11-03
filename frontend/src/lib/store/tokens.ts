/**
 * @module TokenStore
 * @description Provides a Svelte writable store to manage authentication tokens.
 */
import type { TokenPair } from "$lib/models/tokenModels";
import { writable, type Writable } from "svelte/store";

/**
 * A writable Svelte store holding the current authentication tokens.
 */
export const tokens: Writable<TokenPair> = writable({
  access_token: "",
  refresh_token: ""
});