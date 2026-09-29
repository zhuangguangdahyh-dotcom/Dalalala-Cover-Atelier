#!/usr/bin/env python3
"""Audit source integrity, deep-study readiness and generic repetition."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"
REPORT = ROOT / "deep-study-audit.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint(value) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:12]


def main():
    registry = read(REGISTRY)
    category_counts = Counter()
    status_counts = Counter()
    title_mismatches = []
    mechanism_groups = defaultdict(list)
    anatomy_groups = defaultdict(list)
    missing_deep_fields = []

    for entry in registry["rules"]:
        knowledge = read(ROOT / entry["knowledge"])
        rule_id = entry["id"]
        category_counts[entry["category"]] += 1
        status_counts[entry.get("deepStudyStatus", "pending")] += 1
        claim = knowledge.get("sourceEvidence", {}).get("upstreamCatalogClaim", {})
        if claim.get("matchesVisibleTitle") is False:
            title_mismatches.append(rule_id)
        mechanism = knowledge.get("principle", {}).get("visualMechanism", "")
        mechanism_groups[fingerprint(mechanism)].append(rule_id)
        anatomy_groups[fingerprint(knowledge.get("contentAnatomy", {}))].append(rule_id)
        if entry.get("deepStudyStatus") == "verified":
            missing = [
                key
                for key in ("transformationGrammar", "semanticFit", "failureModes")
                if not knowledge.get(key)
            ]
            if missing:
                missing_deep_fields.append({"id": rule_id, "missing": missing})

    repeated_mechanisms = sorted(
        ({"count": len(ids), "ids": ids} for ids in mechanism_groups.values() if len(ids) > 1),
        key=lambda item: (-item["count"], item["ids"][0]),
    )
    repeated_anatomies = sorted(
        ({"count": len(ids), "ids": ids} for ids in anatomy_groups.values() if len(ids) > 1),
        key=lambda item: (-item["count"], item["ids"][0]),
    )
    report = {
        "schemaVersion": 1,
        "sourceReferenceStatus": "350 source works accepted as valid design references",
        "localDistillationStatus": dict(status_counts),
        "categoryCounts": dict(category_counts),
        "upstreamFilenameVisibleTitleMismatchCount": len(title_mismatches),
        "upstreamFilenameVisibleTitleMismatchIds": title_mismatches,
        "uniqueVisualMechanismCount": len(mechanism_groups),
        "uniqueContentAnatomyCount": len(anatomy_groups),
        "largestRepeatedVisualMechanisms": repeated_mechanisms[:10],
        "largestRepeatedContentAnatomies": repeated_anatomies[:10],
        "verifiedEntriesMissingDeepFields": missing_deep_fields,
        "interpretation": (
            "Source validity and local learning completeness are separate. Repeated fingerprints expose "
            "generic distillation that must be replaced by visual-reference-specific anatomy."
        ),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
