from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE
from lxml import etree
import copy

# ---------- palette ----------
INK = RGBColor(0x1B, 0x24, 0x30)
MUTED = RGBColor(0x64, 0x74, 0x8B)
BG = RGBColor(0xF7, 0xF9, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xDD, 0xE4, 0xEC)
BLUE = RGBColor(0x25, 0x63, 0xEB)
TEAL = RGBColor(0x0F, 0x9D, 0x8A)
ORANGE = RGBColor(0xE8, 0x73, 0x2A)
PURPLE = RGBColor(0x7C, 0x3A, 0xED)
RED = RGBColor(0xD1, 0x4B, 0x4B)
LIGHT_BLUE = RGBColor(0xEA, 0xF1, 0xFE)
LIGHT_TEAL = RGBColor(0xE7, 0xF6, 0xF3)
LIGHT_ORANGE = RGBColor(0xFD, 0xF0, 0xE6)
LIGHT_PURPLE = RGBColor(0xEF, 0xEA, 0xFD)
LIGHT_RED = RGBColor(0xFB, 0xEC, 0xEC)
SOFT = RGBColor(0xF2, 0xF5, 0xF9)

FONT = "Microsoft YaHei"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, x, y, w, h, fill, line=None, radius=0.06, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.8)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    shp.shadow.inherit = False
    return shp


def tx(slide, x, y, w, h, text, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, line_spacing=1.12, margins=(0, 0, 0, 0), italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb


def bullets(slide, x, y, w, h, items, size=12, color=INK, bullet_color=BLUE, spacing=7, line_spacing=1.12):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        p.space_after = Pt(spacing)
        r0 = p.add_run()
        r0.text = "•  "
        r0.font.name = FONT
        r0.font.size = Pt(size)
        r0.font.bold = True
        r0.font.color.rgb = bullet_color
        r1 = p.add_run()
        r1.text = item
        r1.font.name = FONT
        r1.font.size = Pt(size)
        r1.font.color.rgb = color
    return tb


def header(slide, kicker, title, subtitle=None, page=None, total=14):
    bg(slide)
    rect(slide, 0, 0, 13.333, 0.055, BLUE, shape=MSO_SHAPE.RECTANGLE)
    tx(slide, 0.72, 0.28, 11.0, 0.28, kicker.upper(), size=9.5, color=BLUE, bold=True)
    tx(slide, 0.72, 0.52, 11.9, 0.62, title, size=26, color=INK, bold=True)
    if subtitle:
        tx(slide, 0.72, 1.12, 11.9, 0.34, subtitle, size=12.5, color=MUTED)
    # footer
    rect(slide, 0.72, 7.08, 11.89, 0.008, LINE, shape=MSO_SHAPE.RECTANGLE)
    tx(slide, 0.72, 7.15, 9.0, 0.22, "反无拦截 · 仿真器与训练栈调研", size=8.5, color=MUTED)
    if page:
        tx(slide, 11.9, 7.15, 0.7, 0.22, f"{page:02d} / {total}", size=8.5, color=MUTED, align=PP_ALIGN.RIGHT)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_slide(kicker, title, subtitle=None, page=None):
    s = prs.slides.add_slide(BLANK)
    header(s, kicker, title, subtitle, page)
    return s


def card(slide, x, y, w, h, fill, line=None, accent=None, radius=0.06):
    rect(slide, x, y, w, h, fill, line, radius)
    if accent:
        rect(slide, x, y, 0.07, h, accent, shape=MSO_SHAPE.RECTANGLE)


def table(slide, data, x, y, w, h, col_widths, font_size=10.5, header_size=10.5,
          row_heights=None, align=None):
    rows, cols = len(data), len(data[0])
    shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shape.table
    for i, cw in enumerate(col_widths):
        tbl.columns[i].width = Inches(cw)
    for r in range(rows):
        tbl.rows[r].height = Inches(row_heights[r] if row_heights else h / rows)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.09)
            cell.margin_right = Inches(0.07)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = INK if r == 0 else (WHITE if r % 2 == 1 else SOFT)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (align[c] if align else (PP_ALIGN.LEFT if c == 0 else PP_ALIGN.LEFT))
            run = p.add_run()
            run.text = str(data[r][c])
            run.font.name = FONT
            run.font.size = Pt(header_size if r == 0 else font_size)
            run.font.bold = (r == 0 or c == 0)
            run.font.color.rgb = WHITE if r == 0 else INK
    return tbl


