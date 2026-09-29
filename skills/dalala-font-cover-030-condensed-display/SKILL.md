---
name: dalala-font-cover-030-condensed-display
description: 030 极窄工业重黑英文与浅灰透视环境字的测试态字体依赖，只生成可核字的透明文字层。
---

# 030 极窄工业展示字

从 `font-style-rules/registry.json` 解析 `dalala-cover-030-condensed-display`。读取本目录 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md` 和 `integration.md`。视觉证据是 `../dalala-cover-030/assets/reference-original.jpg`；`approvedReference=null`。此字体仍在 `testing`，不作为已验收风格自动投产。

接收准确文本和文字盒，按 `main-title`、`identity` 或 `environment` 变体分别生成真 alpha 文字层。先核对字母，再按封面要求进行空间透视合成。环境字也必须是准确的主题短词，不能生成伪字符。
