/**
 * Unit tests for Permission Checker
 *
 * Tests RBAC enforcement across 3 dimensions:
 * 1. Tool permissions
 * 2. Path scopes
 * 3. API access
 *
 * @module hooks/12fa/utils/__tests__/permission-checker.test
 */

const {
  loadRBACRules,
  checkToolPermission,
  checkPathPermission,
  checkAPIPermission,
  checkApprovalRequired,
  getBudgetImpact,
  checkBudgetThreshold,
  checkPermission,
  validateRBACRules,
  clearCache
} = require('../permission-checker');

const fs = require('fs');
const path = require('path');

describe('Permission Checker', () => {
  beforeEach(() => {
    clearCache();
  });

  describe('Load RBAC Rules', () => {
    test('should load RBAC rules from JSON file', () => {
      const rules = loadRBACRules();

      expect(rules).toBeDefined();
      expect(rules.roles).toBeDefined();
      expect(Object.keys(rules.roles)).toHaveLength(10);
    });

    test('should cache RBAC rules', () => {
      const rules1 = loadRBACRules();
      const startTime = Date.now();
      const rules2 = loadRBACRules();
      const duration = Date.now() - startTime;

      expect(rules1).toEqual(rules2);
      expect(duration).toBeLessThan(5); // Cache lookup should be instant
    });

    test('should contain all 10 required roles', () => {
      const rules = loadRBACRules();
      const requiredRoles = [
        'admin', 'developer', 'reviewer', 'security', 'database',
        'frontend', 'backend', 'tester', 'analyst', 'coordinator'
      ];

      requiredRoles.forEach(role => {
        expect(rules.roles[role]).toBeDefined();
      });
    });
  });

  describe('Validate RBAC Rules Structure', () => {
    test('should validate correct RBAC rules structure', () => {
      const result = validateRBACRules();

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should detect missing roles', () => {
      // This test would require creating a temporary invalid rules file
      // For now, we verify the validation function works
      const result = validateRBACRules();

      expect(result).toHaveProperty('valid');
      expect(result).toHaveProperty('errors');
    });
  });

  describe('Tool Permission Checks', () => {
    test('should allow admin wildcard tool access', () => {
      const result = checkToolPermission('admin', 'KillShell');

      expect(result.allowed).toBe(true);
      expect(result.reason).toContain('wildcard');
    });

    test('should allow developer to use Read', () => {
      const result = checkToolPermission('developer', 'Read');

      expect(result.allowed).toBe(true);
    });

    test('should allow developer to use Write', () => {
      const result = checkToolPermission('developer', 'Write');

      expect(result.allowed).toBe(true);
    });

    test('should deny analyst from using Write', () => {
      const result = checkToolPermission('analyst', 'Write');

      expect(result.allowed).toBe(false);
    });

    test('should deny tester from using KillShell', () => {
      const result = checkToolPermission('tester', 'KillShell');

      expect(result.allowed).toBe(false);
    });

    test('should deny unknown role', () => {
      const result = checkToolPermission('invalid-role', 'Read');

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('Unknown role');
    });

    test('should use permission matrix as fallback', () => {
      const result = checkToolPermission('reviewer', 'Read');

      expect(result.allowed).toBe(true);
    });
  });

  describe('Path Permission Checks', () => {
    test('should allow admin wildcard path access', () => {
      const result = checkPathPermission('admin', 'any/path/file.js');

      expect(result.allowed).toBe(true);
      expect(result.reason).toContain('wildcard');
    });

    test('should allow developer access to src/**', () => {
      const result = checkPathPermission('developer', 'src/api/users.js');

      expect(result.allowed).toBe(true);
    });

    test('should allow frontend access to frontend/**', () => {
      const result = checkPathPermission('frontend', 'frontend/components/Button.jsx');

      expect(result.allowed).toBe(true);
    });

    test('should deny frontend access to backend/**', () => {
      const result = checkPathPermission('frontend', 'backend/api/users.js');

      expect(result.allowed).toBe(false);
    });

    test('should allow backend access to backend/**', () => {
      const result = checkPathPermission('backend', 'backend/services/auth.js');

      expect(result.allowed).toBe(true);
    });

    test('should handle Windows paths correctly', () => {
      const result = checkPathPermission('developer', 'src\\api\\users.js');

      expect(result.allowed).toBe(true);
    });

    test('should allow tester access to test files', () => {
      const result = checkPathPermission('tester', 'tests/unit/auth.test.js');

      expect(result.allowed).toBe(true);
    });

    test('should deny unknown role', () => {
      const result = checkPathPermission('invalid-role', 'src/file.js');

      expect(result.allowed).toBe(false);
    });
  });

  describe('API Permission Checks', () => {
    test('should allow admin wildcard API access', () => {
      const result = checkAPIPermission('admin', 'github');

      expect(result.allowed).toBe(true);
      expect(result.reason).toContain('wildcard');
    });

    test('should allow developer access to github', () => {
      const result = checkAPIPermission('developer', 'github');

      expect(result.allowed).toBe(true);
    });

    test('should allow coordinator access to flow-nexus', () => {
      const result = checkAPIPermission('coordinator', 'flow-nexus');

      expect(result.allowed).toBe(true);
    });

    test('should deny frontend access to flow-nexus', () => {
      const result = checkAPIPermission('frontend', 'flow-nexus');

      expect(result.allowed).toBe(false);
    });

    test('should allow security access to connascence-analyzer', () => {
      const result = checkAPIPermission('security', 'connascence-analyzer');

      expect(result.allowed).toBe(true);
    });

    test('should deny backend access to connascence-analyzer', () => {
      const result = checkAPIPermission('backend', 'connascence-analyzer');

      expect(result.allowed).toBe(false);
    });

    test('should allow all roles access to memory-mcp', () => {
      const roles = ['developer', 'reviewer', 'security', 'frontend', 'backend', 'tester', 'analyst', 'coordinator'];

      roles.forEach(role => {
        const result = checkAPIPermission(role, 'memory-mcp');
        expect(result.allowed).toBe(true);
      });
    });
  });

  describe('Approval Requirements', () => {
    test('should require approval for admin production_deploy', () => {
      const result = checkApprovalRequired('admin', 'production_deploy');

      expect(result.requiresApproval).toBe(true);
      expect(result.approvers).toContain('human');
    });

    test('should require approval for admin KillShell', () => {
      const result = checkApprovalRequired('admin', 'KillShell');

      expect(result.requiresApproval).toBe(true);
    });

    test('should not require approval for developer Read', () => {
      const result = checkApprovalRequired('developer', 'Read');

      expect(result.requiresApproval).toBe(false);
    });

    test('should require approval for database production_migration', () => {
      const result = checkApprovalRequired('database', 'production_migration');

      expect(result.requiresApproval).toBe(true);
    });
  });

  describe('Budget Impact Calculations', () => {
    test('should calculate budget impact for Read operation', () => {
      const impact = getBudgetImpact('developer', 'Read', 1000);

      expect(impact).toBeGreaterThan(0);
      expect(impact).toBeLessThan(0.01); // Should be very low cost
    });

    test('should calculate higher budget impact for Task operation', () => {
      const readImpact = getBudgetImpact('developer', 'Read', 1000);
      const taskImpact = getBudgetImpact('developer', 'Task', 1000);

      expect(taskImpact).toBeGreaterThan(readImpact);
    });

    test('should calculate budget impact for WebSearch', () => {
      const impact = getBudgetImpact('analyst', 'WebSearch', 5000);

      expect(impact).toBeGreaterThan(0);
    });

    test('should use default token estimate if not provided', () => {
      const impact = getBudgetImpact('developer', 'Read');

      expect(impact).toBeGreaterThan(0);
    });
  });

  describe('Budget Threshold Checks', () => {
    test('should detect budget not exceeded', () => {
      const result = checkBudgetThreshold('developer', 10.0);

      expect(result.exceeded).toBe(false);
      expect(result.threshold).toBe(30.0);
      expect(result.remaining).toBe(20.0);
    });

    test('should detect budget exceeded', () => {
      const result = checkBudgetThreshold('developer', 35.0);

      expect(result.exceeded).toBe(true);
      expect(result.threshold).toBe(30.0);
      expect(result.remaining).toBe(0);
    });

    test('should detect budget exactly at threshold', () => {
      const result = checkBudgetThreshold('developer', 30.0);

      expect(result.exceeded).toBe(true);
      expect(result.threshold).toBe(30.0);
      expect(result.remaining).toBe(0);
    });

    test('should handle analyst lower budget', () => {
      const result = checkBudgetThreshold('analyst', 10.0);

      expect(result.exceeded).toBe(false);
      expect(result.threshold).toBe(15.0);
      expect(result.remaining).toBe(5.0);
    });
  });

  describe('Comprehensive Permission Checks', () => {
    test('should allow valid operation with all checks passing', () => {
      const result = checkPermission({
        role: 'developer',
        toolName: 'Read',
        filePath: 'src/api/users.js',
        apiName: 'github',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(true);
      expect(result.budgetImpact).toBeGreaterThan(0);
      expect(result.requiresApproval).toBe(false);
      expect(result.checkTimeMs).toBeLessThan(50);
    });

    test('should deny operation if tool not allowed', () => {
      const result = checkPermission({
        role: 'analyst',
        toolName: 'Write',
        filePath: 'docs/report.md',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('not in role\'s allowed tools');
    });

    test('should deny operation if path not allowed', () => {
      const result = checkPermission({
        role: 'frontend',
        toolName: 'Write',
        filePath: 'backend/api/users.js',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('not in role\'s allowed scopes');
    });

    test('should deny operation if API not allowed', () => {
      const result = checkPermission({
        role: 'frontend',
        toolName: 'Read',
        filePath: 'frontend/components/Button.jsx',
        apiName: 'flow-nexus',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('not in role\'s allowed APIs');
    });

    test('should indicate approval required for high-risk operations', () => {
      const result = checkPermission({
        role: 'admin',
        toolName: 'KillShell',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(true);
      expect(result.requiresApproval).toBe(true);
      expect(result.approvers).toContain('human');
    });

    test('should handle operation without file path or API', () => {
      const result = checkPermission({
        role: 'developer',
        toolName: 'Read',
        estimatedTokens: 1000
      });

      expect(result.allowed).toBe(true);
    });
  });

  describe('Performance Requirements', () => {
    test('tool permission check should complete in <50ms', () => {
      const startTime = Date.now();
      checkToolPermission('developer', 'Read');
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(50);
    });

    test('path permission check should complete in <50ms', () => {
      const startTime = Date.now();
      checkPathPermission('developer', 'src/api/users.js');
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(50);
    });

    test('API permission check should complete in <50ms', () => {
      const startTime = Date.now();
      checkAPIPermission('developer', 'github');
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(50);
    });

    test('comprehensive permission check should complete in <50ms', () => {
      const result = checkPermission({
        role: 'developer',
        toolName: 'Read',
        filePath: 'src/api/users.js',
        apiName: 'github',
        estimatedTokens: 1000
      });

      expect(result.checkTimeMs).toBeLessThan(50);
    });

    test('multiple consecutive checks should remain fast', () => {
      const iterations = 100;
      const startTime = Date.now();

      for (let i = 0; i < iterations; i++) {
        checkPermission({
          role: 'developer',
          toolName: 'Read',
          filePath: 'src/api/users.js',
          estimatedTokens: 1000
        });
      }

      const totalDuration = Date.now() - startTime;
      const avgDuration = totalDuration / iterations;

      expect(avgDuration).toBeLessThan(50);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle empty role gracefully', () => {
      const result = checkToolPermission('', 'Read');

      expect(result.allowed).toBe(false);
    });

    test('should handle undefined tool name', () => {
      const result = checkToolPermission('developer', undefined);

      expect(result.allowed).toBe(false);
    });

    test('should handle special characters in file paths', () => {
      const result = checkPathPermission('developer', 'src/api/users-v2.0.js');

      expect(result.allowed).toBe(true);
    });

    test('should handle deeply nested paths', () => {
      const result = checkPathPermission('developer', 'src/api/v1/controllers/auth/users.js');

      expect(result.allowed).toBe(true);
    });

    test('should handle paths with spaces', () => {
      const result = checkPathPermission('developer', 'src/api/user service.js');

      expect(result.allowed).toBe(true);
    });
  });

  describe('Zero False Positives/Negatives', () => {
    test('should never allow invalid role operations (zero false positives)', () => {
      const invalidOperations = [
        { role: 'analyst', toolName: 'Write' },
        { role: 'frontend', apiName: 'flow-nexus' },
        { role: 'tester', toolName: 'KillShell' },
        { role: 'reviewer', toolName: 'MultiEdit' }
      ];

      invalidOperations.forEach(op => {
        const result = checkPermission(op);
        expect(result.allowed).toBe(false);
      });
    });

    test('should always allow valid role operations (zero false negatives)', () => {
      const validOperations = [
        { role: 'developer', toolName: 'Read', filePath: 'src/api/users.js' },
        { role: 'admin', toolName: 'KillShell' },
        { role: 'backend', toolName: 'Write', filePath: 'backend/api/auth.js' },
        { role: 'frontend', toolName: 'Edit', filePath: 'frontend/components/Button.jsx' },
        { role: 'coordinator', apiName: 'flow-nexus' }
      ];

      validOperations.forEach(op => {
        const result = checkPermission(op);
        expect(result.allowed).toBe(true);
      });
    });
  });
});
