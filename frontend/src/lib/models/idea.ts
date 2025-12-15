export type PyObjectId = string;

export interface Link {
  url: string;
  text: string;
}

export interface Idea {
  id: string;
  title: string;
  userId: string;
  description: string;
  longDescription: string;
  links: Link[];
  wantedContributors: string;
  images?: string[];
  likedByUser: string[];
}

export interface IdeaCreate {
  title: string;
  userId: string;
  description: string;
  longDescription: string;
  links: Link[];
  wantedContributors: string;
  likedByUser: string[];
}

export interface IdeaGet {
  id: string;
  title: string;
  userId: string;
  description: string;
  likedByUser: string[];
}

export interface IdeaUpdate {
  title?: string;
  userId?: string;
  description?: string;
  longDescription?: string;
  links?: Link[];
  wantedContributors?: string;
  images?: string[];
  likedByUser?: string[];
}

export interface IdeaFilter extends IdeaUpdate {
  id?: string;
}