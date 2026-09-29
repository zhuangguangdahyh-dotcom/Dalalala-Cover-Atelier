---
name: dalala-cover-022
description: 参考 022 的 3:4 真人教程封面拆解；上下两组手工切边粗字夹住正视人物和双手，右上有轻量说明。当前仅供人工确认与受控测试。
---

# 参考 022｜调用规则

状态 `studied`，拆解待确认，`renderAllowed=false`。本 Skill 只对应注册表 `dalala-cover-022`，不是 `layout-022`，不得用于自动推荐或正式生产。

1. 先看 `assets/reference-original.jpg`，核对 `references/manifest.json` 的尺寸与哈希，再读 `references/anatomy.json`、`references/adaptation-rules.md`、`references/qa.md` 和 manifest 指向的本次 `analysis.md`。本版按“注意文字的图层顺序”修订；旧版笼统的遮挡描述以本版为准。
2. 输入行业、账号身份、主题、真实或可信人物照片、主标题上段、底部结果词、副标题、平台。先判断主题是否适合真人讲解与完整流程承诺；不要默认生成通用 AI 小人。
3. 锁定 3:4：上方白色粗字横贯 x2–96%、y3–22%，右上轻注释 x55–94%、y22–27%，中间脸与双手，底部暖亮粗字 x3–97%、y73–94%。上字只贴近发顶、不压脸；细注释在头发右侧暗区；底字是盖在下段袖子、前臂、胸腹和沙发上的最终前景，双掌主体留在字框上方。身体从底边出画，人物与背景须保持实拍空间关系。
4. 主要中英文字依赖测试态 `dalala-cover-022-cut-display`；副标题依赖测试态 `dalala-cover-022-casual-note`。从 `font-style-rules/registry.json` 解析规则和来源参考。先逐字核对，再分别生成真正透明的字层；每组软影在本组实体字之下，影和字均在照片及人物之上。按照 `references/anatomy.json` 的 `layerOrder` 合成，不抠手掌到黄字上方，不把所有字与影合并为不可控的一层。不得静默换普通黑体、普通手写体。
5. 具体色值可按品牌和素材调整，保留暗中性照片、上方近白、下方暖亮、自然肤色的面积和对比。按 `references/adaptation-rules.md` 诊断素材和内容；正式试作前形成完整 `coverPlan` 并通过项目的 plan 验证。
6. 用户确认拆解后，先试近原主题，再试不同业态但动作和承诺成立的完整新主题。依 `references/qa.md` 检查原尺寸及 360 px 缩略图，记录真实结果。未经过跨内容测试和用户验收，不得提升到 `active`。
