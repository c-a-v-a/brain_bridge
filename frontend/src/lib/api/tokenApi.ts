/**
 * @module api.tokenApi
 * @description Provides API helper functions for refreshing and validating tokens.
 */

import type { TokenPair } from "$lib/models/tokenModels";
import Cookies from 'js-cookie';

const API_ROUTE = "http://localhost:8000/api/auth";
const ACCESS_TOKEN_NAME = 'access_token';
const REFRESH_TOKEN_NAME = 'refresh_token';
const ACCESS_TOKEN_MAX_AGE_DAYS = 5 / (24 * 60); // approx. 5 minutes in days
const REFRESH_TOKEN_MAX_AGE_DAYS = 7; // 7 days

/**
 * Sets tokens in cookies.
 * @param tokens - The new TokenPair to set.
 * @param serverCookies - Optional SvelteKit cookies object for server-side setting.
 */
export function setTokens(tokens: TokenPair, serverCookies?: any): void {
    const accessMaxAgeSeconds = ACCESS_TOKEN_MAX_AGE_DAYS * 24 * 60 * 60;
    const refreshMaxAgeSeconds = REFRESH_TOKEN_MAX_AGE_DAYS * 24 * 60 * 60;
    
    if (serverCookies) {
        // Server-side set: using maxAge in seconds
        serverCookies.set(ACCESS_TOKEN_NAME, tokens.access_token, { 
            path: '/', 
            secure: false, // Set to true for production HTTPS
            sameSite: 'lax', 
            maxAge: accessMaxAgeSeconds
        });
        serverCookies.set(REFRESH_TOKEN_NAME, tokens.refresh_token, { 
            path: '/', 
            secure: false, 
            sameSite: 'lax', 
            maxAge: refreshMaxAgeSeconds
        });
    } else {
        // Client-side set: using expires in days
        Cookies.set(ACCESS_TOKEN_NAME, tokens.access_token, { expires: ACCESS_TOKEN_MAX_AGE_DAYS });
        Cookies.set(REFRESH_TOKEN_NAME, tokens.refresh_token, { expires: REFRESH_TOKEN_MAX_AGE_DAYS });
    }
}

/**
 * Reads tokens from cookies.
 * CRITICAL: If the refresh_token exists but access_token is missing
 * (e.g., cookie expired), we return a dummy access_token
 * to satisfy the backend's validation model.
 */
export function getTokens(serverCookies?: any): TokenPair | null {
    let accessToken: string | undefined | null;
    let refreshToken: string | undefined | null;

    if (serverCookies) {
        // Server-side logic
        accessToken = serverCookies.get(ACCESS_TOKEN_NAME);
        refreshToken = serverCookies.get(REFRESH_TOKEN_NAME);
    } else if (typeof document !== 'undefined') {
        // Client-side logic
        accessToken = Cookies.get(ACCESS_TOKEN_NAME);
        refreshToken = Cookies.get(REFRESH_TOKEN_NAME);
    }

    if (!refreshToken) {
        return null;
    }

    if (!accessToken) {
        return {
            access_token: "expired_cookie",
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
 * @param serverCookies - Optional SvelteKit cookies object for server-side deletion.
 */
export function logout(serverCookies?: any): void {
    if (serverCookies) {
        serverCookies.delete(ACCESS_TOKEN_NAME, { path: '/' });
        serverCookies.delete(REFRESH_TOKEN_NAME, { path: '/' });
    } else if (typeof document !== 'undefined') {
        Cookies.remove(ACCESS_TOKEN_NAME);
        Cookies.remove(REFRESH_TOKEN_NAME);
    }
}

/**
 * Attempts to refresh the access token using the refresh token.
 * @param svelteKitCookies - Optional SvelteKit cookies object (only passed when run on server).
 * @returns The new TokenPair on success, or an Error object on failure.
 */
export async function refresh(svelteKitCookies?: any): Promise<TokenPair | Error> {
    // 1. Get tokens using the universal getter
    const tokens = getTokens(svelteKitCookies); 

    if (!tokens || !tokens.refresh_token) {
        if (tokens) logout(svelteKitCookies);
        return new Error("No refresh token found.");
    }
    
    // 2. Call the backend refresh endpoint
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
            setTokens(newTokens, svelteKitCookies);
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