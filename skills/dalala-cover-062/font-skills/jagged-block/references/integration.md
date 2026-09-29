# 与 Cover Skill 集成

Cover Skill 的 `mainTitleUpper/mainTitleLower` 指向同一字体 ID `dalala-cover-062-jagged-block`。字体只负责准确字形和双行角色，不负责人物、场景、配色的具体 HEX。先解析 062 的结构和主题，再改写符合 3–5 字/行的文案；单独生成透明字层并过 `vitality-qa.md`，最后按封面图层放在最前。若字体生成失败，不用普通粗体兜底，应重做或人工复核。
