---
name: dalala-layout-rule-engine
description: Resolve and apply one of Dalala's 350 project-local cover layout rules, or rank suitable candidates from content, asset, title-length, subject-count, and aspect-ratio constraints. Use for cover composition selection, fixed layout application, layout switching, or checking whether a cover preserves its selected composition. Never freely mix multiple layout IDs.
---

# Dalala 350 排版规则引擎

Use `../../layout-rules/registry.json` as the only layout discovery entry.

## When the user specifies a layout

1. Resolve the ID, number or exact Chinese name with `../../layout-rules/tools/layout_rule.py get`.
2. Load only that rule and its local thumbnail.
3. Preserve every item in `layoutContract.locked`.
4. Change only declared `adaptive` and `optional` fields.
5. Keep the selected font style and palette as separate rule systems.
6. Run every hard gate in the rule before delivery.

## When the user asks Codex to choose

1. Extract content intent, asset type, title length, subject count and target ratio.
2. Run `layout_rule.py select`. Inspect a returned thumbnail as concept evidence only when `useThumbnailAsConceptProof` is true; otherwise rely on the independent concept contract and show its audit status.
3. Choose one rule with a concrete reason tied to the supplied content and image.
4. Lock that single rule before generating the cover.
5. Do not choose a rule whose `autoSelectable` value is false.

The 350 source thumbnails are references for composition logic, not 350 approved customer templates. A rule becomes a production Cover Skill only after real content tests and visual approval.
