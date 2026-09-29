---
name: dalala-font-cover-025-arc-song
description: 参考 025 的弧形话题字和右侧高窄单字，测试态独立字体能力；只输出透明字层。
---

# 参考 025｜弧形话题字和右侧高窄单字

先从 `font-style-rules/registry.json` 解析 `dalala-cover-025-arc-song`，读取本目录 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md` 和 `integration.md`。样式证据为 `../dalala-cover-025/assets/reference-original.jpg`，`approvedReference=null`，原图不等于已复刻通过。

输入准确汉字、画布和每字目标盒；输出有真实 alpha 的独立字层。每字结构必须校对，失败时重做或人工复核，不能静默替换普通字体。状态 `testing`；原尺寸、360 px 缩略图和用户验收前不可升级。
