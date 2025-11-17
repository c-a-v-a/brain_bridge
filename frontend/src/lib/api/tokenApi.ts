/**
 * @module api.tokenApi
 * @description Provides API helper functions for refreshing and validating tokens.
 */

import type { TokenPair } from "$lib/models/tokenModels";
import Cookies from 'js-cookie';

const API_ROUTE = "http://localhost:8000/api/auth";
const ACCESS_TOKEN_NAME = 'access_token';
const REFRESH_TOKEN_NAME = 'refresh_token';
const ACCESS_TOKEN_MAX_AGE_DAYS = 30 / (24 * 60); // approx. 30 minutes in days
const REFRESH_TOKEN_MAX_AGE_DAYS = 7; // 7 days
const EXPIRED_COOKIE = "expired_cookie";

/**
 * Sets tokens in cookies.
 * @param tokens - The new TokenPair to set.
 */
export function setTokens(tokens: TokenPair): void {
  Cookies.set(ACCESS_TOKEN_NAME, tokens.access_token, { expires: ACCESS_TOKEN_MAX_AGE_DAYS });
  Cookies.set(REFRESH_TOKEN_NAME, tokens.refresh_token, { expires: REFRESH_TOKEN_MAX_AGE_DAYS });
}


export function getTokens(): TokenPair | null {
  const accessToken = Cookies.get(ACCESS_TOKEN_NAME);
  const refreshToken = Cookies.get(REFRESH_TOKEN_NAME);

  if (!refreshToken) {
    return null;
  }

  if (!accessToken) {
    return {
      access_token: EXPIRED_COOKIE,
      refresh_token: refreshToken
    };
  }

  return {
    access_token: accessToken,
    refresh_token: refreshToken
  };
}

/**
 * Removes all token cookies.
 */
export function logout(): void {
  Cookies.remove(ACCESS_TOKEN_NAME);
  Cookies.remove(REFRESH_TOKEN_NAME);
}

/**
 * Attempts to refresh the access token using the refresh token.
 * @returns The new TokenPair on success, or an Error object on failure.
 */
export async function refresh(): Promise<TokenPair | Error> {
  const tokens = getTokens();

  if (!tokens) {
    return new Error("Cannot refresh tokens. No refresh token is set.");
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

    return new Error("Token refresh failed due to server rejection.");
  } catch (e) {
    console.error("Network error during refresh:", e);
    return new Error("Communication error with refresh endpoint.");
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