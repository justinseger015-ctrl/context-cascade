#!/usr/bin/env python3
"""Remove VERIX markers from SKILL.md files."""

import re
import sys
from pathlib import Path

def cleanup_skill_file(filepath: str) -> bool:
    """Remove VERIX sections from a SKILL.md file."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return False

    content = path.read_text(encoding='utf-8')
    original_len = len(content)

    # Patterns to remove (sections)
    section_patterns = [
        # VCL COMPLIANCE APPENDIX section and everything after
        r'\n---\n\n## VCL COMPLIANCE APPENDIX.*',
        # HTML comment sections with VERIX content
        r'\n---\n<!-- S\d+ [A-Z ]+\s*-->.*?(?=\n---\n<!-- S|\n---\n\n## VCL|$)',
        # Standalone HTML comment sections at end
        r'\n---\n<!-- [A-Z]+ +-->.*$',
    ]

    # Line patterns to remove
    line_patterns = [
        r'^\[define\|.*\].*$',
        r'^\[direct\|.*\].*$',
        r'^\[commit\|.*\].*$',
        r'^\[assert\|.*\].*$',
        r'^\[query\|.*\].*$',
        r'^- \[\[HON:.*$',
        r'^  - .*\[\[.*\]\].*$',
        r'^<promise>.*</promise>.*$',
        r'^\s*primary:.*$' if 'SUCCESS_CRITERIA :=' in content else r'(?!)',
        r'^\s*quality:.*$' if 'SUCCESS_CRITERIA :=' in content else r'(?!)',
        r'^\s*verification:.*$' if 'SUCCESS_CRITERIA :=' in content else r'(?!)',
        r'^\s*memory_mcp:.*$' if 'MCP_INTEGRATION :=' in content else r'(?!)',
        r'^\s*tools: \["mcp__.*$' if 'MCP_INTEGRATION :=' in content else r'(?!)',
        r'^\s*pattern:.*skills/.*$' if 'MEMORY_NAMESPACE :=' in content else r'(?!)',
        r'^\s*store: \[.*$' if 'MEMORY_NAMESPACE :=' in content else r'(?!)',
        r'^\s*retrieve: \[.*$' if 'MEMORY_NAMESPACE :=' in content else r'(?!)',
        r'^\s*WHO:.*$' if 'MEMORY_TAGGING :=' in content else r'(?!)',
        r'^\s*WHEN:.*$' if 'MEMORY_TAGGING :=' in content else r'(?!)',
        r'^\s*PROJECT:.*$' if 'MEMORY_TAGGING :=' in content else r'(?!)',
        r'^\s*WHY:.*$' if 'MEMORY_TAGGING :=' in content else r'(?!)',
        r'^\s*agent_spawning:.*$' if 'COMPLETION_CHECKLIST :=' in content else r'(?!)',
        r'^\s*registry_validation:.*$' if 'COMPLETION_CHECKLIST :=' in content else r'(?!)',
        r'^\s*todowrite_called:.*$' if 'COMPLETION_CHECKLIST :=' in content else r'(?!)',
        r'^\s*work_delegation:.*$' if 'COMPLETION_CHECKLIST :=' in content else r'(?!)',
        r'^\} \[ground:.*$',
    ]

    # Remove VCL COMPLIANCE APPENDIX and everything after it
    vcl_match = re.search(r'\n---\n\n## VCL COMPLIANCE APPENDIX', content, re.DOTALL)
    if vcl_match:
        content = content[:vcl_match.start()]

    # Remove HTML comment sections with VERIX
    content = re.sub(r'\n---\n<!-- S\d+ [A-Z ]+\s*-->\n---\n.*?(?=\n---\n<!-- S|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'\n---\n<!-- [A-Z]+ +-->\n---\n.*$', '', content, flags=re.DOTALL)

    # Remove individual VERIX marker lines
    lines = content.split('\n')
    cleaned_lines = []
    skip_block = False

    for line in lines:
        # Skip VERIX marker lines
        if re.match(r'^\[define\|', line) or \
           re.match(r'^\[direct\|', line) or \
           re.match(r'^\[commit\|', line) or \
           re.match(r'^\[assert\|', line) or \
           re.match(r'^- \[\[HON:', line) or \
           re.match(r'^  - .*Structure-first', line) and '[[' in line or \
           re.match(r'^  - .*constraint', line, re.I) and '[[' in line or \
           re.match(r'^  - .*Confidence', line) and '[[' in line or \
           '<promise>' in line or \
           'RULE_NO_UNICODE :=' in line or \
           'RULE_EVIDENCE :=' in line or \
           'RULE_REGISTRY :=' in line or \
           'SUCCESS_CRITERIA :=' in line or \
           'MCP_INTEGRATION :=' in line or \
           'MEMORY_NAMESPACE :=' in line or \
           'MEMORY_TAGGING :=' in line or \
           'COMPLETION_CHECKLIST :=' in line:
            continue

        # Skip definition block contents
        if re.match(r'^\s+(primary|quality|verification|memory_mcp|tools|pattern|store|retrieve|WHO|WHEN|PROJECT|WHY|agent_spawning|registry_validation|todowrite_called|work_delegation):', line):
            if skip_block:
                continue

        if re.match(r'^\} \[ground:', line):
            skip_block = False
            continue

        cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)

    # Clean up multiple consecutive empty lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Clean up trailing whitespace and ensure single newline at end
    content = content.rstrip() + '\n'

    # Only write if content changed
    if len(content) != original_len:
        path.write_text(content, encoding='utf-8')
        print(f"Cleaned: {filepath}")
        return True
    else:
        print(f"No changes: {filepath}")
        return False

if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        print("Usage: python cleanup-verix.py <file1> <file2> ...")
        sys.exit(1)

    cleaned = 0
    for f in files:
        if cleanup_skill_file(f):
            cleaned += 1

    print(f"\nCleaned {cleaned}/{len(files)} files")