def chip(slide, x, y, w, h, text, fill, color=INK, size=10, bold=True):
    rect(slide, x, y, w, h, fill, None, 0.5)
    tx(slide, x + 0.05, y + 0.02, w - 0.1, h - 0.04, text, size=size, color=color, bold=bold,
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def arrow_right(slide, x, y, w=0.22, h=0.22, color=MUTED):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def arrow_down(slide, x, y, w=0.22, h=0.22, color=MUTED):
    shp = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


# ============================================================
# Slide 1 — cover
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, INK)
rect(s, 0, 0, 13.333, 0.08, ORANGE, shape=MSO_SHAPE.RECTANGLE)
rect(s, 0.78, 1.55, 0.08, 2.25, ORANGE, shape=MSO_SHAPE.RECTANGLE)
tx(s, 1.02, 1.45, 7.4, 0.28, "COUNTER-UAS · SIMULATOR & TRAINING STACK", size=10, color=RGBColor(0x9F,0xB3,0xC8), bold=True)
tx(s, 1.0, 1.85, 7.2, 1.7, "反无拦截：\n仿真器与训练栈调研", size=40, color=WHITE, bold=True, line_spacing=1.08)
tx(s, 1.0, 3.66, 7.4, 0.34, "固定翼 defender × 旋翼 intruder × 单目视觉 × PX4", size=14.5, color=RGBColor(0xC7,0xD3,0xE0))
tx(s, 1.0, 4.12, 7.2, 0.36, "两条线分开选，一套 19-D 契约拼起来", size=15, color=ORANGE, bold=True)
tx(s, 1.0, 6.55, 6.5, 0.28, "2026.10  ·  UAV-Survey / 10.Simulators", size=10, color=RGBColor(0x8A,0x9B,0xAD))

# cover visual
card(s, 8.55, 1.78, 1.9, 1.05, RGBColor(0x24,0x31,0x40), LINE, BLUE, 0.08)
tx(s, 8.72, 1.92, 1.55, 0.28, "SIM", size=13, color=WHITE, bold=True)
tx(s, 8.72, 2.24, 1.55, 0.42, "物理 · 相机 · PX4", size=9, color=RGBColor(0xB8,0xC6,0xD6))
card(s, 10.72, 1.78, 1.9, 1.05, RGBColor(0x24,0x31,0x40), LINE, TEAL, 0.08)
tx(s, 10.89, 1.92, 1.55, 0.28, "STACK", size=13, color=WHITE, bold=True)
tx(s, 10.89, 2.24, 1.55, 0.42, "环境 · 并行 · 部署", size=9, color=RGBColor(0xB8,0xC6,0xD6))
chip(s, 9.75, 3.18, 1.7, 0.38, "19-D 契约", ORANGE, INK, 10)
# connecting lines
ln = s.shapes.add_connector(1, Inches(9.5), Inches(2.84), Inches(10.15), Inches(3.18))
ln.line.color.rgb = RGBColor(0x6B,0x7C,0x90); ln.line.width = Pt(1.2)
ln2 = s.shapes.add_connector(1, Inches(11.5), Inches(2.84), Inches(11.05), Inches(3.18))
ln2.line.color.rgb = RGBColor(0x6B,0x7C,0x90); ln2.line.width = Pt(1.2)
tx(s, 8.55, 3.85, 4.1, 0.72, "不是把所有东西编译成一个软件，\n而是让它们共用一套数据/时间/场景契约。", size=10.5, color=RGBColor(0xA9,0xB9,0xCB), line_spacing=1.3)
notes(s, "封面。先给听众一个总判断：今天不选“全能冠军”，而是把仿真器和训练栈分开选，最后用 19-D 观测契约拼起来。")

# ============================================================
# Slide 2 — one-page conclusion
# ============================================================
s = new_slide("01 · 结论先行", "一页结论", "不选全能冠军，选可替换组件", 2)
items = [
    ("01", "仿真器", "回答：够不够真", "固定翼气动、PX4、相机、多机。", BLUE, LIGHT_BLUE),
    ("02", "训练栈", "回答：训得快不快、部署通不通", "环境接口、并行、感知、部署。", TEAL, LIGHT_TEAL),
    ("03", "连接", "一套 19-D 契约", "换组件，任务定义不重写。", ORANGE, LIGHT_ORANGE),
]
for i, (num, title, sub, body, accent, light) in enumerate(items):
    x = 0.75 + i * 4.0
    card(s, x, 1.75, 3.75, 3.15, light, None, accent, 0.08)
    tx(s, x + 0.28, 2.0, 0.8, 0.45, num, size=22, color=accent, bold=True)
    tx(s, x + 0.28, 2.52, 3.1, 0.4, title, size=18, color=INK, bold=True)
    tx(s, x + 0.28, 2.98, 3.1, 0.55, sub, size=11.5, color=accent, bold=True)
    tx(s, x + 0.28, 3.62, 3.1, 0.9, body, size=11, color=INK, line_spacing=1.25)

rect(s, 0.75, 5.35, 11.85, 0.85, SOFT, LINE, 0.08)
tx(s, 1.0, 5.52, 11.35, 0.5, "仿真器看“真不真”，训练栈看“快不快、通不通”；两者用 19-D 契约拼接，而不是塞进同一个二进制。",
   size=12.5, color=INK, bold=True)
notes(s, "这一页是全场的主结论。左边是仿真器的评价维度，中间是训练栈的评价维度，右边是连接方式。记住三个词：够真、够快、可拼接。")

