---
name: dalala-cover-050
description: 参考 050 的四角单字、中心暖调肖像封面拆解与受控复刻。当前仅 studied，待用户确认拆解和跨内容测试。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 050｜调用顺序

1. 先看 `assets/reference-original.jpg`，读取 `analysis.md`、`references/anatomy.json`、`references/manifest.json`、`references/adaptation-rules.md` 和 `references/qa.md`。这是独立参考，不按编号映射 layout-050。
2. 输入行业、账号身份、主题、展示对象、可用肖像、四字命题及账号署名。先判断四字是否真构成完整问题或概念，再按适配规则诊断肖像和背景。无合适单人近景时停止选用。
3. 读取 `fontDependencies`；四角主字使用本模板测试态 Font Skill，不能以普通宋体、书法刷字或其他模板字体静默代替。底部署名为可选账号标记，不复制原图字样。
4. 依据 `invariantContract` 建立 coverPlan：固定四角各一字、中心人像、暖暗背景、明亮文字和角字在前景的空间骨架。可改人物身份、具体文案、服装/小配饰和具体色值；不能改变字块面积、肖像景别、阅读路径及效果类型。
5. 本阶段只供人工审阅规则。`renderAllowed=false`；报告经用户确认后才能复刻测试。测试须用另一行业的完整四字主题和不同人物，检查 360 px 缩略图、逐字准确性及人物身份，用户验收前不得上架或设为 active。
