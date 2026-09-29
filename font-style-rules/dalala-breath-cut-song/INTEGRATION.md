# 工作台接入协议

## 固定标识

```text
styleId: dalala-breath-cut-song
displayName: Dalala 呼吸切锋宋体
defaultIntensity: editorial
```

## 调用

```bash
python3 font-style-rules/tools/font_style.py prompt dalala-breath-cut-song \
  --text "高级感不必大声" \
  --vitality editorial \
  --width 1080 \
  --height 1440
```

工作台必须加载 `style.json`、提示词模板、确认样张和 `VITALITY_QA.md`。输出透明 PNG 文字层，并记录风格版本、原文、强度档位、文件路径、QA 分数和审核状态。

## 失败处理

- 不是现代宋体骨架：风格失败。
- 每字超过两处设计动作：退回重生成。
- 切口随机、断裂过多或出现故障感：退回重生成。
- 简约高级感不足或 QA 低于 85 分：针对最低分维度重生成。
- 连续三次失败：进入人工复核，不替换成普通宋体交付。

