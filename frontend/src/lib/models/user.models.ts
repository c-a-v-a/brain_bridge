export interface UserGet {
  //       Base model for User objects.
  id: number;
  username: string;
  email: string;
  name: string;
  surname: string;
  is_admin: boolean;
}

export interface UserCreate {
  //       This model is used to create a new user.
  username: string;
  email: string;
  password: string;
  name: string;
  surname: string;
  is_admin: boolean;
}

export interface UserUpdate {
  //      Model for update operations on user. Id should be passed from route and not included in the model.
  username?: string;
  email?: string;
  password?: string;
  name?: string;
  surename?: string;
  is_admin?: boolean;
}