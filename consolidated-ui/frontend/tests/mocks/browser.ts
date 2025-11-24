/**
 * MSW Browser Setup for E2E Tests (Playwright)
 */

import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

// Setup MSW browser worker with our request handlers
export const worker = setupWorker(...handlers);