# ============================================================
# Slide 3 — task constraints
# ============================================================
s = new_slide("02 · 任务约束", "四条链路，一个 19-D 输入", "先看任务需要什么，再看工具能补什么", 3)
constraints = [
    ("固定翼气动", "失速、侧滑、风扰、舵面延迟", BLUE, LIGHT_BLUE),
    ("旋翼 intruder", "定高 50 m、8 m/s 直线飞行", TEAL, LIGHT_TEAL),
    ("单目视觉", "YOLO v11 → 二阶矩 → 虚拟平面", PURPLE, LIGHT_PURPLE),
    ("PX4 闭环", "SITL/HITL、MAVLink、offboard", ORANGE, LIGHT_ORANGE),
]
for i, (t, b, accent, light) in enumerate(constraints):
    x = 0.75 + i * 3.0
    card(s, x, 1.45, 2.82, 1.32, light, None, accent, 0.08)
    tx(s, x + 0.18, 1.58, 2.5, 0.3, t, size=12.5, color=accent, bold=True)
    tx(s, x + 0.18, 1.95, 2.5, 0.62, b, size=9.8, color=INK, line_spacing=1.2)

steps = [
    ("世界 + PX4", "Gazebo / RflySim"),
    ("单目相机", "FOV / 曝光 / 抖动"),
    ("YOLO + 虚拟平面", "7 维视觉特征"),
    ("19-D PPO", "策略推理"),
    ("PX4 offboard", "acc / pitch / yaw"),
]
for i, (t, b) in enumerate(steps):
    x = 0.75 + i * 2.42
    rect(s, x, 3.45, 2.08, 1.35, WHITE, LINE, 0.08)
    tx(s, x + 0.14, 3.58, 1.8, 0.5, t, size=10.8, color=INK, bold=True, line_spacing=1.1)
    tx(s, x + 0.14, 4.14, 1.8, 0.42, b, size=8.8, color=MUTED, line_spacing=1.15)
    if i < 4:
        arrow_right(s, x + 2.14, 3.92, 0.2, 0.2, RGBColor(0xA8,0xB5,0xC4))

rect(s, 0.75, 5.35, 11.85, 0.82, LIGHT_TEAL, None, 0.08)
tx(s, 1.0, 5.5, 11.3, 0.28, "19-D = 7 视觉 + 4 运动学 + 4 姿态 + 3 历史动作 + 1 高度", size=12.5, color=TEAL, bold=True)
tx(s, 1.0, 5.82, 11.3, 0.26, "PPO 输入是特征，不是像素——训练不必每一步照片级渲染。", size=10.2, color=INK)
notes(s, "任务约束决定选型。固定翼气动、旋翼目标、单目视觉、PX4 闭环，四条链路对仿真器的要求不同。关键一句：PPO 吃的是 19 维特征，不是像素。")

# ============================================================
# Slide 4 — why separate
# ============================================================
s = new_slide("03 · 概念边界", "为什么分开：仿真器 ≠ 训练栈", "一个命令可以启动五个进程，但不要把它们当成一个二进制", 4)
card(s, 0.75, 1.5, 5.2, 2.15, LIGHT_BLUE, None, BLUE, 0.08)
tx(s, 1.0, 1.68, 4.6, 0.36, "仿真器", size=16, color=BLUE, bold=True)
tx(s, 1.0, 2.08, 4.7, 0.3, "世界 · 物理 · 相机 · PX4 接口", size=10.8, color=INK, bold=True)
tx(s, 1.0, 2.45, 4.7, 0.55, "回答：够不够真", size=11, color=MUTED)
tx(s, 1.0, 2.88, 4.7, 0.4, "Gazebo / RflySim / JSBSim", size=10, color=BLUE)
card(s, 0.75, 3.95, 5.2, 2.15, LIGHT_TEAL, None, TEAL, 0.08)
tx(s, 1.0, 4.13, 4.6, 0.36, "训练栈", size=16, color=TEAL, bold=True)
tx(s, 1.0, 4.53, 4.7, 0.3, "环境 · 并行 · 学习器 · 部署", size=10.8, color=INK, bold=True)
tx(s, 1.0, 4.90, 4.7, 0.55, "回答：训得快不快、通不通", size=11, color=MUTED)
tx(s, 1.0, 5.33, 4.7, 0.4, "Isaac Lab / RSL-RL / SB3", size=10, color=TEAL)

