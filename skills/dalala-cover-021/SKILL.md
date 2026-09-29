---
name: dalala-cover-021
description: 参考 021 的 3:4 双景别纪实封面拆解；上方树荫街景远景、下方圆洞前近景，白色中英手写标题跨越硬切线。当前仅供拆解确认与受控测试。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 021｜调用规则

当前状态为 `studied`；拆解尚未经用户确认，`renderAllowed=false`。本 Skill 对应独立参考 021，**不等于** `layout-021`。不得进入自动推荐或正式生产。

1. 先查看 `assets/reference-original.jpg`，核对 `references/manifest.json` 的尺寸与 SHA-256，再读 `references/anatomy.json`、`references/adaptation-rules.md`、`references/qa.md` 及本次 `analysis.md`。原图可从 `cover-skills/registry.json` 追溯。
2. 接收行业、账号身份、主题、需要展示的人或对象、上远下近两幅真实或可信影像、准确中英文文案及平台。判断两幅影像是否讲同一件事；不能用两张无关好看照片拼版。
3. 固定 3:4 画幅、约 y46% 的水平硬切线、上方被空间框住的小主体和下方圆形建筑开口附近的近景主体。主标题在左侧跨接缝，右侧留人物脸；上暗绿中性、下高明度暖色的面积及对比关系要保留，具体颜色重新选。
4. 中文和拉丁标题均绑定测试态字体 `dalala-cover-021-story-hand` 的对应变体。按 `font-style-rules/registry.json` 加载独立 Font Skill，先核对文字和汉字结构，再单独生成透明字层。不可使用普通网页手写字体、旧的油漆体或不相干字体替代。
5. 先依据 `references/adaptation-rules.md` 做素材诊断、主题转换、图层计划和色彩角色分配；实际试作前使用项目封面设计流程完成可验证 `coverPlan`。本阶段只有模板解剖，无用户生产素材，不能放行渲染。
6. 用户确认拆解后，先做结构接近的复刻，再用不同业态且叙事自洽的主题测试。按 `references/qa.md` 检查原尺寸和 360 px 缩略图，并记录用户验收。未完成测试和验收时保持 `studied`。
