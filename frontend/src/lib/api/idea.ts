import type { Idea, IdeaCreate, IdeaGet, IdeaUpdate } from "$lib/models/idea";
import { getTokens } from "./token";

/**
 * Base API endpoint for idea-related operations.
 */
const API_ENDPOINT = "http://localhost:8000/api/ideas";

/**
 * Creates a new idea.
 *
 * @param {IdeaCreate} idea - The idea payload to create.
 * @returns {Promise<Idea | Error>}
 * Resolves with the created idea on success, or an Error on failure.
 */
export async function createIdea(idea: IdeaCreate): Promise<Idea | Error> {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(idea)
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Fetches all ideas.
 *
 * @returns {Promise<IdeaGet[] | Error>}
 * Resolves with an array of ideas on success, or an Error on failure.
 */
export async function getIdeas(): Promise<IdeaGet[] | Error> {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Fetches a single idea by its ID.
 *
 * @param {string} id - The ID of the idea.
 * @returns {Promise<Idea | Error>}
 * Resolves with the idea on success, or an Error on failure.
 */
export async function getIdea(id: string): Promise<Idea | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/${id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Fetches all ideas created by a specific user.
 *
 * @param {string} id - The user ID.
 * @returns {Promise<IdeaGet[] | Error>}
 * Resolves with an array of ideas on success, or an Error on failure.
 */
export async function getUsersIdeas(id: string): Promise<IdeaGet[] | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/user/${id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Fetches all ideas liked by a specific user.
 *
 * @param {string} id - The user ID.
 * @returns {Promise<IdeaGet[] | Error>}
 * Resolves with an array of liked ideas on success, or an Error on failure.
 */
export async function likedIdeas(id: string): Promise<IdeaGet[] | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/liked/${id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Updates an existing idea.
 *
 * @param {string} id - The ID of the idea to update.
 * @param {IdeaUpdate} idea - The updated idea data.
 * @returns {Promise<Idea | Error>}
 * Resolves with the updated idea on success, or an Error on failure.
 */
export async function updateIdea(id: string, idea: IdeaUpdate): Promise<Idea | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(idea)
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Likes an idea on behalf of the authenticated user.
 *
 * Requires a valid access token.
 *
 * @param {string} id - The ID of the idea to like.
 * @returns {Promise<Idea | Error>}
 * Resolves with the updated idea on success, or an Error on failure.
 */
export async function likeIdea(id: string): Promise<Idea | Error> {
  const tokens = getTokens();

  if (!tokens) {
    return new Error("No tokens");
  }

  try {
    const response = await fetch(`${API_ENDPOINT}/${id}/like`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.accessToken}`
      }
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Removes a like from an idea on behalf of the authenticated user.
 *
 * Requires a valid access token.
 *
 * @param {string} id - The ID of the idea to unlike.
 * @returns {Promise<Idea | Error>}
 * Resolves with the updated idea on success, or an Error on failure.
 */
export async function unlikeIdea(id: string): Promise<Idea | Error> {
  const tokens = getTokens();

  if (!tokens) {
    return new Error("No tokens");
  }

  try {
    const response = await fetch(`${API_ENDPOINT}/${id}/unlike`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.accessToken}`
      }
    });

    if (response.ok) {
      return await response.json();
    }

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}

/**
 * Deletes an idea by its ID.
 *
 * @param {string} id - The ID of the idea to delete.
 * @returns {Promise<void | Error>}
 * Resolves with void on success, or an Error on failure.
 */
export async function deleteIdea(id: string): Promise<void | Error> {
  try {
    await fetch(`${API_ENDPOINT}/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (e) {
    return new Error("Connection error");
  }
}
