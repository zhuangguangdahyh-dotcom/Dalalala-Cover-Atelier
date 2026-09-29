---
name: cover-design-reference
description: 将排版图鉴和传统配色参考转译为 AI 封面工作台的固定 Cover Skill 规则。用于参考拆解、模板创作和规则审查；客户生成时保持已发布模板的构图、字体与色值。
---

# 封面设计参考转译

用于创建或审查 Cover Skill。读取 [reference-guide.md](references/reference-guide.md) 了解来源、图文错配和适配边界。

## 工作流程

1. 读取目标 Cover Skill 和用户参考，先识别固定构图、阅读顺序、主体区域、文字层级、字体与色彩角色。
2. 优先从 `../../layout-rules/registry.json` 发现可用规则，使用 `../../layout-rules/tools/layout_rule.py` 按 ID、名称或内容条件调用。原始 `references/layout-catalog.json` 只作为来源元数据。
3. 加载对应独立规则和本地缩略图。目录名称只能作为检索提示，不是图片语义的证明；已知错配规则不得自动选择。
4. 将参考拆成 Locked / Adaptive / Optional 三类。每一条可执行规则明确目标图层、数值范围、单位、失败处理和验证方法。坐标使用 0–1；文字测量使用实际加载字体。
5. 固定阅读顺序与对齐轴线；留白区域作为不能被内容挤占的区域。将文字适配限定为事实不变的重写、换行和有限字号调整。不能为放下长文改变主体左右关系。
6. 需要传统配色时使用已安装的 `xxd-palette-builder`、`xxd-palette-applier` 和 `xxd-accessible-color`。这些工具用于设计阶段；已锁定参考色不强制映射为传统色，不允许自动换色修复已发布模板。
7. 将选定配色落实为 background / primaryText / secondaryText / accent / highlight 的精确 HEX、使用图层、可用面积或次数、允许的变体 ID。只开放 Skill 声明的变体，不开放随机配色。
8. 区分程序 QA 与视觉 QA：程序检查边界、字数、字体、色值和碰撞；视觉检查主体完整、第一眼焦点、缩略图可读性和参考一致性。照片上的文字需检查实际背景，不能只测纯色背景的色差。
9. 用短标题、长标题、混排数字、缺失可选字段、不同素材和冲突要求验证。失败记录具体原因，不冒充已通过，不自动放宽锁定项。

## 输出

输出目标 Skill 的规则修改建议或配置草案、来源与核验状态、适配边界、QA 项目。参考图鉴不是完成的 Cover Skill，不用其编号替代用户的 cover-NNN 编号。

同内容换模板时始终从原始内容重新适配，保留用户事实和素材身份。跨比例用明确布局变体，不能依靠拉伸或翻转核心构图。
