#!/usr/bin/env python3
"""Query and validate Dalala's portable 350-rule composition library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"
REGISTRY = REF / "registry.json"
PLATFORMS = REF / "platform-presets.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_entry(query: str):
    normalized = query.strip()
    if normalized.isdigit():
        normalized = f"layout-{int(normalized):03d}"
    for entry in read(REGISTRY)["rules"]:
        names = (
            entry["id"],
            entry["displayName"],
            entry["displayName"].split(" · ", 1)[-1],
        )
        if normalized in names:
            return entry
    raise SystemExit(f"Unknown composition: {query}")


def resolve_canvas(platform: str | None, ratio: str | None):
    data = read(PLATFORMS)
    if not platform:
        default = data["defaultWhenPlatformUnspecified"]
        return {
            "platformId": "unspecified",
            "displayName": "未指定平台",
            **default,
            "usedDefault": True,
        }
    normalized = platform.strip().lower()
    match = None
    for platform_id, item in data["platforms"].items():
        aliases = [platform_id, *item.get("aliases", [])]
        if normalized in [str(alias).lower() for alias in aliases]:
            match = (platform_id, item)
            break
    if not match:
        raise SystemExit(f"Unknown platform: {platform}")
    platform_id, item = match
    chosen = ratio or item["defaultRatio"]
    if chosen not in item["allowedRatios"]:
        allowed = ", ".join(item["allowedRatios"])
        raise SystemExit(f"{item['displayName']} does not support {chosen}; allowed: {allowed}")
    return {
        "platformId": platform_id,
        "displayName": item["displayName"],
        "ratio": chosen,
        **item["allowedRatios"][chosen],
        "usedDefault": ratio is None,
    }


def knowledge_for(entry: dict):
    return read(REF / entry["knowledge"])


def thumbnail_for(entry: dict) -> Path:
    configured = ROOT / entry.get("thumbnail", "")
    if configured.exists():
        return configured
    return ROOT / "assets/layout-thumbnails" / f"{entry['id'].split('-')[-1]}.jpg"


def command_canvas(args):
    print(json.dumps(resolve_canvas(args.platform, args.ratio), ensure_ascii=False, indent=2))


def command_get(args):
    entry = resolve_entry(args.query)
    knowledge = knowledge_for(entry)
    payload = {
        "registryEntry": entry,
        "knowledge": knowledge,
        "thumbnail": str(thumbnail_for(entry).resolve()),
        "sourceValidated": True,
        "deepStudyStatus": entry.get("deepStudyStatus", "pending"),
        "renderReady": bool(entry.get("renderReady")),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_list(args):
    entries = read(REGISTRY)["rules"]
    if args.category:
        entries = [entry for entry in entries if entry["category"] == args.category]
    print(json.dumps(entries, ensure_ascii=False, indent=2))


def score(entry: dict, knowledge: dict, args) -> tuple[int, list[str]]:
    searchable = json.dumps(knowledge, ensure_ascii=False).lower()
    value = {"direct": 8, "adaptable": 4, "special-purpose": 1}.get(
        entry.get("coverSuitability"), 0
    )
    reasons = [f"适配级别：{entry.get('coverSuitability')}"]
    tokens = [
        token
        for token in args.intent.lower().replace("，", " ").replace("、", " ").split()
        if token
    ]
    semantic_terms = (
        "人物", "产品", "场景", "留白", "信任", "情绪", "观点", "冲突", "对比",
        "步骤", "流程", "清单", "数据", "关系", "故事", "速度", "冲击", "安静",
        "克制", "专业", "文化", "东方", "空间", "标题", "金句", "数字", "教程",
        "选择", "单人", "双人", "群像", "照片", "插画",
    )
    tokens.extend(term for term in semantic_terms if term in args.intent)
    tokens = list(dict.fromkeys(tokens))
    for token in tokens:
        if token in searchable:
            value += 8
            reasons.append(f"内容意图：{token}")
    fit = knowledge["contentFit"]
    if args.asset_type:
        if args.asset_type in fit["suitableAssets"] or "mixed" in fit["suitableAssets"]:
            value += 6
            reasons.append(f"素材：{args.asset_type}")
        else:
            value -= 5
    if args.title_length:
        if args.title_length in fit["titleLengths"]:
            value += 4
            reasons.append(f"标题长度：{args.title_length}")
        else:
            value -= 6
    if args.subject_count is not None:
        if args.subject_count in fit["subjectCounts"]:
            value += 4
            reasons.append(f"主体数量：{args.subject_count}")
        else:
            value -= 10
    if args.ratio not in ("3:4", "4:3", "16:9"):
        value -= 100
    if not entry.get("renderReady"):
        value -= 100
    return value, reasons


def command_select(args):
    candidates = []
    blocked = 0
    for entry in read(REGISTRY)["rules"]:
        if not args.allow_provisional and not entry.get("autoSelectable"):
            blocked += 1
            continue
        knowledge = knowledge_for(entry)
        value, reasons = score(entry, knowledge, args)
        candidates.append(
            {
                "id": entry["id"],
                "displayName": entry["displayName"],
                "score": value,
                "reasons": reasons,
                "thumbnail": str(thumbnail_for(entry).resolve()),
                "whyItWorks": knowledge["principle"]["whyItWorks"],
                "whenToUse": knowledge["principle"]["whenToUse"],
                "avoidWhen": knowledge["principle"]["avoidWhen"],
                "selectionSignals": knowledge["selectionSignals"],
                "deepStudyStatus": entry.get("deepStudyStatus", "pending"),
            }
        )
    candidates.sort(key=lambda item: (-item["score"], item["id"]))
    print(
        json.dumps(
            {
                "request": {
                    "intent": args.intent,
                    "assetType": args.asset_type,
                    "titleLength": args.title_length,
                    "subjectCount": args.subject_count,
                    "ratio": args.ratio,
                },
                "policy": "inspect candidates, then lock exactly one deep-ready composition",
                "blockedProvisionalRuleCount": blocked,
                "candidates": candidates[: args.limit],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def command_plan(args):
    entry = resolve_entry(args.layout)
    if not entry.get("renderReady") or entry.get("deepStudyStatus") != "verified":
        raise SystemExit(
            f"{entry['id']} is source-validated but its local deep study is provisional"
        )
    knowledge = knowledge_for(entry)
    payload = {
        "schemaVersion": 1,
        "renderAllowed": False,
        "canvas": resolve_canvas(args.platform, args.ratio),
        "composition": {
            "ruleId": entry["id"],
            "displayName": entry["displayName"],
            "knowledge": entry["knowledge"],
            "locked": knowledge["layoutContract"]["locked"],
            "referenceContentMap": knowledge["contentAnatomy"],
        },
        "assetAnalysis": {
            "complete": False,
            "assetPaths": args.asset or [],
            "primarySubject": "",
            "identityAnchors": [],
            "compositionFreedoms": [],
            "mustPreserve": [],
            "weakenOrRemove": [],
            "cropAndReposition": "",
            "cutoutDecision": {"required": None, "reason": ""},
            "backgroundDecision": {"action": "", "reason": ""},
            "effects": [],
        },
        "themeAnalysis": {
            "complete": False,
            "topic": args.topic,
            "mainTitle": args.title,
            "subtitle": "",
            "firstEmotion": "",
            "semanticGroups": [],
            "emphasisWords": [],
            "subjectThemeRelationship": "",
            "topicVisualMetaphor": "",
        },
        "designDecision": {
            "complete": False,
            "subjectTreatment": "",
            "transformationLevel": "",
            "subjectChangesRequired": [],
            "mainTitleLayout": "",
            "subtitleLayout": "",
            "decorationPlan": [],
            "backgroundAndEffects": [],
            "layerOrder": [],
        },
        "qa": {
            "compositionIdentifiableAt360px": False,
            "mustPreserveItemsVisible": False,
            "titleHierarchyClear": False,
            "subjectTitleRelationshipClear": False,
            "decorationsServeComposition": False,
            "imageTransformationSufficient": False,
            "layoutWorksWithoutDecoration": False,
        },
    }
    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(path.resolve())
    else:
        print(output, end="")


def command_validate(_args):
    errors = []
    registry = read(REGISTRY)
    entries = registry.get("rules", [])
    if len(entries) != 350:
        errors.append(f"expected 350 registry entries, found {len(entries)}")
    ids = set()
    for entry in entries:
        rule_id = entry.get("id")
        if rule_id in ids:
            errors.append(f"duplicate id: {rule_id}")
        ids.add(rule_id)
        path = REF / entry.get("knowledge", "")
        thumb = thumbnail_for(entry)
        if not path.exists():
            errors.append(f"{rule_id}: missing knowledge")
            continue
        if not thumb.exists():
            errors.append(f"{rule_id}: missing thumbnail")
        knowledge = read(path)
        if knowledge.get("ruleId") != rule_id:
            errors.append(f"{rule_id}: knowledge id mismatch")
        for key in (
            "principle",
            "contentAnatomy",
            "contentFit",
            "assetAdaptation",
            "textStrategy",
            "selectionSignals",
            "rejectionSignals",
            "qa",
        ):
            if not knowledge.get(key):
                errors.append(f"{rule_id}: missing {key}")
    result = {
        "valid": not errors,
        "ruleCount": len(entries),
        "knowledgeCount": len(list((REF / "knowledge").glob("layout-*.json"))),
        "thumbnailCount": len(list((ROOT / "assets/layout-thumbnails").glob("*.jpg"))),
        "renderReadyCount": sum(bool(entry.get("renderReady")) for entry in entries),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    canvas = sub.add_parser("canvas")
    canvas.add_argument("--platform")
    canvas.add_argument("--ratio")
    canvas.set_defaults(func=command_canvas)

    get = sub.add_parser("get")
    get.add_argument("query")
    get.set_defaults(func=command_get)

    listing = sub.add_parser("list")
    listing.add_argument("--category")
    listing.set_defaults(func=command_list)

    select = sub.add_parser("select")
    select.add_argument("--intent", required=True)
    select.add_argument("--asset-type", choices=["photo", "illustration", "text", "mixed", "data", "diagram"])
    select.add_argument("--title-length", choices=["short", "medium", "long"])
    select.add_argument("--subject-count", type=int)
    select.add_argument("--ratio", default="3:4")
    select.add_argument("--limit", type=int, default=8)
    select.add_argument(
        "--allow-provisional",
        action="store_true",
        help="include source-validated references whose local deep study is incomplete; audit only",
    )
    select.set_defaults(func=command_select)

    plan = sub.add_parser("plan")
    plan.add_argument("--layout", required=True)
    plan.add_argument("--platform")
    plan.add_argument("--ratio")
    plan.add_argument("--topic", required=True)
    plan.add_argument("--title", required=True)
    plan.add_argument("--asset", action="append")
    plan.add_argument("--output")
    plan.set_defaults(func=command_plan)

    validate = sub.add_parser("validate")
    validate.set_defaults(func=command_validate)
    return root


def main():
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
