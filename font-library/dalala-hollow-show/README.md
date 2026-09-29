# Dalala 镂空综艺体

这是封面工作台的第二套原创标题字体资源，字体 ID 固定为：

```text
dalala-hollow-show
```

它以粗镂空手写字为基础，重点保留真实书写者的速度、力度和临场决定。生命力来自每一笔不同的长短、粗细、角度、起收和连接方式，而不是给标准字体统一叠加粗糙滤镜。

## 当前版本

`0.2.0` 当前版覆盖：

```text
今 天 有 点 好 笑 这 也 太 离 谱 了 吧 的 不 ！
```

当前 TTF 适合风格验证和短标题试排。复杂字仍需在真实封面尺寸下继续检查和修正，未收录汉字不得混入普通字体冒充完整字库。

## 文件结构

- `sources/glyph-master-v02.png`：当前 4 × 4 独立字形生产母版，严格对齐确认样张的飞笔、急停和局部重压。
- `sources/glyph-master-v01.png`：已淘汰的首版母版，仅保留用于追踪风格偏差。
- `sources/glyphs/`：构建后生成的单字 PNG、SVG 和清单。
- `previews/approved-style-reference.png`：用户确认的最高生命力参考样张。
- `previews/font-render-proof.png`：由实际 TTF 渲染的回测图。
- `previews/expressive-layout-proof.png`：叠加动态综艺排版预设后的效果回测。
- `STYLE_SPEC.md`：字骨、笔画、镂空和排版规则。
- `EXPANSION_PLAN.md`：后续扩字顺序与生产流程。
- `glyph-set.json`：覆盖范围、字形状态和排版参数。
- `prompts/production-master-prompt.md`：生成独立字形母版的标准提示词。
- `scripts/build_font.py`：切字、矢量化、编译 TTF 并生成回测图。
- `scripts/render_expressive.py`：按单字大小、倾斜、基线和间距变化生成动态综艺排版。
- `layout-preset.json`：封面工作台调用时必须配套使用的排版参数。
- `dist/DalalaHollowShow-Regular.ttf`：可安装字体文件。
- `archive/v01/`：风格偏离的旧版字体和回测图，不用于工作台调用。

## 构建

在项目根目录执行：

```bash
.font-venv/bin/python font-library/dalala-hollow-show/scripts/build_font.py
```

## 使用规则

1. 只用于综艺感、娱乐化、情绪反应和轻松吐槽类短标题。
2. 默认单行 4–8 字；长句拆成两行，让字形有空间伸展。
3. 镂空内部允许显示底图，复杂背景应增加浅色承托或局部压暗。
4. 相同文案、作品 ID 和字体版本应得到相同的排版微调结果。
5. 遇到缺字进入扩字队列，不自动混入系统黑体。
6. 要复现确认样张的生命力，必须同时调用 `layout-preset.json`；只把 TTF 整齐排成一行会丢失原效果。
