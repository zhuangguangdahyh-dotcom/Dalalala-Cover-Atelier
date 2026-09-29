#!/usr/bin/env python3
"""Query, compose and validate Dalala's independent traditional-colour library."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "source" if (ROOT / "source").exists() else ROOT / "references"
CSV_PATH = DATA_DIR / "chinese-color-harmony.csv"
REGISTRY_PATH = ROOT / "registry.json" if (ROOT / "registry.json").exists() else DATA_DIR / "registry.json"
PAIR_RE = re.compile(r"^\s*(?:(\d{3})-)?(.+?)\s+(#[0-9A-Fa-f]{6})\s*$")


def load_rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_pairs(value: str) -> list[dict]:
    result = []
    for segment in (value or "").split("|"):
        match = PAIR_RE.match(segment)
        if not match:
            continue
        number, name, hex_value = match.groups()
        result.append(
            {
                "id": number or None,
                "name": name.strip().replace("主色：", "").replace("辅色：", "").replace("点缀色：", ""),
                "hex": hex_value.upper(),
            }
        )
    return result


def normalize_hex(value: str) -> str:
    value = value.strip().upper()
    if not value.startswith("#"):
        value = "#" + value
    if not re.fullmatch(r"#[0-9A-F]{6}", value):
        raise SystemExit(f"Invalid HEX value: {value}")
    return value


def rgb(hex_value: str) -> tuple[int, int, int]:
    value = normalize_hex(hex_value)[1:]
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(hex_value: str) -> float:
    channels = []
    for value in rgb(hex_value):
        c = value / 255
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground: str, background: str) -> float:
    a, b = relative_luminance(foreground), relative_luminance(background)
    light, dark = max(a, b), min(a, b)
    return (light + 0.05) / (dark + 0.05)


def find_row(query: str, rows: list[dict]) -> tuple[dict, bool]:
    query = query.strip()
    for row in rows:
        if query in (row["编号"], row["色名"], row["HEX"], row["HEX"].lower()):
            return row, True
    if re.fullmatch(r"#?[0-9A-Fa-f]{6}", query):
        target = rgb(query)
        row = min(
            rows,
            key=lambda item: sum((a - b) ** 2 for a, b in zip(target, rgb(item["HEX"]))),
        )
        return row, False
    matches = [row for row in rows if query.lower() in row["色名"].lower()]
    if matches:
        return matches[0], True
    raise SystemExit(f"Unknown colour: {query}")


def color_record(row: dict) -> dict:
    return {
        "id": row["编号"],
        "name": row["色名"],
        "hex": row["HEX"].upper(),
        "hsl": {"h": int(row["H"]), "s": int(row["S"]), "l": int(row["L"])},
        "hueFamily": row["色相分类"],
        "temperature": row["冷暖属性"],
    }


def command_search(args):
    rows = load_rows()
    query = args.query.strip().lower()
    matches = [
        color_record(row)
        for row in rows
        if query in row["色名"].lower() or query in row["HEX"].lower() or query == row["编号"]
    ][: args.limit]
    print(json.dumps({"query": args.query, "matches": matches}, ensure_ascii=False, indent=2))


def command_get(args):
    rows = load_rows()
    row, exact = find_row(args.color, rows)
    relations = {
        key: parse_pairs(row[key])
        for key in (
            "同类色",
            "邻近色",
            "互补色",
            "分裂互补",
            "三角色",
            "四角色",
            "冷暖对照",
            "明色搭配",
            "暗色搭配",
            "灰调搭配",
            "中性色搭配",
            "辅色",
            "点缀色",
        )
    }
    print(
        json.dumps(
            {
                "query": args.color,
                "exactSourceMatch": exact,
                "color": color_record(row),
                "relations": relations,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def unique_colors(*groups: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for group in groups:
        for item in group:
            if item["hex"] not in seen:
                seen.add(item["hex"])
                result.append(item)
    return result


def choose_dark(colors: list[dict]) -> dict:
    return min(colors, key=lambda item: relative_luminance(item["hex"]))


def choose_light(colors: list[dict]) -> dict:
    return max(colors, key=lambda item: relative_luminance(item["hex"]))


def readable_colors(rows: list[dict], background: dict, anchor_row: dict) -> list[dict]:
    anchor_h = int(anchor_row["H"])
    anchor_s = int(anchor_row["S"])

    def rank(row: dict):
        hue_gap = abs(int(row["H"]) - anchor_h)
        hue_gap = min(hue_gap, 360 - hue_gap)
        saturation_gap = abs(int(row["S"]) - anchor_s)
        temperature_penalty = 0 if row["冷暖属性"] == anchor_row["冷暖属性"] else 35
        ratio = contrast_ratio(row["HEX"], background["hex"])
        return (hue_gap + saturation_gap * 0.35 + temperature_penalty, -ratio)

    candidates = [row for row in rows if contrast_ratio(row["HEX"], background["hex"]) >= 4.5]
    return [
        {"id": row["编号"], "name": row["色名"], "hex": row["HEX"].upper()}
        for row in sorted(candidates, key=rank)
    ]


def command_palette(args):
    rows = load_rows()
    row, exact = find_row(args.color, rows)
    anchor = {"id": row["编号"], "name": row["色名"], "hex": row["HEX"].upper()}
    strategy_columns = {
        "restrained": ("中性色搭配", "灰调搭配", "同类色"),
        "identity": ("辅色", "点缀色", "同类色"),
        "contrast": ("互补色", "分裂互补", "中性色搭配"),
        "warm-cool": ("冷暖对照", "中性色搭配", "同类色"),
        "light-dark": ("明色搭配", "暗色搭配", "灰调搭配"),
        "series": ("辅色", "同类色", "点缀色"),
        "data": ("三角色", "四角色", "中性色搭配"),
        "print": ("灰调搭配", "中性色搭配", "邻近色"),
    }
    groups = [parse_pairs(row[column]) for column in strategy_columns[args.strategy]]
    pool = unique_colors(*groups)
    if len(pool) < 4:
        pool = unique_colors(pool, parse_pairs(row["邻近色"]), parse_pairs(row["互补色"]))

    candidates = unique_colors([anchor], pool)
    background = choose_light(candidates)
    readable = readable_colors(rows, background, row)
    readable_focus = readable[:12]
    primary_text = (
        max(readable_focus, key=lambda item: contrast_ratio(item["hex"], background["hex"]))
        if readable_focus
        else choose_dark(candidates)
    )
    support = next((item for item in pool if item["hex"] not in {background["hex"], primary_text["hex"]}), anchor)
    accents = parse_pairs(row["点缀色"])
    accent = next((item for item in accents if item["hex"] not in {background["hex"], primary_text["hex"]}), anchor)
    secondary = next(
        (item for item in readable if item["hex"] not in {primary_text["hex"], accent["hex"]}),
        primary_text,
    )

    ratios = {
        "cover": "background/large field 68–78%, subject support 15–24%, accent 4–8%",
        "poster": "dominant field 58–72%, support 20–32%, accent 4–10%",
        "advertisement": "dominant field 62–75%, support 16–26%, offer accent 4–9%",
        "ppt": "canvas 76–86%, text/structure 10–20%, accent 3–7%",
        "resume": "canvas 80–90%, text/structure 8–17%, accent 2–5%",
        "long-graphic": "canvas 70–84%, content structure 12–24%, accents 2–7%",
        "ui": "canvas/surfaces 78–90%, text/borders 8–18%, actions/status 2–7%",
        "data-viz": "quiet background and axes; data area follows series count and semantic mode",
        "brand": "identity anchor repeats consistently; channel-specific ratios must be documented",
        "print": "set by substrate, ink coverage, finish and shelf distance; physical proof required",
    }[args.surface]

    roles = [
        {"role": "background", **background},
        {"role": "primaryText", **primary_text},
        {"role": "secondaryText", **secondary},
        {"role": "subjectSupport", **support},
        {"role": "accent", **accent},
    ]
    primary_ratio = round(contrast_ratio(primary_text["hex"], background["hex"]), 2)
    secondary_ratio = round(contrast_ratio(secondary["hex"], background["hex"]), 2)
    print(
        json.dumps(
            {
                "source": {"query": args.color, "exactSourceMatch": exact, "anchor": anchor},
                "strategy": args.strategy,
                "surface": args.surface,
                "policy": "colour roles are independent from layout and typography; apply and verify on the real artifact",
                "roles": roles,
                "areaRatio": ratios,
                "contrast": {
                    "primaryTextOnBackground": {
                        "ratio": primary_ratio,
                        "normalText": primary_ratio >= 4.5,
                        "largeText": primary_ratio >= 3,
                    },
                    "secondaryTextOnBackground": {
                        "ratio": secondary_ratio,
                        "normalText": secondary_ratio >= 4.5,
                        "largeText": secondary_ratio >= 3,
                    },
                },
                "warnings": [
                    "Candidate roles require review against the actual image and content hierarchy.",
                    "Replace failing text colours with a darker or lighter source colour before production.",
                    "Print output requires substrate and printer-profile proofing.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def command_contrast(args):
    ratio = contrast_ratio(args.foreground, args.background)
    print(
        json.dumps(
            {
                "foreground": normalize_hex(args.foreground),
                "background": normalize_hex(args.background),
                "ratio": round(ratio, 2),
                "normalText": ratio >= 4.5,
                "largeText": ratio >= 3,
                "uiAndGraphics": ratio >= 3,
            },
            indent=2,
        )
    )


def command_validate(_args):
    rows = load_rows()
    errors = []
    required = {
        "编号", "色名", "HEX", "H", "S", "L", "同类色", "邻近色", "互补色",
        "分裂互补", "三角色", "四角色", "冷暖对照", "明色搭配", "暗色搭配",
        "灰调搭配", "中性色搭配", "主色", "辅色", "点缀色"
    }
    if len(rows) != 742:
        errors.append(f"expected 742 colours, found {len(rows)}")
    if rows and not required.issubset(rows[0]):
        errors.append("harmony CSV is missing required columns")
    ids = [row["编号"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate colour ids")
    for row in rows:
        try:
            normalize_hex(row["HEX"])
        except SystemExit as exc:
            errors.append(str(exc))
            break
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if registry["assets"]["harmonySetCount"] != len(rows) * 12:
        errors.append("harmony relation count does not equal 742 × 12")
    print(
        json.dumps(
            {
                "valid": not errors,
                "colorCount": len(rows),
                "harmonySetCount": len(rows) * 12,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if errors:
        raise SystemExit(1)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=command_search)

    get = sub.add_parser("get")
    get.add_argument("--color", required=True)
    get.set_defaults(func=command_get)

    palette = sub.add_parser("palette")
    palette.add_argument("--color", required=True)
    palette.add_argument(
        "--strategy",
        choices=["restrained", "identity", "contrast", "warm-cool", "light-dark", "series", "data", "print"],
        default="restrained",
    )
    palette.add_argument(
        "--surface",
        choices=["cover", "poster", "advertisement", "ppt", "resume", "long-graphic", "ui", "data-viz", "brand", "print"],
        default="cover",
    )
    palette.set_defaults(func=command_palette)

    contrast = sub.add_parser("contrast")
    contrast.add_argument("--foreground", required=True)
    contrast.add_argument("--background", required=True)
    contrast.set_defaults(func=command_contrast)

    validate = sub.add_parser("validate")
    validate.set_defaults(func=command_validate)
    return root


def main():
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
