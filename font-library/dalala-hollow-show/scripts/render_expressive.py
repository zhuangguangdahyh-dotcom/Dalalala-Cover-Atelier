#!/usr/bin/env python3
"""Render Dalala Hollow Show with the approved lively per-glyph rhythm."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = ROOT / "dist/DalalaHollowShow-Regular.ttf"
OUTPUT = ROOT / "previews/expressive-layout-proof.png"
BACKGROUND = "#F7F5EF"
INK = "#111111"


def glyph_layer(char: str, font: ImageFont.FreeTypeFont, scale: float, rotation: float):
    scratch = Image.new("RGBA", (640, 640), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)
    bbox = draw.textbbox((0, 0), char, font=font)
    draw.text((80 - bbox[0], 80 - bbox[1]), char, font=font, fill=INK)
    alpha = scratch.getchannel("A")
    content = alpha.getbbox()
    if content is None:
        return scratch
    glyph = scratch.crop(content)
    glyph = glyph.resize(
        (max(1, round(glyph.width * scale)), max(1, round(glyph.height * scale))),
        Image.Resampling.LANCZOS,
    )
    return glyph.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)


def compose_line(text: str, poses: list[tuple[float, float, int, float]], height: int):
    font = ImageFont.truetype(str(FONT_PATH), 300)
    layers = []
    width = 0
    for char, (scale, rotation, shift, tracking) in zip(text, poses):
        layer = glyph_layer(char, font, scale, rotation)
        layers.append((layer, shift, tracking))
        width += round(layer.width * tracking)
    width += max(layer.width for layer, _, _ in layers)
    line = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 0
    for layer, shift, tracking in layers:
        y = (height - layer.height) // 2 + shift
        line.alpha_composite(layer, (x, y))
        x += round(layer.width * tracking)
    content = line.getchannel("A").getbbox()
    return line.crop(content) if content else line


def fit_width(image: Image.Image, max_width: int):
    if image.width <= max_width:
        return image
    ratio = max_width / image.width
    return image.resize(
        (max_width, round(image.height * ratio)), Image.Resampling.LANCZOS
    )


def main():
    canvas = Image.new("RGB", (1774, 887), BACKGROUND)
    top = compose_line(
        "今天有点好笑",
        [
            (1.18, -4.0, -10, 0.82),
            (1.06, -2.0, 15, 0.82),
            (1.18, 2.5, -12, 0.80),
            (0.92, -1.0, 18, 0.84),
            (0.96, 3.5, 4, 0.80),
            (1.20, 2.0, -14, 0.84),
        ],
        430,
    )
    bottom = compose_line(
        "这也太离谱了吧！",
        [
            (0.94, -3.0, -4, 0.82),
            (0.86, 2.0, 14, 0.84),
            (1.06, -2.5, 1, 0.80),
            (1.06, 2.0, -8, 0.80),
            (1.00, -2.0, -2, 0.78),
            (0.90, 3.0, 16, 0.84),
            (1.02, -2.0, 2, 0.80),
            (0.66, 1.0, 30, 0.88),
        ],
        400,
    )
    top = fit_width(top, 1700)
    bottom = fit_width(bottom, 1700)
    canvas.paste(top, ((canvas.width - top.width) // 2, 20), top)
    canvas.paste(bottom, ((canvas.width - bottom.width) // 2, 455), bottom)
    canvas.save(OUTPUT)


if __name__ == "__main__":
    main()
