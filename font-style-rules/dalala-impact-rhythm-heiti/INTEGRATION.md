# 工作台接入协议

## 固定标识

```text
styleId: dalala-impact-rhythm-heiti
displayName: Dalala 爆点节奏黑体
defaultIntensity: impact-max
```

## 调用

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-impact-rhythm-heiti \
  --text "认真生活自有答案" \
  --vitality impact-max \
  --width 1080 \
  --height 1440
```

工作台必须加载 `style.json`、提示词模板、确认样张和 `VITALITY_QA.md`。输出透明 PNG 文字层，并记录风格版本、标题原文、强度档位、文件路径、QA 分数和审核状态。

## 失败处理

- 第一眼不是加粗黑体：风格失败。
- 只有小幅旋转和统一错落：风格失败。
- 没有 3–4 个清晰爆点字，或没有安静字形成停顿：退回重生成。
- 趣味依赖描边、阴影、贴纸或装饰：退回重生成。
- 汉字结构错误、缩略图不可读或 QA 低于 85：针对最低分维度重生成。
- 连续三次失败：进入人工复核，不替换成普通粗黑体交付。
