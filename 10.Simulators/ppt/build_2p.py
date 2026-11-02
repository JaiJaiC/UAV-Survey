from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

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


def tx(slide, x, y, w, h, text, size=11, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, spacing=1.12, margins=(0, 0, 0, 0)):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color


def header(slide, kicker, title, subtitle, page):
    bg(slide)
    rect(slide, 0, 0, 13.333, 0.055, BLUE, shape=MSO_SHAPE.RECTANGLE)
    tx(slide, 0.62, 0.26, 8.5, 0.24, kicker, size=9.5, color=BLUE, bold=True)
    tx(slide, 0.62, 0.50, 9.8, 0.55, title, size=27, color=INK, bold=True)
    tx(slide, 0.62, 1.06, 10.7, 0.3, subtitle, size=11.2, color=MUTED)
    rect(slide, 0.62, 7.08, 12.1, 0.008, LINE, shape=MSO_SHAPE.RECTANGLE)
    tx(slide, 0.62, 7.16, 9.0, 0.2, "反无拦截 · 仿真器与训练栈调研（2 页版）", size=8.2, color=MUTED)
    tx(slide, 11.6, 7.16, 1.1, 0.2, f"{page} / 2", size=8.2, color=MUTED, align=PP_ALIGN.RIGHT)


def arrow(slide, x, y, w=0.18, h=0.18, color=RGBColor(0xA8, 0xB5, 0xC4)):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); shp.shadow.inherit = False


# ============================================================
# Slide 1 — simulators
# ============================================================
s = prs.slides.add_slide(BLANK)
header(s, "01 · 仿真器", "仿真器：三条互补线",
       "固定翼 defender + 旋翼 intruder + 单目 + PX4：不选全能冠军，按角色选", 1)

