---
name: dalala-cover-044-blade-song
description: Testing-only heavy high-contrast Chinese Song display lettering with blade-like terminals and a soft offset shadow for cover 044.
---

# 044 刀锋重宋标题字体（测试态）

## 使用范围

仅服务 `dalala-cover-044` 的 `hookLead` 与 `answerTitle` 两个文字角色。先读 `references/style.json`、`references/style-rules.md`、`references/generation-prompt.md`、`references/vitality-qa.md`、`references/integration.md`，并观察 `../assets/reference-original.jpg` 的顶部两行。当前无独立获批字体样张，状态为 `testing`，不能称为已验收字体。

## 字形核心

每字保留可辨认的标准汉字结构，以重型展示宋体的横细竖粗、尖楔端部和局部刀锋伸出构成强势标题。字面实心，整体略有向右上生长的势能，但不旋转成逐字跳动的综艺字；成行后形成稳定的宽扁大块。字体只负责字形和字层效果；两行的具体位置、颜色角色和阅读路径由 Cover Skill 规定。

## 调用和验收

逐行输入经确认的准确中文，分别输出透明背景 PNG。主色与阴影分层，阴影右下偏移且柔和，不得用粗黑描边或外发光冒充。合成前逐字比对文本，确认引号成对、横画仍可见、刀锋未造成错字。再在 360 px 封面缩略图检查两行可读性与参考结构相似度。未通过则重做或人工复核，不替换为普通宋体。
