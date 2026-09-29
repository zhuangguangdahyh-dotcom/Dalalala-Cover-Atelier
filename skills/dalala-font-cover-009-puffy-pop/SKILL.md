---
name: dalala-font-cover-009-puffy-pop
description: 参考 009 的测试态软厚圆花字与空心英文拱弧。只生成透明字层；未经样张和用户验收，不用于正式生产。
---

# 参考 009 字体测试依赖

从 `font-style-rules/registry.json` 解析本项，读 [style.json](references/style.json)、[style-rules.md](references/style-rules.md)、[generation-prompt.md](references/generation-prompt.md)、[vitality-qa.md](references/vitality-qa.md)、[integration.md](references/integration.md)。视觉证据是 `skills/dalala-cover-009/assets/reference-original.jpg`，它不是已批准字样；`approvedReference=null`。

输入精确文字、变体、透明画布、字框及文字角色色。`solid-display` 用于右上短喊和底部两行，`arc-outline` 用于顶部英文拱弧。仅生成文字 alpha 层，逐字检查；粉色窄边和黄色右下硬影由 Cover Skill 分层合成，不在字芯层预烘焙。禁止静默替换为普通圆体或通用卡通字。状态 testing。
