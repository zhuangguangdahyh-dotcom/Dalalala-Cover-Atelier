# 与封面集成

按 manifest 的 `fontDependencies` 调用；分别生成 prefix、mainTitle、四个 cardLabels 的透明层，再依 anatomy 坐标放入封面。先在 360 px 预览检查大标题，再放大逐字检查。该依赖只在服务端校验并登记测试条目后可用于复刻测试；用户确认前保持 testing。
