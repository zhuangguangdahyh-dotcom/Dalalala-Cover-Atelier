---
name: dalala-cover-009
description: 参考 009 的 3:4 真人近脸、多件同主题物件环抱、顶部弧字、右上短喊与下方两行阶梯花字封面。仅 studied，供拆解确认；不得自动推荐或生产。
---

# 参考 009 Cover Skill

从 `cover-skills/registry.json` 解析唯一原图 `参考封面图/dalala-cover-ref-009.jpg`，再读 [anatomy.json](references/anatomy.json)、[adaptation-rules.md](references/adaptation-rules.md)、[manifest.json](references/manifest.json) 和 [qa.md](references/qa.md)。本轮给用户确认的完整中文报告为 `skills/dalala-cover-009/references/adaptation-rules.md`。原图已无损保存于 `assets/reference-original.jpg`。

## 调用步骤

1. 确定行业、账号身份、主题、展示对象与可验证的数量关系。必须有一个近景可举的主对象和 3–5 个同主题、外形不同的子对象，以及能够自然同框的真人；不满足则拒用。
2. 固定 3:4。以左真人近脸、中央偏上的手举大物、周围小物和真实室内场景重建图片区域。保留双眼、主物表情及真实握持；不把物件摆成网格。
3. 文案分三层：顶部 6–10 字母的弧形语境词；右上 1–2 汉字加感叹标点的短喊；底部两行“数量/动作 → 对象/结果”阶梯式巨字。标题过长先改写，不能增行或压缩版式。
4. 从 `font-style-rules/registry.json` 调用测试态 `dalala-cover-009-puffy-pop`：主字用 `solid-display`，顶部用 `arc-outline`。透明字层逐字生成；粉边与黄影在合成时分层实现，不得静默改为普通圆体。
5. 依照 anatomy 的位置、面积、保护区、层级和阅读路径合成；按 qa 检查原尺寸与 360 px 缩略图。本 Skill 只有结构知识，尚无复刻测试与用户验收。`analysisConfirmed=false`、`renderAllowed=false`，不可 active。

## 固定机制与可变内容

固定：左贴脸人物、中央大物、3–5 个环抱小物、顶部弧字、右上短喊、下方两行阶梯巨字，及白芯/细暖色轮廓/右下硬影的字效与视觉层级。人物、文字、物件、具体颜色和真实场景可换，仍必须落入固定角色的位置、面积、角度和遮挡关系。色值调整只能重选颜色角色，不能改掉明暗结构和颜色面积关系。任何跨行业转换都先保持内容逻辑与可见证据，不生成通用 AI 小人。
