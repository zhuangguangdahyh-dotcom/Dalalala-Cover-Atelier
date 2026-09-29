# Dalala 生长行写体调用说明

## 入口

风格 ID：`dalala-growing-gel-xingshu`

默认生命力：`selective-growth`

生产渲染器：`imagegen-transparent-title-layer`

## 调用顺序

1. 从 `font-style-rules/registry.json` 解析本风格。
2. 加载 `style.json`、`STYLE_RULES.md`、提示词模板和确认样张。
3. 使用 `font_style.py plan` 为每个字符分配独立姿态，检查每个短语只有 1–2 个重点字。
4. 以确认样张为视觉基准，单独生成透明文字层。
5. 按 `VITALITY_QA.md` 检查文字准确、中性笔材质、选择性生长和缩略图可读性。
6. 通过后再与封面底图合成。

## 命令示例

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-growing-gel-xingshu \
  --text '认真生活 Write freely.' \
  --width 1080 \
  --height 500 \
  --vitality selective-growth
```

```bash
python3 font-style-rules/tools/font_style.py plan dalala-growing-gel-xingshu \
  --text '认真生活 Write freely.' \
  --width 1080 \
  --height 500 \
  --vitality selective-growth \
  --seed cover-001
```

未指定档位时保持 `selective-growth`。用户明确要求更强时可使用 `high-growth`，但仍不得让所有字符同时爆发。
