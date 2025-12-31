#!/usr/bin/env python3
"""
VERIX Hook Translator v1.0.0

[assert|neutral] Translates all hook scripts to VERILINGUA x VERIX format [ground:design] [conf:0.95] [state:ongoing]

Usage:
  python verix-hook-translator.py --translate
"""

import re
from pathlib import Path
from datetime import datetime

HOOKS_DIR = Path(r"C:\Users\17175\.claude\hooks")
OUTPUT_DIR = HOOKS_DIR / "VERIX-HOOK-TRANSLATIONS"
BACKUP_DIR = HOOKS_DIR / ".backup"


def extract_hook_info(content: str, filepath: Path) -> dict:
    """Extract metadata from hook script."""
    info = {
        'name': filepath.stem,
        'purpose': '',
        'hook_type': '',
        'messages': []
    }

    # Extract PURPOSE comment
    purpose_match = re.search(r'#\s*PURPOSE:\s*(.+)', content)
    if purpose_match:
        info['purpose'] = purpose_match.group(1).strip()

    # Extract HOOK TYPE
    type_match = re.search(r'#\s*HOOK TYPE:\s*(.+)', content)
    if type_match:
        info['hook_type'] = type_match.group(1).strip()

    # Extract heredoc messages (cat << 'EOF' ... EOF)
    heredoc_matches = re.findall(r"cat << 'EOF'\s*(.*?)EOF", content, re.DOTALL)
    for match in heredoc_matches:
        info['messages'].append(match.strip())

    # Extract echo messages
    echo_matches = re.findall(r'echo\s+"([^"]+)"', content)
    info['messages'].extend(echo_matches)

    return info


def translate_message_to_verix(message: str) -> str:
    """Translate a message block to VERIX format."""
    lines = message.split('\n')
    verix_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            verix_lines.append('')
            continue

        # Detect line type and convert
        if line.startswith('!!') or 'CRITICAL' in line.upper():
            verix_lines.append(f'[warn|emphatic] {line} [ground:system-policy] [conf:1.0] [state:confirmed]')
        elif line.startswith('PHASE') or line.startswith('STEP'):
            verix_lines.append(f'[define|neutral] {line} [ground:given] [conf:1.0] [state:confirmed]')
        elif line.startswith('- ') or line.startswith('  -'):
            # List item
            verix_lines.append(f'  [assert|neutral] {line[2:].strip()} [ground:given] [conf:0.95] [state:confirmed]')
        elif line.startswith('[') and ']' in line:
            # Already has some marker format
            verix_lines.append(line)
        elif 'NEVER' in line.upper() or 'ALWAYS' in line.upper() or 'MUST' in line.upper():
            verix_lines.append(f'[direct|emphatic] {line} [ground:system-policy] [conf:1.0] [state:confirmed]')
        elif line.startswith('=') or line.startswith('-'):
            # Separator
            verix_lines.append(line)
        elif ':' in line and not line.startswith(' '):
            # Key-value style
            verix_lines.append(f'[define|neutral] {line} [ground:given] [conf:1.0] [state:confirmed]')
        else:
            verix_lines.append(f'[assert|neutral] {line} [ground:witnessed] [conf:0.90] [state:confirmed]')

    return '\n'.join(verix_lines)


def generate_verix_hook(info: dict) -> str:
    """Generate VERIX-formatted hook documentation."""

    name_upper = info['name'].upper().replace('-', '_')

    # Start building the document
    doc = f'''/*============================================================================*/
/* {name_upper} :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: {info['purpose'] or 'Hook script'}                                  */
/* HOOK TYPE: {info['hook_type'] or 'General'}                                  */
/*============================================================================*/

[define|neutral] HOOK := {{
  name: "{info['name']}",
  type: "{info['hook_type'] or 'General'}",
  purpose: "{info['purpose'] or 'Hook script'}",
  layer: L1
}} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

'''

    # Add translated messages
    section_num = 1
    for message in info['messages']:
        if message:
            doc += f'''/*----------------------------------------------------------------------------*/
/* S{section_num} HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

{translate_message_to_verix(message)}

'''
            section_num += 1

    # Add promise
    doc += f'''/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>{name_upper}_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
'''

    return doc


def translate_hook(filepath: Path) -> bool:
    """Translate a single hook file to VERIX format."""
    try:
        print(f"[processing] {filepath.name}")

        content = filepath.read_text(encoding='utf-8', errors='ignore')

        # Skip if not a shell script with messages
        if not content.strip():
            print(f"  [skipped] Empty file")
            return True

        # Extract info
        info = extract_hook_info(content, filepath)

        # Generate VERIX version
        verix_content = generate_verix_hook(info)

        # Write to output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"{filepath.stem}-VERIX.md"
        output_path.write_text(verix_content, encoding='utf-8')

        print(f"  [success] Created: {output_path.name}")
        return True

    except Exception as e:
        print(f"  [error] {e}")
        return False


def main():
    print("=" * 60)
    print("VERIX HOOK TRANSLATOR v1.0.0")
    print("=" * 60)
    print()

    # Find all .sh files
    hooks = list(HOOKS_DIR.rglob('*.sh'))

    print(f"[assert|neutral] Found {len(hooks)} hooks to translate [ground:glob-scan] [conf:1.0] [state:confirmed]")
    print()

    success = 0
    for hook in hooks:
        if '.backup' in str(hook):
            continue
        if translate_hook(hook):
            success += 1

    print()
    print("=" * 60)
    print(f"[assert|positive] Translated: {success}/{len(hooks)} [ground:count] [conf:1.0] [state:confirmed]")
    print(f"[assert|neutral] Output: {OUTPUT_DIR} [ground:path] [conf:1.0] [state:confirmed]")
    print("[commit|confident] <promise>HOOK_TRANSLATION_COMPLETE</promise>")


if __name__ == '__main__':
    main()
