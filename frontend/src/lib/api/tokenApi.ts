/**
 * @module api.tokenApi
 * @description Provides API helper functions for refreshing and validating tokens.
 */

import type { TokenPair } from "$lib/models/tokenModels";
import Cookies from 'js-cookie';

const API_ROUTE = "http://localhost:8000/api/auth";
const ACCESS_TOKEN_NAME = 'access_token';
const REFRESH_TOKEN_NAME = 'refresh_token';

/**
 * Saves both tokens in cookies.
 *
 * @param {TokenPair} tokens
 */
export function setTokens(tokens: TokenPair): void {
  // Access token - 1/288 day = 5 min
  Cookies.set(ACCESS_TOKEN_NAME, tokens.access_token, {
    expires: 1 / 288,
    secure: false, // Should be `true` in prod (HTTPS required)
    sameSite: 'Lax'
  });

  // Refresh token
  Cookies.set(REFRESH_TOKEN_NAME, tokens.refresh_token, {
    expires: 7,
    secure: false, // Should be `true` in prod
    sameSite: 'Lax'
  });
}

/**
 * Get JWT tokens from cookies
 *
 * @returns {TokenPair | null} Resolves with a new TokenPair if successful, or null otherwise
 */
export function getTokens(): TokenPair | null {
  const accessToken = Cookies.get(ACCESS_TOKEN_NAME);
  const refreshToken = Cookies.get(REFRESH_TOKEN_NAME);

  if (accessToken && refreshToken) {
    return {
      access_token: accessToken,
      refresh_token: refreshToken
    };
  }
  return null;
}

export function logout(): void {
  Cookies.remove(ACCESS_TOKEN_NAME);
  Cookies.remove(REFRESH_TOKEN_NAME);
}

/**
 * Refreshes the given authentication tokens.
 *
 * Sends a POST request to the `/refresh` endpoint with the provided tokens.
 *
 * @returns {Promise<TokenPair | Error>} Resolves with a new TokenPair if successful, or an Error otherwise.
 */
export async function refresh(): Promise<TokenPair | Error> {
  const tokens = getTokens();
  if (!tokens) {
    return new Error("Brak tokenów do odświeżenia.");
  }

  try {
    const response = await fetch(`${API_ROUTE}/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tokens)
    });

    if (response.ok) {
      const newTokens: TokenPair = await response.json();
      setTokens(newTokens);
      return newTokens;
    }

    const error: Error = new Error(await response.text());
    return error;
  } catch (e) {
    return new Error("Nie można połączyć się z API.");
  }
}

/**
 * Validates the given access token.
 *
 * Sends a GET request to the `/validate` endpoint with the access token in the Authorization header.
 *
 * @returns {Promise<boolean | Error>} Resolves with `true` if the token is valid, `false` if not, or an Error if the request fails.
 */
export async function validate(): Promise<boolean | Error> {
  const tokens = getTokens();
  if (!tokens) {
    return false;
  }

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