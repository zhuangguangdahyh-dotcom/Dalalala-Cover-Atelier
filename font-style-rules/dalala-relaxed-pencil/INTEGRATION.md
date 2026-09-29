# Dalala 松弛速写铅笔体调用说明

## 入口

风格 ID：`dalala-relaxed-pencil`

默认生命力：`alive-clean`

生产渲染器：`imagegen-transparent-title-layer`

## 调用顺序

1. 从 `font-style-rules/registry.json` 解析本风格。
2. 加载 `style.json`、`STYLE_RULES.md`、提示词模板和确认样张。
3. 使用 `font_style.py plan` 为每个中文字符、英文字母、数字和标点分配独立姿态。
4. 将确认样张作为唯一视觉基准，单独生成透明文字层。
5. 按 `VITALITY_QA.md` 检查文字准确、中英文同源、铅笔压力、清爽度和生命力。
6. 通过后再与封面底图合成。

## 命令示例

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-relaxed-pencil \
  --text '认真生活 Take it easy.' \
  --width 1080 \
  --height 500 \
  --vitality alive-clean
```

```bash
python3 font-style-rules/tools/font_style.py plan dalala-relaxed-pencil \
  --text '认真生活 Take it easy.' \
  --width 1080 \
  --height 500 \
  --vitality alive-clean \
  --seed cover-001
```

未指定生命力时保持 `alive-clean`，不得自动降级。只需更强动作时使用 `freehand-max`。
