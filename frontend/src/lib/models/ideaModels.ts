export type PyObjectId = string; 

/**
 * @description Model dla danych do utworzenia nowego pomysłu.
 */
export interface IdeaCreate {
    title: string;
    user_id: PyObjectId;
    desc: string;
}

export interface IdeaGet {
    id: PyObjectId; // Zmienione z Optional[PyObjectId] na wymagane id
    title: string;
    user_id: PyObjectId;
    desc: string;
}