# right diagram
card(s, 6.55, 1.5, 6.05, 4.6, WHITE, LINE, None, 0.08)
tx(s, 6.82, 1.68, 5.5, 0.32, "一个命令 ≠ 一个进程", size=12.5, color=INK, bold=True)
chip(s, 6.95, 2.12, 4.9, 0.42, "ros2 launch / Python orchestrator", INK, WHITE, 9.5)
# process chips
procs = [("Gazebo", BLUE), ("PX4 ×2", TEAL), ("YOLO", PURPLE), ("PPO", ORANGE), ("MCAP", MUTED)]
for i, (name, col) in enumerate(procs):
    x = 6.95 + (i % 3) * 1.62
    y = 2.92 + (i // 3) * 0.95
    rect(s, x, y, 1.42, 0.55, SOFT, LINE, 0.12)
    tx(s, x + 0.06, y + 0.09, 1.3, 0.3, name, size=9.8, color=col, bold=True, align=PP_ALIGN.CENTER)
    # connector from launcher
    if i < 3:
        ln = s.shapes.add_connector(1, Inches(9.4), Inches(2.54), Inches(x + 0.71), Inches(y))
        ln.line.color.rgb = RGBColor(0xB8,0xC5,0xD4); ln.line.width = Pt(0.8)
tx(s, 6.95, 4.85, 5.3, 0.55, "用户看到的是“一条命令启动一个系统”；\n内部是多个进程 + 一组接口。", size=9.8, color=MUTED, line_spacing=1.25)
tx(s, 6.95, 5.58, 5.3, 0.32, "统一在契约，不在二进制。", size=12, color=ORANGE, bold=True)
notes(s, "这一页消除一个常见误解：统一不等于单体。Gazebo + PX4 + YOLO + PPO 本来就是多进程，ros2 launch 只是把它们串起来。")

# ============================================================
# Slide 5 — simulator landscape
# ============================================================
s = new_slide("04 · 仿真器", "仿真器全景：按角色分，不按品牌分", "只列与固定翼 / 旋翼 / PX4 / 视觉相关的候选", 5)
cols = [
    ("系统闭环", "PX4 / ROS / HIL", "首选：Gazebo Sim + PX4", BLUE, LIGHT_BLUE, ["Gazebo Sim (Jetty)", "RflySim", "XTDrone", "Gazebo Classic (EOL)"]),
    ("气动基准", "配平 / 失速 / 风扰", "首选：JSBSim + FlightGear", ORANGE, LIGHT_ORANGE, ["JSBSim", "FlightGear", "X-Plane"]),
    ("视觉渲染", "相机 / 图像 / 场景", "首选：RflySim / AirSim", PURPLE, LIGHT_PURPLE, ["AirSim", "FlightGoggles", "Flightmare", "UE5 自定义"]),
    ("GPU / 物理", "并行 / 多物理", "首选：Isaac Lab（训练）", TEAL, LIGHT_TEAL, ["Isaac Lab", "MuJoCo / MJX", "Genesis", "Aerial Gym（仅旋翼）"]),
]
for i, (t, sub, pick, accent, light, items) in enumerate(cols):
    x = 0.75 + i * 3.0
    card(s, x, 1.5, 2.82, 4.55, light, None, accent, 0.08)
    tx(s, x + 0.2, 1.68, 2.45, 0.32, t, size=14, color=accent, bold=True)
    tx(s, x + 0.2, 2.03, 2.45, 0.3, sub, size=8.8, color=MUTED)
    for j, it in enumerate(items):
        yy = 2.5 + j * 0.7
        tx(s, x + 0.2, yy, 0.2, 0.25, "·", size=12, color=accent, bold=True)
        tx(s, x + 0.38, yy - 0.01, 2.2, 0.5, it, size=10.5, color=INK, bold=(j == 0), line_spacing=1.1)
    tx(s, x + 0.2, 5.45, 2.45, 0.3, pick, size=8.8, color=accent, bold=True)

tx(s, 0.75, 6.3, 11.85, 0.3, "同名工具可能跨类；分类看主要用途，不否定其他能力。完整 19 个候选见 counter-uav-simulators.html。",
   size=9.2, color=MUTED)
notes(s, "先给全景，不急着排名。四类角色：系统闭环、气动基准、视觉渲染、GPU 物理。听众先建立地图，再看 shortlist。")

# ============================================================
# Slide 6 — simulator shortlist
# ============================================================
s = new_slide("04 · 仿真器", "仿真器 shortlist：七个候选", "每个候选只回答：强在哪、代价是什么、用在哪", 6)
data = [
    ["仿真器", "角色", "强项", "代价 / 边界"],
    ["Gazebo Sim (Jetty)", "系统闭环", "PX4 + advanced_plane + 多机 + HITL", "视觉中等、CPU 单实例"],
    ["RflySim", "工程化闭环", "PX4 + HIL + UE + 固定翼配置", "商业授权、工作流较重"],
    ["JSBSim + FlightGear", "气动基准", "高保真气动、配平/失速/风扰", "无 RL、多机弱"],
    ["AirSim / UE5", "视觉数据", "照片级相机、天气、深度", "固定翼弱、单实例"],
    ["Isaac Lab", "GPU 仿真", "RTX + GPU 并行 + 多模态", "无 PX4、固定翼需自定义"],
    ["MuJoCo / MJX", "控制仿真", "快、易调试、可微路径", "视觉弱、无 PX4"],
    ["Aerial Gym / Flightmare", "旋翼 intruder", "万级并行 / 快速渲染", "仅四旋翼，不能训 defender"],
]
table(s, data, 0.75, 1.48, 11.85, 4.9, [2.35, 1.95, 4.1, 3.45],
      font_size=10.3, header_size=10.5, row_heights=[0.52] + [0.61] * 7)
tx(s, 0.75, 6.55, 11.85, 0.25, "注：表中“强项 / 边界”是面向本任务的主观判断，不是通用 benchmark。", size=8.8, color=MUTED)
notes(s, "这七行是后面结论的依据。注意 Aerial Gym / Flightmare 只适合旋翼 intruder，不能训练固定翼 defender。Gazebo Sim 的强项是系统闭环，不是视觉。")

# ============================================================
# Slide 7 — simulator conclusions
# ============================================================
s = new_slide("04 · 仿真器", "仿真器结论：三条互补线", "系统闭环、气动复核、视觉验证，各用各的", 7)
concl = [
    ("系统闭环", "Gazebo Sim + PX4", "advanced_plane + AVL；rc_cessna 起步；两机 / MAVLink / HITL。", "offboard 切换 / 指令延迟 / 时钟偏差", BLUE, LIGHT_BLUE),
    ("气动复核", "JSBSim + FlightGear", "配平、失速、侧滑、风扰；X-Plane 可选。", "配平误差 / 失速边界 / 风扰响应", ORANGE, LIGHT_ORANGE),
    ("视觉验证", "RflySim / AirSim / UE5", "YOLO 数据、相机内参、虚拟平面误差；Gazebo 相机只做 baseline。", "mAP / s1,s2 误差 / 漏检率", PURPLE, LIGHT_PURPLE),
]
for i, (t, stack, body, accept, accent, light) in enumerate(concl):
    x = 0.75 + i * 4.0
    card(s, x, 1.55, 3.75, 3.55, light, None, accent, 0.08)
    tx(s, x + 0.26, 1.75, 3.2, 0.3, t, size=12.5, color=accent, bold=True)
    tx(s, x + 0.26, 2.15, 3.2, 0.7, stack, size=15, color=INK, bold=True, line_spacing=1.1)
    tx(s, x + 0.26, 2.95, 3.2, 1.25, body, size=10.5, color=INK, line_spacing=1.3)
    tx(s, x + 0.26, 4.25, 3.2, 0.24, "验收", size=8.3, color=MUTED, bold=True)
    tx(s, x + 0.26, 4.51, 3.2, 0.45, accept, size=9.2, color=accent, bold=True, line_spacing=1.15)

rect(s, 0.75, 5.45, 11.85, 0.85, LIGHT_RED, None, 0.08)
tx(s, 0.98, 5.57, 11.4, 0.3, "不要", size=9.5, color=RED, bold=True)
tx(s, 0.98, 5.86, 11.4, 0.3, "Gazebo Classic 已 EOL  ·  AirSim 固定翼弱  ·  Aerial Gym 只训旋翼  ·  “能加载模型” ≠ “气动可信”",
   size=10.3, color=INK, bold=True)
notes(s, "仿真器不需要一个赢家。系统闭环用 Gazebo/RflySim，气动用 JSBSim/FlightGear，视觉用 RflySim/AirSim/UE5。最后一行是四个常见坑。")

# ============================================================
# Slide 8 — training stack anatomy
# ============================================================
s = new_slide("05 · 训练栈", "训练栈是什么：五个部件", "训练栈比的是组织方式，不是单个仿真器", 8)
parts = [
    ("环境接口", "Gymnasium\nmanager terms"),
    ("仿真后端", "Gazebo\nIsaac / MuJoCo"),
    ("学习器", "PPO\nRSL-RL / Brax"),
    ("感知桥", "YOLO\n虚拟平面 / 19-D"),
    ("部署评估", "PX4\nONNX / MCAP"),
]
for i, (t, b) in enumerate(parts):
    x = 0.75 + i * 2.42
    card(s, x, 1.75, 2.08, 1.55, WHITE, LINE, BLUE if i < 2 else (TEAL if i == 2 else (PURPLE if i == 3 else ORANGE)), 0.08)
    tx(s, x + 0.16, 1.9, 1.75, 0.3, t, size=11.5, color=INK, bold=True)
    tx(s, x + 0.16, 2.28, 1.75, 0.8, b, size=9.2, color=MUTED, line_spacing=1.25)
    if i < 4:
        arrow_right(s, x + 2.1, 2.45, 0.2, 0.2, RGBColor(0xA8,0xB5,0xC4))

rect(s, 0.75, 3.85, 11.85, 0.86, SOFT, LINE, 0.08)
tx(s, 1.0, 4.0, 11.3, 0.3, "RSL-RL 是“学习器”，不是仿真器，也不是飞控。", size=12.2, color=TEAL, bold=True)
tx(s, 1.0, 4.33, 11.3, 0.3, "Isaac Lab / mjlab / MuJoCo Playground 都用它做默认 PPO；它不负责 Gazebo/ROS/PX4。",
   size=9.8, color=INK)
tx(s, 0.75, 4.95, 11.85, 0.34, "19-D 观测 + 3-D 动作 → 普通 PPO 问题；差异在环境接口、并行、感知与部署。",
   size=12.2, color=INK, bold=True)
judg = [
    ("接口稳定", "任务可迁移", BLUE, LIGHT_BLUE),
    ("后端可换", "不锁定仿真器", TEAL, LIGHT_TEAL),
    ("学习器独立", "算法可对照", ORANGE, LIGHT_ORANGE),
]
for i, (k, v, accent, light) in enumerate(judg):
    x = 0.75 + i * 4.0
    card(s, x, 5.5, 3.75, 0.9, light, None, accent, 0.08)
    tx(s, x + 0.2, 5.6, 3.3, 0.26, k, size=9.5, color=accent, bold=True)
    tx(s, x + 0.2, 5.88, 3.3, 0.26, v, size=10.5, color=INK, bold=True)
notes(s, "训练栈有五段。RSL-RL 只是第三段“学习器”。很多讨论把 RSL-RL 当成仿真器，这是概念混淆。")

# ============================================================
# Slide 9 — stack shortlist
# ============================================================
s = new_slide("05 · 训练栈", "训练栈 shortlist：六个候选", "只比组织方式：吞吐、视觉、PX4、固定翼、阶段", 9)
data = [
    ["训练栈", "吞吐", "视觉", "PX4", "固定翼", "适合阶段"],
    ["当前 Gazebo + PX4 + PPO", "低", "中", "原生", "中", "系统 / 基线"],
    ["RflySim + Simulink", "中", "高", "原生", "高", "工程化 / HIL"],
    ["Isaac Lab + RSL-RL", "高", "高", "无", "中（需补）", "PPO 规模化"],
    ["MuJoCo + MJX", "高", "低—中", "无", "中（自定义）", "控制 RL"],
    ["JSBSim + Gym", "中", "无", "外接", "高", "气动可信 PPO"],
    ["Aerial Gym / Flightmare", "高", "中—高", "无", "低（旋翼）", "仅 intruder"],
]
table(s, data, 0.75, 1.5, 11.85, 4.55, [2.95, 1.05, 1.05, 0.95, 1.7, 4.15],
      font_size=10.8, header_size=10.5, row_heights=[0.52] + [0.62] * 6)
tx(s, 0.75, 6.3, 11.85, 0.3, "注：吞吐 / 视觉 / 固定翼为定性判断；“中（需补）”意味着要自己建模气动或执行器。",
   size=8.8, color=MUTED)
notes(s, "这一页只比训练栈。当前 Gazebo 栈不是不能用，而是吞吐低；Isaac Lab 吞吐高但没 PX4；RflySim 工程化强但重。Aerial Gym 仍然只适合 intruder。")

# ============================================================
# Slide 10 — stack conclusions
# ============================================================
s = new_slide("05 · 训练栈", "训练栈结论：三种运行模式", "不要用一个栈硬扛训练、系统、视觉", 10)
modes = [
    ("训练模式", "Isaac Lab + RSL-RL\nMuJoCo + MJX", "19-D 特征 + 噪声；GPU 并行；不渲染照片。", "env/s、样本效率、命中率", TEAL, LIGHT_TEAL),
    ("系统模式", "Gazebo Sim + PX4\n+ PPO 推理", "MAVLink、offboard、两机同步、HITL。", "offboard 切换、指令延迟、时钟", BLUE, LIGHT_BLUE),
    ("视觉模式", "RflySim / AirSim / UE5\n+ YOLO", "只做 YOLO 数据与视觉闭环，不进 PPO 训练循环。", "mAP、s1/s2 误差、漏检率", PURPLE, LIGHT_PURPLE),
]
for i, (t, stack, body, accept, accent, light) in enumerate(modes):
    x = 0.75 + i * 4.0
    card(s, x, 1.55, 3.75, 3.85, light, None, accent, 0.08)
    tx(s, x + 0.26, 1.75, 3.2, 0.3, t, size=12.5, color=accent, bold=True)
    tx(s, x + 0.26, 2.18, 3.2, 0.85, stack, size=13.5, color=INK, bold=True, line_spacing=1.15)
    tx(s, x + 0.26, 3.25, 3.2, 1.1, body, size=10.5, color=INK, line_spacing=1.3)
    tx(s, x + 0.26, 4.55, 3.2, 0.24, "验收", size=8.3, color=MUTED, bold=True)
    tx(s, x + 0.26, 4.81, 3.2, 0.45, accept, size=9.2, color=accent, bold=True, line_spacing=1.15)

rect(s, 0.75, 5.75, 11.85, 0.55, SOFT, LINE, 0.08)
tx(s, 1.0, 5.86, 11.3, 0.32, "同一份 19-D 契约，三种执行循环。", size=12.5, color=INK, bold=True, align=PP_ALIGN.CENTER)
notes(s, "这一页把训练栈落到三种运行模式。训练模式追吞吐，系统模式追闭环，视觉模式追图像。三者共用 19-D 契约，但不共用同一个循环。")

# ============================================================
# Slide 11 — integration
# ============================================================
s = new_slide("06 · 连接方式", "两条线怎么拼：一套契约", "一个命令，五个进程；五个进程，一套契约", 11)
# left column
card(s, 0.75, 1.55, 2.55, 0.62, INK, None, None, 0.08)
tx(s, 0.9, 1.67, 2.3, 0.3, "scenario.yaml", size=10.5, color=WHITE, bold=True)
arrow_down(s, 1.86, 2.25, 0.2, 0.2, RGBColor(0xA8,0xB5,0xC4))
card(s, 0.75, 2.55, 2.55, 0.62, WHITE, LINE, BLUE, 0.08)
tx(s, 0.9, 2.67, 2.3, 0.3, "launcher", size=10.5, color=INK, bold=True)
tx(s, 0.9, 2.92, 2.3, 0.2, "ros2 launch / Python", size=8, color=MUTED)

# three mode cards
cards = [
    ("系统模式", "Gazebo + PX4\n+ YOLO + PPO", "250–400 Hz 飞控 · 30 Hz 视觉", BLUE, LIGHT_BLUE),
    ("训练模式", "Isaac Lab / MuJoCo\n+ 19-D 特征", "10k+ envs · 特征级并行", TEAL, LIGHT_TEAL),
    ("视觉模式", "RflySim / AirSim\n+ YOLO", "30–60 Hz 相机 · 离线数据", PURPLE, LIGHT_PURPLE),
]
for i, (t, b, freq, accent, light) in enumerate(cards):
    x = 4.0 + i * 2.95
    card(s, x, 1.55, 2.7, 2.1, light, None, accent, 0.08)
    tx(s, x + 0.18, 1.7, 2.35, 0.28, t, size=10.8, color=accent, bold=True)
    tx(s, x + 0.18, 2.06, 2.35, 0.9, b, size=10.5, color=INK, bold=True, line_spacing=1.25)
    tx(s, x + 0.18, 3.05, 2.35, 0.42, freq, size=8.2, color=MUTED, line_spacing=1.15)

# contract bar
rect(s, 0.75, 4.35, 11.85, 0.75, SOFT, LINE, 0.08)
tx(s, 1.0, 4.48, 2.1, 0.24, "共用契约", size=9, color=MUTED, bold=True)
for i, item in enumerate(["observation.py", "action.py", "scenario.yaml", "metrics.py", "MCAP"]):
    chip(s, 2.45 + i * 2.02, 4.47, 1.88, 0.45, item, WHITE, INK, 8.8)

# bottom statement
tx(s, 0.75, 5.55, 11.85, 0.55, "换仿真器只换“执行器”，不重写任务。", size=16, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)
tx(s, 0.75, 6.12, 11.85, 0.32, "气动返工换 FDM · 视觉返工换渲染 · PPO 返工换训练环境 · PX4 返工换仿真平台",
   size=9.8, color=MUTED, align=PP_ALIGN.CENTER)
notes(s, "这一页回答“怎么统一”。左边一份场景配置，右边三种模式，底部一份契约。换组件不重写任务，这是整套方法的核心。")

# ============================================================
# Slide 12 — roadmap
# ============================================================
s = new_slide("07 · 落地", "落地路线：先跑通，再提速", "每个阶段只换一层，19-D 契约不变", 12)
phases = [
    ("0–4 周", "基线", "Gazebo Sim + PX4\nadvanced_plane；两机；19-D logger", "可复现两机 SITL", BLUE, LIGHT_BLUE),
    ("1–3 月", "提速", "Isaac Lab / MuJoCo\n特征级 PPO；噪声与域随机化", "特征级 PPO baseline", TEAL, LIGHT_TEAL),
    ("2–4 月", "视觉", "RflySim / AirSim\nYOLO 数据；虚拟平面误差", "YOLO 数据 + 误差报告", PURPLE, LIGHT_PURPLE),
    ("4–6 月", "闭环", "HITL + 真机\nJSBSim 气动复核；失败回流", "HITL / 实飞报告", ORANGE, LIGHT_ORANGE),
]
# timeline
rect(s, 0.9, 2.55, 11.55, 0.03, RGBColor(0xC9,0xD4,0xE1), shape=MSO_SHAPE.RECTANGLE)
for i, (period, title, body, deliver, accent, light) in enumerate(phases):
    x = 0.75 + i * 3.0
    # dot
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 1.18), Inches(2.44), Inches(0.25), Inches(0.25))
    dot.fill.solid(); dot.fill.fore_color.rgb = accent; dot.line.fill.background(); dot.shadow.inherit = False
    card(s, x, 2.95, 2.75, 2.55, light, None, accent, 0.08)
    tx(s, x + 0.18, 3.08, 2.4, 0.28, period, size=10, color=accent, bold=True)
    tx(s, x + 0.18, 3.42, 2.4, 0.32, title, size=14, color=INK, bold=True)
    tx(s, x + 0.18, 3.85, 2.4, 0.95, body, size=9.8, color=INK, line_spacing=1.3)
    tx(s, x + 0.18, 4.78, 2.4, 0.24, "交付", size=8, color=MUTED, bold=True)
    tx(s, x + 0.18, 5.02, 2.4, 0.35, deliver, size=8.8, color=accent, bold=True, line_spacing=1.1)
