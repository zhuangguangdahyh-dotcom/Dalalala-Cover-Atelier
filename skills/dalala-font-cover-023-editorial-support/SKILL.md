---
name: dalala-font-cover-023-editorial-support
description: 参考 023 的竖排宋体、四行大写衬线英文和小型书写署名的独立测试态字体能力。
---

# 023 辅助字形测试依赖

先查看 `../dalala-cover-023/assets/reference-original.jpg`，读取 references/style.json、style-rules.md、generation-prompt.md、vitality-qa.md 和 integration.md。接收角色、准确文案、画布与文本框，分别生成透明字层。字体能力只管字骨；不改 Cover Skill 的坐标、行列和层级。不生成印章。状态 testing，approvedReference=null，productionApproved=false；实际字体匹配、字形和 alpha 须测试，不自动用于生产。
