# Dalala 封面字体资源库

## 历史字体资产

### 1. Dalala 松弛油漆体

- 字体 ID：`dalala-songchi-paint`
- 目录：`dalala-songchi-paint/`
- 方向：宽刷油漆、松弛字骨、干刷缺墨。
- 状态：已归档的固定字体原型，只保留作失败对照。
- 替代方案：正式封面必须调用 `../font-style-rules/dalala-living-paint/`，每个字符实例逐字重画。

### 2. Dalala 镂空综艺体

- 字体 ID：`dalala-hollow-show`
- 目录：`dalala-hollow-show/`
- 方向：粗镂空手写、综艺娱乐、强活人生命力。
- 状态：`0.2.0`，已按确认样张重建 TTF，首批覆盖 15 个汉字与全角感叹号。
- 角色：辅助预览字体。正式封面优先调用 `../font-style-rules/dalala-hollow-show/` 的生成式规则。

## 通用规则

- 每套字体都必须保留风格规范、独立字形母版、覆盖清单、扩字计划、构建脚本和真实字体回测图。
- 缺字进入对应字体的扩字队列，禁止用普通系统字体静默补齐。
- 概念样张只用于确认方向，只有独立字形母版生成并通过 TTF 回测后，才能标记为可用字体资源。
- 具有强动态生命力的风格，以 `font-style-rules/registry.json` 为主入口；固定字体文件不能替代逐字生成和动态排版。
