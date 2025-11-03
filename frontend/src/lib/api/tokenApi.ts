/**
 * @module api.tokenApi
 * @description Provides API helper functions for refreshing and validating tokens.
 */

import type { TokenPair } from "$lib/models/tokenModels";

const API_ROUTE = "http://localhost:8000/api/auth";

/**
 * Refreshes the given authentication tokens.
 *
 * Sends a POST request to the `/refresh` endpoint with the provided tokens.
 *
 * @param {TokenPair} tokens - The current access and refresh tokens.
 * @returns {Promise<TokenPair | Error>} Resolves with a new TokenPair if successful, or an Error otherwise.
 */
export async function refresh(tokens: TokenPair): Promise<TokenPair | Error> {
  try {
    const response = await fetch(`${API_ROUTE}/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tokens)
    });

    if (response.ok) {
      const tokens: TokenPair = await response.json();
      return tokens;
    }
    
    const error: Error = new Error(await response.text());
    return error;
  } catch (e) {
    return new Error("Could not connect to the api.");
  }
}

/**
 * Validates the given access token.
 *
 * Sends a GET request to the `/validate` endpoint with the access token in the Authorization header.
 *
 * @param {TokenPair} tokens - The current access and refresh tokens.
 * @returns {Promise<boolean | Error>} Resolves with `true` if the token is valid, `false` if not, or an Error if the request fails.
 */
export async function validate(tokens: TokenPair): Promise<boolean | Error> {
    try {
    const response = await fetch(`${API_ROUTE}/validate`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.access_token}`
      },
    });
    
    return response.ok;
  } catch (e) {
    return new Error("Could not connect to the api.");
  }
}