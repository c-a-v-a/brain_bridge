import type { Comment } from "$lib/models/comment";

const API_ENDPOINT = "http://localhost:8000/api/comments";

export async function createComment(comment: Comment): Promise<Comment | Error> {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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

export async function getComments(ideaId: string): Promise<Comment[] | Error> {
  try {
    const response = await fetch(`API_ENDPOINT${ideaId}`, {
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

export async function deleteComment(commentId: string): Promise<void | Error> {
  try {
    const response = await fetch(`API_ENDPOINT${commentId}`, {
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