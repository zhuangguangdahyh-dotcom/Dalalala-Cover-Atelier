# 工作台接入协议

## 固定标识

```text
styleId: dalala-chunky-marker
displayName: Dalala 粗记号趣味体
defaultVitality: playful
```

## 调用

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-chunky-marker \
  --text "今天有点好笑" \
  --vitality playful \
  --width 1080 \
  --height 1440
```

工作台必须同时加载：

- `style.json`
- `prompts/imagegen-title-layer.md`
- `references/approved-reference.png`
- `VITALITY_QA.md`

## 输出

输出透明 PNG 文字层，与封面底图分开保存。记录 `styleId`、`styleVersion`、标题原文、生命力档位、资源路径、QA 分数和审核状态。

## 失败处理

- 错字、漏字或多字：立即重新生成。
- 出现镂空、双描边、油漆刷毛或普通黑体感：判定风格失败。
- QA 低于 85 分：针对最低分项目重生成。
- 连续三次失败：进入人工复核，不静默替换为系统字体。

