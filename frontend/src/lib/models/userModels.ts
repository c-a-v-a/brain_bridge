/**
 * @module models.userModels
 * @description This module contains TypeScript interfaces for user-related operations,
 * such as getting user details, creating a new user, updating user information,
 * and user login data structure.
 */

/**
 * Represents a user retrieved from the system.
 */
export interface UserGet {
  id: string;
  username: string;
  email: string;
  name: string;
  surname: string;
  is_admin: boolean;
}


/**
 * Represents the data required to create a new user.
 */
export interface UserCreate {
  username: string;
  email: string;
  password: string;
  name: string;
  surname: string;
  is_admin: boolean;
}

/**
 * Represents the data used to update an existing user.
 * All fields are optional.
 */
export interface UserUpdate {
  username?: string;
  email?: string;
  password?: string;
  name?: string;
  surename?: string;
  is_admin?: boolean;
}


/**
 * Represents the data required for a user login attempt.
 */
export interface UserLogin {
  email?: string;
  password?: string;
}