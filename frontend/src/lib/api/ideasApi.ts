/**
 * @module api.ideasApi
 * @description Provides api helper functions for managing ideas.
 */

import type { IdeaCreate, IdeaGet } from "$lib/models/ideaModels";

const API_ENDPOINT = "http://localhost:8000/api/ideas";

/**
 * Sends new idea to a server
 *
 * Sends POST to '/ideas' endpoint with data from modal form.
 *
 * @param {IdeaCreate} idea
 * @returns {Promise<IdeaGet | Error>} Resolves with the created idea data if successful, or an Error if it fails.
 */
export async function createIdea(idea: IdeaCreate): Promise<IdeaGet | Error> {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(idea)
        });

        if (response.ok) {
            const createdIdea: IdeaGet = await response.json();
            return createdIdea;
        }

        const errorText = await response.text();
        const error: Error = new Error(`Błąd serwera (${response.status}): ${errorText}`);
        return error;
    } catch (e) {
        const errorMessage = e instanceof Error ? e.message : "Nie można połączyć się z API.";
        return new Error(`Błąd połączenia: ${errorMessage}`);
    }
}

/**
 * Pobiera listę wszystkich pomysłów z serwera.
 *
 * @returns {Promise<IdeaGet[] | Error>} Resolves with an array of ideas, or an Error if it fails.
 */
export async function getIdeas(): Promise<IdeaGet[] | Error> {
    try {
        // GET request do tego samego endpointu
        const response = await fetch(API_ENDPOINT, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (response.ok) {
            const ideas: IdeaGet[] = await response.json();
            return ideas;
        }

        const errorText = await response.text();
        const error: Error = new Error(`Błąd serwera (${response.status}): ${errorText}`);
        return error;
    } catch (e) {
        const errorMessage = e instanceof Error ? e.message : "Nie można połączyć się z API.";
        return new Error(`Błąd połączenia: ${errorMessage}`);
    }
}