---
name: dalala-cover-061
description: 3:4 旧纸建筑招牌与黑白行业纪实照上下拼接，两行描边白色硬块巨字跨介质覆盖，底部单行行业判断。参考拆解测试态。
---

# 参考封面 061 Cover Skill

调用前依次读取 `assets/reference-original.jpg`、`references/manifest.json`、`references/anatomy.json`、`references/adaptation-rules.md` 和 `references/analysis.md`。本模板目前仅 `studied`，`renderAllowed=false`；先用于拆解核对，不得进入自动推荐或生产。待用户确认拆解后，仍须有原题近似复刻、跨行业新主题测试和最终验收。

## 调用流程

1. 明确行业、账号身份、主题判断、可展示的职业场景与历史/档案证据。判断照片中哪些人物、器具、建筑关系是事实锚点，哪些可裁切；没有可信现场素材时先补素材。
2. 在 3:4 画布建立上 53% 旧纸印刷招牌、下 47% 黑白纪实照片，双层黑框和右侧大黑剪影按 `anatomy.json` 约束配置。
3. 将新主标题改写成“上短下长”的两行，把上行压在旧纸黑影前，下行横压照片上部。主字层依赖 `dalala-cover-061-outlined-poster-block`，按角色单独生成透明文字层并逐字校对，不得以普通加粗黑体静默替换。
4. 上栏衬线英文与左侧三行分类依赖 `dalala-cover-061-archive-roman`，必须有真实语义；底部单行观点句依赖 `dalala-cover-061-verdict-han`，并与主标题形成因果延伸。按图层顺序合成，保留纸张、旧墨和黑白摄影差异。
5. 检查原尺寸和 360 px 缩略图：两行字、纸/照分界、右侧黑影、现场关系和底句仍可辨；逐项排除 `analysis.md` 的失败模式。

人物、文字、产品/器具、具体色值可变；构图、面积比、层级、上下介质、上短下长字块、字效类型与阅读路径锁定。跨比例需另建布局变体，禁止机械裁切。未完成模板/素材/主题/设计决策分析前，`renderAllowed` 一直为 false。
