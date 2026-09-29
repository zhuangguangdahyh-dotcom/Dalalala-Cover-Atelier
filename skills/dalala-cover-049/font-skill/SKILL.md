# 049 专属测试态字形 Skill

仅服务 `dalala-cover-049` 的英文双层标题。状态 `testing`，没有批准样张；不能进入正式生产。两个字体角色分别由 `references/style.json` 中 `dalala-cover-049-city-roman` 与 `dalala-cover-049-city-sans` 定义。以封面原图为视觉证据，不能复制原文。

输入精确文字、角色、目标字框、画布尺寸和颜色角色；按 `generation-prompt.md` 单独输出透明 RGBA 文字层，再合成到真实照片上。先逐字核对拼写、字形和字距，再按 `vitality-qa.md` 验收。字宽与字距须通过光学排版解决，不得机械横向缩放。中文主标题尚未测试，不得自动替换。
