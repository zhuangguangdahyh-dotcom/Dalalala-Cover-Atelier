# Runtime contract

The project source of truth is `../../../font-style-rules/registry.json`, style ID `dalala-living-paint`.

Required pipeline:

1. Resolve the style from the registry.
2. Generate a deterministic occurrence plan with `font_style.py plan`.
3. Verify standard structure for every unique Chinese character.
4. Generate every occurrence independently as a transparent glyph asset.
5. Reject only failed glyphs and regenerate them.
6. Compose and save the transparent title layer.
7. Pass `VITALITY_QA.md` before cover composition.

Do not use any file in `font-library/dalala-songchi-paint/dist/` as the title renderer.
