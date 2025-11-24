/**
 * API Helper for E2E Testing
 * Provides typed API interactions and response validation
 */

import { Page } from '@playwright/test';

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export class ApiHelper {
  private page: Page;
  private baseUrl: string;

  constructor(page: Page, baseUrl?: string) {
    this.page = page;
    this.baseUrl = baseUrl || process.env.API_BASE_URL || 'http://localhost:8000';
  }

  /**
   * GET request
   */
  async get<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    const response = await this.page.request.get(`${this.baseUrl}${endpoint}`);

    return this.parseResponse<T>(response);
  }

  /**
   * POST request
   */
  async post<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    const response = await this.page.request.post(`${this.baseUrl}${endpoint}`, {
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    return this.parseResponse<T>(response);
  }

  /**
   * PATCH request
   */
  async patch<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    const response = await this.page.request.patch(`${this.baseUrl}${endpoint}`, {
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    return this.parseResponse<T>(response);
  }

  /**
   * DELETE request
   */
  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    const response = await this.page.request.delete(`${this.baseUrl}${endpoint}`);

    return this.parseResponse<T>(response);
  }

  /**
   * Parse API response
   */
  private async parseResponse<T>(response: any): Promise<ApiResponse<T>> {
    const status = response.status();
    const isSuccess = status >= 200 && status < 300;

    try {
      const body = await response.json();

      return {
        success: isSuccess,
        data: isSuccess ? body : undefined,
        error: !isSuccess ? (body.error || body.message || 'Request failed') : undefined,
        message: body.message,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to parse response: ${error}`,
      };
    }
  }

  /**
   * Wait for API endpoint to be ready
   */
  async waitForReady(endpoint: string = '/health', timeout: number = 30000): Promise<void> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      try {
        const response = await this.get(endpoint);
        if (response.success) {
          return;
        }
      } catch (error) {
        // Continue waiting
      }

      await this.page.waitForTimeout(1000);
    }

    throw new Error(`API not ready after ${timeout}ms`);
  }
}
