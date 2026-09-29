---
name: dalala-cover-023
description: 参考 023 的手持斜书页连续摄影、中央五组错位宽笔标题和编辑式辅助文字；小印章可替换可省略，仅供拆解确认及受控测试。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 023｜调用规则

版本 0.2.0；status=studied，analysisConfirmed=false，renderAllowed=false。只绑定 cover-skills/registry.json 中 dalala-cover-023，不映射 layout-023，不自动推荐、不正式生产。

1. 从注册表解析原图，查看 assets/reference-original.jpg；读取 references/manifest.json、anatomy.json、adaptation-rules.md、qa.md 和 `skills/dalala-cover-023/references/adaptation-rules.md`。本版依据前一版保留正确项并响应“小红印章不是固定的内容”。
2. 接收行业、账号身份、主题、手持阅读物件照片、准确八字主句、竖文、英文、真实署名和平台。先检查“阅读者—被阅读对象—主张”的同一主题关系。素材无法支持时换素材，不默认加书或通用 AI 人物。
3. 锁定 3:4 连续暗调近景摄影。保留斜向书页和手的真实接触。中央标题包络 x30–68%、y15–85%，分成 2／1／2／1／2，双字组内部逐字错位；左上三列不等长竖文、中左四行英文、右下短线署名。比例以 anatomy 为准，不靠几个固定坐标替代主题关系。
4. 小印章是可选辅助标记：内容、颜色、形状可替换，整枚可省略。保留时落在 x56–64%、y65–71% 的空档，包络面积不超过约0.6%；去掉后保持留白，不扩大标题、不加 CTA。不得强制红色、原章文或方形章式，不生成假认证。
5. 主标题绑定测试态 dalala-cover-017-journey-brush，读取其注册配置、提示词和 QA；复用须对照 023 原图证明，不符再建立此模板的独立字体能力。竖文、英文、署名分别绑定 dalala-cover-023-editorial-support 对应角色，不共享错误字骨。字体规则只由依赖定义；Cover Skill 管字框和层级。逐字准确生成真实 alpha 图层，禁止静默换普通字体。
6. 按 adaptation-rules 保护手、纸页透视和事实锚点，重裁、必要扩暗区或局部压暗；具体色值可变，明暗和视觉重量不变，强调色允许为零。新主题试作前完成 coverPlan 三层分析与设计决定，并用项目工具验证；最新拆解未确认时始终 renderAllowed=false。
7. 最新拆解经确认才进入受控复刻。做近原结构校验，再做不同业态且完整新主题的迁移测试；仅换名词不算通过。原尺寸与360px检查通过并获用户验收后才讨论升级。此阶段不编封面名称和前台说明、不标 active。
