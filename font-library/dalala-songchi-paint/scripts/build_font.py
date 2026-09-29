#!/usr/bin/env python3
"""Build Dalala Songchi Paint v0.2 from isolated production glyph sheets."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
GLYPH_DIR = ROOT / "sources/glyphs"
DIST_DIR = ROOT / "dist"
PREVIEW_DIR = ROOT / "previews"
FONT_PATH = DIST_DIR / "DalalaSongchiPaint-Regular-v0.2.ttf"
WOFF2_PATH = DIST_DIR / "DalalaSongchiPaint-Regular-v0.2.woff2"

SOURCES = {
    "v01": ROOT / "sources/glyph-master-v01.png",
    "v02a": ROOT / "sources/glyph-master-v02a.png",
    "v02b": ROOT / "sources/glyph-master-v02b.png",
    "v03kan": ROOT / "sources/glyph-master-kan-v03.png",
}

UNITS_PER_EM = 1000
CAP_HEIGHT = 820
BASELINE = 90


def cell(column: int, row: int) -> tuple[int, int, int, int]:
    """Return a cell from the 1774 x 887, 4 x 2 master-sheet grid."""
    xs = [0, 443, 887, 1330, 1774]
    ys = [0, 443, 887]
    return xs[column], ys[row], xs[column + 1], ys[row + 1]


# glyph_name may differ from Unicode name for alternates.
GLYPH_SPECS = [
    {"char": "松", "source": "v01", "crop": cell(0, 0)},
    {"char": "弛", "source": "v01", "crop": cell(1, 0)},
    {"char": "感", "source": "v01", "crop": cell(2, 0)},
    {"char": "建", "source": "v01", "crop": cell(3, 0)},
    {"char": "立", "source": "v01", "crop": cell(0, 1)},
    {"char": "信", "source": "v01", "crop": cell(1, 1)},
    {"char": "任", "source": "v01", "crop": cell(2, 1)},
    {"char": "选", "source": "v02a", "crop": cell(0, 0)},
    {"char": "准", "source": "v02a", "crop": cell(1, 0)},
    {"char": "心", "source": "v02a", "crop": cell(2, 0)},
    {"char": "理", "source": "v02a", "crop": cell(3, 0)},
    {"char": "咨", "source": "v02a", "crop": cell(0, 1)},
    {"char": "询", "source": "v02a", "crop": cell(1, 1)},
    {"char": "师", "source": "v02a", "crop": cell(2, 1)},
    {"char": "先", "source": "v02a", "crop": cell(3, 1)},
    {"char": "看", "source": "v03kan", "crop": (0, 0, 887, 887)},
    {
        "char": "看",
        "source": "v03kan",
        "crop": (887, 0, 1774, 887),
        "glyph_name": "uni770B.alt1",
        "alternate_of": "uni770B",
    },
    {"char": "这", "source": "v02b", "crop": cell(2, 0)},
    {"char": "点", "source": "v02b", "crop": cell(3, 0)},
    {"char": "4", "source": "v02b", "crop": cell(0, 1), "glyph_name": "four"},
    {
        "char": "，",
        "source": "v02b",
        "crop": cell(1, 1),
        "glyph_name": "uniFF0C",
        "target_height": 230,
        "advance": 1000,
        "x_offset": 235,
        "baseline": 105,
    },
]


def unicode_name(ch: str) -> str:
    if ch == "4":
        return "four"
    return f"uni{ord(ch):04X}"


def clean_mask(crop_image: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
    mask = np.all(rgb > np.array([205, 205, 205]), axis=2).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    cleaned = np.zeros_like(mask)
    for index in range(1, count):
        if stats[index, cv2.CC_STAT_AREA] >= 5:
            cleaned[labels == index] = 255
    return cleaned


def trim_mask(mask: np.ndarray) -> np.ndarray:
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        raise ValueError("Glyph crop contains no white paint")
    pad = 5
    return mask[
        max(0, int(ys.min()) - pad) : min(mask.shape[0], int(ys.max()) + pad + 1),
        max(0, int(xs.min()) - pad) : min(mask.shape[1], int(xs.max()) + pad + 1),
    ]


def vector_contours(mask: np.ndarray):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = []
    for contour in contours:
        if abs(cv2.contourArea(contour)) < 5:
            continue
        perimeter = cv2.arcLength(contour, True)
        epsilon = max(0.55, perimeter * 0.0012)
        simplified = cv2.approxPolyDP(contour, epsilon, True).reshape(-1, 2)
        if len(simplified) >= 3:
            result.append(simplified)
    return result


def transform_for(mask: np.ndarray, spec: dict):
    height, width = mask.shape
    target_height = spec.get("target_height", CAP_HEIGHT)
    scale = target_height / height
    visual_width = width * scale
    advance = spec.get("advance", int(max(880, min(1120, visual_width + 145))))
    x_offset = spec.get("x_offset", (advance - visual_width) / 2)
    baseline = spec.get("baseline", BASELINE)
    return scale, x_offset, advance, baseline


def contours_to_glyph(contours, mask: np.ndarray, spec: dict):
    scale, x_offset, advance, baseline = transform_for(mask, spec)
    height = mask.shape[0]
    pen = TTGlyphPen(None)
    for contour in contours:
        points = [
            (
                int(round(x_offset + x * scale)),
                int(round(baseline + (height - y) * scale)),
            )
            for x, y in contour
        ]
        pen.moveTo(points[0])
        for point in points[1:]:
            pen.lineTo(point)
        pen.closePath()
    return pen.glyph(), advance, int(round(x_offset))


def contours_to_svg(contours, mask: np.ndarray, destination: Path):
    height, width = mask.shape
    path_parts = []
    for contour in contours:
        points = contour.tolist()
        commands = [f"M {points[0][0]} {points[0][1]}"]
        commands.extend(f"L {x} {y}" for x, y in points[1:])
        commands.append("Z")
        path_parts.append(" ".join(commands))
    destination.write_text(
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
            f'<path fill="#000" fill-rule="nonzero" d="{" ".join(path_parts)}"/>'
            "</svg>\n"
        ),
        encoding="utf-8",
    )


def notdef_glyph():
    pen = TTGlyphPen(None)
    pen.moveTo((80, 80))
    pen.lineTo((720, 80))
    pen.lineTo((720, 820))
    pen.lineTo((80, 820))
    pen.closePath()
    pen.moveTo((150, 150))
    pen.lineTo((150, 750))
    pen.lineTo((650, 750))
    pen.lineTo((650, 150))
    pen.closePath()
    return pen.glyph()


def empty_glyph():
    return TTGlyphPen(None).glyph()


def build():
    GLYPH_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    source_images = {
        key: cv2.imread(str(path), cv2.IMREAD_COLOR) for key, path in SOURCES.items()
    }
    missing = [key for key, image in source_images.items() if image is None]
    if missing:
        raise FileNotFoundError(f"Missing source sheets: {missing}")

    glyph_order = [".notdef", "space"]
    glyphs = {".notdef": notdef_glyph(), "space": empty_glyph()}
    metrics = {".notdef": (800, 40), "space": (420, 0)}
    cmap = {32: "space"}
    manifest = []

    for spec in GLYPH_SPECS:
        ch = spec["char"]
        glyph_name = spec.get("glyph_name", unicode_name(ch))
        x0, y0, x1, y1 = spec["crop"]
        crop_image = source_images[spec["source"]][y0:y1, x0:x1]
        mask = trim_mask(clean_mask(crop_image))
        contours = vector_contours(mask)
        glyph, advance, lsb = contours_to_glyph(contours, mask, spec)

        if glyph_name not in glyph_order:
            glyph_order.append(glyph_name)
        glyphs[glyph_name] = glyph
        metrics[glyph_name] = (advance, lsb)
        if "alternate_of" not in spec:
            cmap[ord(ch)] = glyph_name

        safe_file_char = "comma" if ch == "，" else ch
        file_stem = f"{glyph_name}-{safe_file_char}"
        Image.fromarray(mask).save(GLYPH_DIR / f"{file_stem}.png")
        contours_to_svg(contours, mask, GLYPH_DIR / f"{file_stem}.svg")
        manifest.append(
            {
                "char": ch,
                "glyphName": glyph_name,
                "unicode": None if "alternate_of" in spec else f"U+{ord(ch):04X}",
                "alternateOf": spec.get("alternate_of"),
                "source": SOURCES[spec["source"]].name,
                "sourceCrop": [x0, y0, x1, y1],
                "advanceWidth": advance,
                "leftSideBearing": lsb,
                "contourCount": len(contours),
            }
        )

    fb = FontBuilder(UNITS_PER_EM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-120)
    fb.setupNameTable(
        {
            "familyName": "Dalala Songchi Paint",
            "styleName": "Regular",
            "uniqueFontIdentifier": "Dalala Songchi Paint 0.2",
            "fullName": "Dalala Songchi Paint Regular",
            "psName": "DalalaSongchiPaint-Regular",
            "version": "Version 0.2.0",
        }
    )
    fb.setupOS2(
        sTypoAscender=900,
        sTypoDescender=-120,
        usWinAscent=940,
        usWinDescent=140,
        sxHeight=500,
        sCapHeight=820,
        ulUnicodeRange2=0x10000000,
    )
    fb.setupPost()
    fb.setupMaxp()
    fb.save(FONT_PATH)

    font = TTFont(FONT_PATH)
    addOpenTypeFeaturesFromString(
        font,
        """
        feature calt {
          sub uni770B uni770B' by uni770B.alt1;
        } calt;
        feature ss01 {
          sub uni770B by uni770B.alt1;
        } ss01;
        """,
    )
    font.save(FONT_PATH)

    webfont = TTFont(FONT_PATH)
    webfont.flavor = "woff2"
    webfont.save(WOFF2_PATH)

    (GLYPH_DIR / "manifest-v02.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    render_proof()


def render_proof():
    width, height = 1500, 1550
    canvas = Image.new("RGB", (width, height), "#1754A5")
    draw = ImageDraw.Draw(canvas)
    large = ImageFont.truetype(str(FONT_PATH), 210)
    medium = ImageFont.truetype(str(FONT_PATH), 155)
    small = ImageFont.truetype(str(FONT_PATH), 74)

    draw.text((90, 110), "选准", font=large, fill="#FFFDF5")
    draw.text((70, 390), "心理咨询师，", font=medium, fill="#FFFDF5")
    try:
        draw.text((65, 650), "先看看这", font=large, fill="#FFFDF5", features=["calt"])
    except (KeyError, OSError):
        draw.text((65, 650), "先看看这", font=large, fill="#FFFDF5")
    draw.text((80, 940), "4点", font=large, fill="#FFF238")
    draw.text((85, 1300), "松 弛 感 建 立 信 任", font=small, fill="#F3A2BC")

    pixels = np.asarray(canvas)
    rng = np.random.default_rng(204)
    noise = rng.normal(0, 3.0, pixels.shape[:2])[..., None]
    pixels = np.clip(pixels.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    Image.fromarray(pixels).save(PREVIEW_DIR / "font-render-proof-v02.png")


if __name__ == "__main__":
    build()
