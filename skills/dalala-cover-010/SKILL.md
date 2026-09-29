---
name: dalala-cover-010
description: 参考 010 的 3:4 低彩户外摄影、上半幅双字锋利飞白、下半幅背向单主体与右伸主题物、极小暖色英文译注的独立 Cover Skill。当前 studied，仅供拆解确认与受控测试，不得自动推荐或生产。
---

# 参考 010 Cover Skill

唯一原图从 `cover-skills/registry.json` 的 `dalala-cover-010.reference` 解析；归档副本为 `assets/reference-original.jpg`。先看原图，再读 [anatomy.json](references/anatomy.json)、[adaptation-rules.md](references/adaptation-rules.md)、[manifest.json](references/manifest.json) 和 [qa.md](references/qa.md)。本轮中文逐项确认报告位于 `skills/dalala-cover-010/references/adaptation-rules.md`。

## 调用步骤

1. 判定行业、账号身份、当前主题和展示对象。需要能用两个汉字概括的身份/概念、一位单主体、一件与主题有真实关系的头肩附近物件，以及可以向右延展的真实形态。不能满足就拒用并说明缺少哪个素材条件。
2. 锁定 3:4。用连续摄影或可信合成建立上部低杂讯天空、中下部背/侧背人物、远山/地景和底部失焦前景。人物、道具、文字的外框与主次轴按 anatomy 执行；不能只保留同一张底图后移动标题。
3. 将主标题改写为优先两字的高信息词，英文只做短译名。上方白字是第一焦点，人物和右伸物件是第二焦点，小字是语义确认；不可扩为长副标题或第三行说明。
4. 从 `font-style-rules/registry.json` 分别加载测试态 `dalala-cover-010-ritual-brush` 与 `dalala-cover-010-italic-note` 的字体 Skill、字形规则、生成提示和 QA，依据参考原图生成独立的透明中文标题层与英文译注层。逐字检查中文及英文拼写，禁止静默使用普通书法体或 034 干刷字体。
5. 按 adaptation-rules 的 T0–T3 决定裁切、清理天空、扩图或重组；每项动作有内容理由。保留人物身份、产品结构、细羽/枝条边缘、光向、景深和遮挡。
6. 按 qa 在原尺寸与 360 px 缩略图检查。当前 `analysisConfirmed=false`、`renderAllowed=false`；仅允许研究和后续人工复刻测试。未完成跨内容测试与用户验收不得置为 `active`。

## 变量合同

人物身份/服装、具体主题词、道具品类、场景地点和具体色值可换；仍须进入模板规定的背向景别、位置、面积、向右延伸关系及层级。主标题的双字横展、上下视觉重量、低彩实景、极小暖色英文、飞白笔画类别和景深/光影关系不可变。禁止无内容理由的羽毛或神秘道具、通用 AI 小人、正脸大特写、纯色商品底、额外贴纸、普通字体回退。
