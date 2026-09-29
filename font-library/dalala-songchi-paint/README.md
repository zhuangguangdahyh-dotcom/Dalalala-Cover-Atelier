# Dalala 松弛油漆体

这是封面工作台的第一套原创标题字体资源。它不是把普通字体叠加做旧纹理，而是把不规则的字骨、每一笔不同的书写动作和真实干刷缺墨一起固化进字形。

当前 `0.2` 版收录 20 个 Unicode 字符，并为“看”增加 1 个 OpenType 替换字形：

`松 弛 感 建 立 信 任 选 准 心 理 咨 询 师 先 看 这 点 4 ，`

## 文件结构

- `sources/glyphs/`：每个汉字的黑白母字 PNG 与可编辑 SVG 轮 Ring。
- `glyph-set.json`：字库覆盖范围、字形来源、设计状态和扩字参数。
- `STYLE_SPEC.md`：后续所有汉字必须遵守的造字规则。
- `scripts/build_font.py`：从母字图生成 TrueType 字体和验证样张。
- `dist/DalalaSongchiPaint-Regular-v0.2.ttf`：当前可安装、可被封面引擎调用的字体文件。
- `dist/DalalaSongchiPaint-Regular-v0.2.woff2`：工作台网页端直接加载的字体文件。
- `previews/font-render-proof-v02.png`：由 v0.2 TTF 实际渲染，不是图片模型直接写字。

## 构建

在项目根目录执行：

```bash
.font-venv/bin/python font-library/dalala-songchi-paint/scripts/build_font.py
```

## 在 Cover Engine 中调用

字体 ID 固定为：

```text
dalala-songchi-paint
```

当前版本只在标题中使用已覆盖字符。遇到缺字必须进入扩字队列，禁止混入普通黑体冒充完整字库。

连续输入“看看”时，字体的 `calt` 特性会把第二个“看”替换为独立重写的字形；支持字形面板的软件也可通过 `ss01` 手动调用该替换形。

## 扩字顺序

1. 先补封面高频字，不按字典顺序盲目铺满。
2. 每个新字先做 1 个基础母字，通过风格检查后再进入字体。
3. 高频字最终制作 3 个手工替换字形，用于同一句中重复出现时保持自然差异。
4. Cover Engine 根据作品 ID 选择替换字形和微小排版偏移，保证结果可复现。
