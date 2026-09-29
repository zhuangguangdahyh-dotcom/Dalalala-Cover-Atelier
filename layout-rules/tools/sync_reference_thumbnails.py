#!/usr/bin/env python3
"""Sync correctly named thumbnails from the pinned source checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
CATALOG = PROJECT / "skills/cover-design-reference/references/layout-catalog.json"
TARGET = ROOT / "references/source-thumbnails"
CONTACTS = ROOT / "references/contact-sheets"
LEGACY = ROOT / "references/legacy-misaligned-thumbnails"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync(source_repo: Path, archive_existing: bool, source_kind: str) -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if archive_existing and TARGET.exists() and not LEGACY.exists():
        shutil.copytree(TARGET, LEGACY)

    TARGET.mkdir(parents=True, exist_ok=True)
    missing = []
    mappings = []
    for item in catalog:
        rel = item["image"] if source_kind == "original" else item["thumbnail"]
        source = source_repo / rel
        target = TARGET / f"{item['id']}.jpg"
        if not source.exists():
            missing.append(str(source))
            continue
        if source_kind == "original":
            image = Image.open(source).convert("RGB")
            image.thumbnail((1200, 1680), Image.Resampling.LANCZOS)
            image.save(target, quality=92, optimize=True)
        else:
            shutil.copy2(source, target)
        mappings.append({
            "id": item["id"],
            "name": item["name"],
            "sourceKind": source_kind,
            "sourcePath": rel,
            "sourceSha256": digest(source),
            "expectedOriginalSha256": item.get("sha256"),
            "localPath": f"source-thumbnails/{item['id']}.jpg",
            "localSha256": digest(target),
            "visibleTitleReviewStatus": "pending-contact-sheet-review",
        })
    if missing:
        raise SystemExit("Missing source thumbnails:\n" + "\n".join(missing))

    CONTACTS.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=22)
    for start in range(1, 351, 25):
        end = min(350, start + 24)
        cell_w, cell_h = 240, 332
        sheet = Image.new("RGB", (cell_w * 5, cell_h * 5), "#171717")
        draw = ImageDraw.Draw(sheet)
        for offset, number in enumerate(range(start, end + 1)):
            row, col = divmod(offset, 5)
            thumb = Image.open(TARGET / f"{number:03d}.jpg").convert("RGB")
            thumb = thumb.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            x, y = col * cell_w, row * cell_h
            sheet.paste(thumb, (x, y))
            draw.rectangle((x, y, x + 55, y + 26), fill="#171717")
            draw.text((x + 5, y + 3), f"{number:03d}", fill="white", font=font)
        sheet.save(CONTACTS / f"contact-{start:03d}-{end:03d}.jpg", quality=92)

    manifest = {
        "schemaVersion": 1,
        "sourceKind": source_kind,
        "sourceCommit": "34dc39cb5128776b594754624fa2202d5942a35b",
        "count": len(mappings),
        "items": mappings,
    }
    (ROOT / "references/source-mapping.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"synced {len(catalog)} correctly mapped thumbnails")
    print(f"archive: {LEGACY if LEGACY.exists() else 'not created'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_repo", type=Path)
    parser.add_argument("--archive-existing", action="store_true")
    parser.add_argument("--source-kind", choices=["original", "thumbnail"], default="original")
    args = parser.parse_args()
    sync(args.source_repo.resolve(), args.archive_existing, args.source_kind)


if __name__ == "__main__":
    main()
