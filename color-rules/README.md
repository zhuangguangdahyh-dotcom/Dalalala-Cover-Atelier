# Dalala 长期配色资源库

本资源库把中国传统色作为可检索的颜色证据，并把配色从“好看的色块”转化为可执行的角色系统。

## 入口

```text
color-rules/registry.json
color-rules/tools/color_rule.py
```

数据锁定自 `nevertoday/zhongguo-traditional-colors` 提交 `57321fc69663bc0ea0cfa3376a9eed8b576ecd98`，包含 742 个命名色和 8,904 组和谐关系。

## 核心边界

- 构图、字体、配色分别选择。
- 模板参考中的具体色值不跟随模板永久复用。
- 先根据当前内容、素材和媒介选择锚点色，再建立背景、文字、辅助、主体支持、强调和功能色。
- 必须同时决定面积比例和对比度；只列 HEX 不算配色方案。
- 同一锚点色可以形成克制、文化、对比、年轻、技术或印刷等不同方案。
- 屏幕通过不代表印刷准确；物理成品必须校样。

## 命令

```bash
python3 color-rules/tools/color_rule.py search --query 月白
python3 color-rules/tools/color_rule.py get --color "月白"
python3 color-rules/tools/color_rule.py palette --color "月白" --strategy restrained --surface cover
python3 color-rules/tools/color_rule.py contrast --foreground "#1F1F1F" --background "#F9F4DC"
python3 color-rules/tools/color_rule.py validate
```

`palette` 返回候选角色方案，不替代对实际画面的取色、可读性检查和最终视觉复核。
