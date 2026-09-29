# Image–Text Fit Engine

Use when type and image share one canvas.

## Read the image as occupied space

Map the image before placing text:

- `protected`: face, eyes, hands, expression, product features, architectural nodes, signage, action, and factual evidence.
- `active`: gaze direction, motion vector, road, gesture, strong light, leading line, or perspective corridor.
- `resting`: genuinely low-detail regions that remain stable after contrast and crop changes.
- `structural`: walls, horizons, door frames, tabletops, shadow boundaries, columns, and repeated edges that can align type.
- `unstable`: hair, foliage, patterned fabric, reflections, highlights, busy shelving, crowds, or high-frequency texture.

Text normally belongs in `resting` or along `structural` space. It may enter `active` space only when it participates in the movement. It must not enter `protected` space unless deliberate obstruction is the actual message.

## Choose the image–text relationship

1. **Counterweight** — subject is heavy on one side; type stabilizes the other. Best for portraits, products, and single-point covers.
2. **Follow** — type begins where an existing vector starts or pauses. Best for gaze, roads, architecture, process, and action.
3. **Embed** — type sits on a believable surface or plane already present. Best for documentary, spatial, and editorial work.
4. **Frame** — type uses an existing boundary without covering the subject. Best for doors, windows, screens, paper, and layered foregrounds.
5. **Lead** — type is the dominant shape and the image becomes proof. Best only for short, sharp propositions.
6. **Field** — type stays quiet while atmosphere or environment carries the message. Best for spatial, reflective, premium, or slow-reading work.

Avoid default `panelize`: adding an opaque text panel that ignores the image. Use a panel only if the content itself contains a real separation, interface, document, label, or comparison.

## Decide whether a region can carry text

A region is usable only if all are true:

- its shape can contain the intended line breaks without forced fragmentation;
- local contrast can be made readable without flattening the whole image;
- the text does not close needed gaze or motion space;
- the region remains usable after the target crop;
- the text adds to the image's balance instead of becoming a second unrelated poster.

If no region qualifies, change the crop, choose another frame, extend the environment, reduce the copy, or redesign as type-led. Do not solve the problem with a random dark gradient or half-screen rectangle.

## Cropping logic

- Crop around identity and action first, geometry second.
- Preserve space in front of gaze and motion unless the message is obstruction, confinement, or conflict.
- Avoid tangent crops through chin, joints, fingers, product corners, door edges, or the top of a head.
- A close crop increases intimacy and pressure; a wide crop increases context, evidence, and breath. Choose based on meaning.
- Environmental extension may create type space, but it must continue perspective, light, texture, and scale without inventing false evidence.

## Contrast under text

Prefer these in order:

1. naturally calm region;
2. local tonal correction consistent with the light;
3. subtle scrim following an existing shadow or plane;
4. material-aware label or caption surface that belongs to the scene;
5. opaque panel only when semantically justified.

Outlines, glow, hard drop shadows, and blurred black boxes are last resorts and usually signal that the placement is wrong.
