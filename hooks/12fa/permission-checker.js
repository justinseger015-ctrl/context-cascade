/**
 * RBAC Permission Checker
 * Enforces role-based access control for agent operations
 * Performance: <10ms per check
 */

const fs = require('fs');
const path = require('path');

const RBAC_POLICIES = path.join(__dirname, 'rbac-policies.json');

class PermissionChecker {
  constructor() {
    this.policies = this.loadPolicies();
  }

  loadPolicies() {
    try {
      if (fs.existsSync(RBAC_POLICIES)) {
        return JSON.parse(fs.readFileSync(RBAC_POLICIES, 'utf8'));
      }
    } catch (error) {
      console.error('[PermissionChecker] Failed to load policies:', error.message);
    }

    // Default RBAC policies
    return {
      roles: {
        admin: {
          permissions: ['*'],
          description: 'Full system access'
        },
        developer: {
          permissions: [
            'file:read', 'file:write', 'file:edit',
            'task:spawn', 'task:monitor',
            'memory:read', 'memory:write',
            'bash:execute'
          ],
          description: 'Standard development operations'
        },
        reviewer: {
          permissions: [
            'file:read',
            'task:monitor',
            'memory:read'
          ],
          description: 'Read-only review access'
        },
        tester: {
          permissions: [
            'file:read',
            'task:spawn',
            'bash:execute'
          ],
          description: 'Testing and validation'
        }
      },
      agentRoles: {},
      operationMap: {
        'Edit': 'file:edit',
        'Write': 'file:write',
        'Read': 'file:read',
        'Bash': 'bash:execute',
        'Task': 'task:spawn',
        'TodoWrite': 'task:monitor',
        'memory_store': 'memory:write',
        'vector_search': 'memory:read'
      }
    };
  }

  savePolicies() {
    try {
      fs.writeFileSync(RBAC_POLICIES, JSON.stringify(this.policies, null, 2));
    } catch (error) {
      console.error('[PermissionChecker] Failed to save policies:', error.message);
    }
  }

  /**
   * Assign role to agent
   * @param {string} agentId - Agent identifier
   * @param {string} role - Role name
   */
  assignRole(agentId, role) {
    if (!this.policies.roles[role]) {
      return { success: false, reason: `Role '${role}' does not exist` };
    }

    this.policies.agentRoles[agentId] = role;
    this.savePolicies();
    return { success: true, agentId, role };
  }

  /**
   * Check if agent has permission for operation
   * @param {string} agentId - Agent identifier
   * @param {string} operation - Operation name (e.g., 'Edit', 'file:write')
   * @param {object} context - Additional context (resource, metadata)
   * @returns {object} Permission check result
   */
  checkPermission(agentId, operation, context = {}) {
    const startTime = Date.now();

    // Get agent role
    const role = this.policies.agentRoles[agentId] || 'developer'; // Default to developer

    if (!this.policies.roles[role]) {
      return {
        allowed: false,
        reason: `Unknown role: ${role}`,
        agentId,
        operation,
        checkTime: Date.now() - startTime
      };
    }

    // Map operation to permission
    const permission = this.policies.operationMap[operation] || operation;

    // Check permissions
    const rolePermissions = this.policies.roles[role].permissions;

    // Admin has wildcard access
    if (rolePermissions.includes('*')) {
      return {
        allowed: true,
        reason: 'Admin access',
        agentId,
        role,
        operation,
        permission,
        checkTime: Date.now() - startTime
      };
    }

    // Exact match
    if (rolePermissions.includes(permission)) {
      return {
        allowed: true,
        reason: 'Permission granted',
        agentId,
        role,
        operation,
        permission,
        checkTime: Date.now() - startTime
      };
    }

    // Wildcard match (e.g., 'file:*' matches 'file:read')
    const wildcardMatch = rolePermissions.some(perm => {
      if (perm.endsWith(':*')) {
        const prefix = perm.slice(0, -1);
        return permission.startsWith(prefix);
      }
      return false;
    });

    if (wildcardMatch) {
      return {
        allowed: true,
        reason: 'Wildcard permission granted',
        agentId,
        role,
        operation,
        permission,
        checkTime: Date.now() - startTime
      };
    }

    return {
      allowed: false,
      reason: `Permission denied: ${permission} not in role ${role}`,
      agentId,
      role,
      operation,
      permission,
      checkTime: Date.now() - startTime
    };
  }

  /**
   * Get agent permissions
   * @param {string} agentId - Agent identifier
   */
  getPermissions(agentId) {
    const role = this.policies.agentRoles[agentId] || 'developer';
    return {
      agentId,
      role,
      permissions: this.policies.roles[role]?.permissions || []
    };
  }

  /**
   * List all roles
   */
  listRoles() {
    return Object.entries(this.policies.roles).map(([name, config]) => ({
      name,
      permissions: config.permissions,
      description: config.description
    }));
  }
}

module.exports = new PermissionChecker();
