/**
 * @module api.userApi
 * @description Provides api helper functions for user authentication, including login and registration.
 */

import type { TokenPair } from "$lib/models/tokenModels";
import type { UserCreate, UserGet, UserLogin } from "$lib/models/userModels";
import { setTokens } from "./tokenApi";

const API_ROUTE = "http://localhost:8000/api/auth";

/**
 * Logs in a user with the provided credentials.
 *
 * Sends a POST request to the `/login` endpoint with the user's login data.
 *
 * @param {UserLogin} user - The user's login information (username/email and password).
 * @returns {Promise<TokenPair | Error>} Resolves with a TokenPair if login is successful, or an Error if it fails.
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
    
    const error: Error = new Error(await response.text());
    return error;
  } catch (e) {
    return new Error("Could not connect to the api.");
  }
}

/**
 * Registers a new user with the provided information.
 *
 * Sends a POST request to the `/register` endpoint with the user's registration data.
 *
 * @param {UserCreate} user - The user's registration information.
 * @returns {Promise<UserGet | Error>} Resolves with the created user data if successful, or an Error if registration fails.
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
      const user: UserGet = await response.json();
      return user;
    }
    
    const error: Error = new Error(await response.text());
    return error;
  } catch (e) {
    return new Error("Could not connect to the api.");
  }
}