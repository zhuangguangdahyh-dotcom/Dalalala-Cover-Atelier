# 工作台调用协议

## 输入

```json
{
  "styleId": "dalala-living-paint",
  "text": "选准心理咨询师，先看看这4点",
  "canvasWidth": 768,
  "canvasHeight": 1024,
  "coverId": "chen-na-001",
  "vitality": "alive-max",
  "seed": "chen-na-001-title-v1"
}
```

`vitality` 省略时使用 `alive-max`。`seed` 只稳定逐字差异计划，不把字变成固定轮廓。

## 调用

```bash
python3 font-style-rules/tools/font_style.py plan dalala-living-paint \
  --text "选准心理咨询师，先看看这4点" \
  --vitality alive-max \
  --width 768 --height 1024 \
  --seed "chen-na-001-title-v1"

python3 font-style-rules/tools/font_style.py prompt dalala-living-paint \
  --text "选准心理咨询师，先看看这4点" \
  --vitality alive-max \
  --width 768 --height 1024
```

工作台将 `approvedReference` 作为主视觉参考，将 `energyReference` 作为生命力补充参考。两张 `rejected` 图只用于 QA，不能传入正向生成。

## 生产资产

每个封面实例应保存：

```text
output/title-layers/<coverId>/
├── plan.json
├── glyph-instances/
│   ├── 000-选.png
│   ├── 001-准.png
│   └── ...
├── title-layer.png
└── qa.json
```

- `plan.json`：每个字符实例的姿态与笔触差异。
- `glyph-instances/`：逐字透明资产，失败时只替换对应实例。
- `title-layer.png`：最终透明标题层。
- `qa.json`：原文、结构、生命力和缩略图检查结果。

## 失败码

- `TEXT_STRUCTURE_FAIL`：错字、漏字、多字或汉字结构错误。
- `REPEATED_GLYPH_DUPLICATE`：重复字使用相同轮廓或仅做几何变换。
- `LIFEFORCE_LOW`：低于 88 分或像固定字体。
- `PAINT_TEXTURE_FAKE`：缺墨呈统一噪点、毛边或贴图感。
- `MOBILE_READABILITY_FAIL`：360 px 宽无法立即识别。

连续三次生成失败时保留候选并进入人工复核，不得自动切换到普通字体或旧 TTF。
