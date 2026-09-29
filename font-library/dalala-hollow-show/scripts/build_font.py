#!/usr/bin/env python3
"""Build Dalala Hollow Show from the approved 4 x 4 raster master."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/glyph-master-v02.png"
GLYPH_DIR = ROOT / "sources/glyphs"
DIST_DIR = ROOT / "dist"
PREVIEW_DIR = ROOT / "previews"
FONT_PATH = DIST_DIR / "DalalaHollowShow-Regular.ttf"

UNITS_PER_EM = 1000
CAP_HEIGHT = 820
BASELINE = 90
GRID = [
    ["今", "天", "有", "点"],
    ["好", "笑", "这", "也"],
    ["太", "离", "谱", "了"],
    ["吧", "的", "不", "！"],
]
CELL_INSET = 18


def safe_name(ch: str) -> str:
    return f"uni{ord(ch):04X}"


def clean_mask(crop: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    mask = (gray < 185).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    cleaned = np.zeros_like(mask)
    for index in range(1, count):
        if stats[index, cv2.CC_STAT_AREA] >= 4:
            cleaned[labels == index] = 255
    return cleaned


def trim_mask(mask: np.ndarray) -> np.ndarray:
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        raise ValueError("Glyph cell contains no black outline")
    pad = 5
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(mask.shape[1], int(xs.max()) + pad + 1)
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(mask.shape[0], int(ys.max()) + pad + 1)
    return mask[y0:y1, x0:x1]


def vector_contours(mask: np.ndarray):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = []
    for contour in contours:
        if abs(cv2.contourArea(contour)) < 3:
            continue
        perimeter = cv2.arcLength(contour, True)
        epsilon = max(0.42, perimeter * 0.00075)
        simplified = cv2.approxPolyDP(contour, epsilon, True).reshape(-1, 2)
        if len(simplified) >= 3:
            result.append(simplified)
    return result


def fit_transform(mask: np.ndarray):
    height, width = mask.shape
    scale = min(CAP_HEIGHT / height, 900 / width)
    visual_width = width * scale
    advance = int(max(760, min(1120, visual_width + 120)))
    x_offset = (advance - visual_width) / 2
    y_offset = BASELINE + (CAP_HEIGHT - height * scale) / 2
    return scale, x_offset, y_offset, advance


def contours_to_glyph(contours, mask: np.ndarray):
    scale, x_offset, y_offset, advance = fit_transform(mask)
    height = mask.shape[0]
    pen = TTGlyphPen(None)
    for contour in contours:
        points = [
            (
                int(round(x_offset + x * scale)),
                int(round(y_offset + (height - y) * scale)),
            )
            for x, y in contour
        ]
        pen.moveTo(points[0])
        for point in points[1:]:
            pen.lineTo(point)
        pen.closePath()
    return pen.glyph(), advance


def contours_to_svg(contours, mask: np.ndarray, destination: Path):
    height, width = mask.shape
    paths = []
    for contour in contours:
        pts = contour.tolist()
        commands = [f"M {pts[0][0]} {pts[0][1]}"]
        commands.extend(f"L {x} {y}" for x, y in pts[1:])
        commands.append("Z")
        paths.append(" ".join(commands))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        f'<path fill="#000" fill-rule="nonzero" d="{" ".join(paths)}"/>'
        "</svg>\n"
    )
    destination.write_text(svg, encoding="utf-8")


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


def build():
    GLYPH_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    source = cv2.imread(str(SOURCE), cv2.IMREAD_COLOR)
    if source is None:
        raise FileNotFoundError(SOURCE)

    source_height, source_width = source.shape[:2]
    cell_width = source_width // 4
    cell_height = source_height // 4
    glyph_order = [".notdef", "space"]
    glyphs = {".notdef": notdef_glyph(), "space": TTGlyphPen(None).glyph()}
    metrics = {".notdef": (800, 40), "space": (420, 0)}
    cmap = {32: "space"}
    manifest = []

    for row, characters in enumerate(GRID):
        for column, ch in enumerate(characters):
            x0, y0 = column * cell_width, row * cell_height
            x1 = source_width if column == 3 else (column + 1) * cell_width
            y1 = source_height if row == 3 else (row + 1) * cell_height
            # The generated master uses invisible cells. A narrow inset removes
            # expressive tails that occasionally cross a cell boundary without
            # trimming the intended glyph centred inside the cell.
            top_inset = 50 if row == 1 else CELL_INSET
            crop = source[
                y0 + top_inset:y1 - CELL_INSET,
                x0 + CELL_INSET:x1 - CELL_INSET,
            ]
            mask = trim_mask(clean_mask(crop))
            contours = vector_contours(mask)
            name = safe_name(ch)
            glyph, advance = contours_to_glyph(contours, mask)
            glyph_order.append(name)
            glyphs[name] = glyph
            metrics[name] = (advance, 30)
            cmap[ord(ch)] = name
            Image.fromarray(mask).save(GLYPH_DIR / f"{name}-{ch}.png")
            contours_to_svg(contours, mask, GLYPH_DIR / f"{name}-{ch}.svg")
            manifest.append({
                "char": ch,
                "glyphName": name,
                "unicode": f"U+{ord(ch):04X}",
                "advanceWidth": advance,
                "contourCount": len(contours),
                "sourceCell": [row, column],
            })

    fb = FontBuilder(UNITS_PER_EM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-100)
    fb.setupNameTable({
        "familyName": "Dalala Hollow Show",
        "styleName": "Regular",
        "uniqueFontIdentifier": "Dalala Hollow Show 0.2",
        "fullName": "Dalala Hollow Show Regular",
        "psName": "DalalaHollowShow-Regular",
        "version": "Version 0.2.0",
    })
    fb.setupOS2(
        sTypoAscender=900,
        sTypoDescender=-100,
        usWinAscent=900,
        usWinDescent=100,
        sxHeight=500,
        sCapHeight=820,
        ulUnicodeRange2=0x10000000,
    )
    fb.setupPost()
    fb.setupMaxp()
    fb.save(FONT_PATH)
    (GLYPH_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    render_proof()


def render_proof():
    width, height = 1774, 887
    canvas = Image.new("RGB", (width, height), "#F7F5EF")
    draw = ImageDraw.Draw(canvas)
    large = ImageFont.truetype(str(FONT_PATH), 220)
    medium = ImageFont.truetype(str(FONT_PATH), 190)
    draw.text((65, 120), "今天有点好笑", font=large, fill="#121212")
    draw.text((45, 470), "这也太离谱了吧！", font=medium, fill="#121212")
    Image.fromarray(np.array(canvas)).save(PREVIEW_DIR / "font-render-proof.png")


if __name__ == "__main__":
    build()
