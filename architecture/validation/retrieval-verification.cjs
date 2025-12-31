/**
 * Retrieval Verification
 * Phase 4.5 Architecture Optimization
 *
 * Verifies accuracy of information retrieved from large context or memory.
 * Guards against the "infinite context" fallacy by checking retrieval quality.
 *
 * @module architecture/validation/retrieval-verification
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Verification strategies for different retrieval types
 */
const RETRIEVAL_STRATEGIES = {
  // File content retrieval
  file_content: {
    id: 'file_content',
    name: 'File Content Verification',
    method: 'verifyFileContent'
  },

  // Code symbol retrieval
  code_symbol: {
    id: 'code_symbol',
    name: 'Code Symbol Verification',
    method: 'verifyCodeSymbol'
  },

  // Search result verification
  search_result: {
    id: 'search_result',
    name: 'Search Result Verification',
    method: 'verifySearchResult'
  },

  // Memory retrieval
  memory_retrieval: {
    id: 'memory_retrieval',
    name: 'Memory Retrieval Verification',
    method: 'verifyMemoryRetrieval'
  },

  // Summary accuracy
  summary: {
    id: 'summary',
    name: 'Summary Verification',
    method: 'verifySummary'
  }
};

/**
 * Verify file content retrieval
 * @param {Object} claim - What was claimed to be retrieved
 * @param {Object} options - Verification options
 * @returns {Object} Verification result
 */
function verifyFileContent(claim, options = {}) {
  const { filePath, content, lineNumbers } = claim;

  if (!filePath) {
    return { valid: false, error: 'No file path specified' };
  }

  try {
    if (!fs.existsSync(filePath)) {
      return {
        valid: false,
        error: 'File does not exist',
        filePath
      };
    }

    const actualContent = fs.readFileSync(filePath, 'utf8');
    const lines = actualContent.split('\n');

    // If specific line numbers claimed
    if (lineNumbers) {
      const { start, end } = lineNumbers;
      const claimedLines = content.split('\n');
      const actualLines = lines.slice(start - 1, end);

      const matches = claimedLines.every((line, i) =>
        actualLines[i] && actualLines[i].trim() === line.trim()
      );

      return {
        valid: matches,
        strategy: 'file_content',
        filePath,
        lineNumbers,
        claimedLineCount: claimedLines.length,
        actualLineCount: actualLines.length,
        match: matches
      };
    }

    // Full content verification
    if (content) {
      const normalizedClaim = content.replace(/\s+/g, ' ').trim();
      const normalizedActual = actualContent.replace(/\s+/g, ' ').trim();
      const match = normalizedActual.includes(normalizedClaim);

      return {
        valid: match,
        strategy: 'file_content',
        filePath,
        contentMatch: match,
        claimedLength: content.length,
        actualLength: actualContent.length
      };
    }

    return {
      valid: true,
      strategy: 'file_content',
      filePath,
      fileExists: true,
      lineCount: lines.length
    };

  } catch (err) {
    return {
      valid: false,
      error: err.message,
      filePath
    };
  }
}

/**
 * Verify code symbol retrieval (function, class, variable)
 * @param {Object} claim - Symbol claim
 * @param {Object} options - Options
 * @returns {Object} Verification result
 */
