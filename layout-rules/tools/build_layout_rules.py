#!/usr/bin/env python3
"""Build 350 independent cover-layout rules from the pinned source catalog."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
ROOT = PROJECT / "layout-rules"
CATALOG = ROOT / "visual-truth-catalog.json"
RULES = ROOT / "rules"
THUMBNAILS = ROOT / "references/source-thumbnails"
MAPPING = ROOT / "references/source-mapping.json"
KNOWLEDGE = ROOT / "knowledge"
COMMIT = "34dc39cb5128776b594754624fa2202d5942a35b"
REPO = "https://github.com/nevertoday/350-layout-compositions"
RAW_ROOT = f"https://raw.githubusercontent.com/nevertoday/350-layout-compositions/{COMMIT}/"


def source_mapping() -> dict[str, dict]:
    if not MAPPING.exists():
        return {}
    data = json.loads(MAPPING.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data.get("items", [])}


SOURCE_MAPPING = source_mapping()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def contains(name: str, *words: str) -> bool:
    return any(word in name for word in words)


def concept_profile(name: str, category: str, subcategory: str) -> dict:
    axis = "adaptive"
    focus = "single-primary"
    reading = "primary-to-secondary"
    mechanism = f"以“{name}”的核心空间关系组织主体、标题和辅助信息。"

    if contains(name, "三分法"):
        axis, focus, reading = "thirds-grid", "thirds-intersection", "focus-to-counterspace"
        mechanism = "把主体放在三分线或交点，把标题放入与主体平衡的空白三分区。"
    elif contains(name, "黄金螺旋", "螺旋"):
        axis, focus, reading = "spiral", "spiral-eye", "outer-to-inner-spiral"
        mechanism = "让视线沿螺旋由大面积信息收拢到唯一焦点，标题顺势占据外圈。"
    elif contains(name, "黄金比例"):
        axis, focus, reading = "golden-ratio", "golden-intersection", "large-field-to-small-field"
        mechanism = "按约 1:1.618 分配主次面积，主体与标题分别占据大小关系明确的区域。"
    elif contains(name, "对角", "斜投影", "欹正"):
        axis, focus, reading = "diagonal", "axis-end-or-crossing", "diagonal-sweep"
        mechanism = "建立清楚的斜向主轴，让主体、标题和动势沿同一方向推进。"
    elif contains(name, "偏心", "偏轴", "非对称", "边角"):
        axis, focus, reading = "off-centre", "off-centre-anchor", "anchor-to-counterweight"
        mechanism = "把主要视觉重量推离中心，用另一侧标题或留白完成不对称平衡。"
    elif contains(name, "居中", "中轴", "对称", "镜像", "金字塔"):
        axis, focus, reading = "central", "canvas-centre", "centre-out"
        mechanism = "锁定中央轴与稳定重心，标题、主体和辅助信息围绕中心建立秩序。"
    elif contains(name, "放射", "向心", "离心"):
        axis, focus, reading = "radial", "radial-centre", "centre-out" if "离心" in name else "outside-in"
        mechanism = "以明确中心组织放射路径，所有方向线必须服务同一焦点或同一扩散动作。"
    elif contains(name, "圆形", "环形", "椭圆", "弧形", "C 形"):
        axis, focus, reading = "curved", "curve-enclosed-focus", "along-curve"
        mechanism = "用弧线或环形包围焦点，标题沿曲率或切线组织，保留呼吸内白。"
    elif contains(name, "X 形", "交叉", "十字"):
        axis, focus, reading = "crossed", "axis-crossing", "edges-to-crossing"
        mechanism = "以两条交叉轴制造聚焦，关键内容靠近交点，次要内容退到轴线两侧。"
    elif contains(name, "T 形"):
        axis, focus, reading = "t-axis", "top-centre", "top-then-down"
        mechanism = "用顶部横向标题与向下延伸的主体形成 T 形骨架。"
    elif contains(name, "L 形", "侧栏", "边注"):
        axis, focus, reading = "l-axis", "corner-junction", "vertical-then-horizontal"
        mechanism = "锁定一条竖向边栏和一条横向内容带，在转角处建立主焦点。"
    elif contains(name, "V 形", "三角", "倒三角"):
        axis, focus, reading = "triangular", "triangle-tip-or-centre", "wide-to-narrow"
        mechanism = "让三个视觉节点形成稳定或倒置三角，标题承担其中一个重量节点。"
    elif contains(name, "Z 形", "Z 型", "古腾堡"):
        axis, focus, reading = "z-path", "terminal-emphasis", "top-left-to-bottom-right"
        mechanism = "把阅读路径锁为左上、右上、左下、右下的 Z 形推进。"
    elif contains(name, "S 形", "曲线", "波浪", "流动", "游观"):
        axis, focus, reading = "flowing-curve", "multiple-along-path", "curved-sequence"
        mechanism = "以连续曲线路径串联标题、主体和次级信息，让视线自然游走。"
    elif contains(name, "网格", "棋盘", "模块", "矩阵", "便当盒", "四象限"):
        axis, focus, reading = "modular-grid", "cell-hierarchy", "ordered-cells"
        mechanism = "先锁定可见网格和模块跨度，再用跨格、留空或尺度差建立主次。"
    elif contains(name, "分栏", "双栏", "多栏", "单栏", "两端对齐"):
        axis, focus, reading = "column-grid", "lead-column", "column-flow"
        mechanism = "锁定栏数、栏宽和栏间距，标题与图片只能按声明的跨栏关系变化。"
    elif contains(name, "层叠", "级联", "重叠", "多层", "深度", "深空间", "前中后"):
        axis, focus, reading = "depth-layers", "foreground-or-middle", "front-to-back"
        mechanism = "以前、中、后层的遮挡和尺度差建立深度，标题固定在不破坏层次的表面。"
    elif contains(name, "透视", "深远", "高远", "平远"):
        axis, focus, reading = "perspective", "vanishing-region", "near-to-far"
        mechanism = "用透视或远近尺度引导视线，标题避开消失线和主体关键结构。"
    elif contains(name, "负空间", "留白", "计白当黑", "空间法则"):
        axis, focus, reading = "negative-space", "subject-edge", "subject-to-open-field"
        mechanism = "把留白作为主动形状锁定，主体与标题不得同时填满受保护区域。"
    elif contains(name, "框", "窗口", "截景", "藏露"):
        axis, focus, reading = "framed", "inside-frame", "frame-to-subject"
        mechanism = "用前景、窗口或裁切边界建立框景，标题不能破坏框景的开口方向。"
    elif contains(name, "重复", "图案", "节奏", "渐变", "交替", "渐进", "随机"):
        axis, focus, reading = "rhythmic-series", "pattern-break", "series-to-exception"
        mechanism = "建立重复单元与间隔规则，用一个受控差异点形成标题或主体焦点。"
    elif contains(name, "聚类", "群组", "簇群", "邻近", "相似", "共同区域"):
        axis, focus, reading = "grouped", "dominant-cluster", "cluster-to-cluster"
        mechanism = "依靠距离、相似性或共同边界形成信息组，组间留白必须大于组内间距。"
    elif contains(name, "分支", "网络", "流程", "时间线", "树形"):
        axis, focus, reading = "connected-path", "start-node", "node-sequence"
        mechanism = "用节点和连接关系规定阅读顺序，标题作为入口，路径不能交叉到不可辨认。"
    elif contains(name, "大标题", "文字主导", "引语", "仅标题"):
        axis, focus, reading = "type-dominant", "headline", "headline-first"
        mechanism = "让标题成为最大视觉主体，图片只承担语境或纹理，不能与标题争夺第一眼。"
    elif contains(name, "图片主导", "全图", "Hero", "画廊", "轮播"):
        axis, focus, reading = "image-dominant", "image-subject", "image-to-title"
        mechanism = "让图片承担第一焦点，标题进入稳定低干扰区并保持缩略图可读。"
    elif contains(name, "分屏", "比较", "双边", "两项", "双列", "列表—详情"):
        axis, focus, reading = "split", "paired-focus", "left-right-compare"
        mechanism = "把画面分成两个关系明确的区域，用统一轴线支持比较或前后关系。"
    elif contains(name, "填满", "满幅", "满出血"):
        axis, focus, reading = "full-bleed", "dominant-field", "largest-to-smallest"
        mechanism = "让主图或主色块覆盖画布边界，文字必须依附安全区而不削弱满幅冲击。"
    elif contains(name, "裁切", "剪影", "折枝"):
        axis, focus, reading = "crop-driven", "recognisable-fragment", "crop-edge-to-subject"
        mechanism = "用有意裁切制造张力，保留主体最关键的识别特征与标题安全区。"
    elif contains(name, "卡片", "区块", "面板", "仪表盘", "表格", "看板"):
        axis, focus, reading = "panel-system", "dominant-panel", "panel-hierarchy"
        mechanism = "以卡片或面板组织信息，必须有一个显著主面板，不能平均分配视觉重量。"
    elif contains(name, "垂直", "直排", "纵"):
        axis, focus, reading = "vertical", "upper-or-centre", "top-to-bottom"
        mechanism = "用竖向轴和纵向阅读组织信息，标题方向与图片重心保持一致。"
    elif contains(name, "水平", "横排", "横向"):
        axis, focus, reading = "horizontal", "left-or-centre", "left-to-right"
        mechanism = "用横向轴展开主体与标题，控制左右重量和水平留白。"

    tags = [category, subcategory, name]
    tag_map = {
        "人物": ["人物", "单人", "双人", "三人", "群像", "过肩", "单人镜头"],
        "图文": ["图文", "图片", "媒体", "封面", "Hero", "全图"],
        "文字": ["文字", "字体", "标题", "引语", "诗", "排版"],
        "数据": ["数据", "图表", "表格", "矩阵", "仪表盘", "大数字"],
        "流程": ["流程", "时间线", "分步", "导航", "路径", "树形"],
        "对比": ["对比", "比较", "并置", "双", "两项"],
        "空间": ["空间", "透视", "远法", "景深", "深焦", "前景"],
        "留白": ["留白", "负空间", "计白", "疏密"],
        "网格": ["网格", "模块", "分栏", "矩阵", "方格"],
        "动势": ["动态", "运动", "放射", "斜", "曲线", "波浪", "流动"],
    }
    for tag, words in tag_map.items():
        if contains(name, *words):
            tags.append(tag)

    asset_types = ["mixed"]
    if contains(name, "图片", "全图", "画廊", "影视", "人物", "镜头", "景深", "透视"):
        asset_types += ["photo", "illustration"]
    if contains(name, "文字", "字体", "标题", "引语", "排版", "网格"):
        asset_types += ["text"]
    if contains(name, "数据", "图表", "表格", "矩阵", "流程", "时间线"):
        asset_types += ["data", "diagram"]

    title_lengths = ["short", "medium"]
    if contains(name, "文字主导", "单栏", "多栏", "内容", "引语"):
        title_lengths.append("long")
    if contains(name, "大标题", "仅标题", "图标文字"):
        title_lengths = ["short"]

    subject_counts = [0, 1, 2, 3, 4]
    if "单人" in name:
        subject_counts = [1]
    elif "双人" in name or "两项" in name:
        subject_counts = [2]
    elif "三人" in name:
        subject_counts = [3]
    elif "群像" in name:
        subject_counts = [4]

    if category == "网页与 UI":
        suitability = "adaptable"
    elif contains(name, "索引", "目录", "设置页面", "表单", "导航", "日历", "数据表格"):
        suitability = "special-purpose"
    else:
        suitability = "direct"

    return {
        "mechanism": mechanism,
        "axis": axis,
        "focus": focus,
        "readingPath": reading,
        "tags": list(dict.fromkeys(tags)),
        "assetTypes": list(dict.fromkeys(asset_types)),
        "titleLengths": title_lengths,
        "subjectCounts": subject_counts,
        "coverSuitability": suitability,
    }


def make_rule(item: dict) -> dict:
    rule_id = f"layout-{item['id']}"
    anatomy_path = ROOT / "anatomy" / f"{rule_id}.json"
    thumb = THUMBNAILS / f"{item['id']}.jpg"
    mapped = SOURCE_MAPPING.get(item["id"], {})
    mapped_to_original = (
        mapped.get("sourceKind") == "original"
        and mapped.get("sourcePath") == item["image"]
        and mapped.get("sourceSha256") == item.get("sha256")
    )
    review_status = item.get("visualReviewStatus", mapped.get("visibleTitleReviewStatus", "pending"))
    audit = {
        "status": "verified-match" if mapped_to_original and review_status == "verified-match" else "pending-original-review",
        "observedTitle": item["name"] if review_status == "verified-match" else None,
        "sourceMappingVerified": mapped_to_original,
    }
    profile = concept_profile(item["name"], item["category"], item["subcategory"])
    mismatch = audit["status"] != "verified-match"
    thumbnail_is_concept_proof = audit["status"] == "verified-match"
    rule = {
        "schemaVersion": 1,
        "id": rule_id,
        "displayName": f"{item['id']} · {item['name']}",
        "status": "active",
        "kind": "independent-cover-layout-rule",
        "source": {
            "repository": REPO,
            "commit": COMMIT,
            "catalogId": item["id"],
            "catalogName": item["name"],
            "category": item["category"],
            "subcategory": item["subcategory"],
            "originalImagePath": item["image"],
            "originalImageUrl": RAW_ROOT + item["image"],
            "originalImageSha256": item["sha256"],
            "localThumbnail": f"../references/source-thumbnails/{item['id']}.jpg",
            "localThumbnailSha256": sha256(thumb),
            "visualAudit": audit,
            "useThumbnailAsConceptProof": thumbnail_is_concept_proof,
            "upstreamCatalogClaim": item.get("catalogClaim"),
        },
        "selection": {
            "autoSelectable": not mismatch,
            "coverSuitability": profile["coverSuitability"],
            "tags": profile["tags"],
            "assetTypes": profile["assetTypes"],
            "titleLengths": profile["titleLengths"],
            "subjectCounts": profile["subjectCounts"],
            "supportedRatios": ["3:4", "4:3", "16:9"],
        },
        "layoutContract": {
            "primaryMechanism": profile["mechanism"],
            "dominantAxis": profile["axis"],
            "primaryFocus": profile["focus"],
            "readingPath": profile["readingPath"],
            "locked": [
                f"以“{item['name']}”作为唯一主构图机制，不与其他编号的骨架混用。",
                f"保持 {profile['axis']} 主轴、{profile['focus']} 焦点和 {profile['readingPath']} 阅读顺序。",
                "保持主标题、主体、辅助信息的视觉等级，不允许三个层级平均抢眼。",
                "先保护参考中的留白与主体识别区，再适配文字长度。",
            ],
            "adaptive": [
                "标题原文、逐字字形与合理换行。",
                "素材在既定主体区域内的裁切和缩放。",
                "已选字体风格与已批准配色方案。",
                "跨平台比例对应的独立布局变体。",
            ],
            "optional": [
                "副标题、标签、角标和署名仅在不改变阅读顺序时出现。"
            ],
            "forbidden": [
                "自由混合多个布局规则",
                "为容纳长标题改变主轴或主体左右关系",
                "拉伸整张参考图适配其他比例",
                "用装饰元素填满受保护留白",
                "让 AI 同时重新设计构图、字体和配色",
            ],
        },
        "runtime": {
            "input": ["title", "assets", "canvasRatio", "fontStyleId", "paletteId"],
            "output": ["layoutPlan", "renderedCover", "thumbnailPreview", "qaResult"],
            "referencePolicy": "load-this-rule-only",
            "crossRatioPolicy": "use-explicit-variant-never-stretch",
            "titleOverflowPolicy": "rewrite-without-changing-facts-then-limited-size-adjustment",
        },
        "qa": {
            "hardGates": [
                "selected-rule-id-preserved",
                "single-primary-focus",
                "declared-reading-path-preserved",
                "subject-critical-region-visible",
                "title-readable-at-360px",
                "no-text-or-subject-collision",
                "no-unapproved-layout-mixing",
            ],
            "humanReview": [
                "第一眼焦点与内容重点一致",
                "缩略图仍能看出该编号的构图身份",
                "文字、人物和留白之间有明确呼吸",
            ],
        },
    }
    if anatomy_path.exists():
        anatomy = json.loads(anatomy_path.read_text(encoding="utf-8"))
        rule["templateAnatomy"] = {
            "status": anatomy.get("analysisStatus", "pending"),
            "ref": f"../anatomy/{rule_id}.json",
        }
    knowledge_path = KNOWLEDGE / f"{rule_id}.json"
    if knowledge_path.exists():
        knowledge = json.loads(knowledge_path.read_text(encoding="utf-8"))
        rule["compositionKnowledge"] = {
            "status": knowledge.get("learningStatus", "pending"),
            "ref": f"../knowledge/{rule_id}.json",
        }
    return rule


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    RULES.mkdir(parents=True, exist_ok=True)
    registry = {
        "schemaVersion": 2,
        "sourceCommit": COMMIT,
        "sourceAuthority": "visual-truth-catalog.json",
        "upstreamCatalogWarning": "The upstream v2 filenames and embedded visual titles diverge for 336 of 350 items. Selection follows the visible title recorded in visual-truth-catalog.json.",
        "defaultSelectionMode": "content-fit-ranked",
        "rules": [],
    }
    for item in data:
        rule = make_rule(item)
        path = RULES / f"{rule['id']}.json"
        path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        registry["rules"].append({
            "id": rule["id"],
            "displayName": rule["displayName"],
            "category": item["category"],
            "subcategory": item["subcategory"],
            "status": rule["status"],
            "autoSelectable": rule["selection"]["autoSelectable"],
            "coverSuitability": rule["selection"]["coverSuitability"],
            "visualAuditStatus": rule["source"]["visualAudit"]["status"],
            "useThumbnailAsConceptProof": rule["source"]["useThumbnailAsConceptProof"],
            "anatomyStatus": rule.get("templateAnatomy", {}).get("status", "pending"),
            "knowledgeStatus": rule.get("compositionKnowledge", {}).get("status", "pending"),
            "renderReady": (
                rule.get("compositionKnowledge", {}).get("status") == "studied"
                and rule["source"]["visualAudit"]["status"] == "verified-match"
            ),
            "rule": f"rules/{rule['id']}.json",
            **({"anatomy": f"anatomy/{rule['id']}.json"} if "templateAnatomy" in rule else {}),
            **({"knowledge": f"knowledge/{rule['id']}.json"} if "compositionKnowledge" in rule else {}),
            "thumbnail": f"references/source-thumbnails/{item['id']}.jpg",
        })
    (ROOT / "registry.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"built {len(registry['rules'])} independent layout rules")


if __name__ == "__main__":
    main()
