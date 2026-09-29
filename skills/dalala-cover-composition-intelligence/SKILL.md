---
name: dalala-cover-composition-intelligence
description: Select, deeply analyse, adapt, and validate Dalala's 350 source-validated cover and layout references. Use when a task involves cover composition, template selection, title placement, subject transformation, crop, cutout or background decisions, decoration zones, Xiaohongshu, Douyin, Bilibili, WeChat Channels, or converting supplied assets into a designed cover.
---

# Dalala Cover Composition Intelligence

Use the visible-title truth catalog and the original thumbnail. Treat each reference as a complete design precedent containing composition, content anatomy, typography, image treatment, hierarchy, colour roles, material language, and decoration. Treat the upstream repository filename as audit metadata.

All 350 source works are accepted references. `deepStudyStatus` reports whether the local rule is complete enough for autonomous execution; it does not rate the source design. Only verified deep studies may be automatically selected or rendered.

## Required workflow

1. Resolve platform and canvas with `scripts/cover_composition.py canvas`. If the platform is absent, use portrait `3:4`, `1080 × 1440`.
2. Read `references/registry.json`. For automatic work, run `select` with intent, asset type, title length, subject count, and ratio.
3. Inspect the visual references for the best candidates, then lock one `layout-XXX`. Do not blend the skeletons of several rules.
4. Run `get layout-XXX`. Analyze why the rule fits, its subject, title, subtitle, evidence, decoration, protected whitespace, mass distribution, reading path, and image-type relationship.
5. Diagnose the supplied asset: primary subject, identity or fact anchors, composition freedoms, elements to weaken or remove, crop, cutout, background replacement, extension, repair, and effects.
6. Analyze the topic: first emotion, title semantics, emphasis words, subject-title relationship, subtitle need, and one visible topic metaphor.
7. Create a concrete plan with `plan`. Complete every placeholder before rendering.
8. Keep layout, font style, and palette as separate rule systems. Generate or render only after the composition plan validates.
9. Review the full-size image and a 360 px thumbnail. The chosen composition must remain identifiable without its rule name. Hide the title and decoration once: the transformed source and major masses must still support the topic.

## Selection rules

- Prefer content fit over visual novelty.
- A composition change must alter the crop, subject position and scale, image region, whitespace, title structure, reading path, and decoration flow as required by the rule.
- A supplied image is source material. Preserve identity and factual anchors, then rebuild its composition freedoms when the existing structure conflicts with the selected rule.
- Pet, lifestyle, and non-evidence images normally permit T2 structural transformation. Use T3 thematic reconstruction when the topic needs a visual metaphor.
- A reference palette expresses contrast roles. It never fixes the palette for future uses of that template.
- Do not promote a learned composition to a fixed approved cover template until it has passed real-content testing and human review.

## Commands

```bash
python3 scripts/cover_composition.py select \
  --intent "人物观点封面，需要留白与信任感" \
  --asset-type photo --title-length medium --subject-count 1 --ratio 3:4

python3 scripts/cover_composition.py get layout-013

python3 scripts/cover_composition.py plan \
  --layout layout-013 --platform 小红书 \
  --topic "主题" --title "标题" --asset /absolute/path/image.jpg \
  --output /absolute/path/cover-plan.json

python3 scripts/cover_composition.py validate
```

Read `references/SOURCE_AND_SCOPE.md` and `references/DEEP_STUDY_STANDARD.md` when reporting provenance, readiness, or the difference between a valid source reference and completed local distillation.
