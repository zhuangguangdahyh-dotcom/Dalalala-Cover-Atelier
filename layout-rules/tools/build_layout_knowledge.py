#!/usr/bin/env python3
"""Build one durable, queryable composition knowledge asset for every layout."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
CATALOG = ROOT / "visual-truth-catalog.json"
RULES = ROOT / "rules"
KNOWLEDGE = ROOT / "knowledge"
SOURCE_COMMIT = "34dc39cb5128776b594754624fa2202d5942a35b"


def has(name: str, *tokens: str) -> bool:
    return any(token in name for token in tokens)


def category_purpose(category: str) -> tuple[str, str]:
    return {
        "构图逻辑": (
            "用空间位置、几何骨架和视觉动线分配画面重量",
            "人物、产品、场景或插画主体需要被重新裁切和定位的封面",
        ),
        "视觉原则与阅读模式": (
            "控制第一眼焦点、信息分组、对比关系和阅读顺序",
            "信息层级比画面造型更重要的知识、观点和方法类封面",
        ),
        "平面、出版与广告": (
            "把标题、图片、说明和品牌信息组织成稳定的编辑版面",
            "标题较长、需要副标题或栏目身份的内容型封面",
        ),
        "字体、网格与东亚文字": (
            "用网格、对齐和文字方向建立秩序并容纳复杂中文信息",
            "文字主导、系列化、需要稳定复用的封面",
        ),
        "网页与 UI": (
            "借用界面模块、卡片和导航关系表达步骤、系统或选择",
            "工具、教程、清单、对比、流程和数据类封面",
        ),
        "影视画面构图": (
            "以人物数量、镜头视点和空间调度组织情绪与关系",
            "真人、角色、访谈、故事和情绪类封面",
        ),
        "中国传统构图": (
            "以游观、虚实、三远和景式控制气韵、深度与留白",
            "文化、空间、东方审美、人物与环境关系类封面",
        ),
        "演示文稿页面": (
            "用演示页面的单一论点结构强化标题、证据或数字",
            "观点、结论、数据、流程和一句话承诺类封面",
        ),
    }[category]


def mechanism_detail(name: str, axis: str, focus: str) -> dict:
    why = f"“{name}”通过可识别的 {axis} 骨架，把分散元素收束到 {focus}，让用户在缩略图里迅速找到主次。"
    motion = "主标题先被看见，再由主体或连接线把视线带向副信息。"
    mood = "清楚、稳定、有控制力"
    use = ["主题只有一个核心判断", "主体与标题可以形成明确空间关系"]
    avoid = ["所有信息都要求同等突出", "素材无法为主标题让出可读区域"]

    if has(name, "留白", "负空间", "空间法则", "计白", "疏密"):
        why = f"“{name}”把空白本身当成主动形状，靠少量元素和大面积呼吸制造关注与想象。"
        motion, mood = "视线先停在孤立主体，再进入受保护的文字空场。", "克制、安静、意味深长"
        use += ["情绪、人物态度或高信任表达需要停顿感"]
        avoid += ["必须罗列很多卖点", "背景杂物无法被弱化"]
    elif has(name, "非对称", "偏心", "偏轴", "边角", "参差"):
        why = f"“{name}”把重量推离中心，再用标题、色块或留白形成反向配重，因此画面稳定但不僵硬。"
        motion, mood = "视线从偏置主体跳向另一侧标题，形成一次有张力的跨越。", "松弛、现代、有张力"
    elif has(name, "对称", "镜像", "中轴", "居中", "金字塔"):
        why = f"“{name}”依靠中心轴和左右视觉重量的呼应建立稳定感，适合把主体塑造成确定的第一焦点。"
        motion, mood = "视线进入中心，再向两侧或上下读取补充信息。", "稳重、正式、确定"
    elif has(name, "对角", "斜", "动态", "运动", "放射", "离心", "向心"):
        why = f"“{name}”用方向性很强的线或尺度变化推动视线，适合把动作、冲突或情绪放大。"
        motion, mood = "视线沿主轴快速推进，在终点或交汇点完成聚焦。", "有速度、兴奋、具有冲击"
    elif has(name, "重复", "图案", "节奏", "渐变", "交替", "渐进", "随机"):
        why = f"“{name}”先建立可预测的重复，再用一个受控差异制造焦点和记忆点。"
        motion, mood = "视线先识别规律，再停在破坏规律的标题或主体。", "有秩序、活泼、节拍明确"
    elif has(name, "透视", "深远", "高远", "平远", "景深", "前景", "空间层次"):
        why = f"“{name}”利用尺度、遮挡、清晰度或消失线制造深度，使主体和标题获得前后关系。"
        motion, mood = "视线由近到远进入画面，最后落到消失区域或关键人物。", "沉浸、叙事、空间感强"
    elif has(name, "网格", "模块", "分栏", "栏版", "矩阵", "方格"):
        why = f"“{name}”通过固定栏宽、单元和间距管理复杂信息，再用跨格或尺度差建立首要层级。"
        motion, mood = "视线按网格先读最大单元，再读取相邻的次级模块。", "理性、清晰、系统化"
    elif has(name, "标题", "文字主导", "引语", "字体", "文字排版"):
        why = f"“{name}”把文字形态当成主要图像，标题本身承担构图重量，其他元素只提供语境。"
        motion, mood = "视线先读完整标题，再通过少量图片或署名确认语境。", "直接、有观点、传播性强"
    elif has(name, "图片主导", "全图", "Hero", "封面版式", "画廊", "媒体对象"):
        why = f"“{name}”让图片承担情绪和第一焦点，文字退入稳定安全区完成解释。"
        motion, mood = "视线先识别人物或场景，再进入标题与补充标签。", "沉浸、直观、情绪先行"
    elif has(name, "双", "两项", "比较", "并置"):
        why = f"“{name}”把两个对象放在同一视觉尺度上，让差异、关系或选择在第一眼成立。"
        motion, mood = "视线在两个区域之间往返，标题负责指出比较维度。", "明确、理性、具有冲突"
    elif has(name, "流程", "时间线", "分步", "路径", "导航", "树形", "分支"):
        why = f"“{name}”用节点、顺序和连接关系把内容变成可追踪的路径，降低复杂主题的理解成本。"
        motion, mood = "视线从入口节点依次移动到结果节点，中途不应出现无意义回跳。", "有推进、可执行、信息明确"

    return {
        "whyItWorks": why,
        "visualMechanism": f"以 {axis} 为主骨架，以 {focus} 为第一焦点；其他元素必须承担引导、配重或说明功能。",
        "readingMotion": motion,
        "emotionalEffect": mood,
        "whenToUse": use,
        "avoidWhen": avoid,
    }


def role_map(name: str, axis: str, focus: str, reading: str) -> dict:
    title_position = "与主体错位布置，在主阅读路径的入口或第二停顿点"
    subject_position = f"占据 {focus}，并服从 {axis} 主轴"
    subtitle_position = "靠近主标题形成同组，字号和对比不得超过主标题的 45%"
    whitespace = "保护主体轮廓外侧与主标题周围至少一处完整空场"
    decorations = "只放在阅读路径的转折、端点或视觉失衡处"

    if has(name, "文字主导", "大标题", "仅标题", "标题幻灯片"):
        title_position = "占据最大面积，成为画面第一主体"
        subject_position = "图片缩为语境符号、纹理或可省略的次级层"
    elif has(name, "图片主导", "全图", "Hero", "剪影", "人物", "镜头"):
        subject_position = "占据最大可识别区域，脸、眼神、动作或产品关键结构不可被文字遮挡"
        title_position = "进入低细节安全区，或与主体形成明确左右、上下配重"
    elif has(name, "偏心", "偏轴", "非对称", "边角"):
        subject_position = "推向一侧或角部，保留完整识别轮廓"
        title_position = "占据反侧配重区，与主体形成距离感"
    elif has(name, "居中", "对称", "中轴", "金字塔"):
        subject_position = "锁在中心轴或稳定三角重心"
        title_position = "沿中心轴上方、下方或环绕主体布置"
    elif has(name, "分栏", "栏版", "双列", "多列", "侧栏"):
        subject_position = "进入声明的图片栏或主栏，不跨越未授权栏线"
        title_position = "进入主标题栏，可跨栏但必须保留栏间距节奏"
        whitespace = "保护栏间距、页边距和标题段前段后空间"
    elif has(name, "留白", "负空间", "计白"):
        subject_position = "缩小并靠近边缘、三分点或角部，形成孤立焦点"
        title_position = "只占留白的一部分，不能把空场填满"
        whitespace = "至少保留一个连续的大面积空白形状，禁止碎片化填充"
    elif has(name, "对角", "斜", "运动", "动态"):
        subject_position = "放在斜向轴的起点、交点或终点，动作朝向必须顺轴"
        title_position = "沿同一斜向动势分行，保持文字可读角度"
    elif has(name, "环", "圆", "椭圆", "弧", "曲线", "波浪", "S 形", "C 形"):
        subject_position = "靠近曲线焦点或被曲线包围的内区"
        title_position = "沿曲率、切线或曲线外侧布置，不堵塞曲线通道"
    elif has(name, "网格", "模块", "面板", "卡片", "表格", "看板"):
        subject_position = "占据最大或跨格模块，其他模块提供说明或证据"
        title_position = "位于入口模块或跨格标题带"
        decorations = "由网格线、编号、标签或状态点承担，不能额外堆贴纸"

    return {
        "primarySubject": {"role": "第一视觉焦点和主题载体", "placement": subject_position},
        "mainTitle": {"role": "把主题压缩成第一眼可读的判断", "placement": title_position, "recommendedLines": "1–3 行，按语义断句"},
        "subtitle": {"role": "补充对象、条件或结果，不重复主标题", "placement": subtitle_position},
        "supportingInfo": {"role": "栏目、数字、署名、提示或证据", "placement": "只进入第三级信息区，数量受构图剩余空间限制"},
        "decoration": {"role": "强化方向、情绪或分组", "placement": decorations},
        "protectedWhitespace": whitespace,
        "readingPath": reading,
    }


def content_fit(name: str, category: str, asset_types: list[str], title_lengths: list[str], subject_counts: list[int]) -> dict:
    _, base_use = category_purpose(category)
    themes = [base_use]
    if has(name, "对比", "并置", "双", "两项"):
        themes += ["前后对比、选择判断、关系冲突、两类人或两种方案"]
    if has(name, "流程", "时间线", "步骤", "路径", "导航"):
        themes += ["方法步骤、成长过程、问题到结果、路线说明"]
    if has(name, "人物", "镜头", "景深", "视角"):
        themes += ["人物情绪、关系、故事瞬间、专业人物表达"]
    if has(name, "留白", "负空间", "疏密", "虚实"):
        themes += ["情绪观点、高信任表达、文化审美、克制型品牌内容"]
    if has(name, "标题", "文字", "引语", "大数字"):
        themes += ["强观点、金句、结果数字、反常识判断"]
    if has(name, "数据", "表格", "矩阵", "看板"):
        themes += ["数据结论、清单、参数比较、系统框架"]
    return {
        "idealThemes": list(dict.fromkeys(themes)),
        "suitableAssets": asset_types,
        "titleLengths": title_lengths,
        "subjectCounts": subject_counts,
        "platformNotes": {
            "3:4": "默认竖版；优先保留上下阅读推进和人物完整轮廓。",
            "4:3": "横版重建左右关系，不得把竖版直接拉伸。",
            "16:9": "横向留白增加，主体与标题可分居两端，但焦点仍只能有一个。",
        },
        "unsuitedContent": ["信息层级无法排序的主题", "没有可识别主体且标题也不明确的素材"],
    }


def asset_adaptation(name: str) -> dict:
    preserve = ["人物脸、眼神、动作或产品关键结构", "与主题直接相关的环境证据"]
    weaken = ["无关杂物、抢眼高光、背景文字、水印和重复信息"]
    crop = "先按构图焦点重新裁切，再按平台比例重建周围空间；禁止整图等比缩小后只把字贴上去。"
    cutout = "当原背景无法提供标题安全区、主体位置与规则冲突，或需要跨层遮挡时抠出主体。"
    background = "当背景杂乱、方向错误、色彩抢夺主标题或无法建立规则所需空场时更换或重绘。"
    effects = "只有能强化规则主轴、焦点、深度或主题情绪时才加光影、速度线、重复影像或手绘装饰。"
    if has(name, "满幅", "全图", "图片主导", "Hero"):
        preserve += ["图片的情绪氛围和边缘延展"]
        crop = "让图片覆盖画布并围绕主体重新取景，保留标题安全区和平台裁切余量。"
    if has(name, "剪影", "裁切", "截景", "窗口", "框"):
        preserve += ["主体最有识别力的轮廓或被框取的关键局部"]
    if has(name, "留白", "负空间", "计白"):
        weaken += ["所有会把连续空场切碎的小装饰"]
        background = "优先清理、延展或重绘为连续低细节背景，保证留白形状完整。"
    if has(name, "人物", "镜头", "过肩", "主观", "客观"):
        preserve += ["人物朝向、视线方向、人与环境或人物之间的关系"]
    return {
        "mustPreserve": list(dict.fromkeys(preserve)),
        "weakenOrRemove": list(dict.fromkeys(weaken)),
        "cropAndReposition": crop,
        "cutoutWhen": cutout,
        "changeBackgroundWhen": background,
        "effectsWhen": effects,
    }


def text_strategy(name: str, axis: str) -> dict:
    scale = "主标题约为副标题的 2.2–3.5 倍，关键词可再放大 15%–35%"
    placement = f"文字组合服从 {axis} 主轴，以语义分组形成一个整体，不把每个字平均铺开。"
    emphasis = "只突出能改变点击判断的对象、冲突、数字或结果词。"
    if has(name, "仅标题", "大标题", "文字主导"):
        scale = "主标题占据画面主要面积，内部再以字重、尺寸或颜色形成两级"
    if has(name, "引语", "诗", "正文", "单栏", "多栏"):
        emphasis = "依靠行宽、段落、标点和留白组织节奏，避免同时突出过多词。"
    if has(name, "竖", "纵", "直排"):
        placement = "中文可竖排并从右向左组织列序；数字、英文和标点必须单独处理方向。"
    return {
        "mainTitleScale": scale,
        "placement": placement,
        "emphasisLogic": emphasis,
        "subtitleRule": "副标题只解释主标题缺失的上下文，保持低对比并贴近所属信息组。",
        "legibilityGate": "缩到 360 px 宽时，标题语义、第一焦点和主体身份仍可辨认。",
    }


def signals(name: str, axis: str, focus: str) -> tuple[list[str], list[str]]:
    select = [
        f"素材天然存在或可以重构出 {axis} 方向",
        f"主题需要把第一眼落在 {focus}",
        f"标题与主体能共同呈现“{name}”的构图身份",
    ]
    reject = [
        "套用后只能看出文字换了位置，看不出构图骨架变化",
        "主体关键结构被遮挡、切断或失去识别性",
        "标题、主体和装饰形成三个同等焦点",
        "为了填空加入与主题无关的贴纸或小图标",
    ]
    return select, reject


def make_knowledge(item: dict, rule: dict) -> dict:
    contract = rule["layoutContract"]
    selection = rule["selection"]
    name = item["name"]
    principle = mechanism_detail(name, contract["dominantAxis"], contract["primaryFocus"])
    purpose, _ = category_purpose(item["category"])
    select, reject = signals(name, contract["dominantAxis"], contract["primaryFocus"])
    return {
        "schemaVersion": 2,
        "ruleId": rule["id"],
        "name": name,
        "category": item["category"],
        "subcategory": item["subcategory"],
        "learningStatus": "studied",
        "learningMethod": "pinned-original-reference + visual-contact-sheet-review + composition-theory-model",
        "sourceEvidence": {
            "repositoryCommit": SOURCE_COMMIT,
            "originalImagePath": item["image"],
            "localReference": f"../references/source-thumbnails/{item['id']}.jpg",
            "mappingRequirement": "visible title is authoritative; the unreliable upstream filename claim is retained for audit only",
            "upstreamCatalogClaim": item.get("catalogClaim"),
        },
        "purpose": purpose,
        "principle": principle,
        "contentAnatomy": role_map(name, contract["dominantAxis"], contract["primaryFocus"], contract["readingPath"]),
        "contentFit": content_fit(name, item["category"], selection["assetTypes"], selection["titleLengths"], selection["subjectCounts"]),
        "assetAdaptation": asset_adaptation(name),
        "textStrategy": text_strategy(name, contract["dominantAxis"]),
        "selectionSignals": select,
        "rejectionSignals": reject,
        "layoutContract": {
            "locked": contract["locked"],
            "adaptive": contract["adaptive"],
            "optional": contract["optional"],
            "forbidden": contract["forbidden"],
        },
        "qa": {
            "hardGates": [
                "来源编号、名称和画面标题一致",
                "输出中可辨认该规则的空间骨架",
                "主体、主标题、副标题和装饰层级明确",
                "素材经过构图需要的裁切、抠图、弱化或重绘决策",
                "平台比例通过独立重排获得，未拉伸旧画布",
                "360 px 缩略图可读",
            ],
            "reviewQuestion": f"遮住规则名称后，是否仍能从主体、标题和留白关系判断这是“{name}”？",
        },
    }


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    index = {"schemaVersion": 1, "sourceCommit": SOURCE_COMMIT, "count": 0, "items": []}
    for item in catalog:
        rule_path = RULES / f"layout-{item['id']}.json"
        rule = json.loads(rule_path.read_text(encoding="utf-8"))
        knowledge = make_knowledge(item, rule)
        out = KNOWLEDGE / f"layout-{item['id']}.json"
        out.write_text(json.dumps(knowledge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index["items"].append({
            "id": knowledge["ruleId"],
            "name": knowledge["name"],
            "category": knowledge["category"],
            "subcategory": knowledge["subcategory"],
            "learningStatus": knowledge["learningStatus"],
            "path": f"knowledge/layout-{item['id']}.json",
            "selectionSignals": knowledge["selectionSignals"],
        })
    index["count"] = len(index["items"])
    (ROOT / "knowledge-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"built {index['count']} composition knowledge assets")


if __name__ == "__main__":
    main()
