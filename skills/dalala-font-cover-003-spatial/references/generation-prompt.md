# 透明字层测试提示词

读取 style.json 与来源图，仅借鉴其中“顶部空间字”部分。准确生成输入的 {title}，保持 {canvasWidth} × {canvasHeight} 透明画布，使用 {textRole} 的颜色角色与规定文字框。遵守 style-rules.md，逐字保留汉字结构与标点，重复字也逐个检查。只输出文字及可拆分的字效，不生成照片、墙面或额外文案。尺寸、行数与位置从调用方的已确认 coverPlan 读取。测试结果须通过 vitality-qa.md，不得以提示词执行完成代替通过。
