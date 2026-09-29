#!/usr/bin/env python3
"""Rebuild registry readiness from verified anatomy and deep knowledge evidence."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"
PROGRESS = ROOT / "deep-study-progress.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    registry = load(REGISTRY)
    progress = []

    for entry in registry["rules"]:
        rule_id = entry["id"]
        default_anatomy = ROOT / "anatomy" / f"{rule_id}.json"
        anatomy_path = ROOT / entry["anatomy"] if entry.get("anatomy") else default_anatomy
        if anatomy_path.exists() and not entry.get("anatomy"):
            entry["anatomy"] = str(anatomy_path.relative_to(ROOT))
        knowledge_path = ROOT / entry["knowledge"] if entry.get("knowledge") else None
        anatomy_verified = bool(
            anatomy_path
            and anatomy_path.exists()
            and load(anatomy_path).get("analysisStatus") == "verified"
        )
        knowledge = load(knowledge_path) if knowledge_path and knowledge_path.exists() else {}
        deep_status = knowledge.get("deepStudyStatus", "pending")
        deep_verified = deep_status == "verified"
        required_blocks = all(
            knowledge.get(key)
            for key in ("transformationGrammar", "semanticFit", "failureModes")
        )
        distilled = anatomy_verified and deep_status in ("deep-studied", "verified") and required_blocks
        ready = distilled and deep_verified

        entry["anatomyStatus"] = "verified" if anatomy_verified else "pending"
        entry["knowledgeStatus"] = "deep-studied" if distilled else "provisional"
        entry["deepStudyStatus"] = deep_status if distilled else "pending"
        entry["autoSelectable"] = ready
        entry["renderReady"] = ready

        rule_path = ROOT / entry["rule"]
        rule = load(rule_path)
        rule["selection"]["autoSelectable"] = ready
        rule["runtime"]["renderReady"] = ready
        save(rule_path, rule)

        if knowledge_path and knowledge_path.exists() and not distilled:
            knowledge["learningStatus"] = "provisional"
            knowledge["deepStudyStatus"] = knowledge.get("deepStudyStatus", "pending")
            save(knowledge_path, knowledge)
        elif knowledge_path and knowledge_path.exists() and distilled:
            knowledge["learningStatus"] = "studied"
            save(knowledge_path, knowledge)

        progress.append(
            {
                "id": rule_id,
                "displayName": entry["displayName"],
                "category": entry["category"],
                "subcategory": entry["subcategory"],
                "anatomyStatus": entry["anatomyStatus"],
                "deepStudyStatus": entry["deepStudyStatus"],
                "autoSelectable": ready,
                "renderReady": ready,
            }
        )

    save(REGISTRY, registry)
    counts = Counter(item["deepStudyStatus"] for item in progress)
    save(
        PROGRESS,
        {
            "schemaVersion": 1,
            "total": len(progress),
            "counts": dict(counts),
            "policy": "Only verified deep studies may be automatically selected or rendered.",
            "rules": progress,
        },
    )
    print(
        json.dumps(
            {
                "total": len(progress),
                "deepReady": counts.get("verified", 0),
                "deepStudiedAwaitingRealTests": counts.get("deep-studied", 0),
                "pending": counts.get("pending", 0),
                "progress": str(PROGRESS),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
