---
name: dalala-font-cover-026-editorial-song
description: 参考 026 的端正宽展高对比中文展示宋字及其地点、章节、说明级差；测试态独立字体能力，只生成透明文字层。
---

# 参考 026｜中文编辑宋体测试依赖

从 `font-style-rules/registry.json` 解析 `dalala-cover-026-editorial-song`，读取本目录 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md`、`integration.md`。形态证据是 `../dalala-cover-026/assets/reference-original.jpg`；`approvedReference=null` 表示尚无复刻通过的字体样张。

输入准确中文字稿、画布和目标盒，按主标题、地点、栏目或说明角色输出独立真 alpha 文字层。必须保留标准汉字结构；普通宋体加粗或拉伸不能作为静默替代。状态 `testing`，原尺寸、360 px 和用户验收前不可升级。
