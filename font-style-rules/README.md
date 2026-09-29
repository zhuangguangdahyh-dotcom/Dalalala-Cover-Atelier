# 封面文字风格规则库

这里保存封面工作台可直接发现和调用的生成式字体规则。规则控制字骨、笔画、轮廓、生命力、逐字排版和 Imagegen 提示词。`dalala-living-paint` 不使用固定字体文件，每个字符实例都单独重画。

## 唯一入口

```text
font-style-rules/registry.json
```

工作台不得扫描目录猜测可用风格，只读取注册表中的 `styles`。
未指定风格时读取 `defaultTitleStyleId`。历史 ID 和中文叫法通过风格条目的 `aliases` 路由到正式规则。

## 调用示例

列出所有风格：

```bash
python3 font-style-rules/tools/font_style.py list
```

读取完整机器配置：

```bash
python3 font-style-rules/tools/font_style.py get dalala-living-paint
```

为生命油漆字生成逐字符实例计划：

```bash
python3 font-style-rules/tools/font_style.py plan dalala-living-paint \
  --text "选准心理咨询师，先看看这4点" \
  --vitality alive-max \
  --width 768 --height 1024 \
  --seed "cover-001-title-v1"
```

生成可直接交给 Imagegen 的提示词：

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-hollow-show \
  --text "这也太离谱了吧！" \
  --vitality alive3x \
  --width 1080 \
  --height 1440
```

生命油漆字使用 `dalala-living-paint`，默认生命力为 `alive-max`。旧的 `dalala-songchi-paint` 字体文件已经归档，不得用于工作台标题渲染。

验证注册表、文件和提示词变量：

```bash
python3 font-style-rules/tools/font_style.py validate
```

## 新增风格

每套风格至少包含：

- `style.json`：机器可读参数与 QA 条件。
- `STYLE_RULES.md`：供人和 Codex 阅读的完整风格说明。
- `VITALITY_QA.md`：生命力硬门槛与 100 分验收标准。
- `INTEGRATION.md`：工作台输入、输出、失败处理和调用示例。
- `prompts/imagegen-title-layer.md`：运行时提示词模板。
- `references/approved-reference.*`：用户明确确认的主正向样张。
- 注册表记录：固定 ID、版本、状态和上述路径。
