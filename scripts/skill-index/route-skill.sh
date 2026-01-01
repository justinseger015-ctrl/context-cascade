#!/bin/bash
# route-skill.sh - Query skill index and return top matching skills
#
# Usage: route-skill.sh "user request text"
# Output: Top 5 matching skills with confidence scores
#
# Uses Python trigger_matcher.py with rapidfuzz for fuzzy matching.
# Falls back to Node.js if Python matcher unavailable.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="${SCRIPT_DIR%/scripts/skill-index}"
INDEX_FILE="$SCRIPT_DIR/skill-index.json"
PYTHON_MATCHER="$PLUGIN_DIR/cognitive-architecture/skills/trigger_matcher.py"

# Check if index exists
if [ ! -f "$INDEX_FILE" ]; then
  echo "ERROR: skill-index.json not found. Run build-skill-index.py first." >&2
  exit 1
fi

# Get user request
REQUEST="$1"
if [ -z "$REQUEST" ]; then
  echo "Usage: route-skill.sh \"user request text\"" >&2
  exit 1
fi

# Try Python matcher first (has fuzzy matching with rapidfuzz)
if [ -f "$PYTHON_MATCHER" ]; then
  python "$PYTHON_MATCHER" "$REQUEST" 0.6 5 2>/dev/null
  if [ $? -eq 0 ]; then
    exit 0
  fi
fi

# Fallback to Node.js matcher
node - "$REQUEST" "$INDEX_FILE" <<'NODEJS'
const request = process.argv[2];
const indexFile = process.argv[3];
const fs = require('fs');

// Stopwords to filter
const STOPWORDS = new Set([
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
  'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
  'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where', 'why', 'how',
  'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
  'such', 'no', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
  'just', 'also', 'now', 'here', 'there', 'this', 'that', 'these', 'those',
  'it', 'its', 'you', 'your', 'we', 'our', 'they', 'their', 'i', 'my',
  'use', 'using', 'want', 'need', 'help', 'please', 'can', 'me'
]);

// Load index
const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));

// Tokenize request
function tokenize(text) {
  return text.toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2)
    .filter(w => !STOPWORDS.has(w));
}

// Score a skill against request tokens
function scoreSkill(skill, tokens, categoryScores) {
  let score = 0;
  const matchedTriggers = [];

  // Keyword matching (50% weight)
  for (const token of tokens) {
    if (skill.triggers.includes(token)) {
      score += 5;
      matchedTriggers.push(token);
    }
    // Partial match
    for (const trigger of skill.triggers) {
      if (trigger.includes(token) || token.includes(trigger)) {
        score += 2;
      }
    }
  }

  // Category bonus (30% weight)
  const catScore = categoryScores[skill.category] || 0;
  score += catScore * 3;

  // Negative trigger penalty
  for (const token of tokens) {
    if (skill.negativeTriggers && skill.negativeTriggers.includes(token)) {
      score -= 5;
    }
  }

  // Description match bonus
  const descWords = skill.description.toLowerCase().split(/\s+/);
  for (const token of tokens) {
    if (descWords.includes(token)) {
      score += 2;
    }
  }

  return { score, matchedTriggers };
}

// Score categories
function scoreCategories(tokens) {
  const scores = {};
  for (const [category, keywords] of Object.entries(index.category_keywords)) {
    scores[category] = 0;
    for (const token of tokens) {
      if (keywords.includes(token)) {
        scores[category] += 3;
      }
      for (const keyword of keywords) {
        if (keyword.includes(token) || token.includes(keyword)) {
          scores[category] += 1;
        }
      }
    }
  }
  return scores;
}

// Main matching logic
const tokens = tokenize(request);
if (tokens.length === 0) {
  console.log('No meaningful keywords extracted from request');
  process.exit(0);
}

// Score categories first
const categoryScores = scoreCategories(tokens);

// Score all skills
const skillScores = [];
for (const [name, skill] of Object.entries(index.skills)) {
  const { score, matchedTriggers } = scoreSkill(skill, tokens, categoryScores);
  if (score > 0) {
    skillScores.push({
      name,
      category: skill.category,
      description: skill.description,
      path: skill.path,
      files: skill.files,
      score,
      matchedTriggers,
      confidence: Math.min(100, Math.round(score * 5))
    });
  }
}

// Sort by score
skillScores.sort((a, b) => b.score - a.score);

// Get top 5
const topSkills = skillScores.slice(0, 5);

if (topSkills.length === 0) {
  console.log('No matching skills found for: ' + tokens.join(', '));
  process.exit(0);
}

// Output results
console.log('MATCHED_SKILLS:');
console.log('');

for (let i = 0; i < topSkills.length; i++) {
  const s = topSkills[i];
  console.log(`${i + 1}. ${s.name} (${s.confidence}%)`);
  console.log(`   Category: ${s.category}`);
  console.log(`   Path: ${s.path}`);
  console.log(`   Description: ${s.description.substring(0, 100)}...`);
  console.log(`   Matched: ${s.matchedTriggers.join(', ') || 'category match'}`);
  console.log(`   Files: ${s.files.join(', ')}`);
  console.log('');
}

// Output top categories
const topCategories = Object.entries(categoryScores)
  .filter(([_, s]) => s > 0)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 3);

if (topCategories.length > 0) {
  console.log('TOP_CATEGORIES: ' + topCategories.map(([c, s]) => `${c}(${s})`).join(', '));
}

console.log('');
console.log('TOKENS_EXTRACTED: ' + tokens.join(', '));

NODEJS
