# 接入

从 `font-style-rules/registry.json` 按 `dalala-cover-012-power-oblique` 解析资源。输入 `text`、`variant`、画布尺寸、`textBox` 与 `colorRoles`；输出一张完整透明文字层。

- `headline`：Cover Skill 传入数字、中文、拉丁三段及其颜色角色，字体依赖负责同字族骨架、相对高度、斜度、紧配和单个星芒。
- `banner`：只输出稳定的深色中文透明层；Cover Skill 负责亮色圆角底板、内边距和整组 4°–6° 旋转。
- `card-label`：只输出编号和短类别名透明层；Cover Skill 负责黄色等强调角色的标签底板与卡片位置。

字体不控制封面构图，也不绑定具体 HEX。当前状态 `testing`、`approvedReference=null`；完成独立样张、整版复刻、360 px QA 和用户确认前不得改为 active。
