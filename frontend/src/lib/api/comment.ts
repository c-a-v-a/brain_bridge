import type { Comment, CommentFilter } from "$lib/models/comment";
import { getTokens } from "./token";

/**
 * Base API endpoint for comment-related operations.
 */
const API_ENDPOINT = "http://localhost:8000/api/comments";

/**
 * Creates a new comment.
 *
 * Requires a valid access token for authentication.
 *
 * @param {CommentFilter} comment - The comment payload to create.
 * @returns {Promise<Comment | Error>}
 * Resolves with the created comment on success, or an Error on failure.
 */
export async function createComment(comment: CommentFilter): Promise<Comment | Error> {
  const tokens = getTokens();

  if (!tokens) {
    return new Error("No tokens");
  }

  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.accessToken}`
      },
      body: JSON.stringify(comment)
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
 * Fetches all comments associated with a specific idea.
 *
 * @param {string} ideaId - The ID of the idea to retrieve comments for.
 * @returns {Promise<Comment[] | Error>}
 * Resolves with an array of comments on success, or an Error on failure.
 */
export async function getComments(ideaId: string): Promise<Comment[] | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/${ideaId}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
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
 * Deletes a comment by its ID.
 *
 * @param {string} commentId - The ID of the comment to delete.
 * @returns {Promise<void | Error>}
 * Resolves with void on success, or an Error on failure.
 */
export async function deleteComment(commentId: string): Promise<void | Error> {
  try {
    const response = await fetch(`${API_ENDPOINT}/${commentId}`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json'
      }
    });

    const error = await response.text();
    return new Error(`Server error (${response.status}): ${error}`);
  } catch (e) {
    return new Error("Connection error");
  }
}
