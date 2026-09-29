---
name: dalala-font-cover-036-condensed-cut
description: 参考 036 顶部主标题的双语极窄展示字测试依赖；分别生成 latin 与 cjk 透明单行文字层，保持高耸、强压缩、选择性刀切和清楚字骨。尚未获验收，不得回退普通窄体或机械压扁字体。
---

读取 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md` 与 `integration.md`。源证据由字体注册表 `sourceReference` 指向参考 036 原图。只迁移字形语言，不复制原题；状态 `testing`、`approvedReference=null`。按 `variant=latin|cjk` 单独生成逐字准确的透明文字层，再由 Cover Skill 组合；不能生成背景、人物、副标题或额外符号。
