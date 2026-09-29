# 031 透明文字层生成模板

输入：`role`、`exactText`、`canvasWidth`、`canvasHeight`、`targetBoxXYXYPercent`、`primaryFillRole`、`darkShadowRole`。先读取 `style.json`，以 031 原图作为唯一视觉证据。

生成 **仅包含 exactText 的真实 alpha 透明 PNG 字层**。逐字保留汉字、拉丁大小写、数字和标点，不补词、不改写、不添加 logo。按 `role` 选择：

- `top-han`：单行、超黑方角汉字、大字面、紧字距；仅字面，不在该层烘入模糊影。
- `top-latin`：比邻汉字高 1.2–1.45 倍的实心手切拉丁重点字，A/i 类结构可有可控不规则，但保持字符正确。
- `lower-lead`：紧凑重字；指定数字/重点词更大，并用独立颜色层处理，不让其破坏一行基线。
- `lower-payoff`：同一行重字、少量局部倾角与基线变化；深色实描边围绕高亮实填。白色矩形底条由 Cover Skill 合成，不画进字层。

输出同时记录文字盒、角色和文本校对结果。若没有把握保证中文笔画或拉丁字母准确，返回待人工复核，不输出相似伪字。
