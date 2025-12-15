import type { Idea, IdeaCreate, IdeaGet, IdeaUpdate } from "$lib/models/idea";

const API_ENDPOINT = "http://localhost:8000/api/ideas";

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

export async function getIdea(id: string): Promise<Idea | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/${id}`, {
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

export async function getUsersIdeas(id: string): Promise<IdeaGet[] | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/user/${id}`, {
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

export async function likedIdeas(id: string) {
  try {
    const response = await fetch(`API_ENDPOINT/liked/${id}`, {
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

export async function updateIdea(id: string, idea: IdeaUpdate): Promise<Idea | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/${id}`, {
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

export async function likeIdea(id: string): Promise<Idea | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/${id}/like`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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

export async function unlikeIdea(id: string): Promise<Idea | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/${id}/unlike`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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

export async function deleteIdea(id: String): Promise<void | Error> {
  try {
    const response = await fetch(`API_ENDPOINT/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (e) {
    return new Error("Connection error");
  }
}