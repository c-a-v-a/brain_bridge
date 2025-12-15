export interface Comment {
  id: string;
  userId: string;
  content: string;
  createdAt: number;
  replies: Comment[];
}

export interface CommentFilter {
  id?: string;
  userId?: string;
  content?: string;
  createdAt?: number;
  replies?: Comment[];
}