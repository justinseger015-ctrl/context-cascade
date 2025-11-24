/**
 * Memory MCP Helper for E2E Testing
 * Verifies WHO/WHEN/PROJECT/WHY tagging protocol
 */

import axios from 'axios';

export interface MemoryMCPTags {
  who: string;
  when: string;
  project: string;
  why: string;
  [key: string]: any;
}

export class MemoryMCPHelper {
  private mcpUrl: string;

  constructor(mcpUrl?: string) {
    this.mcpUrl = mcpUrl || process.env.MEMORY_MCP_URL || 'http://localhost:9001';
  }

  /**
   * Query task execution from Memory MCP
   */
  async queryTaskExecution(taskId: string): Promise<MemoryMCPTags> {
    try {
      const response = await axios.post(`${this.mcpUrl}/vector_search`, {
        query: `task_id:${taskId}`,
        mode: 'execution',
        top_k: 1,
      });

      if (!response.data || response.data.length === 0) {
        throw new Error(`No Memory MCP entry found for task ${taskId}`);
      }

      const entry = response.data[0];

      // Extract WHO/WHEN/PROJECT/WHY tags from metadata
      const tags: MemoryMCPTags = {
        who: entry.metadata?.who || entry.metadata?.agent || 'unknown',
        when: entry.metadata?.when || entry.metadata?.timestamp || new Date().toISOString(),
        project: entry.metadata?.project || 'unknown',
        why: entry.metadata?.why || entry.metadata?.intent || 'unknown',
        ...entry.metadata,
      };

      return tags;
    } catch (error) {
      console.error('Error querying Memory MCP:', error);
      throw error;
    }
  }

  /**
   * Store task execution in Memory MCP
   */
  async storeTaskExecution(taskId: string, executionData: any): Promise<void> {
    const tags: MemoryMCPTags = {
      who: executionData.agent || 'e2e-test-agent',
      when: new Date().toISOString(),
      project: 'ruv-sparc-ui-dashboard',
      why: executionData.intent || 'testing',
      task_id: taskId,
      ...executionData,
    };

    try {
      await axios.post(`${this.mcpUrl}/memory_store`, {
        content: JSON.stringify(executionData),
        metadata: tags,
        layer: 'short-term', // 24h retention for E2E tests
      });
    } catch (error) {
      console.error('Error storing in Memory MCP:', error);
      throw error;
    }
  }

  /**
   * Verify Memory MCP tagging protocol compliance
   */
  async verifyTaggingProtocol(taskId: string): Promise<{
    compliant: boolean;
    missing: string[];
    errors: string[];
  }> {
    const result = {
      compliant: true,
      missing: [] as string[],
      errors: [] as string[],
    };

    try {
      const tags = await this.queryTaskExecution(taskId);

      // Check required WHO tag
      if (!tags.who || tags.who === 'unknown') {
        result.compliant = false;
        result.missing.push('WHO');
        result.errors.push('WHO tag missing or unknown');
      }

      // Check required WHEN tag
      if (!tags.when) {
        result.compliant = false;
        result.missing.push('WHEN');
        result.errors.push('WHEN tag missing');
      } else {
        // Verify timestamp is valid
        const timestamp = new Date(tags.when);
        if (isNaN(timestamp.getTime())) {
          result.compliant = false;
          result.errors.push('WHEN tag has invalid timestamp');
        }
      }

      // Check required PROJECT tag
      if (!tags.project || tags.project === 'unknown') {
        result.compliant = false;
        result.missing.push('PROJECT');
        result.errors.push('PROJECT tag missing or unknown');
      }

      // Check required WHY tag
      if (!tags.why || tags.why === 'unknown') {
        result.compliant = false;
        result.missing.push('WHY');
        result.errors.push('WHY tag missing or unknown');
      }

      return result;
    } catch (error) {
      result.compliant = false;
      result.errors.push(`Error verifying tags: ${error}`);
      return result;
    }
  }

  /**
   * Query agent activity from Memory MCP
   */
  async queryAgentActivity(agentId: string): Promise<any[]> {
    try {
      const response = await axios.post(`${this.mcpUrl}/vector_search`, {
        query: `agent_id:${agentId}`,
        mode: 'execution',
        top_k: 10,
      });

      return response.data || [];
    } catch (error) {
      console.error('Error querying agent activity:', error);
      return [];
    }
  }

  /**
   * Clear Memory MCP entries for testing
   */
  async clearTestEntries(): Promise<void> {
    try {
      // Clear short-term layer (where E2E test data lives)
      await axios.post(`${this.mcpUrl}/clear_layer`, {
        layer: 'short-term',
      });
    } catch (error) {
      console.warn('Error clearing Memory MCP test entries:', error);
    }
  }

  /**
   * Check Memory MCP health
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${this.mcpUrl}/health`);
      return response.status === 200;
    } catch (error) {
      console.error('Memory MCP health check failed:', error);
      return false;
    }
  }
}
