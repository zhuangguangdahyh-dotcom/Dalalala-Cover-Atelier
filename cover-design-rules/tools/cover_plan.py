#!/usr/bin/env python3
"""Resolve platform canvases and enforce the cover design analysis pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRESETS = ROOT / "cover-design-rules/platform-presets.json"
LAYOUT_REGISTRY = ROOT / "layout-rules/registry.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_platform(query: str | None, ratio: str | None):
    presets = read_json(PRESETS)
    if not query:
        default = presets["defaultWhenPlatformUnspecified"]
        return {
            "platformId": "unspecified",
            "displayName": "未指定平台",
            "ratio": default["ratio"],
            "width": default["width"],
            "height": default["height"],
            "orientation": default["orientation"],
            "usedProjectDefault": True,
        }

    normalized = query.strip().lower()
    match = None
    for platform_id, platform in presets["platforms"].items():
        aliases = [platform_id, *platform.get("aliases", [])]
        if normalized in [str(item).lower() for item in aliases]:
            match = (platform_id, platform)
            break
    if not match:
        raise SystemExit(f"Unknown platform: {query}")

    platform_id, platform = match
    selected_ratio = ratio or platform["defaultRatio"]
    if selected_ratio not in platform["allowedRatios"]:
        allowed = ", ".join(platform["allowedRatios"])
        raise SystemExit(f"{platform['displayName']} does not allow {selected_ratio}; allowed: {allowed}")
    size = platform["allowedRatios"][selected_ratio]
    return {
        "platformId": platform_id,
        "displayName": platform["displayName"],
        "ratio": selected_ratio,
        "width": size["width"],
        "height": size["height"],
        "orientation": size["orientation"],
        "usedProjectDefault": ratio is None,
    }


def resolve_layout(query: str):
    normalized = query.strip()
    if normalized.isdigit():
        normalized = f"layout-{int(normalized):03d}"
    registry = read_json(LAYOUT_REGISTRY)
    for entry in registry["rules"]:
        if normalized in (entry["id"], entry["displayName"], entry["displayName"].split(" · ", 1)[-1]):
            if not entry.get("renderReady") or entry.get("deepStudyStatus") != "verified":
                raise SystemExit(
                    f"{entry['id']} is source-validated but its local deep study is provisional; "
                    "inspect and complete its anatomy and transformation grammar before rendering"
                )
            anatomy_path = entry.get("anatomy")
            knowledge_path = entry.get("knowledge")
            if anatomy_path and knowledge_path:
                anatomy = read_json(ROOT / "layout-rules" / anatomy_path)
                knowledge = read_json(ROOT / "layout-rules" / knowledge_path)
                if (
                    anatomy.get("analysisStatus") == "verified"
                    and knowledge.get("deepStudyStatus") == "verified"
                    and all(knowledge.get(key) for key in ("transformationGrammar", "semanticFit", "failureModes"))
                ):
                    return entry, {
                        "analysisStatus": "verified",
                        "reviewedReference": anatomy.get(
                            "reviewedReference", knowledge["sourceEvidence"]["localReference"]
                        ),
                        "referenceContentMap": anatomy.get(
                            "referenceContentMap", knowledge["contentAnatomy"]
                        ),
                        "coverTranslation": {
                            "purpose": knowledge["purpose"],
                            "principle": knowledge["principle"],
                            "contentFit": knowledge["contentFit"],
                            "assetAdaptation": knowledge["assetAdaptation"],
                            "textStrategy": knowledge["textStrategy"],
                            "transformationGrammar": knowledge["transformationGrammar"],
                            "semanticFit": knowledge["semanticFit"],
                            "failureModes": knowledge["failureModes"],
                            "selectionSignals": knowledge["selectionSignals"],
                            "rejectionSignals": knowledge["rejectionSignals"],
                            "layoutContract": knowledge["layoutContract"],
                        },
                    }
            raise SystemExit(
                f"{entry['id']} is missing verified anatomy or executable transformation knowledge"
            )
    raise SystemExit(f"Unknown layout rule: {query}")


def command_canvas(args):
    print(json.dumps(resolve_platform(args.platform, args.ratio), ensure_ascii=False, indent=2))


def command_new(args):
    canvas = resolve_platform(args.platform, args.ratio)
    entry, anatomy = resolve_layout(args.layout)
    payload = {
        "schemaVersion": 1,
        "renderAllowed": False,
        "canvas": canvas,
        "templateAnalysis": {
            "complete": True,
            "ruleId": entry["id"],
            "displayName": entry["displayName"],
            "referenceReviewed": anatomy["reviewedReference"],
            "referenceContentMap": anatomy["referenceContentMap"],
            "coverTranslation": anatomy["coverTranslation"],
        },
        "assetAnalysis": {
            "complete": False,
            "assetPaths": args.asset or [],
            "primarySubject": "",
            "identityAnchors": [],
            "compositionFreedoms": [],
            "mustPreserve": [],
            "mayWeakenOrRemove": [],
            "backgroundDecision": {"action": "", "reason": ""},
            "cutoutDecision": {"required": None, "reason": ""},
            "effects": [],
            "qualityRisks": [],
        },
        "themeAnalysis": {
            "complete": False,
            "topic": args.topic,
            "mainTitle": args.title,
            "subtitle": "",
            "firstEmotion": "",
            "titleSemanticGroups": [],
            "emphasisWords": [],
            "subjectThemeRelationship": "",
            "topicVisualMetaphor": "",
        },
        "designDecision": {
            "complete": False,
            "visualStyle": "",
            "subjectTreatment": "",
            "transformationLevel": "",
            "subjectChangesRequired": [],
            "mainTitleLayout": "",
            "subtitleLayout": "",
            "decorationPlan": [],
            "backgroundAndEffects": [],
            "paletteRoles": {},
            "layerOrder": [],
        },
        "qa": {
            "templateAnatomyPreserved": False,
            "mustPreserveItemsVisible": False,
            "titleHierarchyClear": False,
            "subjectTitleRelationshipClear": False,
            "decorationsServeComposition": False,
            "imageTransformationSufficient": False,
            "layoutWorksWithoutDecoration": False,
            "thumbnailReadable": False,
        },
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
        print(output.resolve())
    else:
        print(text)


def command_validate(args):
    plan = read_json(Path(args.plan))
    errors = []
    canvas = plan.get("canvas", {})
    try:
        expected = resolve_platform(
            None if canvas.get("platformId") == "unspecified" else canvas.get("platformId"),
            canvas.get("ratio"),
        )
        for key in ("width", "height", "orientation"):
            if canvas.get(key) != expected.get(key):
                errors.append(f"canvas.{key} must be {expected.get(key)}")
    except SystemExit as exc:
        errors.append(str(exc))

    for phase in ("templateAnalysis", "assetAnalysis", "themeAnalysis", "designDecision"):
        if not plan.get(phase, {}).get("complete"):
            errors.append(f"{phase}.complete must be true")

    template = plan.get("templateAnalysis", {})
    if not template.get("referenceContentMap") or not template.get("coverTranslation"):
        errors.append("templateAnalysis must contain content map and cover translation")

    asset = plan.get("assetAnalysis", {})
    for key in (
        "primarySubject",
        "identityAnchors",
        "compositionFreedoms",
        "mustPreserve",
        "backgroundDecision",
        "cutoutDecision",
    ):
        if not asset.get(key) and asset.get(key) is not False:
            errors.append(f"assetAnalysis.{key} is required")

    theme = plan.get("themeAnalysis", {})
    for key in (
        "topic",
        "mainTitle",
        "firstEmotion",
        "emphasisWords",
        "subjectThemeRelationship",
        "topicVisualMetaphor",
    ):
        if not theme.get(key):
            errors.append(f"themeAnalysis.{key} is required")

    decision = plan.get("designDecision", {})
    for key in (
        "visualStyle",
        "subjectTreatment",
        "transformationLevel",
        "subjectChangesRequired",
        "mainTitleLayout",
        "decorationPlan",
        "layerOrder",
    ):
        if not decision.get(key):
            errors.append(f"designDecision.{key} is required")

    if args.stage == "release":
        qa = plan.get("qa", {})
        for key, value in qa.items():
            if value is not True:
                errors.append(f"qa.{key} must be true for release")

    payload = {
        "valid": not errors,
        "stage": args.stage,
        "renderAllowed": not errors,
        "releaseAllowed": not errors if args.stage == "release" else False,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    canvas = sub.add_parser("canvas")
    canvas.add_argument("--platform")
    canvas.add_argument("--ratio")
    canvas.set_defaults(func=command_canvas)

    new = sub.add_parser("new")
    new.add_argument("--layout", required=True)
    new.add_argument("--platform")
    new.add_argument("--ratio")
    new.add_argument("--topic", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--asset", action="append")
    new.add_argument("--output")
    new.set_defaults(func=command_new)

    validate = sub.add_parser("validate")
    validate.add_argument("plan")
    validate.add_argument("--stage", choices=["plan", "release"], default="plan")
    validate.set_defaults(func=command_validate)
    return root


def main():
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
