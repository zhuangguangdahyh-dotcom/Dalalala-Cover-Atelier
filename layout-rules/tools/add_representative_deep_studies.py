#!/usr/bin/env python3
"""Add manually observed anatomy for nine cross-media representative references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DATA = {
    "layout-172": {
        "title": "放射网格",
        "family": "system-map",
        "observed": {
            "primarySubject": "画面正中的金色核心圆与八条放射轴",
            "mainTitle": "顶部居中的大标题，字面本身沿弧形形成冠部",
            "subtitle": "标题下方英文名与一句原理说明",
            "supportingInformation": "轴端模块、左右解释栏、底部应用示例和设计要点",
            "decorations": "同心圆、辐射线、节点、星点与底部横线",
            "protectedWhitespace": "核心圆内、轴线之间及左右说明与主系统之间的间隔"
        },
        "mechanism": "强中心作为信息源，模块沿辐射轴分布，距离、环级和轴向共同表达层级与关系。",
        "reading": "先进入中心，再沿辐射轴向外读取分支，最后回到底部总结。",
        "use": ["一个核心概念连接多个并列分支", "关系、能力、流程或生态需要围绕中心解释"],
        "avoid": ["没有真实中心关系的普通清单", "分支多到缩略图无法区分"],
        "level": "T2",
        "actions": ["把人物、产品、关键词或数字压缩成中心锚", "将最多 4–8 个分支放到明确辐射方向", "用距离和节点大小区分重要度"],
        "titleAction": ["标题可拱在系统上方或沿外环排列", "标题不得与中心争夺第一焦点"],
        "metaphor": "专家 IP 可将人物头像作为中心，方法、案例、结果和信任证据沿四条主轴展开。",
        "question": "中心是否真能解释所有分支，且遮住标签后仍看得出由内向外的关系？",
        "failures": ["只画一个装饰圆盘，分支之间没有语义", "中心与标题一样大导致双焦点", "所有节点同权且过密"]
    },
    "layout-181": {
        "title": "大标题版式",
        "family": "typographic-stage",
        "observed": {
            "primarySubject": "左上至中部两行超大黑色中文标题",
            "mainTitle": "标题本身就是第一视觉主体",
            "subtitle": "大标题下方蓝色英文标题",
            "supportingInformation": "左下解释文字与底部四项关键词",
            "decorations": "右中蓝圆、斜穿圆形的黑线、右下越界蓝三角和点阵",
            "protectedWhitespace": "标题字腔、标题右侧与几何形之间的呼吸区"
        },
        "mechanism": "把标题作为最大视觉质量，利用行宽差、紧凑字距与一组巨大几何配重建立张力。",
        "reading": "先读超大标题，再被圆与斜线带向右下配重，最后回到说明。",
        "use": ["短而有判断力的标题", "素材弱但文案强的封面、章节页或海报"],
        "avoid": ["标题过长无法形成清楚轮廓", "必须完整展示复杂主体或大量证据"],
        "level": "T2",
        "actions": ["按语义把标题压成 1–3 个不同宽度的大块", "允许关键词越界、错位或与主体局部遮挡", "让一组主体或几何体承担反向配重"],
        "titleAction": ["标题占据最大面积并形成独立剪影", "字形变化服务整块轮廓，不能逐字平均装饰"],
        "metaphor": "“头大”可让“头大”两字成为巨大块面，并让放大的猫头从字块或圆形后方顶出。",
        "question": "缩略图中只看标题轮廓，是否已经形成唯一主角和可辨认节奏？",
        "failures": ["只是把普通字体整体放大", "每行一样长导致呆板矩形", "主体、标题与几何同时抢眼"]
    },
    "layout-182": {
        "title": "图片窗口版式",
        "family": "framed-window",
        "observed": {
            "primarySubject": "右侧四个不同比例和圆角的图片窗口",
            "mainTitle": "左上两行超大黑色标题",
            "subtitle": "标题下方青色英文名与短横线",
            "supportingInformation": "左中说明、左下图标关键词和底部提示框",
            "decorations": "圆角边界、圆点、短横线和窗口间的对齐间隔",
            "protectedWhitespace": "左侧标题与说明之间、窗口外侧以及各窗口之间的白边"
        },
        "mechanism": "用不同形状和尺度的裁切窗口控制可见信息，制造预览、聚焦、节奏与层级。",
        "reading": "标题进入，先看最大窗口，再按窗口尺度下降浏览局部。",
        "use": ["产品局部、案例细节、人物多景别或场景预览", "需要用裁切而非完整图建立悬念"],
        "avoid": ["主体关键识别点不能被窗口裁切", "所有图片同等重要且无法排序"],
        "level": "T2",
        "actions": ["把同一素材拆成全貌、细节和动作三个景别", "用窗口形状主动裁掉无关背景", "最大窗口承载唯一主视觉"],
        "titleAction": ["标题与窗口形成左右或上下两大块", "关键词可轻微侵入窗口边界但不能破坏主体识别"],
        "metaphor": "选择类主题可用多个窗口只透露局部，最大窗口给出关键判断，小窗口补充证据。",
        "question": "每个窗口是否展示不同层级的信息，而不是重复缩放同一画面？",
        "failures": ["把完整图片等比塞进每个窗口", "窗口大小不同但内容价值相同", "边框成为唯一设计特征"]
    },
    "layout-191": {
        "title": "蒙太奇版式",
        "family": "editorial-narrative",
        "observed": {
            "primarySubject": "右半部相互遮叠的多张纸片、图像卡与引语纸",
            "mainTitle": "左上超大标题",
            "subtitle": "标题下方暗红英文名和短横线",
            "supportingInformation": "左侧六条原理说明与底部总结",
            "decorations": "撕纸边、胶带、网格、曲线、点阵和越界色块",
            "protectedWhitespace": "左侧标题与条目区的浅色阅读场，以及右侧碎片之间的层间缝隙"
        },
        "mechanism": "用大小、方向、材质和遮挡不同的碎片形成有主次的叙事组，层间关系比碎片数量更重要。",
        "reading": "标题建立主题，视线进入最大碎片，再通过遮挡和方向跳转到证据与引语。",
        "use": ["人物故事、事件回顾、案例证据、文化情绪或多来源素材", "需要手作、档案或记忆感"],
        "avoid": ["只有一张素材且无法创造有效细节", "严肃证据不能被装饰性撕裂或遮挡"],
        "level": "T3",
        "actions": ["把素材拆成主图、局部、文字证据与纹理层", "用真实遮挡建立前中后景", "让一个碎片明显最大并承担主题"],
        "titleAction": ["标题可压住一层纸片或被前景局部遮挡", "字块需像素材的一部分，不能浮在拼贴上方"],
        "metaphor": "复杂心理或回忆主题可把同一人物拆成表情、手势、场景与一句原话，让碎片关系形成叙事。",
        "question": "拿掉胶带和纹理后，碎片的大小、遮挡和信息顺序是否仍然成立？",
        "failures": ["随机堆纸片和胶带", "所有碎片同尺寸", "只有复古纹理，没有叙事关系"]
    },
    "layout-192": {
        "title": "模块化页面",
        "family": "modular-evidence",
        "observed": {
            "primarySubject": "上方标题区与右上 2×2 几何模块共同构成入口",
            "mainTitle": "左上单行超大标题",
            "subtitle": "标题下方英文名和短横线",
            "supportingInformation": "中部六个原理模块、右侧三个实例卡、下方三种组合示意与应用建议",
            "decorations": "统一圆形图标、细边框、短横线和重复网格",
            "protectedWhitespace": "模块内部边距、列间距和上下章节分隔带"
        },
        "mechanism": "把不同内容压缩成可复用单元，用统一网格、边距和样式建立秩序，再用一个例外模块制造重点。",
        "reading": "标题进入，横向读取原理单元，再进入实例列和组合示意。",
        "use": ["卖点、证据、功能、作品、履历或数据需要分组展示", "PPT、简历、长图和说明型广告"],
        "avoid": ["只有一个核心判断却硬拆成很多卡片", "模块内容长度差异过大无法压缩"],
        "level": "T2",
        "actions": ["先确定模块类型和信息上限，再填内容", "用一个放大、跨格或高对比模块作为主角", "重复边距和对齐，变化内容尺度"],
        "titleAction": ["标题属于独立入口区，不能与每张卡同级", "卡片标题短且一致，正文密度受控"],
        "metaphor": "四点、五步、案例清单可变成统一卡片系统，并用一张跨格主卡承载最关键判断。",
        "question": "模块是否对应真实内容类型，且存在清楚的优先级例外？",
        "failures": ["为了填满网格制造无用卡片", "所有模块同权", "每张卡内部使用不同边距和字体逻辑"]
    },
    "layout-231": {
        "title": "双列页面",
        "family": "split-comparison",
        "observed": {
            "primarySubject": "右半部两列平行案例，左列中文自然生活，右列英文 Design for Life",
            "mainTitle": "左上三行超大标题",
            "subtitle": "标题下方英文名与左中说明",
            "supportingInformation": "右侧两列标题、图像和要点，左下设计要点与底部线框示意",
            "decorations": "中央分隔线、列内短横线、圆点和统一底部基线",
            "protectedWhitespace": "两列之间的分隔沟、列内标题与图像之间的空隙"
        },
        "mechanism": "用共同基线、相同信息层级和清楚列沟让两个对象并行读取，可用于比较、分类或对话。",
        "reading": "先识别双列关系，再左右对照同层信息，最后读取共同结论。",
        "use": ["前后、对错、方案 A/B、人物对话或双案例", "内容天然能按相同维度对齐"],
        "avoid": ["两侧信息没有共同维度", "一侧内容量远大于另一侧且无法压缩"],
        "level": "T2",
        "actions": ["把两侧主体裁成相近视觉重量", "锁定共同顶部、图像线与结论线", "允许一侧用更强对比表示结论，但结构仍对齐"],
        "titleAction": ["总标题位于双列之外或跨越两列", "列标题保持同等级和同基线"],
        "metaphor": "选择类主题可让错误示范和正确示范共享同一裁切与指标，只让关键差异跳出。",
        "question": "两列是否能沿同一维度逐项比较，还是只是把两个无关区块并排？",
        "failures": ["只有左右分栏，没有比较关系", "列沟过窄导致混读", "总标题被拆进一列破坏共同语境"]
    },
    "layout-264": {
        "title": "Hero 主视觉布局",
        "family": "monumental-symbol",
        "observed": {
            "primarySubject": "右中占据大半画面的蓝色闪电与黄色圆形主视觉",
            "mainTitle": "左上超大蓝色中英文标题",
            "subtitle": "左中一句主张与右下行动引导",
            "supportingInformation": "三处引线说明、底部 H/M/A 解释与结论带",
            "decorations": "引线、短横线、箭头和底部蓝色横带",
            "protectedWhitespace": "主视觉轮廓外的浅色区、标题下方和行动入口周围"
        },
        "mechanism": "让一个人物、产品、数字或符号形成压倒性主视觉，再用一句价值主张和一个行动点完成首屏。",
        "reading": "先看主视觉，再读价值主张，最后到行动或结论。",
        "use": ["广告首屏、PPT 标题页、产品发布、强主张封面", "存在可被放大的强主体或符号"],
        "avoid": ["没有明确核心利益", "多个产品或观点都要求主视觉待遇"],
        "level": "T3",
        "actions": ["把关键主体或符号放大至越界", "让文字和主体产生穿插、切入或指向", "弱化所有非核心信息"],
        "titleAction": ["标题与主视觉组成一个首屏句子", "行动信息必须处在阅读路径终点"],
        "metaphor": "“头大”可把猫头放大成占画面一半的 Hero 圆形，耳朵越界，标题从侧面被挤压或切入。",
        "question": "第一眼能否同时看懂主角、主张和下一步，而不是只看到一块大图？",
        "failures": ["整图铺满但没有主视觉焦点", "标题、按钮和主体三者同权", "大色块与主题无关"]
    },
    "layout-292": {
        "title": "时间线布局",
        "family": "sequential-flow",
        "observed": {
            "primarySubject": "画面中部由左向右连接的五个圆形节点与对应卡片",
            "mainTitle": "左上单行超大暗红标题",
            "subtitle": "标题下方英文名与原理说明",
            "supportingInformation": "五个阶段卡、下方三段阶段带与底部布局要点",
            "decorations": "连接线、箭头、节点图标、右上同心圆和浅色弧带",
            "protectedWhitespace": "节点之间、卡片列沟以及阶段带上下的连续通道"
        },
        "mechanism": "用有方向的连续线与里程碑节点编码先后关系，节点、阶段和结果形成三层时间尺度。",
        "reading": "从起点沿连接线依次经过节点，最后到结论或结果。",
        "use": ["过程、成长、项目履历、事件回顾、方法步骤", "顺序变化会改变意义"],
        "avoid": ["项目之间没有先后或因果", "节点过多导致移动端不可读"],
        "level": "T2",
        "actions": ["把 3–7 个关键节点压缩到一条主路径", "用节点大小或颜色标记真正里程碑", "将图片或人物姿态朝向下一节点"],
        "titleAction": ["总标题在路径之外建立主题", "节点标题使用短动词或结果词，不能塞成长句"],
        "metaphor": "职业履历可用三段路径连接关键成果，人物照片只在转折节点出现。",
        "question": "如果删除编号，连接关系本身是否仍能表达正确顺序？",
        "failures": ["把普通卡片排成一行后加箭头", "节点过多且同权", "路径方向与阅读方向冲突"]
    },
    "layout-318": {
        "title": "虚实相生构图",
        "family": "layered-depth",
        "observed": {
            "primarySubject": "右中巨大的白色实体圆环与其内部绿色空洞",
            "mainTitle": "左上实心加描边混排的四字标题",
            "subtitle": "标题下方英文名与原理说明",
            "supportingInformation": "左侧三条知识点、右侧引线说明和底部图例",
            "decorations": "半透明矩形、模糊圆、轮廓圆、波线和橙色焦点",
            "protectedWhitespace": "圆环内部负形、实体之间的穿插缝隙和左侧说明区"
        },
        "mechanism": "让实体、空洞、透明过渡和模糊层相互定义，利用穿插与遮挡建立深度和概念张力。",
        "reading": "从实心标题进入，被巨大实体吸引，再穿过空洞和透明层读取焦点。",
        "use": ["存在与缺席、看见与隐藏、边界、心理空间或抽象概念", "需要克制但有概念张力的海报和章节页"],
        "avoid": ["主体必须完整无损展示", "信息密集且不能形成大面积空洞"],
        "level": "T3",
        "actions": ["把主体轮廓切成实体、空洞或透明层", "用一处重叠确定前后关系", "让主题焦点出现在实体与虚空的交界"],
        "titleAction": ["标题可使用实心与空心字重对照，但必须保持可读", "文字与空洞共用一个形状逻辑"],
        "metaphor": "心理主题可保留人物脸部为实，身体或背景转为半透明和留白，让界线本身表达情绪。",
        "question": "空的部分是否参与塑造主体，还是只是随意降低透明度？",
        "failures": ["统一降透明度冒充虚实", "负形没有清楚轮廓", "叠加很多玻璃块却没有前后焦点"]
    }
}


def save(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    for rule_id, data in DATA.items():
        number = rule_id.split("-")[-1]
        knowledge_path = ROOT / "knowledge" / f"{rule_id}.json"
        knowledge = json.loads(knowledge_path.read_text(encoding="utf-8"))
        knowledge["learningStatus"] = "studied"
        knowledge["learningMethod"] = "pinned-original-reference + full-size-visual-review + cross-media-distillation"
        knowledge["deepStudyStatus"] = "deep-studied"
        knowledge["principle"].update({
            "whyItWorks": data["mechanism"],
            "visualMechanism": data["mechanism"],
            "readingMotion": data["reading"],
            "whenToUse": data["use"],
            "avoidWhen": data["avoid"],
        })
        knowledge["contentAnatomy"] = {
            "primarySubject": {"role": "第一视觉焦点和主题载体", "placement": data["observed"]["primarySubject"]},
            "mainTitle": {"role": "建立入口与核心判断", "placement": data["observed"]["mainTitle"], "recommendedLines": "按语义和参考轮廓决定"},
            "subtitle": {"role": "补充语境", "placement": data["observed"]["subtitle"]},
            "supportingInfo": {"role": "证据、解释或行动", "placement": data["observed"]["supportingInformation"]},
            "decoration": {"role": "强化结构、方向或材质", "placement": data["observed"]["decorations"]},
            "protectedWhitespace": data["observed"]["protectedWhitespace"],
            "readingPath": data["reading"],
        }
        knowledge["contentFit"]["idealThemes"] = data["use"]
        knowledge["contentFit"]["unsuitedContent"] = data["avoid"]
        knowledge["assetAdaptation"].update({
            "cropAndReposition": "先锁定身份或事实锚点，再按该规则主动改变景别、裁切、位置、层间关系与可见范围。",
            "effectsWhen": "只有能强化该规则的主骨架、阅读动作或主题隐喻时使用。",
        })
        knowledge["textStrategy"].update({
            "placement": "；".join(data["titleAction"]),
            "legibilityGate": "360 px 缩略图仍能识别标题、第一焦点与主阅读方向。",
        })
        knowledge["selectionSignals"] = [*data["use"], data["question"]]
        knowledge["rejectionSignals"] = data["failures"]
        knowledge["transformationGrammar"] = {
            "minimumTransformationLevel": data["level"],
            "identityAnchors": ["人物脸与真实表情", "产品关键结构", "事实与数据证据"],
            "compositionFreedoms": data["actions"],
            "imageRebuildActions": data["actions"],
            "titleInteraction": data["titleAction"],
            "topicMetaphorExample": data["metaphor"],
        }
        knowledge["semanticFit"] = {
            "templateFamily": data["family"],
            "bestFor": data["use"],
            "avoidFor": data["avoid"],
            "selectionQuestion": data["question"],
        }
        knowledge["failureModes"] = data["failures"]
        knowledge["layoutContract"]["locked"] = [
            f"以 {data['family']} 作为唯一主骨架。",
            f"保持阅读动作：{data['reading']}",
            "保持参考中的主次重量、关键对齐、受保护留白和图文关系。",
        ]
        knowledge["layoutContract"]["adaptive"] = [
            "当前标题、语义分组和信息数量",
            "素材裁切、景别、位置、遮挡与背景",
            "独立选择的字体风格",
            "按当前内容重新建立的颜色角色与色值",
            "目标媒介和画幅的独立重构",
        ]
        save(knowledge_path, knowledge)

        anatomy = {
            "schemaVersion": 1,
            "ruleId": rule_id,
            "analysisStatus": "verified",
            "reviewedReference": f"../references/source-thumbnails/{number}.jpg",
            "observedTitle": data["title"],
            "referenceContentMap": data["observed"],
            "coverTranslation": {
                "templateFamily": data["family"],
                "subjectRole": data["actions"][0],
                "mainTitleRole": data["titleAction"][0],
                "subtitleRole": "只补充标题缺失的语境，并依附同一对齐系统。",
                "decorationZones": [data["observed"]["decorations"]],
                "decorationLimits": "拿掉装饰后，主骨架、主体与标题关系仍必须成立。",
                "protectedRegions": [data["observed"]["protectedWhitespace"], "身份与事实锚点"],
                "defaultReadingPath": data["reading"],
                "assetOperations": data["actions"],
            },
        }
        save(ROOT / "anatomy" / f"{rule_id}.json", anatomy)
        print(f"deep-studied {rule_id} {data['title']}")


if __name__ == "__main__":
    main()
