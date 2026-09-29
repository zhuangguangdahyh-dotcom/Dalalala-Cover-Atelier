# 与 Cover Skill 014 的接口

从 `font-style-rules/registry.json` 解析本依赖与变体。Cover Skill 决定原文、各字块位置、面积和遮挡：`leadPossessive/methodLine→lead`，`coreTitle→core`，`rightTopic/resultLine→promise`。字体只输出文字透明层。合成时对字层添加短柔软的暗色局部影，核心词单独蒙版压在手机上边框前。状态 `testing` 且无已批准样张；失败时人工复核，不静默替换字体。
