---
name: dalala-cover-011
description: 参考 011 的拉链近景开口、人物双手前探、双组斜排厚块红字与右侧小注的 3:4 独立 Cover Skill。当前 studied，供拆解确认与后续受控复刻测试，不供前台自动推荐。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 011 Cover Skill

先从 `cover-skills/registry.json` 的 `dalala-cover-011.reference` 解析并查看原图；归档副本为 `assets/reference-original.jpg`。随后读取 [anatomy.json](references/anatomy.json)、[adaptation-rules.md](references/adaptation-rules.md)、[manifest.json](references/manifest.json) 和 [qa.md](references/qa.md)。本轮中文人工确认报告为 `skills/dalala-cover-011/references/adaptation-rules.md`。

## 调用顺序

1. 判断行业、账号身份、主题、要揭示的对象，以及能否找到有因果关系的开口物、人物/主角、近距动作和简净内景。缺少真实动作关系时说明不适用，不能默认放通用 AI 小人。
2. 锁定近 3:4 画布。按 anatomy 建立不规则暗色近景开口、可见边缘细节、亮色内景、中下部前探人物、近手透视、左侧两组斜排主标题及右侧极小注脚。改变行业素材时必须同时重建裁切、主体位置、开口形状、遮挡和阅读路径。
3. 根据 adaptation-rules 选择素材处理等级。身份、产品结构和真实手物接触是事实锚点；可调整背景、服装、色值、标题内容与开口对应材料。任何抠图、扩图、换景、透视调整均记录内容理由。
4. 主标题依赖 `font-style-rules/registry.json` 中测试态 `dalala-cover-011-diagonal-block`。从其 Font Skill 读取字形与透明层合同，逐字生成上组和下组；右侧窄身栏目词和细注脚依赖 `dalala-cover-011-editorial-condensed`。栏目词必须完整，细注脚仅非关键信息末端可越过右边。不得用普通黑体斜转替代，不在 Cover Skill 内复制字形规则。
5. 依据当前素材重新分配色彩角色：大面积低明度外框、高明度内景、中暗主体、两处受控高饱和焦点与极小暗色注脚。只锁关系与面积，不锁原图具体 HEX。
6. 按 qa 检查原尺寸和 360 × 480 缩略图。现阶段 `analysisConfirmed=false`、`renderAllowed=false`；尚无复刻与跨内容测试，不能自动生产、命名或发布为 `active`。

## 变量合同

人物身份/造型、主题短词、行业相关开口材料、真实产品或工具、具体配色可变；每个替换项仍进入参考约定的位置、面积、角度、透视与前后关系。构图骨架、内容画面占比、拉链式边缘细节与近手遮挡、斜排主标题和两级小注不可自由改动。若行业开口不一定有拉链，应保留连续可辨的真实边缘构造与“被打开”的动作；此替换须先通过跨内容测试，不能在当前阶段认定为正式变体。
