/**
 * MSW Server Setup for Node.js (Jest) Tests
 */

import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup MSW server with our request handlers
export const server = setupServer(...handlers);
