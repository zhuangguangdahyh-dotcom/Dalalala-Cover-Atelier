---
name: dalala-cover-018
description: 仅用于参考018的原图拆解、确认与受控测试；按上方单行出血巨字、中央前倾近景、非对称现场道具、下方同色中英长条重建内容。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 018 调用协议

状态studied；analysisConfirmed=false、renderAllowed=false。未有成功测试或用户验收，不参与自动推荐与正式生产；不得与layout-018混用。

1. 先看assets/reference-original.jpg，读取references/anatomy.json、adaptation-rules.md、manifest.json、qa.md；中文确认报告为项目根目录下skills/dalala-cover-018/references/adaptation-rules.md。报告未确认时只允许分析，不渲染。
2. 判断行业、账号身份、主题、展示对象和现场事实锚点。抽取一个可近拍的清楚主角与同事件的左右次级道具。
3. 锁定上下单行巨字、上大下小、中央面部保护区、上字在头发后下字在衣服前、非对称前景及街景纵深。左手机原型完整入画，不能误写成两侧全部裁断。换人物、文案、产品、色值仍按anatomy的窄区间重建。
4. 执行adaptation-rules的素材诊断和T1–T2处理；仅相交头发需精细蒙版，换景才完整抠主体。右侧白衣归属未知，不虚构人物肢体关系。
5. 从font-style-rules/registry.json解析upperHook与bottomTopic的dalala-cover-018-kinetic-condensed测试态依赖，读取其完整规则；单独生成透明字层再合成弱偏移阴影。无批准样张，不静默替换普通字体。
6. 拆解确认后，按cover-design-rules/COVER_DESIGN_PIPELINE.md建完整coverPlan并用tools/cover_plan.py验证。真实主题、素材和设计决定缺失时renderAllowed保持false。当前工具只支持layout注册条目，不能为通过工具检查而选用无关layout编号。
7. 后续近内容复刻与跨行业真实主题迁移，按qa.md检查原尺寸和360px，保存实际结果与用户验收后再决定状态。未确认前不写模板名称/前台说明，不升级active。
