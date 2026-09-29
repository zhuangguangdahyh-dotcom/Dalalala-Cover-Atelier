#!/usr/bin/env python3
"""Validate coverage and minimum decision fields for composition cards."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CARD_RE = re.compile(r"^## (?P<id>\d{3})｜(?P<name>.+)$", re.MULTILINE)
REQUIRED = ("语义任务", "底图条件", "文字行为", "空间与留白", "禁用")


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    reference_dir = skill_dir / "references"
    paths = sorted(reference_dir.glob("composition-cards-*.md"))
    if not paths:
        print("FAIL: no composition card files found")
        return 1

    found: dict[int, tuple[str, Path]] = {}
    errors: list[str] = []

    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = list(CARD_RE.finditer(text))
        for index, match in enumerate(matches):
            card_id = int(match.group("id"))
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = text[match.end():end]
            if card_id in found:
                errors.append(f"duplicate {card_id:03d}: {path.name}")
            found[card_id] = (match.group("name").strip(), path)
            for field in REQUIRED:
                if f"**{field}**" not in body:
                    errors.append(f"{card_id:03d} missing field {field}")

    expected = set(range(1, 101))
    actual = set(found)
    for card_id in sorted(expected - actual):
        errors.append(f"missing card {card_id:03d}")
    for card_id in sorted(actual - expected):
        errors.append(f"unexpected card {card_id:03d}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {len(found)} cards, IDs 001–100, all required fields present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
