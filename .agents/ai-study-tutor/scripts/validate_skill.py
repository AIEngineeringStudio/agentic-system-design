#!/usr/bin/env python3
"""Offline structural checks for ai-study-tutor (Python standard library only).

This does not evaluate teaching quality or host skill activation.
"""
from pathlib import Path
from collections import Counter
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def read(relative):
    p = ROOT / relative
    if not p.is_file():
        errors.append(f"Missing file: {relative}")
        return ""
    return p.read_text(encoding="utf-8")


skill = read("SKILL.md")
check(skill.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
match = re.match(r"\A---\n(.*?)\n---\n", skill, flags=re.S)
check(match is not None, "Missing closing YAML frontmatter")
meta = match.group(1) if match else ""
name = re.search(r"^name:\s*(\S+)\s*$", meta, re.M)
check(bool(name) and bool(
    re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1) if name else "")),
      "Invalid skill name")
check(not name or name.group(1) == ROOT.name,
      "Skill name does not match parent directory")
description = re.search(r"^description:\s*(.+)$", meta, re.M)
check(bool(description) and 1 <= len(
    description.group(1)) <= 1024 if description else False,
      "Invalid description length")
check(len(skill.splitlines()) < 500, "Core SKILL.md should be <500 lines")

try:
    data = json.loads(read('cases.json'))
except Exception as ex:
    errors.append(f'Invalid cases.json: {ex}')
    data = []
check(len(data) == 73, f'Expected 73 cases, found {len(data)}')
check([x.get('id') for x in data] == list(range(1, 74)),
      'Case IDs must be contiguous 1–73')
mods = Counter(x.get('module') for x in data)
check(mods == {1: 8, 2: 9, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8},
      f'Unexpected module counts: {dict(mods)}')
anchors = [x.get('id') for x in data if x.get('anchor')]
check(anchors == [1, 3, 9, 14, 18, 21, 26, 28, 34, 36, 38, 42, 43, 50, 58, 73],
      f'Unexpected anchors: {anchors}')

catalog = read('references/case-catalog.md')
rows = re.findall(r'^\| (\d\d) \| ([^|]+) \| `([^`]+)` \| ([^|]*)\|$', catalog,
                  re.M)
check(len(rows) == 73, f'Catalog rows should be 73, got {len(rows)}')
for c in data:
    n = c.get('id')
    if not isinstance(n, int) or not 1 <= n <= 73:
        continue
    slug = c.get('module_slug')
    module_file = f'references/module-{c["module"]:02d}-{slug}.md'
    text = read(module_file)
    check(bool(re.search(r'^### #' + str(n).zfill(2) + r' — ' + re.escape(
        c.get('title', '')) + r'(?: ★ anchor)?$', text, re.M)),
          f'Module missing #{n}: {c.get("title")}')
    if len(rows) >= n:
        row = rows[n - 1]
        check(row[0] == str(n).zfill(2), f'Catalog ID mismatch #{n}')
        check(row[1].strip() == c.get('title'), f'Catalog title mismatch #{n}')
        check(row[2] == module_file, f'Catalog file mismatch #{n}')
        check(('★' in row[3]) == bool(c.get('anchor')),
              f'Catalog anchor mismatch #{n}')

for f in [
    'references/teaching-method.md',
    'references/architecture-templates.md',
    'references/standards-and-sources.md',
    'assets/architecture-checklist.md',
    'assets/example-design.md',
    'assets/expense-preview.html',
    'tests/tutor-behavior-cases.md',
    'README.md',
]:
    read(f)

check('No quizzes' in skill,
      'Core should explicitly prohibit unrequested quizzes')
check('references/case-catalog.md' in skill,
      'Core must route via lightweight index')
check('module-05-generative-ui.md' in skill, 'Core must route module 05')
check('references/teaching-method.md' in skill,
      'Core must refer to teaching method')
check('continuous solid lines' in skill,
      'Core must preserve solid-line ASCII style')
check('only the selected' in skill.lower(),
      'Core should say to load only selected module')

# Keep references directly under references/ to minimize loading depth.
check(not (ROOT / 'references' / 'modules').exists(),
      'Module references should live one level under references/')

if errors:
    for e in errors:
        print('FAIL:', e, file=sys.stderr)
    print(f'Validation failed: {len(errors)} issue(s)', file=sys.stderr)
    sys.exit(1)
print(
    f'PASS: skill frontmatter, 73 cases, 9 modules, {len(anchors)} anchors, routing and required assets')