# top-right stat
rect(s, 10.55, 0.48, 2.15, 0.5, INK, None, 0.4)
tx(s, 10.55, 0.56, 2.15, 0.3, "19 个候选  →  3 条线", size=9.2, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

rows = [
    ("系统闭环", "PX4 / HIL", "Gazebo Sim + PX4\nRflySim",
     "PX4 + advanced_plane + AVL；两机 / MAVLink / HITL",
     "视觉中等、CPU 单实例", BLUE, LIGHT_BLUE),
    ("气动复核", "配平 / 失速", "JSBSim + FlightGear\nX-Plane（可选）",
     "高保真气动；配平、失速、侧滑、风扰",
     "无 RL、多机弱", ORANGE, LIGHT_ORANGE),
    ("视觉验证", "相机 / YOLO", "RflySim / AirSim\nUE5",
     "照片级相机、天气、深度；虚拟平面误差",
     "固定翼弱、单实例", PURPLE, LIGHT_PURPLE),
]
for i, (role, sub, tools, strong, boundary, accent, light) in enumerate(rows):
    y = 1.55 + i * 1.42
    rect(s, 0.62, y, 12.1, 1.28, light, None, 0.05)
    rect(s, 0.62, y, 2.0, 1.28, accent, None, 0.05)
    tx(s, 0.8, y + 0.2, 1.7, 0.3, role, size=14, color=WHITE, bold=True)
    tx(s, 0.8, y + 0.55, 1.7, 0.25, sub, size=8.4, color=RGBColor(0xE8, 0xF0, 0xF9))
    tx(s, 2.9, y + 0.15, 0.6, 0.2, "首选", size=7.5, color=MUTED, bold=True)
    tx(s, 2.9, y + 0.37, 3.85, 0.78, tools, size=12.2, color=INK, bold=True, spacing=1.15)
    tx(s, 7.0, y + 0.16, 0.6, 0.2, "强项", size=7.5, color=MUTED, bold=True)
    tx(s, 7.0, y + 0.37, 5.35, 0.32, strong, size=9.3, color=INK, bold=True)
    tx(s, 7.0, y + 0.76, 0.6, 0.2, "边界", size=7.5, color=MUTED, bold=True)
    tx(s, 7.0, y + 0.95, 5.35, 0.25, boundary, size=8.8, color=accent, bold=True)

rect(s, 0.62, 5.95, 12.1, 0.55, LIGHT_RED, None, 0.08)
tx(s, 0.8, 6.05, 1.0, 0.22, "不要", size=8.2, color=RED, bold=True)
tx(s, 1.55, 6.04, 11.0, 0.3, "Gazebo Classic 已 EOL  ·  AirSim 固定翼弱  ·  Aerial Gym 只训旋翼  ·  能加载 ≠ 气动可信",
   size=9.2, color=INK, bold=True)
tx(s, 0.62, 6.65, 12.1, 0.3, "三条线互补，不是三选一；系统闭环优先，气动/视觉单独验证。",
   size=10.5, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)

s.notes_slide.notes_text_frame.text = "仿真器只讲三条线：系统闭环、气动复核、视觉验证。系统闭环优先 Gazebo Sim + PX4；气动用 JSBSim/FlightGear 复核；视觉用 RflySim/AirSim/UE5。Aerial Gym 只适合旋翼 intruder。"

# ============================================================
# Slide 2 — training stacks
# ============================================================
s = prs.slides.add_slide(BLANK)
header(s, "02 · 训练栈", "训练栈：三种运行模式",
       "仿真器选完，再决定怎么训、怎么部署；不要一个栈硬扛", 2)

modes = [
    ("训练模式", "Isaac Lab + RSL-RL\nMuJoCo + MJX",
     "19-D 特征 + 噪声；GPU 并行；不渲染照片。",
     "env/s · 样本效率 · 命中率", TEAL, LIGHT_TEAL),
    ("系统模式", "Gazebo Sim + PX4\n+ PPO 推理",
     "MAVLink / offboard / 两机同步 / HITL。",
     "offboard 切换 · 指令延迟 · 时钟", BLUE, LIGHT_BLUE),
    ("视觉模式", "RflySim / AirSim / UE5\n+ YOLO",
     "只做 YOLO 数据与视觉闭环，不进 PPO 训练循环。",
     "mAP · s1/s2 误差 · 漏检率", PURPLE, LIGHT_PURPLE),
]
for i, (mode, stack, body, metric, accent, light) in enumerate(modes):
    x = 0.62 + i * 4.04
    rect(s, x, 1.5, 3.9, 3.55, light, None, 0.05)
    rect(s, x, 1.5, 0.08, 3.55, accent, shape=MSO_SHAPE.RECTANGLE)
    tx(s, x + 0.25, 1.68, 3.4, 0.28, mode, size=12.5, color=accent, bold=True)
    tx(s, x + 0.25, 2.05, 3.4, 0.78, stack, size=13.2, color=INK, bold=True, spacing=1.15)
    tx(s, x + 0.25, 2.95, 3.4, 0.8, body, size=9.7, color=INK, spacing=1.25)
    tx(s, x + 0.25, 3.95, 3.4, 0.2, "验收", size=7.8, color=MUTED, bold=True)
    tx(s, x + 0.25, 4.18, 3.4, 0.35, metric, size=8.8, color=accent, bold=True)

# contract band
rect(s, 0.62, 5.3, 12.1, 0.62, SOFT, LINE, 0.08)
tx(s, 0.82, 5.4, 1.0, 0.2, "共用契约", size=8.2, color=MUTED, bold=True)
tx(s, 1.95, 5.38, 10.5, 0.3, "19-D  observation.py · action.py · scenario.yaml · metrics.py",
   size=10.2, color=INK, bold=True)

# roadmap chips
steps = [("0–4 周", "基线"), ("1–3 月", "提速"), ("2–4 月", "视觉"), ("4–6 月", "HITL")]
for i, (period, name) in enumerate(steps):
    x = 0.62 + i * 3.02
    rect(s, x, 6.15, 2.78, 0.55, WHITE, LINE, 0.12)
    tx(s, x + 0.14, 6.2, 2.5, 0.2, f"{period}  {name}", size=8.8, color=INK, bold=True)
    if i < 3:
        arrow(s, x + 2.84, 6.32, 0.14, 0.16)

tx(s, 0.62, 6.82, 12.1, 0.25, "先跑通系统闭环，再把 PPO 搬到 GPU，再补视觉，最后 HITL / 真机。",
   size=9.2, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)

s.notes_slide.notes_text_frame.text = "训练栈只讲三种模式：训练模式追吞吐，系统模式追闭环，视觉模式追图像。三者共用 19-D 契约，但不共用同一个执行循环。路线是先跑通、再提速、再补视觉、最后 HITL。"

out = "counter-uav-2p-deck.pptx"
prs.save(out)
print("saved", out, "slides", len(prs.slides))
