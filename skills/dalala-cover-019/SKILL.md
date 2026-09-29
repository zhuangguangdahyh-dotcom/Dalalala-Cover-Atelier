---
name: dalala-cover-019
description: 参考 019 的竖版双语巨字与主题场景封面规则。拆解修订待确认，仅供受控测试。
---
> 公开安装版当前状态：此模板已验收上架，可以制作。以 `cover-skills/registry.json` 与本机模板目录为准；下文历史拆解阶段的 `studied`、`testing`、未验收或 `renderAllowed=false` 字样不构成当前调用禁令。视觉参考已替换为已验收展示样张，仍须执行质量检查。


# 参考 019｜调用协议

当前 `testing` 且拆解待重新确认；`analysisConfirmed=false`、`renderAllowed=false`。本 Skill 只描述参考结构和后续复刻方法，不是 `layout-019`，也不是可自动推荐的正式模板。

1. 先看 `assets/reference-original.jpg`，再读 `references/anatomy.json`、`references/adaptation-rules.md`、`references/qa.md`、`references/manifest.json` 及当前 `skills/dalala-cover-019/references/adaptation-rules.md`。原图哈希应与 manifest 一致。
2. 接收行业、账号身份、主题、展示对象、准确拉丁短词与中文短词、平台和候选素材。先判断内容逻辑，再挑图。海湾、钟楼、红瓦、船只只是来源图中的实例，不是生成提示词的必带元素。
3. 锁定 3:4 画幅与空间语法：上方低纹理承字面；单行高瘦前倾拉丁大字横贯 x10–93%、y6–19%；右上直立厚块中文 x59–90%、y22–35%；中下某一侧为可辨认主题证据，另一侧为连续安静展开面；真实边界或透视线把目光带向下方。图像不是固定底图换字。
4. 按 `references/adaptation-rules.md` 将素材拆成事实/身份锚点与可改造区。优先选择自身具备该空间关系的照片或内容合理的场景；必要时重裁、扩出文字承接面、清理干扰或做局部影调。人物、产品、建筑、品牌等锚点保持真实可信。若无法满足画面关系，判为不适配并改选素材/模板。
5. 分别从 `font-style-rules/registry.json` 加载测试态 `dalala-cover-019-latin` 和 `dalala-cover-019-han`。依各自 Font Skill 生成真正透明的文字层；前者核验高瘦前倾与边缘切口，后者核验方硬厚块与标准汉字结构。字层逐字正确后，再按当前素材选择明度与色温角色并合成；不得静默改用普通字体。
6. 在用户确认拆解、提供新主题与素材后，按项目 `cover-design-rules/COVER_DESIGN_PIPELINE.md` 建立完整 coverPlan，验证模板、素材、主题和配色。先做近结构试作，再做不同内容的迁移试作，检查原尺寸及宽 360 px 缩略图，记录用户验收。所有门槛未过时继续保持测试态，不升级为 `active`。

## 变量合同

人物、产品、文字内容、具体颜色和具体场景可变，但都必须回到 `references/anatomy.json` 的角色、位置、面积、层级和方向关系。版式、双语字块的等级、上静下实与一侧密一侧疏的画面骨架、低强度字效不可变。英文超长或中文超过短词容器时先改写准确短名；无法改写就换模板。
