#!/usr/bin/env python3
"""Package the project knowledge base as a self-contained reusable skill."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT / "layout-rules"
SKILL = PROJECT / "skills/dalala-cover-composition-intelligence"
REF = SKILL / "references"
KNOWLEDGE = REF / "knowledge"
THUMBS = SKILL / "assets/layout-thumbnails"
CONTACTS = SKILL / "assets/contact-sheets"


def main() -> None:
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    THUMBS.mkdir(parents=True, exist_ok=True)
    CONTACTS.mkdir(parents=True, exist_ok=True)

    registry = json.loads((SOURCE / "registry.json").read_text(encoding="utf-8"))
    portable_entries = []
    for entry in registry["rules"]:
        number = entry["id"].split("-")[-1]
        knowledge = json.loads((SOURCE / entry["knowledge"]).read_text(encoding="utf-8"))
        knowledge["sourceEvidence"]["localReference"] = f"assets/layout-thumbnails/{number}.jpg"
        (KNOWLEDGE / f"layout-{number}.json").write_text(
            json.dumps(knowledge, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        image = Image.open(SOURCE / entry["thumbnail"]).convert("RGB")
        image.thumbnail((540, 720), Image.Resampling.LANCZOS)
        image.save(THUMBS / f"{number}.jpg", quality=82, optimize=True)

        portable_entries.append(
            {
                "id": entry["id"],
                "displayName": entry["displayName"],
                "category": entry["category"],
                "subcategory": entry["subcategory"],
                "status": entry["status"],
                "autoSelectable": entry["autoSelectable"],
                "coverSuitability": entry["coverSuitability"],
                "visualAuditStatus": entry["visualAuditStatus"],
                "knowledgeStatus": entry["knowledgeStatus"],
                "renderReady": entry["renderReady"],
                "knowledge": f"knowledge/layout-{number}.json",
                "thumbnail": f"assets/layout-thumbnails/{number}.jpg",
            }
        )

    portable_registry = {
        "schemaVersion": 2,
        "sourceCommit": registry["sourceCommit"],
        "sourceAuthority": registry["sourceAuthority"],
        "upstreamCatalogWarning": registry["upstreamCatalogWarning"],
        "defaultSelectionMode": registry["defaultSelectionMode"],
        "rules": portable_entries,
    }
    (REF / "registry.json").write_text(
        json.dumps(portable_registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for source_name, target_name in (
        ("visual-truth-catalog.json", "visual-truth-catalog.json"),
        ("references/source-mapping.json", "source-mapping.json"),
        ("LICENSE-CC-BY-4.0.txt", "LICENSE-CC-BY-4.0.txt"),
    ):
        shutil.copy2(SOURCE / source_name, REF / target_name)
    shutil.copy2(
        PROJECT / "cover-design-rules/platform-presets.json",
        REF / "platform-presets.json",
    )
    for source in (SOURCE / "references/contact-sheets").glob("*.jpg"):
        shutil.copy2(source, CONTACTS / source.name)
    print(
        f"packaged {len(portable_entries)} rules, "
        f"{len(list(KNOWLEDGE.glob('layout-*.json')))} knowledge files, "
        f"{len(list(THUMBS.glob('*.jpg')))} visual references"
    )


if __name__ == "__main__":
    main()
