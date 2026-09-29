# 与 Cover Skill 051 的集成

Cover Skill 在 `fontDependencies` 的 `latinDisplayTitle` 和 `chineseDisplayTitle` 两个角色均指向 `dalala-cover-051-mint-freehand`。生产时分别生成透明层、逐字校验，再放到 anatomy 的两个边界内；颜色参数共用。叠加顺序为照片 → 英文字层 → 中文字层。若局部发丝穿过笔画，仅在设计证据充分时增加发丝局部前景蒙版，不改变人物身份或头发形状。

当前 registry 候选记录在封面目录 `references/font-registry-entries.json`，供服务端逐项登记；不要直接编辑共享字体注册表。通过真实复刻、跨内容标题与用户确认前保持 testing，且 Cover Skill 保持 studied。
