import type { TokenPair } from "$lib/models/token";
import type { UserCreate, UserGet, UserLogin } from "$lib/models/user";
import { setTokens } from "./token";

/**
 * Base API route for authentication endpoints.
 */
const API_ROUTE = "http://localhost:8000/api/auth";

/**
 * Authenticates a user and retrieves an access/refresh token pair.
 *
 * On successful login, the returned tokens are automatically
 * stored using {@link setTokens}.
 *
 * @param {UserLogin} user - The user login credentials.
 * @returns {Promise<TokenPair | Error>}
 * Resolves with a token pair on success, or an Error on failure.
 */
export async function login(user: UserLogin): Promise<TokenPair | Error> {
  try {
    const response = await fetch(`${API_ROUTE}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
    });
    
    if (response.ok) {
      const tokens: TokenPair = await response.json();
      setTokens(tokens);
      return tokens;
    }
    
    return new Error(await response.text());
  } catch (e) {
    return new Error("Connection error.");
  }
}

/**
 * Registers a new user account.
 *
 * @param {UserCreate} user - The user registration data.
 * @returns {Promise<UserGet | Error>}
 * Resolves with the created user on success, or an Error on failure.
 */
export async function register(user: UserCreate): Promise<UserGet | Error> {
  try {
    const response = await fetch(`${API_ROUTE}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
    });
    
    if (response.ok) {
      return await response.json();
    }
    
    return new Error(await response.text());
  } catch (e) {
    return new Error("Connection error.");
  }
}
