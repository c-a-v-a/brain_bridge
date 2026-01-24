import type { TokenPair } from "$lib/models/token";
import type { UserGet } from "$lib/models/user";
import Cookies from 'js-cookie';

/**
 * Base API route for authentication-related endpoints.
 */
const API_ROUTE = "http://localhost:8000/api/auth";

/**
 * Cookie name for the access token.
 */
const ACCESS_TOKEN_NAME = 'access_token';

/**
 * Cookie name for the refresh token.
 */
const REFRESH_TOKEN_NAME = 'refresh_token';

/**
 * Access token expiration in days.
 * (30 minutes expressed in days for js-cookie)
 */
const ACCESS_TOKEN_MAX_AGE_DAYS = 30 / (24 * 60);

/**
 * Refresh token expiration in days.
 */
const REFRESH_TOKEN_MAX_AGE_DAYS = 7;

/**
 * Placeholder value used when the access token is expired
 * but a refresh token is still present.
 */
const EXPIRED_COOKIE = "expired_cookie";

/**
 * Stores access and refresh tokens in cookies.
 *
 * @param {TokenPair} tokens - The access and refresh token pair to store.
 */
export function setTokens(tokens: TokenPair): void {
  Cookies.set(ACCESS_TOKEN_NAME, tokens.accessToken, { expires: ACCESS_TOKEN_MAX_AGE_DAYS });
  Cookies.set(REFRESH_TOKEN_NAME, tokens.refreshToken, { expires: REFRESH_TOKEN_MAX_AGE_DAYS });
}

/**
 * Retrieves stored authentication tokens from cookies.
 *
 * @returns {TokenPair | null}
 * Returns null if no refresh token exists.
 * If the access token is missing but the refresh token exists,
 * the access token will be set to a placeholder value.
 */
export function getTokens(): TokenPair | null {
  const accessToken = Cookies.get(ACCESS_TOKEN_NAME);
  const refreshToken = Cookies.get(REFRESH_TOKEN_NAME);

  if (!refreshToken) {
    return null;
  }

  if (!accessToken) {
    return {
      accessToken: EXPIRED_COOKIE,
      refreshToken: refreshToken
    };
  }

  return {
    accessToken: accessToken,
    refreshToken: refreshToken
  };
}

/**
 * Logs the user out by removing authentication cookies.
 */
export function logout(): void {
  Cookies.remove(ACCESS_TOKEN_NAME);
  Cookies.remove(REFRESH_TOKEN_NAME);
}

/**
 * Attempts to refresh authentication tokens using the refresh token.
 *
 * On success, newly issued tokens are stored in cookies.
 *
 * @returns {Promise<TokenPair | Error>}
 * Resolves with a new token pair on success, or an Error on failure.
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
    return new Error("Connection error.");
  }
}

/**
 * Validates the current access token and retrieves the authenticated user.
 *
 * Requires a valid access token.
 *
 * @returns {Promise<UserGet | Error>}
 * Resolves with the user data on success, or an Error on failure.
 */
export async function validate(): Promise<UserGet | Error> {
  const tokens = getTokens();

  if (!tokens) {
    return new Error("No tokens set");
  }

  try {
    const response = await fetch(`${API_ROUTE}/validate`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.accessToken}`
      },
    });

    return await response.json();
  } catch (e) {
    return new Error("Connection error.");
  }
}
