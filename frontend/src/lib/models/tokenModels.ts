/**
 * @module models.tokenModels
 * @description Defines interfaces related to authentication tokens.
 */

/**
 * Represents a pair of authentication tokens.
 */
export interface TokenPair {
  access_token: string;
  refresh_token: string;
};