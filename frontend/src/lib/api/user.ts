import type { TokenPair } from "$lib/models/token";
import type { UserCreate, UserGet, UserLogin } from "$lib/models/user";
import { setTokens } from "./token";

const API_ROUTE = "http://localhost:8000/api/auth";

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
    return new Error("Connection error.");
  }
}

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
    return new Error("Connection error.");
  }
}