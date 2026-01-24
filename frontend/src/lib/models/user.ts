export interface UserGet {
  _id: string;
  username: string;
  email: string;
  name: string;
  surname: string;
  isAdmin: boolean;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  name: string;
  surname: string;
  isAdmin: boolean;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  password?: string;
  name?: string;
  surename?: string;
  isAdmin?: boolean;
}

export interface UserLogin {
  email?: string;
  password?: string;
}