function verifyCodeSymbol(claim, options = {}) {
  const { symbolName, symbolType, filePath, definition } = claim;

  if (!filePath || !symbolName) {
    return { valid: false, error: 'Missing file path or symbol name' };
  }

  try {
    if (!fs.existsSync(filePath)) {
      return { valid: false, error: 'File does not exist', filePath };
    }

    const content = fs.readFileSync(filePath, 'utf8');

    // Build regex based on symbol type
    let patterns = [];
    switch (symbolType) {
      case 'function':
        patterns = [
          new RegExp(`function\\s+${symbolName}\\s*\\(`),
          new RegExp(`const\\s+${symbolName}\\s*=\\s*(?:async\\s+)?function`),
          new RegExp(`const\\s+${symbolName}\\s*=\\s*(?:async\\s+)?\\(`),
          new RegExp(`${symbolName}\\s*:\\s*(?:async\\s+)?function`),
          new RegExp(`def\\s+${symbolName}\\s*\\(`)
        ];
        break;
      case 'class':
        patterns = [
          new RegExp(`class\\s+${symbolName}\\s*[{(]`),
          new RegExp(`class\\s+${symbolName}\\s+extends`)
        ];
        break;
      case 'variable':
        patterns = [
          new RegExp(`(?:const|let|var)\\s+${symbolName}\\s*=`),
          new RegExp(`${symbolName}\\s*=`)
        ];
        break;
      default:
        patterns = [new RegExp(symbolName)];
    }

    const found = patterns.some(pattern => pattern.test(content));

    // If definition was claimed, verify it
    let definitionMatch = true;
    if (definition && found) {
      const normalizedDef = definition.replace(/\s+/g, ' ').trim();
      const normalizedContent = content.replace(/\s+/g, ' ');
      definitionMatch = normalizedContent.includes(normalizedDef);
    }

    return {
      valid: found && definitionMatch,
      strategy: 'code_symbol',
      symbolName,
      symbolType,
      filePath,
      symbolFound: found,
      definitionMatch
    };

  } catch (err) {
    return { valid: false, error: err.message };
  }
}

/**
 * Verify search result accuracy
 * @param {Object} claim - Search result claim
 * @param {Object} options - Options
 * @returns {Object} Verification result
 */
function verifySearchResult(claim, options = {}) {
  const { query, files, matches } = claim;

  if (!query || !files) {
    return { valid: false, error: 'Missing query or files' };
  }

  const verified = [];
  const failed = [];

  for (const file of files) {
    try {
      if (!fs.existsSync(file.path)) {
        failed.push({ path: file.path, error: 'File not found' });
        continue;
      }

      const content = fs.readFileSync(file.path, 'utf8');

      // Check if claimed matches exist in file
      if (file.matches) {
        const allFound = file.matches.every(match => content.includes(match));
        if (allFound) {
          verified.push(file.path);
        } else {
          failed.push({ path: file.path, error: 'Match not found in file' });
        }
      } else {
        // Just check if query pattern exists
        const regex = new RegExp(query, 'i');
        if (regex.test(content)) {
          verified.push(file.path);
        } else {
          failed.push({ path: file.path, error: 'Query not found in file' });
        }
      }
    } catch (err) {
      failed.push({ path: file.path, error: err.message });
    }
  }

  return {
    valid: failed.length === 0,
    strategy: 'search_result',
    query,
    totalFiles: files.length,
    verifiedFiles: verified.length,
    failedFiles: failed.length,
    verified,
    failed
  };
}

/**
 * Verify memory retrieval accuracy
 * @param {Object} claim - Memory retrieval claim
 * @param {Object} actual - Actual memory data
 * @returns {Object} Verification result
 */
function verifyMemoryRetrieval(claim, actual) {
  if (!claim || !actual) {
    return { valid: false, error: 'Missing claim or actual data' };
  }

  const { key, value, timestamp } = claim;

  // Check key exists
  if (actual[key] === undefined) {
    return {
      valid: false,
      strategy: 'memory_retrieval',
      error: 'Key not found in memory',
      key
    };
  }

  // Check value matches
  const claimedStr = JSON.stringify(value);
  const actualStr = JSON.stringify(actual[key]);
  const valueMatch = claimedStr === actualStr;

  return {
    valid: valueMatch,
    strategy: 'memory_retrieval',
    key,
    valueMatch,
    claimedType: typeof value,
    actualType: typeof actual[key]
  };
}

/**
 * Verify summary accuracy against source
 * @param {Object} claim - Summary claim
 * @param {string} source - Original source content
 * @returns {Object} Verification result
 */
