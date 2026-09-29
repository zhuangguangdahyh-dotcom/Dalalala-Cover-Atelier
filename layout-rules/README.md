# Dalala 350 独立排版规则库

这里是 Dalala 可跨项目复用的排版知识库。它收录用户最初提供的 `350-layout-compositions` 固定版本，包含 350 张本地视觉参考、350 份独立规则和 350 份构图知识文件。

14 张总览图位于 `references/contact-sheets/`，用于快速浏览全部参考；单条规则始终加载自己的 `references/source-thumbnails/XXX.jpg`。

## 唯一入口

```text
layout-rules/registry.json
```

工作台不得扫描图片目录猜测规则，也不得把多个编号自由混合。先选择一个 `layout-XXX`，再只读取该规则的 Locked / Adaptive / Optional 合同。

构图名称和几何机制不足以直接生成封面。正式渲染还必须读取该规则的 `knowledge/layout-XXX.json`，获得原理、适用内容、主体、主标题、副标题、辅助信息、装饰位、受保护留白、素材处理方式和失败条件。只有来源视觉核验与知识建模都完成的规则才会标记为 `renderReady: true`。

## 三种调用方式

按编号读取：

```bash
python3 layout-rules/tools/layout_rule.py get layout-013
python3 layout-rules/tools/layout_rule.py get 013
```

按中文全名读取：

```bash
python3 layout-rules/tools/layout_rule.py get 负空间构图
```

让工作台自动推荐：

```bash
python3 layout-rules/tools/layout_rule.py select \
  --intent "心理咨询师人物封面，需要留白和信任感" \
  --asset-type photo \
  --title-length medium \
  --subject-count 1 \
  --ratio 3:4 \
  --limit 8
```

自动推荐只返回候选和理由。选定后锁定一个规则，不能在生成阶段让 AI 自由拼装。

`get` 的输出会同时返回 `compositionKnowledge`。其中的内容用于候选判断和模板解剖；生成前仍需针对用户的真实素材完成一次具体素材诊断与主题设计。

## 封面分析单

平台画幅、素材诊断、主题分析与最终设计决策使用：

```bash
python3 cover-design-rules/tools/cover_plan.py canvas --platform 小红书

python3 cover-design-rules/tools/cover_plan.py new \
  --layout layout-013 \
  --platform 小红书 \
  --topic "真让人头大" \
  --title "真让人头大" \
  --asset /absolute/path/to/image.jpg \
  --output /absolute/path/to/cover-plan.json
```

新建分析单默认 `renderAllowed: false`。完成模板、素材、主题和设计四部分后运行 `validate --stage plan`，全部通过才允许合成；完成实际成图 QA 后运行 `validate --stage release`，通过后才允许交付。

## 规则层级

- `source`：固定来源、版本、原图路径、哈希和本地缩略图。
- `selection`：适合的素材、标题长度、主体数量、画幅和检索标签。
- `compositionKnowledge`：为什么这样排、什么时候使用、内容组成、素材重构、文字策略和失败条件。
- `layoutContract.locked`：主轴、焦点、阅读路径、主体关系和留白，不能自由改变。
- `layoutContract.adaptive`：标题、素材裁切、字体风格和已批准配色。
- `layoutContract.optional`：副标题、角标等可选层。
- `qa`：程序与人工验收门槛。

## 来源错配处理

原仓库固定版本中存在大面积文件名、目录名称与图片内标题不一致。350 张原图经哈希核对后，发现上游目录名称与画面可见标题有 336 条不一致。本库按以下方式修正：

- `visual-truth-catalog.json` 记录画面中真正显示的概念名称，是规则编号和选择逻辑的唯一名称依据。
- `source.catalogClaim` 保留上游目录原本声称的名称，仅供追溯，不能参与自动选择。
- `references/source-mapping.json` 保存原图路径、SHA-256 和本地参考哈希。
- `references/legacy-misaligned-thumbnails/` 保存修正前的错位版本，工作台不得调用。
- 350 条来源参考已按视觉真值重新绑定。来源本身全部有效；`renderReadyCount` 只统计已经完成本地深度解剖和可执行蒸馏的条目，禁止为了数字好看把粗分类标成已掌握。

来源核验解决“这张图到底在讲什么”；真实内容测试仍决定某条规则是否晋升为经过用户审美确认的固定 Cover Skill。

## 验证

```bash
python3 layout-rules/tools/layout_rule.py validate
```

验证必须确认 350 个规则文件、350 张参考、350 个知识文件、文件哈希和规则合同全部存在。
