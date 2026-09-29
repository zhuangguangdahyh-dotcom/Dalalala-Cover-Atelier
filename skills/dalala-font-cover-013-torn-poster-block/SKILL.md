---
name: dalala-font-cover-013-torn-poster-block
description: 参考 013 的逐字撕纸标题字骨测试依赖。生成厚重平切、局部漏墨的中文标题透明字层；状态 testing，无已批准样张，不得自动回退普通黑体。
---

# 参考 013 字体测试规则

先读 `references/style.json`、`style-rules.md`、`generation-prompt.md`、`vitality-qa.md`、`integration.md`，并以字体注册表 `sourceReference` 指向的参考 013 原图核对。输入为准确标题、字序、画布、标题区和颜色角色。逐字生成透明字层，不在字体层内生成撕纸、报纸、人物或背景；纸片形状与叠压由 Cover Skill 控制。每个字实例独立处理粗颗粒与边缘缺墨，不能六字机械复制同一磨损图案。

此依赖仅处于 `testing`，`approvedReference=null`，`productionApproved=false`。没有成功复刻并经用户确认时，不得宣称它是已批准字体，也不能静默换成 `dalala-hard-fold-heiti` 或系统粗黑体。
