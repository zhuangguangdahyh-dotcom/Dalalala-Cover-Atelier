---
name: dalala-cover-053
description: 参考封面 053 的六格实拍、斜向撕纸主景、右侧人物与左下地点词构图。当前 studied，待拆解确认与真实内容测试。
---

# 参考 053｜调用说明

1. 先看 `assets/reference-original.jpg`；再读 `references/anatomy.json`、`references/adaptation-rules.md`、`references/manifest.json`、`references/qa.md` 和对应任务 `analysis.md`。这是独立参考，不按编号借用 `layout-053`。
2. 输入行业、账号身份、同一事件／地点的多张实拍、前景人物、主景物、次景物及准确地点短词。先判定内容能否组成一致的纪实叙事，再进入素材诊断；素材不足时不强行套版。
3. 按 `anatomy.json` 建立 3:4 画布与六格底图，分别处理主景斜纸片、左中宽纸片和人物纸片。保留事实锚点与人物身份，按规定占位、层级和撕边工艺组装。
4. 地点词绑定 `fontDependencies` 中的测试态罗马衬线依赖；只在拉丁词形验证范围内使用。单独输出透明文字层并逐字检查。中文主题尚需合格的中文字体测试，不能静默用普通宋体替换。
5. 当前 `renderAllowed=false`。先请用户逐项确认本次拆解；确认后用非原地点、非原人物的完整主题复刻并检查 360 px 缩略图。通过真实内容测试和用户验收后，才可申请上架状态。
