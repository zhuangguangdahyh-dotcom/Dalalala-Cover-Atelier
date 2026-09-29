---
name: dalala-font-cover-008-casual-hand
description: 参考 008 的细圆头随手写与粗圆笔结果标题的同家族测试字体。仅用于透明文字层试作，未通过样张和用户验收。
---

# 参考 008 手写字测试依赖

从 `font-style-rules/registry.json` 解析本项，读取 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md` 与 `integration.md`。源图为 `skills/dalala-cover-008/assets/reference-original.jpg`；`approvedReference=null`，不得把源图当已批准字样。

输入精确文字、`fine` 或 `display`、透明画布尺寸、字框、文字角色色。逐字生成并检查字符结构、混排字母和透明度；不输出人物、照片或封面底图。`fine` 用于右上三行与右中旁白，`display` 用于底部两行。字的右下硬色错位背影由 Cover Skill 合成，不在本字体透明层中预烘焙。状态 testing；禁止静默回退到普通圆体或别的手写字体。
