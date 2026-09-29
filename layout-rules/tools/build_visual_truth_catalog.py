#!/usr/bin/env python3
"""Rebuild the catalog from titles visibly present in the 350 reference images."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_CATALOG = PROJECT / "skills/cover-design-reference/references/layout-catalog.json"
MAPPING = ROOT / "references/source-mapping.json"
OUTPUT = ROOT / "visual-truth-catalog.json"


NAMES = """
三分法构图
黄金比例构图
黄金螺旋构图
黄金三角构图
对角线法
矩形折入法
奇数法则
空间法则
视线空间
运动空间
头部空间构图
填满画面构图
负空间构图
框中框构图
引导线构图
居中构图
偏心构图
对称构图
非对称构图
镜像构图
放射平衡
晶体式平衡
静态构图
动态构图
开放式构图
封闭式构图
单一焦点构图
多重焦点构图
视觉层级
主次关系
平衡
比例
尺度对比
明暗对比
色彩对比
形状对比
质感对比
动静对比
并置
隔离构图
重复原则
图案组织
节奏组织
渐变组织
交替节奏组织
渐进节奏组织
流动节奏组织
随机节奏组织
相似性原则
邻近性原则
水平构图
垂直构图
对角线构图
平行线构图
汇聚线构图
交叉线构图
中轴构图
偏轴构图
双轴构图
十字构图
X 形构图
T 形构图
L 形构图
V 形构图
Z 形构图
C 形构图
S 形构图
曲线构图
波浪形构图
锯齿形构图
三角构图
金字塔构图
倒三角构图
菱形构图
方形构图
矩形构图
圆形构图
椭圆构图
弧形构图
环形构图
螺旋构图
放射式构图
向心式构图
离心式构图
同心式构图
四象限构图
棋盘构图
阶梯构图
层叠构图
级联构图
聚类构图
分散构图
尺度递减构图
前景框架构图
一点透视
重叠空间构图
前景框架构图
线性透视
网络构图
前中后景构图
两点透视
三点透视
平行透视构图
斜投影构图
等距构图
轴测构图
鸟瞰构图
虫视构图
顶视构图
平视构图
竖排文字排版
横排文字排版
手稿网格
分栏网格
模块化网格
层级网格
基线网格
复合网格
非对称网格
方格网格
轮廓绕排
矩形绕排
跨栏标题
悬挂缩进
首行缩进
凸排标点
基线对齐
形状文字
图形诗排版
路径文字
强制透视构图
空气透视构图
浅景深构图
深焦构图
平面化构图
深空间构图
轴线系统
放射系统
扩张系统
随机系统
网格系统
模块系统
过渡系统
双边系统
左对齐右参差
右对齐左参差
居中排版
两端对齐
强制两端对齐
非对称字体排版
单栏版式
对称跨页
通版跨页
双栏版式
图片主导版式
无出血版式
非对称跨页
文字主导版式
满出血版式
多栏版式
方格网格
模块化网格
非对称网格
手稿网格
层级网格
分栏网格
基线网格
水平文字排版
复合网格
垂直文字排版
等距网格
放射网格
极坐标网格
嵌套网格
子网格
固定网格
流体网格
响应式网格
破格网格
解构网格
大标题版式
图片窗口版式
框架版式
多面板版式
蒙德里安版式
马戏团版式
剪影版式
字母造型版式
图文谜语版式
拼贴版式
蒙太奇版式
模块化页面
区块式版式
插页式版式
侧栏版式
边注版式
环绕图版式
浮动块版式
封面版式
章节扉页
弹性盒布局
网格布局
子网格布局
多栏布局
表格布局
浮动布局
相对定位布局
绝对定位布局
固定定位布局
粘性定位布局
瀑布流布局
覆盖层布局
固定宽度布局
流体布局
响应式布局
自适应布局
容器查询布局
堆栈
盒子
居中器
簇群
侧栏原语
切换器
封面原语
自适应网格原语
比例框
水平滚轴
悬浮层
图标文字组合
单列页面
双列页面
三列页面
侧边栏页面
分屏布局
圣杯布局
页眉—主体—页脚
顶部导航布局
导航抽屉布局
底部导航布局
标签页布局
栏目开启页
特写跨页
目录版式
索引版式
图录版式
引语版式
普通流布局
块级布局
行内布局
流根布局
手风琴布局
列表—详情布局
辅助窗格布局
信息流布局
卡片网格布局
瀑布流页面
便当盒布局
仪表盘布局
数据表格布局
画廊布局
搜索结果布局
设置页面布局
媒体对象布局
Hero 主视觉布局
分层导航布局
宏观流动模式
列下落模式
布局切换模式
微调模式
画布外模式
单人物构图
双人物构图
三人物构图
群像构图
过肩构图
主观视角构图
客观视角构图
干净单人镜头
脏单人镜头
深度调度
堆叠重排
顺序重排
折叠双窗格
自适应网格
组件级响应布局
F 型扫描模式
Z 型扫描模式
古腾堡图式
层蛋糕扫描模式
斑点扫描模式
轮播布局
时间线布局
看板布局
日历布局
树形浏览布局
对话布局
地图主导布局
画布工作区布局
表单布局
分步表单
平面调度
三角调度
横向调度
多层前景调度
高远法
深远法
平远法
三远综合构图
散点透视
游观式构图
全景式构图
河两岸式构图
边角式构图
截景式构图
折枝式构图
留白构图
计白当黑构图
虚实相生构图
疏密相间构图
主宾关系构图
竖排中西文转向
直排中西文直立
双向文字排版
旁注（Ruby）排版
标题幻灯片版式
标题和内容幻灯片版式
节标题幻灯片版式
两项内容幻灯片版式
比较幻灯片版式
仅标题幻灯片版式
空白幻灯片版式
内容与标题说明幻灯片版式
图片与标题说明幻灯片版式
大数字页幻灯片版式
引语页幻灯片版式
时间线页幻灯片版式
流程幻灯片版式
矩阵页幻灯片版式
数据图表页幻灯片版式
全图页幻灯片版式
开合构图
起承转合构图
藏露关系构图
欹正关系构图
横排左起
横排右起
直排右起
直排左起
横直混排
纵中横排
"""


def classification(index: int, name: str) -> tuple[str, str]:
    if index <= 20:
        return "构图逻辑", "经典法则与空间留白"
    if index <= 50:
        return "视觉原则与阅读模式", "平衡、层级、对比与节奏"
    if index <= 110:
        return "构图逻辑", "轴线、几何、空间与透视"
    if index <= 130:
        return "字体、网格与东亚文字", "文字造型、绕排与对齐"
    if index <= 140:
        return "构图逻辑", "视点、景深与空间系统"
    if index <= 180:
        return "字体、网格与东亚文字", "排版系统与网格系统"
    if index <= 200:
        return "平面、出版与广告", "表现型版式与出版功能页"
    if index <= 270:
        return "网页与 UI", "布局原语、页面模式与响应重排"
    if index <= 285:
        return "影视画面构图", "人物、镜头与场面调度"
    if index <= 300:
        return "网页与 UI", "阅读模式与产品页面"
    if index <= 320:
        return "中国传统构图", "三远、游观、取景与章法"
    if index <= 324:
        return "字体、网格与东亚文字", "东亚文字与混排"
    if index <= 340:
        return "演示文稿页面", "基础、叙事与数据页面"
    if index <= 344:
        return "中国传统构图", "开合、起承转合、藏露与欹正"
    return "字体、网格与东亚文字", "东亚文字方向与混排"


def main() -> None:
    names = [line.strip() for line in NAMES.splitlines() if line.strip()]
    if len(names) != 350:
        raise SystemExit(f"visual title list must contain 350 names; found {len(names)}")
    source = json.loads(SOURCE_CATALOG.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    mapped = {item["id"]: item for item in mapping["items"]}
    items = []
    for index, (claimed, visual_name) in enumerate(zip(source, names), start=1):
        rule_id = f"{index:03d}"
        category, subcategory = classification(index, visual_name)
        source_item = mapped[rule_id]
        items.append({
            "id": rule_id,
            "name": visual_name,
            "category": category,
            "subcategory": subcategory,
            "image": claimed["image"],
            "thumbnail": f"layout-rules/references/source-thumbnails/{rule_id}.jpg",
            "sha256": source_item["sourceSha256"],
            "visualReviewStatus": "verified-match",
            "catalogClaim": {
                "name": claimed["name"],
                "category": claimed["category"],
                "subcategory": claimed["subcategory"],
                "matchesVisibleTitle": claimed["name"] == visual_name,
            },
        })
    OUTPUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mismatches = sum(not x["catalogClaim"]["matchesVisibleTitle"] for x in items)
    print(f"built visual truth catalog: {len(items)} items; corrected {mismatches} mislabeled source entries")


if __name__ == "__main__":
    main()
