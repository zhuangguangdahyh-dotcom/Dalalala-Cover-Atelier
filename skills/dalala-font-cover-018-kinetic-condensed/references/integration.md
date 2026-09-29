# 与封面 018 的集成

`upperHook` 和 `bottomTopic` 均依赖本字体规则，但文字框、上下字号比、出血、头发遮挡和图层顺序由 Cover Skill 018 的 `anatomy.json` 决定。先从 `font-style-rules/registry.json` 读取本规则，分别生成两张透明字层；不要把参考图的具体黄色固化进字体。当前无 `approvedReference`，只允许受控测试，不能标为可正式生产。
