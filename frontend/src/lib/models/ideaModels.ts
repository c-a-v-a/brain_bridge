export type PyObjectId = string;

export interface Link {
    url: string;
    text: string;
}

/**
 * @description Model dla danych do utworzenia nowego pomysłu.
 */
export interface Link {
    url: string;
    text: string;
}

/**
 * @description Model for creating a new idea.
 */
export interface IdeaCreate {
    title: string;
    user_id: PyObjectId;
    description: string;
    long_description?: string;
    links: Link[];
    wanted_contributors: string;
}

export interface IdeaGet {
    id: PyObjectId;
    title: string;
    user_id: PyObjectId;
    description: string;
}