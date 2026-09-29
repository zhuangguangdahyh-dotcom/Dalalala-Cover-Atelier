# Runtime Visual QA

Inspect the rendered artifact, not only the prompt, source code, or layout specification.

## Hard failures

Rebuild when any is true:

- identity, expression, action, business category, or factual evidence was damaged;
- type covers a protected feature or blocks required gaze/motion space;
- there are two or more competing visual centres;
- the title's line breaks distort its meaning or cadence;
- an opaque panel was used because image–text fit was not solved;
- multiple contrasts are simultaneously maximised;
- the composition can accept an unrelated image and title without structural change;
- the target ratio is a crop of another ratio rather than a recomposition;
- decoration can be removed with no loss of meaning yet dominates attention;
- the result looks like a dashboard, template marketplace poster, cheap promotion, AI-plastic image, or generic premium beige layout;
- the user rejects the aesthetic.

## Three-distance test

### Thumbnail

- one memory anchor;
- one recognisable subject or evidence source;
- one dominant contrast;
- no small-text dependency.

### Normal view

- intended entry → meaning → proof/exit path is clear;
- title and image form one relationship;
- hierarchy and native line breaks are readable;
- whitespace has a visible function.

### Close view

- edges, crop points, faces, hands, architecture, materials, and light remain credible;
- punctuation, baselines, tracking, and annotations are intentional;
- no rendering, export, or AI artefacts.

## Counterfactual tests

- `hide-title`: if the image no longer supports the intended theme, the visual base is generic.
- `hide-image`: if the type arrangement becomes a generic quote card, typography is not integrated.
- `swap-content`: if unrelated content fits without recomposition, the layout is a template.
- `remove-accent`: if meaning is unchanged, reduce or delete the accent.
- `trace-path`: if the eye cannot describe the first three fixations, simplify the structure.
- `contact-sheet`: for a series or deck, reject repeated crop, centre, density, or silhouette even when individual pages pass.

User feedback overrides internal scoring. Diagnose rejection as a failure of meaning, subject treatment, force, hierarchy, material, colour, type, or format adaptation, then rebuild from that layer.
