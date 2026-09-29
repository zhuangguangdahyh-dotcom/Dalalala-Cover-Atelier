# 工作台接入协议

## 输入

```json
{
  "styleId": "dalala-hollow-show",
  "text": "这也太离谱了吧！",
  "canvasWidth": 1080,
  "canvasHeight": 1440,
  "vitality": "alive3x",
  "coverId": "example-001"
}
```

`vitality` 省略时必须使用 `alive3x`。工作台不得静默降低生命力。

## 解析

1. 在 `../registry.json` 中按 `styleId` 精确查询。
2. 加载 `style.json`、提示词模板和确认样张。
3. 使用下面的命令生成最终 Imagegen 提示词：

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-hollow-show \
  --text "这也太离谱了吧！" \
  --vitality alive3x \
  --width 1080 \
  --height 1440
```

4. 将 `references/approved-reference.png` 作为正向风格参考图传入 Imagegen。
5. `references/rejected-uniform-dry-brush.png` 仅用于 QA 对照，不作为生成参考。

## 输出

```json
{
  "styleId": "dalala-hollow-show",
  "styleVersion": "1.0.1",
  "text": "这也太离谱了吧！",
  "vitality": "alive3x",
  "assetType": "transparent-png-title-layer",
  "assetPath": "output/title-layers/example-001.png",
  "qa": {
    "score": 0,
    "hardGatesPassed": false,
    "reviewStatus": "pending"
  }
}
```

## 失败处理

- 错字、漏字、多字：立即重生成。
- 生命力低于 85 分：针对最低分维度重生成。
- 统一干刷、统一圆润、统一字号或统一倾斜：直接判定风格失败。
- 连续三次失败：进入人工复核，并保留候选图；不得自动换成普通字体交付。
- 只有用户明确要求快速可读草稿时，才可调用 `supportingFont`，并标记为预览稿。

## 合成

文字层与封面底图分别保存。工作台必须允许二次调整整体大小、位置和裁切范围，不把文字永久烧录进首次生成的底图。
