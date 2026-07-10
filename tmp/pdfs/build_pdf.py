# -*- coding: utf-8 -*-
"""AI 学习·使用·时间管理 — 新手入门指南 PDF"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, KeepTogether, NextPageTemplate
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FONT_REG = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
pdfmetrics.registerFont(TTFont("SansSC", FONT_REG))
pdfmetrics.registerFont(TTFont("SansSC-Bold", FONT_REG))
registerFontFamily("SansSC", normal="SansSC", bold="SansSC-Bold", italic="SansSC", boldItalic="SansSC-Bold")

INK       = colors.HexColor("#0F172A")
INK_SOFT  = colors.HexColor("#334155")
MUTED     = colors.HexColor("#64748B")
LINE      = colors.HexColor("#E2E8F0")
BG_SOFT   = colors.HexColor("#F8FAFC")
ACCENT    = colors.HexColor("#2563EB")
ACCENT_2  = colors.HexColor("#0EA5E9")
ACCENT_3  = colors.HexColor("#10B981")
WARN      = colors.HexColor("#F59E0B")
DANGER    = colors.HexColor("#DC2626")

OUT_PDF = r"D:\valut\agent\output\pdf\AI学习·使用·时间管理-新手入门指南.pdf"

PAGE_W, PAGE_H = A4
M_X, M_Y = 18*mm, 18*mm
CONTENT_W = PAGE_W - 2*M_X

def draw_chrome(canv, doc):
    canv.saveState()
    canv.setStrokeColor(LINE); canv.setLineWidth(0.5)
    canv.line(M_X, PAGE_H - 12*mm, PAGE_W - M_X, PAGE_H - 12*mm)
    canv.setFillColor(MUTED); canv.setFont("SansSC", 8)
    canv.drawString(M_X, PAGE_H - 10*mm, "AI 学习·使用·时间管理 · 新手入门指南")
    canv.drawRightString(PAGE_W - M_X, PAGE_H - 10*mm, "v1.0  ·  2026-07-10")
    canv.line(M_X, 14*mm, PAGE_W - M_X, 14*mm)
    canv.setFont("SansSC", 8)
    canv.drawString(M_X, 10*mm, "D:\\valut\\agent")
    canv.drawRightString(PAGE_W - M_X, 10*mm, f"— {doc.page} —")
    canv.setFillColor(ACCENT);   canv.rect(M_X,        8*mm, 6*mm, 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_2); canv.rect(M_X + 7*mm, 8*mm, 6*mm, 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_3); canv.rect(M_X + 14*mm,8*mm, 6*mm, 1.2*mm, stroke=0, fill=1)
    canv.restoreState()

def draw_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(colors.HexColor("#0F172A"))
    canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canv.setFillColor(ACCENT);   canv.rect(0, PAGE_H - 18*mm, PAGE_W, 4*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_2); canv.rect(0, PAGE_H - 22*mm, PAGE_W, 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_3); canv.rect(0, PAGE_H - 24*mm, PAGE_W, 0.6*mm, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor("#94A3B8"))
    canv.setFont("SansSC", 12)
    canv.drawString(M_X, PAGE_H - 45*mm, "AI · AGENT · WORKFLOW")
    canv.setFillColor(colors.HexColor("#F8FAFC"))
    canv.setFont("SansSC", 30)
    canv.drawString(M_X, PAGE_H - 70*mm, "学习 · 使用 · 时间管理")
    canv.setFillColor(ACCENT_2)
    canv.setFont("SansSC", 22)
    canv.drawString(M_X, PAGE_H - 82*mm, "新手入门指南")
    canv.setFillColor(colors.HexColor("#CBD5E1"))
    canv.setFont("SansSC", 11)
    desc_lines = [
        "一份给第一次接触 AI Agent 的新手准备的实战手册",
        "从看懂知识库、到第一次跑通 AI 助手、再到用 AI 节省每天的时间",
    ]
    y = PAGE_H - 100*mm
    for line in desc_lines:
        canv.drawString(M_X, y, line); y -= 6*mm
    box_y = 55*mm
    canv.setFillColor(colors.HexColor("#1E293B"))
    canv.roundRect(M_X, box_y, CONTENT_W, 38*mm, 4*mm, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor("#334155"))
    canv.roundRect(M_X, box_y, CONTENT_W, 38*mm, 4*mm, stroke=1, fill=0)
    canv.setFillColor(colors.HexColor("#94A3B8"))
    canv.setFont("SansSC", 9)
    canv.drawString(M_X + 8*mm, box_y + 30*mm, "适用读者")
    canv.setFillColor(colors.HexColor("#F8FAFC"))
    canv.setFont("SansSC", 11)
    info_pairs = [
        ("版本", "v1.0"), ("更新", "2026-07-10"),
        ("读者", "零基础新手 / 想用 AI 提效的同学"),
        ("预计阅读", "30 分钟"),
    ]
    for i, (k, v) in enumerate(info_pairs):
        col = i % 2; row = i // 2
        x = M_X + 8*mm + col * (CONTENT_W/2 - 2*mm)
        y2 = box_y + 22*mm - row * 10*mm
        canv.setFillColor(colors.HexColor("#94A3B8"))
        canv.setFont("SansSC", 9); canv.drawString(x, y2, k)
        canv.setFillColor(colors.HexColor("#F8FAFC"))
        canv.setFont("SansSC", 11); canv.drawString(x + 20*mm, y2, v)
    canv.setFillColor(ACCENT);   canv.circle(M_X + 4*mm,  25*mm, 1.5*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_2); canv.circle(M_X + 10*mm, 25*mm, 1.5*mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT_3); canv.circle(M_X + 16*mm, 25*mm, 1.5*mm, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor("#64748B"))
    canv.setFont("SansSC", 8)
    canv.drawString(M_X + 24*mm, 24*mm, "Build with Codex · Rendered by ReportLab")
    canv.restoreState()

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="SansSC-Bold", fontSize=22, leading=28, textColor=INK, spaceBefore=4, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="SansSC-Bold", fontSize=15, leading=20, textColor=INK, spaceBefore=14, spaceAfter=6)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="SansSC-Bold", fontSize=12, leading=16, textColor=ACCENT, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="SansSC", fontSize=10.5, leading=17, textColor=INK_SOFT, spaceAfter=6, alignment=0)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=9, leading=13, textColor=MUTED)
CODE = ParagraphStyle("Code", fontName="SansSC", fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), backColor=BG_SOFT, leftIndent=8, rightIndent=8, spaceBefore=2, spaceAfter=2)
TOC1 = ParagraphStyle("TOC1", fontName="SansSC-Bold", fontSize=12, leading=22, textColor=INK)
TOC2 = ParagraphStyle("TOC2", fontName="SansSC", fontSize=10.5, leading=18, textColor=INK_SOFT, leftIndent=14)
CELL = ParagraphStyle("Cell", fontName="SansSC", fontSize=9.5, leading=14, textColor=INK_SOFT)
CELL_B = ParagraphStyle("CellB", fontName="SansSC-Bold", fontSize=9.5, leading=14, textColor=ACCENT)

def HLine():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=4, spaceAfter=8)

def callout(title, body, accent=ACCENT):
    inner = [
        Paragraph(f'<b>{title}</b>', ParagraphStyle("cH", fontName="SansSC-Bold", fontSize=10.5, leading=14, textColor=accent)),
        Paragraph(body, BODY),
    ]
    t = Table([inner], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BG_SOFT),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LINEBEFORE", (0,0), (0,-1), 2.4, accent),
        ("BOX", (0,0), (-1,-1), 0.25, LINE),
    ]))
    return t

def bullet_list(items):
    return [Paragraph(f"· {it}", BODY) for it in items]

def checklist_table(rows):
    data = [Paragraph("<font color='#94A3B8'>☐</font>",
                       ParagraphStyle("cb", fontName="SansSC-Bold", fontSize=13, leading=18, textColor=colors.HexColor("#94A3B8"))),
             Paragraph(t, BODY)] for t in rows]
    t = Table(data, colWidths=[9*mm, CONTENT_W - 9*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LINEBELOW", (0,0), (-1,-2), 0.25, LINE),
    ]))
    return t

def two_col(left, right):
    w = CONTENT_W
    col0 = w / 2 - 4*mm; col1 = w / 2 - 4*mm
    t = Table([left, right], colWidths=[col0, col1])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (0,0), 8*mm),
        ("RIGHTPADDING", (1,0), (1,0), 0),
        ("BACKGROUND", (0,0), (-1,-1), BG_SOFT),
        ("BOX", (0,0), (-1,-1), 0.25, LINE),
        ("LEFTPADDING", (0,0), (0,0), 6),
        ("LEFTPADDING", (1,0), (1,0), 6),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def section_num(n, title):
    return Paragraph(f'<font color="{ACCENT.hexval()}"><b>{n:02d}</b></font>  <font color="{INK.hexval()}"><b>{title}</b></font>', H1)

def code_block(text):
    return Paragraph(text.replace("\n", "<br/>"), CODE)

def para_cell(text, style=CELL):
    return Paragraph(text, style)

doc = BaseDocTemplate(OUT_PDF, pagesize=A4,
                      leftMargin=M_X, rightMargin=M_X, topMargin=18*mm, bottomMargin=18*mm,
                      title="AI 学习·使用·时间管理-新手入门指南",
                      author="Agent Environment Operator")
frame = Frame(M_X, M_Y, CONTENT_W, PAGE_H - 2*M_Y - 6*mm, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
    PageTemplate(id="Body", frames=[frame], onPage=draw_chrome),
])

story = []

# ---- 封面 ----
story.append(Spacer(1, 1))
story.append(NextPageTemplate("Body"))
story.append(PageBreak())

# ---- 致读者 + 目录(同一页密集排版) ----
story.append(Paragraph("致读者", H1))
story.append(HLine())
story.append(Paragraph(
    "如果你第一次接触 <b>AI Agent</b>(能帮你写代码、查资料、跑命令的智能助手),这本小册子就是为你准备的。"
    "我们不会讲太多术语,只会陪你走三步: <b>看懂</b>、<b>用上</b>、<b>省时间</b>。",
    BODY))
story.append(Paragraph(
    "这本指南来自 <font color=\"#2563EB\"><b>D:\\valut\\agent</b></font> 项目,它的核心是一份「知识库 + 工具箱」——"
    "读完这 30 分钟,你就能独立启动一个 AI 助手,让它每天替你省下一小时。",
    BODY))
story.append(callout(
    "[ 阅读建议 ]",
    "不需要一次读完。建议顺序:第 1-3 章一次看完(15 分钟)建立认知,然后照着第 6 章「实战 7 天」边做边学。过程中遇到名词不懂,直接查第 7 章 FAQ。",
    accent=ACCENT,
))

story.append(Spacer(1, 6))
story.append(Paragraph("目录", H1))
story.append(HLine())
toc_items = [
    ("01", "认识 AI 助手 —— 它是什么、能做什么"),
    ("",    "1.1 什么是 AI Agent"),
    ("",    "1.2 你能拿来干什么"),
    ("",    "1.3 知识库 00-AgentBase 是什么"),
    ("02", "学习路径 —— 三步法:看 → 试 → 用"),
    ("",    "2.1 推荐阅读顺序"),
    ("",    "2.2 学习节奏(每天 30 分钟)"),
    ("03", "快速上手 —— 零基础跑通你的第一个 Agent"),
    ("",    "3.1 准备工作"),
    ("",    "3.2 安装 Runtime"),
    ("",    "3.3 第一次对话"),
    ("",    "3.4 加载资产(Skills / Plugins / MCP)"),
    ("04", "时间管理 —— 让 AI 替你省时间"),
    ("",    "4.1 AI 能省时间的三类场景"),
    ("",    "4.2 自动化任务模板"),
    ("",    "4.3 每日 / 每周时间表"),
    ("05", "安全边界 —— 新手必知的三条线"),
    ("06", "实战 7 天 —— Day 1 到 Day 7 任务卡"),
    ("07", "自检与 FAQ"),
]
for num, title in toc_items:
    if num:
        story.append(Paragraph(f'<font color="{ACCENT.hexval()}"><b>{num}</b></font>   {title}', TOC1))
    else:
        story.append(Paragraph(title, TOC2))

story.append(PageBreak())

# === 01 认识 AI 助手 ===
story.append(section_num(1, "认识 AI 助手"))
story.append(HLine())
story.append(Paragraph("1.1 什么是 AI Agent", H2))
story.append(Paragraph(
    "<b>AI Agent</b>(智能体) = 一个能理解你意图、调用工具、自主完成多步任务的 AI 程序。"
    "和普通的聊天 AI 不同,它不仅会回答问题,还会<b>动手做事</b>——读文件、写代码、跑命令、查网页。",
    BODY))
story.append(Paragraph(
    "你可以把它理解成「一位住在你电脑里的实习生」:你告诉它目标,它在你的许可范围内自己想办法。",
    BODY))
story.append(Paragraph("1.2 你能拿来干什么", H2))
story.append(Paragraph("对新手来说,以下几类任务最容易立刻见效:", BODY))
story.extend(bullet_list([
    "<b>查资料</b>:问 AI 帮你读文档、对比方案、翻译资料",
    "<b>写文档</b>:起草周报、生成 README、写技术笔记",
    "<b>改文件</b>:批量重命名、格式转换、批量改文案",
    "<b>跑命令</b>:在沙箱里跑构建脚本、生成报告 PDF",
    "<b>学知识</b>:让 AI 当你的私教,边问边学",
]))
story.append(Paragraph("1.3 知识库 00-AgentBase 是什么", H2))
story.append(Paragraph(
    "本项目根目录的 <font color=\"#2563EB\"><b>00-AgentBase/</b></font> 是一个「AI Agent 百科全书」——"
    "人类可以读懂,AI 也可以当作 wiki 检索。它分为 7 大模块:",
    BODY))
modules = [
    ["模块", "内容", "新手先看"],
    ["00-human/", "Agent 的本质与人类协作", "可选"],
    ["01-AgentBase总览", "整体目录与结构", "★ 推荐"],
    ["02-.../", "Agent 的能力与边界", "★ 推荐"],
    ["03-知识地图", "全知识库索引", "★ 推荐"],
    ["behavior/", "Skill / Prompt 怎么设计", "进阶"],
    ["runtime/", "Claude Code / Codex / Hermes 专题", "★ 用前必读"],
    ["safety/", "安全边界与限制", "★ 必读"],
    ["tools/", "Plugin / MCP 工具配置", "进阶"],
]
m_rows = []
for r_idx, row in enumerate(modules):
    cells = []
    for c_idx, txt in enumerate(row):
        if r_idx == 0:
            cells.append(para_cell(txt, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)))
        else:
            if c_idx == 0:
                cells.append(para_cell(txt, ParagraphStyle("c0", fontName="SansSC", fontSize=9.5, leading=14, textColor=INK)))
            elif c_idx == 1:
                cells.append(para_cell(txt, CELL))
            else:
                star = "★" in txt
                cells.append(para_cell(txt, ParagraphStyle("c2", fontName="SansSC-Bold" if star else "SansSC", fontSize=9.5, leading=14, textColor=ACCENT if star else MUTED, alignment=1)))
    m_rows.append(cells)
m_tbl = Table(m_rows, colWidths=[42*mm, 80*mm, 38*mm])
m_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(m_tbl)
story.append(Spacer(1, 4))
story.append(callout(
    "[ 提示 ]",
    "看不懂某个名词没关系。打开 <font color=\"#2563EB\"><b>00-AgentBase/03-知识地图.md</b></font>,"
    "它是整本百科的索引页,会告诉你每篇文档讲什么、什么时候读。",
    accent=ACCENT_3,
))
story.append(PageBreak())

# === 02 学习路径 ===
story.append(section_num(2, "学习路径"))
story.append(HLine())
story.append(Paragraph("2.1 推荐阅读顺序", H2))
story.append(Paragraph("按下面这个顺序读,最快建立完整认知:", BODY))
steps_data = []
for title, body, c in [
    ("[1] 看 5 分钟", "读 00-AgentBase 总览 + 知识地图,知道「有什么」", ACCENT),
    ("[2] 选 1 个 Runtime", "从 Claude Code / Codex / Hermes 选一个,读对应专题的开篇", ACCENT_2),
    ("[3] 跑 1 次", "按第 3 章「快速上手」装好,跑通最小任务", ACCENT_3),
    ("[4] 读 1 篇", "挑一篇你最想用的 Skill / Plugin 看完整流程", WARN),
    ("[5] 复盘 5 分钟", "用笔记写下:今天我让 AI 做了什么、用了多久、明天还能做什么", ACCENT),
]:
    steps_data.append([para_cell(f'<font color="{c.hexval()}"><b>{title}</b></font>',
                                  ParagraphStyle("st", fontName="SansSC-Bold", fontSize=11, leading=14, textColor=c)),
                       para_cell(body)])
t = Table(steps_data, colWidths=[40*mm, CONTENT_W - 40*mm])
t.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [BG_SOFT, colors.white]),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LINEBEFORE", (0,0), (0,-1), 3, colors.HexColor("#E2E8F0")),
]))
story.append(t)
story.append(Paragraph("2.2 学习节奏(每天 30 分钟)", H2))
rhythm = [
    ["时间", "做什么", "产出"],
    ["第 1 周 每天 30 min", "读 00 总览 + 一个 Runtime 专题", "能讲清「Agent 是什么」"],
    ["第 2 周 每天 30 min", "跑第 3 章最小任务,试 3-5 个 Skill", "能完成 1 个真实小项目"],
    ["第 3 周 每天 30 min", "接入 1 个 Plugin 或 MCP", "工具箱扩展 +1"],
    ["第 4 周 每天 30 min", "搭一个自动化脚本(见第 4 章)", "每天省 30 min 时间"],
]
rh_rows = [para_cell(c) for c in row] for row in rhythm]
rh_tbl = Table(rh_rows, colWidths=[42*mm, 72*mm, CONTENT_W - 42*mm - 72*mm])
rh_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
rh_tbl.setStyle(TableStyle([("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"SansSC-Bold")]))
story.append(rh_tbl)
story.append(PageBreak())

# === 03 快速上手 ===
story.append(section_num(3, "快速上手"))
story.append(HLine())
story.append(Paragraph("3.1 准备工作", H2))
prep_left = [
    para_cell("<b>硬件</b>", ParagraphStyle("hh", fontName="SansSC-Bold", fontSize=10.5, textColor=ACCENT, leading=14)),
    para_cell("· 现代 PC(Mac / Windows / Linux 均可)", SMALL),
    para_cell("· 8 GB 内存以上,能跑 IDE 更佳", SMALL),
    Spacer(1, 4),
    para_cell("<b>账户</b>", ParagraphStyle("hh", fontName="SansSC-Bold", fontSize=10.5, textColor=ACCENT, leading=14)),
    para_cell("· 一个 AI 模型 API Key(Claude / OpenAI 任一)", SMALL),
    para_cell("· GitHub 账号(用于同步资产)", SMALL),
]
prep_right = [
    para_cell("<b>软件</b>", ParagraphStyle("hh", fontName="SansSC-Bold", fontSize=10.5, textColor=ACCENT_2, leading=14)),
    para_cell("· Node.js 18+(Runtime 多数用 JS)", SMALL),
    para_cell("· Python 3.10+(跑脚本用)", SMALL),
    para_cell("· Git(同步仓库)", SMALL),
    Spacer(1, 4),
    para_cell("<b>网络</b>", ParagraphStyle("hh", fontName="SansSC-Bold", fontSize=10.5, textColor=ACCENT_2, leading=14)),
    para_cell("· 能访问 npm / pypi / github.com", SMALL),
    para_cell("· 必要时准备代理", SMALL),
]
story.append(two_col(prep_left, prep_right))
story.append(Spacer(1, 8))
story.append(Paragraph("3.2 安装 Runtime", H2))
story.append(Paragraph("新手推荐从下面 3 个 Runtime 中选一个(选一个即可,不要贪多):", BODY))
rt_data = [
    ["Runtime", "特点", "适合谁", "上手命令"],
    ["Claude Code", "工具丰富 / Hooks / 子代理", "想深度定制的人", "npm i -g @anthropic-ai/claude-code"],
    ["Codex CLI", "安全审批 / 自定义技能", "看重安全的人", "npm i -g @openai/codex"],
    ["Hermes Agent", "轻量 / 定时任务 / 网关", "想跑自动化的同学", "见 Hermes 文档"],
]
rt_rows = [para_cell(c) for c in row] for row in rt_data]
rt_rows[0] = [para_cell(c, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)) for c in rt_data[0]
rt_tbl = Table(rt_rows, colWidths=[30*mm, 38*mm, 32*mm, 48*mm])
rt_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(rt_tbl)
story.append(Spacer(1, 4))
story.append(callout(
    "[ 新手建议 ]",
    "如果只能选一个:<b>Codex CLI</b> 审批机制完善,出错时不容易翻车。装好后用 <font color=\"#0F172A\"><b>codex --help</b></font> 验证。",
    accent=ACCENT,
))
story.append(Paragraph("3.3 第一次对话", H2))
story.append(Paragraph("第一次跑通,做 3 件事就够:", BODY))
story.extend(bullet_list([
    "<b>身份问候</b>:输入 <font color=\"#0F172A\"><b>你好,我是新手,请自我介绍</b></font>,看 AI 是否正常响应",
    "<b>读一个文件</b>:让 AI 读 <font color=\"#0F172A\"><b>D:\\valut\\agent\\AGENTS.md</b></font> 的前 50 行,体验「让 AI 替你读文档」",
    "<b>跑一个命令</b>:让 AI 列出 <font color=\"#0F172A\"><b>D:\\valut\\agent\\01-Skills\\</b></font> 下的目录,体验「让 AI 替你动手」",
]))
story.append(callout(
    "[ 通过标准 ]",
    "3 个任务都成功完成 = Runtime 已可用。失败请检查:① API Key 是否设置 ② 网络是否通畅 ③ 权限审批是否点了同意。",
    accent=ACCENT_3,
))
story.append(Paragraph("3.4 加载资产(Skills / Plugins / MCP)", H2))
story.append(Paragraph("本项目把 Skill / Plugin / Prompt / MCP 沉淀在 01-06 工具箱目录,加载方式:", BODY))
story.append(code_block(
    "01-Skills/      → AI 技能(写作、读图、跑测试)  → 部署到 Runtime 的 skills 目录<br/>"
    "02-Plugins/     → 插件(扩展工具能力)          → 按插件 README 安装<br/>"
    "03-Prompts/     → 验证过的提示词模板            → 直接复制到 System Prompt<br/>"
    "04-MCP/         → MCP Server(连接外部数据)     → 写到 Runtime 的 MCP 配置<br/>"
    "05-Boundaries/  → 安全边界规则                  → 写到 Runtime 的权限配置<br/>"
    "06-Migration/   → Runtime 迁移 Playbook         → 切换 Runtime 时参考"
))
story.append(Paragraph("新手只需要记住一个原则: <b>需要什么 → 去对应目录找 → 按目录里的 AGENTS.md 操作</b>。", BODY))
story.append(Spacer(1, 6))
story.append(callout(
    "[小贴士]",
    "不要贪多。第一周先<b>只用 01-Skills/</b> 里的 skill，跑通 3 个真实任务后再加插件。",
    accent=WARN,
))
story.append(Spacer(1, 4))
# === 04 时间管理 ===
story.append(KeepTogether([section_num(4, "时间管理"), HLine(), Paragraph("用 AI 把每天重复的事自动化,留下时间做重要的事。", BODY)]))
story.append(HLine())
story.append(Paragraph("4.1 AI 能省时间的三类场景", H2))
scenes = [
    ["类型", "例子", "节省", "难度"],
    ["资料整理", "读完 20 篇网页 → 一页摘要", "30 min/次", "★"],
    ["重复写作", "周报 / 邮件 / 文档模板", "15 min/次", "★"],
    ["代码工作流", "改文件 / 跑测试 / 生成报告", "1 h/天", "★★"],
    ["学习陪练", "边问边学 / 模拟面试 / 解释概念", "20 min/次", "★"],
    ["定时任务", "每天 9 点生成日报", "持续省时", "★★★"],
]
sc_rows = [para_cell(c) for c in row] for row in scenes]
sc_rows[0] = [para_cell(c, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)) for c in scenes[0]
sc_tbl = Table(sc_rows, colWidths=[28*mm, 60*mm, 36*mm, 24*mm])
sc_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("ALIGN", (3,1), (3,-1), "CENTER"),
    ("TEXTCOLOR", (3,1), (3,-1), WARN),
    ("FONTNAME", (3,1), (3,-1), "SansSC-Bold"),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(sc_tbl)
story.append(Paragraph("4.2 自动化任务模板", H2))
story.append(Paragraph("复制下面任意一条,直接发给 AI:", BODY))
story.extend(bullet_list([
    "<b>模板 1:周报生成器</b> — 读取 git log 和本周文档 → 生成 Markdown 周报",
    "<b>模板 2:资料摘要</b> — 粘贴 5-10 个网页 URL → 输出 1 页关键信息摘要",
    "<b>模板 3:学习笔记</b> — 输入一段录音或视频字幕 → 生成结构化笔记",
    "<b>模板 4:每日复盘</b> — 回答 5 个问题 → 自动追加到 memory/daily/YYYY-MM-DD.md",
    "<b>模板 5:周计划</b> — 上传本月目标 → 自动拆分到 4 周,再拆分到每日 3 件要事",
]))
story.append(Paragraph("4.3 每日 / 每周时间表", H2))
daily = [
    ["时段", "动作", "工具", "省时"],
    ["08:30", "让 AI 摘要昨晚邮件和消息", "MCP / 摘要 skill", "10 min"],
    ["09:00", "用 AI 拆解今日 3 件要事", "周计划模板", "5 min"],
    ["12:30", "上午产出 → 让 AI 整理半日小结", "摘要 skill", "10 min"],
    ["17:30", "下班前 → 让 AI 起草明日清单 + 邮件草稿", "写作 skill", "15 min"],
    ["周五 17:00", "生成本周周报 + 下周计划", "周报模板", "30 min"],
]
d_rows = [para_cell(c) for c in row] for row in daily]
d_rows[0] = [para_cell(c, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)) for c in daily[0]
d_tbl = Table(d_rows, colWidths=[28*mm, 60*mm, 38*mm, 22*mm])
d_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT_3),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("ALIGN", (3,1), (3,-1), "CENTER"),
    ("TEXTCOLOR", (3,1), (3,-1), ACCENT_3),
    ("FONTNAME", (3,1), (3,-1), "SansSC-Bold"),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(d_tbl)
story.append(Spacer(1, 4))
story.append(callout(
    "[ 真实收益 ]",
    "坚持使用 1 个月,大多数同学每天可省下 30-60 分钟。瓶颈不在 AI,而在<b>你愿不愿意坚持用</b>。",
    accent=ACCENT_3,
))
story.append(PageBreak())

# === 05 安全边界 ===
story.append(section_num(5, "安全边界"))
story.append(HLine())
story.append(Paragraph("新手只要记住三条线:", BODY))
story.append(Paragraph("① 永远不要把密钥直接粘贴给 AI", H3))
story.append(Paragraph(
    "API Key / 数据库密码 / 私人 Token 都不应该出现在对话里。先把密钥写到本地 <font color=\"#0F172A\"><b>.env</b></font> 或 <font color=\"#0F172A\"><b>~/.config/</b></font>,AI 通过变量名引用即可。",
    BODY))
story.append(Paragraph("② 危险命令先看再跑", H3))
story.append(Paragraph(
    "凡是涉及 <font color=\"#0F172A\"><b>rm / format / drop / reset --hard</b></font> 的命令,先让 AI 解释一遍,确认无误再放行。Runtime 通常会有审批弹窗,不要无脑全部同意。",
    BODY))
story.append(Paragraph("③ 项目级 + 个人信息严格隔离", H3))
story.append(Paragraph(
    "<b>项目级配置</b>(无敏感信息)纳入 Git 版本控制,和团队共享;<b>local 配置</b>(含 API key、token)写进 <font color=\"#0F172A\"><b>.gitignore</b></font>,只在本机保留。",
    BODY))
story.append(callout(
    "[ 警告 ] 一旦泄露怎么办",
    "立刻吊销旧 key、生成新 key、检查 git 历史是否上传过密钥(<font color=\"#0F172A\"><b>git log -p | grep -i key</b></font>)。已上传的密钥视同公开。",
    accent=DANGER,
))
story.append(PageBreak())

# === 06 实战 7 天 ===
story.append(section_num(6, "实战 7 天"))
story.append(HLine())
story.append(Paragraph("把这份小册子收起来,接下来 7 天照着做:", BODY))
days = [
    ("Day 1 · 认识", "读 00-AgentBase 总览 + 知识地图", "能讲清 Agent 是什么"),
    ("Day 2 · 选型", "选 Claude Code / Codex / Hermes 之一,读专题开篇", "做出选择,装好 Runtime"),
    ("Day 3 · 启动", "完成 3.3 节「第一次对话」3 个任务", "Runtime 可用,能正常对话"),
    ("Day 4 · 资产", "从 01-Skills/ 选 1 个 Skill 部署并跑一次", "Skill 加载成功并可用"),
    ("Day 5 · 工具", "配置 1 个 Plugin 或 MCP(按 README)", "工具箱 +1,能调用外部能力"),
    ("Day 6 · 自动化", "跑通 4.2 节 1 个模板(推荐周报生成器)", "每天省 15-30 min"),
    ("Day 7 · 复盘", "写一篇周记:这周让 AI 做了什么、效果、下周计划", "完成第一轮闭环"),
]
day_data_rows = [
    [para_cell(c, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)) for c in ["日期", "任务", "通过标准"]
]
for d, t, ok in days:
    day_data_rows.append([
        para_cell(f'<font color="{ACCENT.hexval()}"><b>{d}</b></font>',
                  ParagraphStyle("dn", fontName="SansSC-Bold", fontSize=9.5, leading=14, textColor=ACCENT)),
        para_cell(t),
        para_cell(ok),
    ])
d_tbl = Table(day_data_rows, colWidths=[38*mm, 80*mm, CONTENT_W - 38*mm - 80*mm])
d_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(d_tbl)
story.append(Spacer(1, 4))
story.append(callout(
    "[ 目标 ] 7 天目标",
    "目标不是「学会 AI」,而是「让 AI 替你做完一件具体的事」。做完一件,第二件就容易十倍。",
    accent=ACCENT,
))
story.append(PageBreak())

# === 07 自检与 FAQ ===
story.append(section_num(7, "自检与 FAQ"))
story.append(HLine())
story.append(Paragraph("7.1 自检清单(打印出来勾)", H2))
story.append(Paragraph("完成下面所有项 = 你已经超过 90% 的新手:", BODY))
story.append(checklist_table([
    "能讲清 Agent、Skill、Plugin、MCP 四个名词",
    "已选好并装好至少 1 个 Runtime",
    "已跑通最小任务(读文件 + 跑命令 + 对话)",
    "已加载至少 1 个 Skill 或 Plugin",
    "已用过至少 1 个时间管理模板(周报 / 摘要 / 计划)",
    "已读过 05-Boundaries 安全章节,关键信息已隔离",
    "已写完 Day 7 的复盘笔记",
    "已制定下个月持续使用的计划",
]))
story.append(Paragraph("7.2 常见问题 FAQ", H2))
faqs = [
    ("Q1. Runtime 启动报错怎么办?",
     "先看错误码。常见三类:① API Key 没设 → 查环境变量;② 网络不通 → 检查代理;③ 依赖缺失 → 重装对应 Node/Python 包。详细排障见 00-AgentBase/runtime/ 各专题。"),
    ("Q2. Skill 加载了但不生效?",
     "先看 Runtime 的 skills 目录是否正确(项目级 vs 用户级),再看 SKILL.md 里的 frontmatter 是否符合规范。最后让 AI 列出当前已加载的 skill,确认是否真的被识别。"),
    ("Q3. AI 跑出来结果不对?",
     "90% 是 prompt 写得不够具体。把「帮我写周报」换成「我是后端工程师,请基于 git log 生成本周周报,包含完成项、进行中、卡点 3 节,300 字以内」。"),
    ("Q4. 一个任务该不该交给 AI?",
     "判断标准:① 重复 > 2 次 → 值得;② 有清晰输入输出 → 适合;③ 涉及隐私/资金 → 不适合,人工把关。"),
    ("Q5. 怎么知道 AI 真的「学会」了?",
     "看 3 个指标:① 准确率(同类任务通过率 > 80%);② 时长(从 1 小时降到 10 分钟);③ 覆盖面(从 1 个场景扩到 N 个场景)。"),
]
for q, a in faqs:
    story.append(Paragraph(f'<font color="{ACCENT.hexval()}"><b>{q}</b></font>', BODY))
    story.append(Paragraph(a, SMALL))
    story.append(Spacer(1, 4))
story.append(Paragraph("7.3 资源索引", H2))
res = [
    ["名称", "位置"],
    ["知识库总览", "00-AgentBase/01-AgentBase总览.md"],
    ["知识地图", "00-AgentBase/03-知识地图.md"],
    ["部署编排指南", "AGENTS.md(本仓库根目录)"],
    ["Skill 工具箱", "01-Skills/AGENTS.md"],
    ["Plugin 工具箱", "02-Plugins/"],
    ["Prompt 工具箱", "03-Prompts/"],
    ["MCP 配置", "04-MCP/"],
    ["安全边界", "05-Boundaries/"],
    ["迁移 Playbook", "06-Migration/"],
    ["路线图", "99-Roadmap.md"],
]
r_rows = [para_cell(c) for c in row] for row in res]
r_rows[0] = [para_cell(c, ParagraphStyle("h", fontName="SansSC-Bold", fontSize=10, textColor=colors.white, leading=14)) for c in res[0]
for i in range(1, len(r_rows)):
    r_rows[i][1] = para_cell(f'<font color="{ACCENT.hexval()}">{res[i][1]}</font>')
res_block = Table(r_rows, colWidths=[45*mm, CONTENT_W - 45*mm])
res_block.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), INK),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, BG_SOFT]),
    ("BOX", (0,0), (-1,-1), 0.4, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(KeepTogether(res_block))
story.append(Spacer(1, 14))
story.append(HRFlowable(width="40%", thickness=0.8, color=ACCENT, hAlign="CENTER", spaceBefore=2, spaceAfter=8))
story.append(Paragraph(
    '<font color="#64748B">祝你玩得开心 —— 让 AI 替你省下时间,留给真正重要的事。</font>',
    ParagraphStyle("end", parent=BODY, fontName="SansSC", fontSize=10, leading=14, alignment=1))
)

doc.build(story)
print(f"OK: {OUT_PDF}")
print(f"size: {os.path.getsize(OUT_PDF)/1024:.1f} KB")