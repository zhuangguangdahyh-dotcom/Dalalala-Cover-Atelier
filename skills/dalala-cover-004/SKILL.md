---
name: dalala-cover-004
description: 按参考 004 重建低机位近镜动作、双字错位且人物遮字的封面；当前仅供拆解确认与后续授权测试，禁止自动推荐或上架。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 004

状态 studied，版本 0.1.0，analysisConfirmed=false，renderAllowed=false。

1. 读取 references/manifest.json、anatomy.json、adaptation-rules.md、qa.md 及 assets/reference-original.jpg。唯一参考是本模板，不混用其他版式。
2. 先核验最新拆解确认。当前报告位于 skills/dalala-cover-004/references/adaptation-rules.md；未确认时仅允许审阅和修正规则。
3. 收集行业、身份、主题、双字标题、素材和事实锚点。执行 adaptation-rules 的语义转换和素材改造，按 anatomy 的空间区间规划。
4. 从 font-style-rules/registry.json 解析 mainTitle 的 dalala-cover-004-smooth-hand；读取其 config、humanRules、promptTemplate、vitalityQA 与 sourceReference。approvedReference 当前为空，不得声称已验收。
5. 形成 coverPlan，缺当前内容/素材时保持 renderAllowed=false。使用 cover-design-rules/tools/cover_plan.py validate 检查；分析确认与测试授权是额外门槛，验证器通过不代表发布批准。
6. 测试时先建立真实动作底图，再生成透明汉字图层，最后主体蒙版遮字；具体字形不在本 Skill 复制，由字体依赖维护。
7. 检查原尺寸与 360 px 缩略图、标题逐字正确、身体连续、空间骨架、图层关系与跨行业语义。记录真实结果，不填虚假通过。
8. 只有复刻、跨内容测试和用户最终验收后，另行执行上架；本版本不能发布 active，也不提供封面名称或前台推荐说明。
