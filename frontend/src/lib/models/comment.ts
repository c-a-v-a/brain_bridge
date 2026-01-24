export interface Comment {
  _id?: string;
  userId: string;
  username: string;
  content: string;
  createdAt: number;
  replies: Comment[];
  ideaId: string;
}

export interface CommentCreate {
  content: string;
  ideaId: string;
}

export interface CommentFilter {
  _id?: string;
  ideaId?: string;
  userId?: string;
  content?: string;
  createdAt?: number;
  replies?: Comment[];
}