tx(s, 0.75, 6.05, 11.85, 0.35, "先跑通系统闭环，再把 PPO 搬到 GPU，再补视觉，最后 HITL / 真机。", size=12.5, color=INK, bold=True, align=PP_ALIGN.CENTER)
notes(s, "路线按“先跑通、再提速、再补视觉、最后闭环”推进。每一阶段只换一层，保持 19-D 契约不变，避免同时改四个变量。")

# ============================================================
# Slide 13 — don'ts
# ============================================================
s = new_slide("08 · 风险", "六个不要", "这些问题比“选错仿真器”更常见", 13)
donts = [
    ("01", "不要一个栈硬扛训练 / 系统 / 视觉", "三种模式的时间尺度与硬件不同。"),
    ("02", "不要用 Gazebo Classic 开新项目", "2025-01-29 已 EOL；迁移 Gazebo Sim。"),
    ("03", "不要指望 AirSim 固定翼", "视觉强，固定翼支持有限。"),
    ("04", "不要用 Aerial Gym 训 defender", "四旋翼专用；只能训 intruder。"),
    ("05", "不要只看 FPS / 厂商数字", "3–10×、89% 都带任务与硬件条件。"),
    ("06", "不要把 PPO 训练绑在照片级渲染上", "19-D 特征训练，视觉单独验证。"),
]
for i, (num, title, body) in enumerate(donts):
    col = i % 2
    row = i // 2
    x = 0.75 + col * 6.0
    y = 1.45 + row * 1.55
    card(s, x, y, 5.7, 1.35, WHITE, LINE, RED, 0.08)
    tx(s, x + 0.2, y + 0.15, 0.55, 0.3, num, size=13, color=RED, bold=True)
    tx(s, x + 0.78, y + 0.14, 4.7, 0.35, title, size=11.2, color=INK, bold=True)
    tx(s, x + 0.78, y + 0.55, 4.7, 0.55, body, size=9.2, color=MUTED, line_spacing=1.2)
