#!/usr/bin/env python3
"""Resolve and validate project-local cover lettering style rules."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry.json"
PATH_KEYS = (
    "config",
    "humanRules",
    "vitalityQA",
    "integration",
    "promptTemplate",
    "approvedReference",
    "energyReference",
    "rejectedReference",
    "wrongCharacterReference",
    "supportingFont",
    "skill",
)
REQUIRED_PATH_KEYS = (
    "config",
    "humanRules",
    "vitalityQA",
    "integration",
    "promptTemplate",
    "approvedReference",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def registry():
    return read_json(REGISTRY_PATH)


def find_style(style_id: str):
    for entry in registry().get("styles", []):
        if entry.get("id") == style_id or style_id in entry.get("aliases", []):
            return entry
    available = ", ".join(item["id"] for item in registry().get("styles", []))
    raise SystemExit(f"Unknown styleId: {style_id}. Available: {available}")


def resolve(entry: dict, key: str) -> Path:
    return (ROOT / entry[key]).resolve()


def command_list(_args):
    payload = [
        {
            "id": item["id"],
            "displayName": item["displayName"],
            "version": item["version"],
            "status": item["status"],
            "primaryRenderer": item["primaryRenderer"],
            "aliases": item.get("aliases", []),
        }
        for item in registry().get("styles", [])
    ]
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_get(args):
    entry = find_style(args.style_id)
    config = read_json(resolve(entry, "config"))
    payload = {
        "registryEntry": entry,
        "config": config,
        "resolvedPaths": {
            key: str(resolve(entry, key))
            for key in PATH_KEYS
            if key in entry
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_prompt(args):
    entry = find_style(args.style_id)
    config = read_json(resolve(entry, "config"))
    presets = config.get("vitalityPresets", {})
    vitality = args.vitality or config.get("identityCore", {}).get("defaultIntensity")
    if vitality not in presets:
        choices = ", ".join(presets)
        raise SystemExit(f"Unknown vitality: {vitality}. Available: {choices}")
    template = resolve(entry, "promptTemplate").read_text(encoding="utf-8")
    prompt = (
        template.replace("{TEXT}", args.text)
        .replace("{WIDTH}", str(args.width))
        .replace("{HEIGHT}", str(args.height))
        .replace("{VITALITY}", vitality)
    )
    vitality_parameters = json.dumps(presets[vitality], ensure_ascii=False)
    print(f"{prompt.rstrip()}\n\nMachine vitality parameters: {vitality_parameters}")


def stable_rng(seed: str, index: int, character: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}\0{index}\0{character}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def sample_range(rng: random.Random, values, digits=3):
    return round(rng.uniform(values[0], values[1]), digits)


def command_plan(args):
    entry = find_style(args.style_id)
    config = read_json(resolve(entry, "config"))
    construction = config.get("characterConstruction", {})
    presets = config.get("vitalityPresets", {})
    vitality = args.vitality or config.get("identityCore", {}).get("defaultIntensity")
    if vitality not in presets:
        choices = ", ".join(presets)
        raise SystemExit(f"Unknown vitality: {vitality}. Available: {choices}")
    preset = presets[vitality]
    postures = construction.get("postures", ["natural-handwritten"])
    bold_moves = construction.get("boldMoves", ["purposeful-overshoot"])
    quiet_moves = construction.get("quietMoves", ["clean-short-rest"])
    starts = construction.get("gestureStarts", ["natural-entry"])
    endings = construction.get("gestureEndings", ["natural-ending"])
    paint_states = construction.get(
        "paintStates", ["wet-solid", "normal-loaded", "dry-split"]
    )
    required_paint_states = min(
        len(paint_states), construction.get("requiredPaintStatesPerGlyph", 3)
    )
    occurrences = {}
    used_signatures = {}
    glyphs = []
    previous_posture = None
    visible_index = 0
    for source_index, character in enumerate(args.text):
        if character.isspace():
            glyphs.append({
                "sourceIndex": source_index,
                "character": character,
                "kind": "space"
            })
            continue
        occurrence = occurrences.get(character, 0) + 1
        occurrences[character] = occurrence
        rng = stable_rng(args.seed, source_index, character)
        posture_index = (rng.randrange(len(postures)) + occurrence * 3 + visible_index) % len(postures)
        if postures[posture_index] == previous_posture and len(postures) > 1:
            posture_index = (posture_index + 1) % len(postures)
        posture = postures[posture_index]
        previous_posture = posture
        bold_move = bold_moves[(rng.randrange(len(bold_moves)) + occurrence) % len(bold_moves)]
        quiet_move = quiet_moves[(rng.randrange(len(quiet_moves)) + visible_index) % len(quiet_moves)]
        start = starts[(rng.randrange(len(starts)) + occurrence) % len(starts)]
        ending = endings[(rng.randrange(len(endings)) + visible_index) % len(endings)]
        selected_states = rng.sample(paint_states, required_paint_states)
        rotation = sample_range(rng, preset["rotationDegrees"])
        baseline = sample_range(rng, preset["baselineShiftPercent"])
        scale = sample_range(rng, preset["glyphScale"])
        tracking = sample_range(rng, preset["trackingFactor"])
        signature = (posture, bold_move, quiet_move, start, ending)
        previous_signatures = used_signatures.setdefault(character, set())
        if signature in previous_signatures:
            posture_index = (posture_index + occurrence + 1) % len(postures)
            posture = postures[posture_index]
            bold_move = bold_moves[(bold_moves.index(bold_move) + occurrence + 1) % len(bold_moves)]
            rotation = round(-rotation if rotation else occurrence * 0.75, 3)
            signature = (posture, bold_move, quiet_move, start, ending)
        previous_signatures.add(signature)
        codepoint = ord(character)
        requires_skeleton = (
            0x3400 <= codepoint <= 0x4DBF
            or 0x4E00 <= codepoint <= 0x9FFF
            or 0xF900 <= codepoint <= 0xFAFF
        )
        glyphs.append({
            "sourceIndex": source_index,
            "instanceId": f"{source_index:03d}-{character}-{occurrence}",
            "character": character,
            "occurrence": occurrence,
            "requiresStandardSkeleton": requires_skeleton,
            "redrawIndependently": True,
            "isHeroCandidate": visible_index % 5 in (1, 4),
            "posture": posture,
            "boldMove": bold_move,
            "quietMove": quiet_move,
            "gestureStart": start,
            "gestureEnding": ending,
            "paintStates": selected_states,
            "baselineShiftPercent": baseline,
            "rotationDegrees": rotation,
            "glyphScale": scale,
            "trackingFactor": tracking,
            "qaStatus": "pending"
        })
        visible_index += 1
    payload = {
        "schemaVersion": 1,
        "styleId": entry["id"],
        "styleVersion": config.get("version"),
        "text": args.text,
        "canvas": {"width": args.width, "height": args.height},
        "vitality": vitality,
        "seed": args.seed,
        "instancePolicy": construction.get(
            "instancePolicy", "redraw-every-character-occurrence-independently"
        ),
        "glyphs": glyphs,
        "hardGates": config.get("qa", {}).get("vitalityHardGates", [])
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_validate(_args):
    errors = []
    data = registry()
    ids = set()
    route_names = set()
    for entry in data.get("styles", []):
        style_id = entry.get("id")
        if not style_id:
            errors.append("Registry entry missing id")
            continue
        if style_id in ids:
            errors.append(f"Duplicate style id: {style_id}")
        ids.add(style_id)
        for route_name in [style_id, *entry.get("aliases", [])]:
            if route_name in route_names:
                errors.append(f"Duplicate style id or alias: {route_name}")
            route_names.add(route_name)
        for key in REQUIRED_PATH_KEYS:
            if key not in entry:
                errors.append(f"{style_id}: missing registry path {key}")
                continue
            if not resolve(entry, key).exists():
                errors.append(f"{style_id}: missing file {resolve(entry, key)}")
        for key in PATH_KEYS:
            if key in entry and not resolve(entry, key).exists():
                errors.append(f"{style_id}: missing optional file {resolve(entry, key)}")
        if "config" in entry and resolve(entry, "config").exists():
            config = read_json(resolve(entry, "config"))
            if config.get("id") != style_id:
                errors.append(f"{style_id}: config id mismatch")
            if config.get("version") != entry.get("version"):
                errors.append(f"{style_id}: version mismatch")
            identity = config.get("identityCore", {})
            if not identity.get("nonNegotiable"):
                errors.append(f"{style_id}: identity core is not locked")
            default_intensity = identity.get("defaultIntensity")
            if default_intensity not in config.get("vitalityPresets", {}):
                errors.append(f"{style_id}: default vitality is not a declared preset")
            if identity.get("allowAutomaticDowngrade") is not False:
                errors.append(f"{style_id}: automatic vitality downgrade must be disabled")
            if config.get("qa", {}).get("vitalityMinimumScore", 0) < 85:
                errors.append(f"{style_id}: vitality score threshold is below 85")
        if "promptTemplate" in entry and resolve(entry, "promptTemplate").exists():
            template = resolve(entry, "promptTemplate").read_text(encoding="utf-8")
            for token in ("{TEXT}", "{WIDTH}", "{HEIGHT}", "{VITALITY}"):
                if token not in template:
                    errors.append(f"{style_id}: prompt missing {token}")
    default_style_id = data.get("defaultTitleStyleId")
    if default_style_id and default_style_id not in ids:
        errors.append(f"Unknown defaultTitleStyleId: {default_style_id}")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps({"valid": True, "styles": sorted(ids)}, ensure_ascii=False, indent=2))


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    list_parser = sub.add_parser("list")
    list_parser.set_defaults(func=command_list)
    get_parser = sub.add_parser("get")
    get_parser.add_argument("style_id")
    get_parser.set_defaults(func=command_get)
    prompt_parser = sub.add_parser("prompt")
    prompt_parser.add_argument("style_id")
    prompt_parser.add_argument("--text", required=True)
    prompt_parser.add_argument("--vitality")
    prompt_parser.add_argument("--width", type=int, required=True)
    prompt_parser.add_argument("--height", type=int, required=True)
    prompt_parser.set_defaults(func=command_prompt)
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("style_id")
    plan_parser.add_argument("--text", required=True)
    plan_parser.add_argument("--vitality")
    plan_parser.add_argument("--width", type=int, required=True)
    plan_parser.add_argument("--height", type=int, required=True)
    plan_parser.add_argument("--seed", required=True)
    plan_parser.set_defaults(func=command_plan)
    validate_parser = sub.add_parser("validate")
    validate_parser.set_defaults(func=command_validate)
    return root


def main():
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