function verifySummary(claim, source) {
  const { summary, keyPoints } = claim;

  if (!summary || !source) {
    return { valid: false, error: 'Missing summary or source' };
  }

  const sourceWords = source.toLowerCase().split(/\s+/);
  const sourceSet = new Set(sourceWords);

  // Check key points are present in source
  const verifiedPoints = [];
  const missingPoints = [];

  if (keyPoints) {
    for (const point of keyPoints) {
      const pointWords = point.toLowerCase().split(/\s+/);
      // Check if significant words from point exist in source
      const significantWords = pointWords.filter(w => w.length > 4);
      const coverage = significantWords.filter(w => sourceSet.has(w)).length / significantWords.length;

      if (coverage > 0.5) {
        verifiedPoints.push(point);
      } else {
        missingPoints.push(point);
      }
    }
  }

  return {
    valid: missingPoints.length === 0,
    strategy: 'summary',
    totalPoints: keyPoints?.length || 0,
    verifiedPoints: verifiedPoints.length,
    missingPoints: missingPoints.length,
    verified: verifiedPoints,
    missing: missingPoints
  };
}

/**
 * Run comprehensive retrieval verification
 * @param {Object[]} claims - Array of retrieval claims
 * @returns {Object} Verification results
 */
function verifyRetrievals(claims) {
  const results = {
    timestamp: new Date().toISOString(),
    claims: [],
    summary: {
      total: claims.length,
      verified: 0,
      failed: 0
    }
  };

  for (const claim of claims) {
    const strategy = RETRIEVAL_STRATEGIES[claim.type];
    if (!strategy) {
      results.claims.push({
        type: claim.type,
        valid: false,
        error: 'Unknown retrieval type'
      });
      results.summary.failed++;
      continue;
    }

    let result;
    switch (strategy.method) {
      case 'verifyFileContent':
        result = verifyFileContent(claim);
        break;
      case 'verifyCodeSymbol':
        result = verifyCodeSymbol(claim);
        break;
      case 'verifySearchResult':
        result = verifySearchResult(claim);
        break;
      case 'verifyMemoryRetrieval':
        result = verifyMemoryRetrieval(claim, claim.actual);
        break;
      case 'verifySummary':
        result = verifySummary(claim, claim.source);
        break;
      default:
        result = { valid: false, error: 'Unknown method' };
    }

    results.claims.push({
      type: claim.type,
      ...result
    });

    if (result.valid) {
      results.summary.verified++;
    } else {
      results.summary.failed++;
    }
  }

  results.allValid = results.summary.failed === 0;

  return results;
}

/**
 * Calculate retrieval confidence score
 * @param {Object} verificationResult - Verification result
 * @returns {number} Confidence score 0-1
 */
function calculateConfidence(verificationResult) {
  if (!verificationResult.claims || verificationResult.claims.length === 0) {
    return 0;
  }

  const validCount = verificationResult.claims.filter(c => c.valid).length;
  return validCount / verificationResult.claims.length;
}

/**
 * Generate retrieval verification report
 * @param {Object} results - Verification results
 * @returns {string} Markdown report
 */
function generateRetrievalReport(results) {
  const confidence = calculateConfidence(results);

  let report = `# Retrieval Verification Report

**Timestamp**: ${results.timestamp}
**Status**: ${results.allValid ? 'ALL VERIFIED' : 'VERIFICATION FAILURES'}
**Confidence**: ${(confidence * 100).toFixed(1)}%

## Summary

| Metric | Value |
|--------|-------|
| Total Claims | ${results.summary.total} |
| Verified | ${results.summary.verified} |
| Failed | ${results.summary.failed} |

## Claim Details

`;

  for (const claim of results.claims) {
    const status = claim.valid ? 'VERIFIED' : 'FAILED';
    report += `### ${claim.type} - ${status}

- **Strategy**: ${claim.strategy || claim.type}
`;

    if (claim.filePath) report += `- **File**: ${claim.filePath}\n`;
    if (claim.symbolName) report += `- **Symbol**: ${claim.symbolName}\n`;
    if (claim.error) report += `- **Error**: ${claim.error}\n`;

    report += '\n';
  }

  return report;
}

// Export
module.exports = {
  RETRIEVAL_STRATEGIES,
  verifyFileContent,
  verifyCodeSymbol,
  verifySearchResult,
  verifyMemoryRetrieval,
  verifySummary,
  verifyRetrievals,
  calculateConfidence,
  generateRetrievalReport
};