tx(s, 0.75, 6.5, 11.85, 0.32, "先拆链路，再选组件，最后用契约拼起来。", size=13, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)
notes(s, "六个不要是答辩里最容易被问到的坑。尤其第 1 和第 6：不要一个栈硬扛，也不要把 PPO 训练和照片级渲染绑在一起。")

# ============================================================
# Slide 14 — summary
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, INK)
rect(s, 0, 0, 13.333, 0.08, ORANGE, shape=MSO_SHAPE.RECTANGLE)
tx(s, 0.9, 0.65, 7.0, 0.3, "SUMMARY", size=10, color=RGBColor(0x9F,0xB3,0xC8), bold=True)
tx(s, 0.9, 1.05, 11.5, 0.75, "总结：两条线，三种模式，一套契约", size=30, color=WHITE, bold=True)
nums = [("2", "条线", "仿真器 / 训练栈"), ("3", "种模式", "训练 / 系统 / 视觉"), ("1", "套契约", "19-D observation")]
for i, (n, t, b) in enumerate(nums):
    x = 0.9 + i * 4.0
    tx(s, x, 2.55, 1.1, 1.0, n, size=54, color=ORANGE, bold=True)
    tx(s, x + 0.95, 2.72, 2.6, 0.36, t, size=15, color=WHITE, bold=True)
    tx(s, x + 0.95, 3.12, 2.6, 0.32, b, size=10, color=RGBColor(0xB8,0xC6,0xD6))

tx(s, 0.9, 4.55, 11.5, 0.45, "仿真器回答“够不够真”，训练栈回答“怎么训、怎么部署”。", size=15, color=WHITE, bold=True)
tx(s, 0.9, 5.1, 11.5, 0.4, "换组件，不重写任务；先跑通，再提速。", size=13, color=ORANGE, bold=True)
rect(s, 0.9, 6.35, 11.5, 0.008, RGBColor(0x3A,0x4A,0x5C), shape=MSO_SHAPE.RECTANGLE)
tx(s, 0.9, 6.52, 5.0, 0.3, "谢谢 / Q&A", size=12, color=RGBColor(0xC7,0xD3,0xE0), bold=True)
tx(s, 8.2, 6.52, 4.2, 0.3, "2026.10 · UAV-Survey / 10.Simulators", size=9, color=RGBColor(0x8A,0x9B,0xAD), align=PP_ALIGN.RIGHT)
notes(s, "收尾。三个数字：两条线、三种模式、一套契约。一句话：仿真器看真不真，训练栈看怎么训怎么部署。")

# ---------- save ----------
out = "counter-uav-simulator-stack-deck.pptx"
prs.save(out)
print("saved", out, "slides", len(prs.slides))
