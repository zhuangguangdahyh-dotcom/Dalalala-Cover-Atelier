# 工作台接入协议

## 固定标识

```text
styleId: dalala-hard-fold-heiti
displayName: Dalala 硬折人文黑体
defaultIntensity: grounded
```

## 调用

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-hard-fold-heiti \
  --text "专业判断值得信任" \
  --vitality grounded \
  --width 1080 \
  --height 1440
```

工作台必须加载 `style.json`、提示词模板、确认样张和 `VITALITY_QA.md`。输出透明 PNG 文字层，并记录风格版本、标题原文、强度档位、文件路径、QA 分数和审核状态。

## 失败处理

- 字重不足、重心偏轻或第一眼不是粗黑体：退回重生成。
- 出现圆头、圆角、药丸字腔或膨胀感：风格失败。
- 所有字完全统一并呈现公文感：退回重生成。
- 为了活力加入明显跳字、旋转或碰撞：退回重生成。
- 汉字错误、缩略图不可读或 QA 低于 85：针对最低分维度重生成。
- 连续三次失败：进入人工复核，不替换成普通黑体交付。
