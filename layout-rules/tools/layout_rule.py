#!/usr/bin/env python3
"""Discover, select and validate project-local cover layout rules."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def registry():
    return read_json(REGISTRY)


def resolve_rule(query: str):
    normalized = query.strip()
    if normalized.isdigit():
        normalized = f"layout-{int(normalized):03d}"
    for entry in registry().get("rules", []):
        if normalized in (entry["id"], entry["displayName"], entry["displayName"].split(" · ", 1)[-1]):
            return entry, read_json(ROOT / entry["rule"])
    raise SystemExit(f"Unknown layout rule: {query}")


def command_list(args):
    entries = registry().get("rules", [])
    if args.category:
        entries = [x for x in entries if x["category"] == args.category]
    if args.suitability:
        entries = [x for x in entries if x["coverSuitability"] == args.suitability]
    print(json.dumps(entries, ensure_ascii=False, indent=2))


def command_get(args):
    entry, rule = resolve_rule(args.query)
    anatomy_path = ROOT / entry["anatomy"] if entry.get("anatomy") else None
    knowledge_path = ROOT / entry["knowledge"] if entry.get("knowledge") else None
    payload = {
        "registryEntry": entry,
        "rule": rule,
        "templateAnatomy": read_json(anatomy_path) if anatomy_path else {
            "analysisStatus": "pending",
            "renderReady": False,
            "message": "必须先查看实际参考图并完成内容组成分析，才能进入封面生成。",
        },
        "compositionKnowledge": read_json(knowledge_path) if knowledge_path else {
            "learningStatus": "pending",
            "renderReady": False,
            "message": "该构图尚未形成可跨项目调用的知识资产。",
        },
        "resolvedPaths": {
            "rule": str((ROOT / entry["rule"]).resolve()),
            "thumbnail": str((ROOT / entry["thumbnail"]).resolve()),
            "anatomy": str(anatomy_path.resolve()) if anatomy_path else None,
            "knowledge": str(knowledge_path.resolve()) if knowledge_path else None,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def score_rule(rule: dict, args, knowledge: dict | None = None) -> tuple[int, list[str]]:
    selection = rule["selection"]
    haystack = " ".join([
        rule["displayName"],
        rule["source"]["category"],
        rule["source"]["subcategory"],
        *selection["tags"],
        rule["layoutContract"]["primaryMechanism"],
    ]).lower()
    if knowledge:
        haystack += " " + json.dumps(knowledge, ensure_ascii=False).lower()
    score = {"direct": 8, "adaptable": 3, "special-purpose": 1}.get(
        selection["coverSuitability"], 0
    )
    reasons = [f"封面适配：{selection['coverSuitability']}"]
    intent = args.intent.lower()
    tokens = [token for token in intent.replace("，", " ").replace("、", " ").split() if token]
    semantic_terms = (
        "人物", "产品", "场景", "留白", "信任", "情绪", "观点", "冲突", "对比",
        "步骤", "流程", "清单", "数据", "关系", "故事", "速度", "冲击", "安静",
        "克制", "专业", "文化", "东方", "空间", "标题", "金句", "数字", "教程",
        "选择", "单人", "双人", "群像", "照片", "插画",
    )
    tokens.extend(term for term in semantic_terms if term in intent)
    tokens = list(dict.fromkeys(tokens))
    for token in tokens:
        if token in haystack:
            score += 8
            reasons.append(f"匹配意图：{token}")
    for tag in selection["tags"]:
        normalized_tag = str(tag).lower()
        if len(normalized_tag) >= 2 and normalized_tag in intent:
            score += 8
            reasons.append(f"匹配标签：{tag}")
    if args.asset_type:
        if args.asset_type in selection["assetTypes"]:
            score += 6
            reasons.append(f"适合素材：{args.asset_type}")
        elif "mixed" not in selection["assetTypes"]:
            score -= 4
    if args.title_length:
        if args.title_length in selection["titleLengths"]:
            score += 4
            reasons.append(f"适合标题长度：{args.title_length}")
        else:
            score -= 5
    if args.subject_count is not None:
        if args.subject_count in selection["subjectCounts"]:
            score += 4
            reasons.append(f"适合主体数量：{args.subject_count}")
        else:
            score -= 8
    if not selection["autoSelectable"]:
        score -= 100
        reasons.append("视觉标题已确认错配，禁止自动选择")
    return score, reasons


def command_select(args):
    candidates = []
    blocked = []
    for entry in registry().get("rules", []):
        if not entry.get("autoSelectable", False) and not args.allow_provisional:
            blocked.append(entry["id"])
            continue
        rule = read_json(ROOT / entry["rule"])
        knowledge = read_json(ROOT / entry["knowledge"]) if entry.get("knowledge") else None
        score, reasons = score_rule(rule, args, knowledge)
        candidates.append({
            "id": rule["id"],
            "displayName": rule["displayName"],
            "score": score,
            "reasons": reasons,
            "thumbnail": str((ROOT / entry["thumbnail"]).resolve()),
            "visualAuditStatus": rule["source"]["visualAudit"]["status"],
            "useThumbnailAsConceptProof": rule["source"]["useThumbnailAsConceptProof"],
            "primaryMechanism": rule["layoutContract"]["primaryMechanism"],
            "anatomyStatus": entry.get("anatomyStatus", "pending"),
            "knowledgeStatus": entry.get("knowledgeStatus", "pending"),
            "deepStudyStatus": entry.get("deepStudyStatus", "pending"),
            "renderReady": bool(entry.get("renderReady", False)),
            "whyItWorks": knowledge.get("principle", {}).get("whyItWorks") if knowledge else None,
            "whenToUse": knowledge.get("principle", {}).get("whenToUse") if knowledge else [],
            "avoidWhen": knowledge.get("principle", {}).get("avoidWhen") if knowledge else [],
        })
    candidates.sort(key=lambda item: (-item["score"], item["id"]))
    payload = {
        "request": {
            "intent": args.intent,
            "assetType": args.asset_type,
            "titleLength": args.title_length,
            "subjectCount": args.subject_count,
            "canvasRatio": args.ratio,
        },
        "selectionPolicy": (
            "allow-provisional-for-audit-only"
            if args.allow_provisional
            else "deep-ready-only-then-lock-one-rule"
        ),
        "deepReadyRuleCount": len(candidates),
        "blockedProvisionalRuleCount": len(blocked),
        "candidates": candidates[: args.limit],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_validate(_args):
    data = registry()
    errors = []
    entries = data.get("rules", [])
    ids = set()
    if len(entries) != 350:
        errors.append(f"expected 350 rules, found {len(entries)}")
    for entry in entries:
        rule_id = entry.get("id")
        if rule_id in ids:
            errors.append(f"duplicate id: {rule_id}")
        ids.add(rule_id)
        rule_path = ROOT / entry.get("rule", "")
        thumb_path = ROOT / entry.get("thumbnail", "")
        if not rule_path.exists():
            errors.append(f"{rule_id}: missing rule file")
            continue
        if not thumb_path.exists():
            errors.append(f"{rule_id}: missing thumbnail")
        anatomy_rel = entry.get("anatomy")
        knowledge_rel = entry.get("knowledge")
        if entry.get("renderReady") and not knowledge_rel:
            errors.append(f"{rule_id}: renderReady requires composition knowledge")
        if anatomy_rel:
            anatomy_path = ROOT / anatomy_rel
            if not anatomy_path.exists():
                errors.append(f"{rule_id}: missing anatomy file")
            else:
                anatomy = read_json(anatomy_path)
                if anatomy.get("ruleId") != rule_id:
                    errors.append(f"{rule_id}: anatomy rule id mismatch")
        if knowledge_rel:
            knowledge_path = ROOT / knowledge_rel
            if not knowledge_path.exists():
                errors.append(f"{rule_id}: missing knowledge file")
            else:
                knowledge = read_json(knowledge_path)
                if knowledge.get("ruleId") != rule_id:
                    errors.append(f"{rule_id}: knowledge rule id mismatch")
                if entry.get("renderReady") and knowledge.get("learningStatus") != "studied":
                    errors.append(f"{rule_id}: renderReady knowledge is not studied")
        rule = read_json(rule_path)
        if rule.get("id") != rule_id:
            errors.append(f"{rule_id}: rule id mismatch")
        for key in ("source", "selection", "layoutContract", "runtime", "qa"):
            if key not in rule:
                errors.append(f"{rule_id}: missing {key}")
        if thumb_path.exists():
            digest = hashlib.sha256(thumb_path.read_bytes()).hexdigest()
            if digest != rule.get("source", {}).get("localThumbnailSha256"):
                errors.append(f"{rule_id}: thumbnail hash mismatch")
        contract = rule.get("layoutContract", {})
        if not contract.get("locked") or not contract.get("adaptive"):
            errors.append(f"{rule_id}: incomplete Locked/Adaptive contract")
    payload = {
        "valid": not errors,
        "ruleCount": len(entries),
        "thumbnailCount": len(list((ROOT / "references/source-thumbnails").glob("*.jpg"))),
        "autoSelectableCount": sum(bool(x.get("autoSelectable")) for x in entries),
        "renderReadyCount": sum(bool(x.get("renderReady")) for x in entries),
        "knowledgeCount": sum(bool(x.get("knowledge")) for x in entries),
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list")
    list_parser.add_argument("--category")
    list_parser.add_argument("--suitability", choices=["direct", "adaptable", "special-purpose"])
    list_parser.set_defaults(func=command_list)

    get_parser = sub.add_parser("get")
    get_parser.add_argument("query", help="layout-001, 001, or exact Chinese name")
    get_parser.set_defaults(func=command_get)

    select_parser = sub.add_parser("select")
    select_parser.add_argument("--intent", required=True)
    select_parser.add_argument("--asset-type", choices=["photo", "illustration", "text", "mixed", "data", "diagram"])
    select_parser.add_argument("--title-length", choices=["short", "medium", "long"])
    select_parser.add_argument("--subject-count", type=int)
    select_parser.add_argument("--ratio", default="3:4")
    select_parser.add_argument("--limit", type=int, default=8)
    select_parser.add_argument(
        "--allow-provisional",
        action="store_true",
        help="include rules that have not completed deep study; audit only, never formal generation",
    )
    select_parser.set_defaults(func=command_select)

    validate_parser = sub.add_parser("validate")
    validate_parser.set_defaults(func=command_validate)
    return root


def main():
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
