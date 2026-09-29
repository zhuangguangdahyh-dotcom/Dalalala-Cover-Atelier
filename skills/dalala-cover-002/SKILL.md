---
name: dalala-cover-002
description: 按参考 002 拆解规则执行单主体近景与超大衬线刊头的封面测试；仅用于该编号，待用户确认拆解后调用。
---

# 参考 002

状态 studied，版本 0.2.0；未验收、未上架、不得自动推荐。先读取 assets/reference-original.jpg、references/anatomy.json、references/adaptation-rules.md、references/manifest.json、references/qa.md。

输入：行业、账号身份、主题、真实主角素材、短刊头、三个辅助文字角色、3:4 画布及配色意图。缺少主体或标题时不能开始渲染。

依照 adaptation-rules 逐步诊断与重建；字体从注册表加载独立依赖，不在本 Skill 内复制字体规则。先确认最新拆解，再制作测试，后续测试与用户验收全部通过才可考虑 active。不得提前生成模板名称或前台推荐说明。

输出：coverPlan、测试成品、逐字与缩略图 QA、待用户确认的测试记录。当前仅有拆解文件，没有成品。

本轮中文拆解报告从 references/manifest.json 的 analysisReport 解析，路径相对 manifest 所在目录。先取得该最新报告的确认，不复用历史任务的确认。坐标为观察初值，真实面积与包围框不可混算。手掌框不包括出画的完整前臂，具体见 anatomy 的 fullForegroundArm。
