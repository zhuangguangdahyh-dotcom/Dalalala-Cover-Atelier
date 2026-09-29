---
name: dalala-font-cover-031-punch-display
description: 031 顶部黄黑重展示字、放大手切拉丁强调词和左下两级结果字的测试态字体依赖；生成准确透明字层。
---

# 031 强冲击展示字｜测试态

从 `font-style-rules/registry.json` 解析 `dalala-cover-031-punch-display`，依次读取 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md` 与 `integration.md`。字形证据是 `../dalala-cover-031/assets/reference-original.jpg`。`approvedReference=null`，用户尚未批准字样；此依赖不得自动投产。

输入准确文案、角色、画布尺寸和文字盒。按 `top-han`、`top-latin`、`lower-lead`、`lower-payoff` 分别生成真实 alpha 文字层；影子、白底条和卡片遮挡在封面合成时按角色添加。逐字核对汉字、英文字母与数字；有误或失去原图字骨时重做/人工复核，不以普通粗黑体静默兜底。
