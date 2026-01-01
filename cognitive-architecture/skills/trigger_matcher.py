#!/usr/bin/env python3
"""
trigger_matcher.py - Fuzzy skill trigger matching using rapidfuzz

FIX-1 from REMEDIATION-PLAN.md:
Problem: 199 skills define TRIGGER_POSITIVE patterns, but matching is only exact/substring.
Solution: Use rapidfuzz for fuzzy matching with configurable threshold.

Usage:
    from trigger_matcher import SkillTriggerMatcher
    matcher = SkillTriggerMatcher()
    matches = matcher.match("help me debug this API error", threshold=0.6)
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    print("Warning: rapidfuzz not installed. Using fallback matching.")


@dataclass
class SkillMatch:
    """Represents a matched skill with confidence score."""
    name: str
    category: str
    path: str
    description: str
    confidence: float
    matched_triggers: List[str]
    matched_keywords: List[str]
    files: List[str]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "path": self.path,
            "description": self.description,
            "confidence": self.confidence,
            "matched_triggers": self.matched_triggers,
            "matched_keywords": self.matched_keywords,
            "files": self.files
        }


class SkillTriggerMatcher:
    """
    Fuzzy matcher for skill triggers using rapidfuzz.

    Matching strategy:
    1. Extract keywords from user prompt
    2. Match against skill triggers with fuzzy matching
    3. Apply category weighting
    4. Apply negative trigger penalties
    5. Return ranked list of matches
    """

    # Stopwords to filter from prompts
    STOPWORDS = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'between',
        'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where', 'why', 'how',
        'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'just', 'also', 'now', 'here', 'there', 'this', 'that', 'these', 'those',
        'it', 'its', 'you', 'your', 'we', 'our', 'they', 'their', 'i', 'my',
        'use', 'using', 'used', 'want', 'need', 'help', 'please', 'me', 'get'
    }

    # Category-specific boost keywords
    CATEGORY_KEYWORDS = {
        'delivery': ['feature', 'implement', 'build', 'develop', 'create', 'add', 'new', 'frontend', 'backend', 'api', 'sparc'],
        'quality': ['test', 'audit', 'review', 'verify', 'validate', 'check', 'quality', 'coverage', 'lint', 'style'],
        'security': ['security', 'auth', 'authentication', 'permission', 'vulnerability', 'pentest', 'compliance', 'encrypt'],
        'research': ['research', 'find', 'discover', 'analyze', 'investigate', 'study', 'literature', 'paper', 'synthesis'],
        'orchestration': ['coordinate', 'orchestrate', 'swarm', 'parallel', 'workflow', 'pipeline', 'cascade', 'hive'],
        'operations': ['deploy', 'devops', 'cicd', 'infrastructure', 'docker', 'kubernetes', 'terraform', 'monitor'],
        'platforms': ['platform', 'database', 'ml', 'neural', 'flow', 'nexus', 'codex', 'gemini', 'multi-model'],
        'foundry': ['create', 'agent', 'skill', 'template', 'forge', 'generator', 'builder', 'prompt'],
        'specialists': ['business', 'finance', 'domain', 'expert', 'specialist', 'industry'],
        'tooling': ['documentation', 'docs', 'github', 'pr', 'issue', 'release', 'tool']
    }

    def __init__(self, index_path: Optional[str] = None):
        """
        Initialize the matcher with a skill index.

        Args:
            index_path: Path to skill-index.json. If None, uses default location.
        """
        if index_path is None:
            # Default to the skill-index.json in scripts directory
            base_dir = Path(__file__).parent.parent.parent
            index_path = base_dir / "scripts" / "skill-index" / "skill-index.json"

        self.index_path = Path(index_path)
        self.index: Dict = {}
        self.skills: Dict = {}
        self.keyword_index: Dict = {}

        self._load_index()

    def _load_index(self) -> None:
        """Load the skill index from JSON file."""
        if not self.index_path.exists():
            raise FileNotFoundError(f"Skill index not found: {self.index_path}")

        with open(self.index_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)

        self.skills = self.index.get('skills', {})
        self.keyword_index = self.index.get('keyword_index', {})
        self.categories = self.index.get('categories', {})

    def _tokenize(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Lowercase and extract words
        words = re.sub(r'[^a-z0-9\s-]', ' ', text.lower()).split()

        # Filter stopwords and short words
        tokens = [w for w in words if len(w) > 2 and w not in self.STOPWORDS]

        return tokens

    def _fuzzy_match_triggers(self, tokens: List[str], skill_triggers: List[str], threshold: float) -> Tuple[float, List[str]]:
        """
        Fuzzy match tokens against skill triggers.

        Returns:
            Tuple of (score, list of matched triggers)
        """
        score = 0.0
        matched = []

        if not RAPIDFUZZ_AVAILABLE:
            # Fallback to exact/substring matching
            for token in tokens:
                for trigger in skill_triggers:
                    if token == trigger:
                        score += 10.0
                        matched.append(trigger)
                    elif token in trigger or trigger in token:
                        score += 5.0
                        matched.append(trigger)
            return score, list(set(matched))

        # Use rapidfuzz for better matching
        for token in tokens:
            if not skill_triggers:
                continue

            # Find best match for this token
            result = process.extractOne(
                token,
                skill_triggers,
                scorer=fuzz.WRatio,
                score_cutoff=threshold * 100
            )

            if result:
                match_trigger, match_score, _ = result
                # Normalize score to 0-1 range
                normalized_score = match_score / 100.0

                if normalized_score >= threshold:
                    # Weight by match quality
                    if normalized_score >= 0.95:  # Near-exact match
                        score += 10.0
                    elif normalized_score >= 0.85:  # Strong match
                        score += 7.0
                    elif normalized_score >= 0.75:  # Good match
                        score += 5.0
                    else:  # Acceptable match
                        score += 3.0

                    matched.append(match_trigger)

        return score, list(set(matched))

    def _score_category(self, tokens: List[str], category: str) -> float:
        """Score how well tokens match a category."""
        if category not in self.CATEGORY_KEYWORDS:
            return 0.0

        cat_keywords = self.CATEGORY_KEYWORDS[category]
        score = 0.0

        for token in tokens:
            if token in cat_keywords:
                score += 3.0
            else:
                # Fuzzy match category keywords
                for keyword in cat_keywords:
                    if token in keyword or keyword in token:
                        score += 1.0
                        break

        return score

    def match(self, prompt: str, threshold: float = 0.6, top_k: int = 5) -> List[SkillMatch]:
        """
        Match a user prompt against all skills.

        Args:
            prompt: User's request text
            threshold: Minimum fuzzy match score (0.0-1.0)
            top_k: Number of top matches to return

        Returns:
            List of SkillMatch objects, sorted by confidence
        """
        tokens = self._tokenize(prompt)

        if not tokens:
            return []

        # Score all skills
        skill_scores: List[Tuple[str, float, List[str], List[str]]] = []

        for skill_name, skill_data in self.skills.items():
            triggers = skill_data.get('triggers', [])
            negative_triggers = skill_data.get('negativeTriggers', [])
            category = skill_data.get('category', 'unknown')
            description = skill_data.get('description', '')

            # Score trigger matches
            trigger_score, matched_triggers = self._fuzzy_match_triggers(
                tokens, triggers, threshold
            )

            # Score category match
            cat_score = self._score_category(tokens, category)

            # Score description match
            desc_words = self._tokenize(description)
            desc_score = sum(2.0 for t in tokens if t in desc_words)

            # Apply negative trigger penalty
            neg_score, neg_matched = self._fuzzy_match_triggers(
                tokens, negative_triggers, threshold
            )

            # Calculate total score
            total_score = trigger_score + cat_score + desc_score - (neg_score * 0.5)

            if total_score > 0:
                skill_scores.append((
                    skill_name,
                    total_score,
                    matched_triggers,
                    tokens
                ))

        # Sort by score descending
        skill_scores.sort(key=lambda x: x[1], reverse=True)

        # Convert to SkillMatch objects
        matches = []
        for skill_name, score, matched_triggers, matched_keywords in skill_scores[:top_k]:
            skill_data = self.skills[skill_name]

            # Normalize confidence to 0-100
            confidence = min(100.0, score * 5)

            match = SkillMatch(
                name=skill_name,
                category=skill_data.get('category', 'unknown'),
                path=skill_data.get('path', ''),
                description=skill_data.get('description', '')[:200],
                confidence=round(confidence, 1),
                matched_triggers=matched_triggers,
                matched_keywords=matched_keywords,
                files=skill_data.get('files', [])
            )
            matches.append(match)

        return matches

    def match_json(self, prompt: str, threshold: float = 0.6, top_k: int = 5) -> str:
        """Match and return results as JSON string."""
        matches = self.match(prompt, threshold, top_k)
        return json.dumps([m.to_dict() for m in matches], indent=2)


def main():
    """CLI interface for testing the matcher."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python trigger_matcher.py \"your prompt here\" [threshold] [top_k]")
        sys.exit(1)

    prompt = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    try:
        matcher = SkillTriggerMatcher()
        matches = matcher.match(prompt, threshold, top_k)

        if not matches:
            print(f"No matching skills found for: {prompt}")
            sys.exit(0)

        print("MATCHED_SKILLS:\n")
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m.name} ({m.confidence}%)")
            print(f"   Category: {m.category}")
            print(f"   Path: {m.path}")
            print(f"   Description: {m.description[:100]}...")
            print(f"   Matched triggers: {', '.join(m.matched_triggers) or 'category match'}")
            print(f"   Files: {', '.join(m.files)}")
            print()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run generate-index.js first to create the skill index.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
