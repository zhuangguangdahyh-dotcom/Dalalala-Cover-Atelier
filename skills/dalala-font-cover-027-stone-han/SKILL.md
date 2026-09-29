---
name: dalala-font-cover-027-stone-han
description: 参考 027 巨幅浅暖做旧中文展示字的测试态字体依赖；仅输出准确透明字层。
---

# 参考 027｜矿物做旧中文测试字体

从 `font-style-rules/registry.json` 解析 `dalala-cover-027-stone-han`，读取本目录 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md`、`integration.md`。证据是 `../dalala-cover-027/assets/reference-original.jpg`；`approvedReference=null`，未获字体样张验收。

输入准确中文短标题、画布和目标盒，只输出真 alpha 字层。标准汉字笔画和部件结构优先，纹理只能在字内。两个点作为封面装饰在封面层绘制，不生成额外语义文字。保持 `testing`，禁止普通粗黑体加噪点静默替代。
