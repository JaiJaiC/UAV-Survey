#!/usr/bin/env python3
"""Build source-grounded 0.Fracture-style notes for Yirui Cong's library."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from rebuild_scholar_indexes import rdf_metadata  # noqa: E402

SCHOLAR = ROOT / "2.Scholar" / "Yirui Cong"

FOCUS = {
    "1348": {
        "tags": ["Set-Membership Filtering", "Filter Stability", "OIT", "Constrained Zonotope"],
        "task": "分析线性集合成员滤波器对初始条件的稳定性，并构造不因不恰当初始集合而失效的稳定滤波框架。",
        "challenge": ["集合滤波没有概率协方差可直接刻画遗忘初值的速度。", "初始集合不准确会导致估计不可行或估计间隙持续放大。", "约束带来的 wrapping effect 使集合复杂度和保守性同时增长。"],
        "insight": "把测量对状态集合的约束按时间堆叠为 Observation-Information Tower（OIT），可将真正来自观测的信息与初始集合解耦，从而直接讨论稳定性。",
        "method": ["用良定性和有界估计间隙定义对初值稳定。", "由 OIT 推导经典线性 SMF 的稳定条件。", "建立 OIT 驱动的稳定保证框架，并设计快速 OIT-CZ 滤波器。"],
        "principle": "集合滤波的本质是预测集合与观测一致集合的递归交；稳定性意味着有限窗口观测最终提供足够约束，使初始集合的差异不再主导估计。",
        "formula": r"X_k=(A X_{k-1}\oplus W)\cap\{x:y_k-Cx\in V\}",
        "flaw": ["理论集中在线性时不变系统与有界扰动。", "OIT 窗口和约束数量在高维系统中可能带来计算压力。", "稳定条件与集合近似算法之间仍存在保守性耦合。"],
        "motivation": "既然滤波不可靠来自初值信息一直残留，那么能否只用一段观测构造与初值无关的信息塔，并让滤波器定期回到这座信息塔上？",
    },
    "1350": {
        "tags": ["Disturbance Observer", "Set Membership", "Boundedness", "Worst-case Optimality"],
        "task": "回答线性离散系统何时存在有界扰动观测器，并给出在存在时必然有界的完备构造。",
        "challenge": ["传统方法从观测器增益出发，难以区分设计失败与问题本身无解。", "未知扰动只有界而没有概率分布，均方误差分析不适用。", "需要同时给出可检验的存在条件和可实现算法。"],
        "insight": "先把扰动观测改写为与模型、测量和有界噪声一致的可行集合，再判断该集合能否保持有界；存在性因此成为集合传播的结构性质。",
        "method": ["建立有界扰动观测器存在的充要条件。", "构造集合成员滤波型扰动观测器并证明完备性。", "证明其可达到最坏情形最优，为其他观测器提供基准。"],
        "principle": "观测器是否有界取决于系统是否能用观测信息排除沿不可辨识方向无限扩张的扰动集合，而不只是某个增益是否稳定。",
        "formula": r"D_k=\{d:x_{k+1}-Ax_k-Bu_k=Ed,\;w_k\in W\}",
        "flaw": ["结论依赖线性离散模型和正确的扰动界。", "精确可行集传播在高维下会快速增大复杂度。", "数值验证尚不能替代真实传感器偏差和模型失配实验。"],
        "motivation": "与其反复调观测器增益，能否先问一个更基本的问题：所有与数据一致的扰动是否天然落在某个有界集合里？",
    },
    "1352": {
        "tags": ["Formation Control", "Channel Capacity", "Guaranteed Communication Region", "Power Control"],
        "task": "刻画无线链路容量对含有界过程噪声的二阶多智能体编队精度的基本限制，并联合设计控制与通信。",
        "challenge": ["智能体位置受过程噪声影响，接收端并不知道确定的链路距离。", "延长传输时间能积累信息，但智能体运动也会扩大位置不确定性。", "控制误差、数据率、发射功率和拓扑彼此耦合。"],
        "insight": "用 guaranteed communication region 表示在所有控制不确定性下仍能成功解码的位置集合，便可把几何可达性、信道容量与编队误差放在同一框架中。",
        "method": ["建立控制系统驱动的链路模型和保证通信区域。", "证明区域不会随传输时间无界扩张，揭示区域与数据率的权衡。", "推导目标精度所需的数据率下界，并联合设计估计控制器与发射功率。"],
        "principle": "通信容量限制了单位时间可消除的不确定性，而过程噪声持续注入新不确定性；稳定编队要求信息消除速率超过不确定性增长速率。",
        "formula": r"R\le B\log_2(1+\mathrm{SNR}),\qquad \|e_k\|\le\varepsilon",
        "flaw": ["信道与噪声模型的理想化可能低估遮挡、干扰和时变衰落。", "结果针对特定二阶动力学和有界不确定性。", "大规模网络中的联合功率控制与拓扑调度仍需扩展。"],
        "motivation": "若编队精度本质上依赖邻居信息，那能否把“需要多准”直接换算成“链路至少要传多快、发多大功率”？",
    },
    "1354": {
        "tags": ["Set-Membership Smoothing", "Hidden Markov Model", "Uncertain Variables", "Constrained Zonotope"],
        "task": "为非随机隐藏马尔可夫模型建立最优集合成员平滑理论，并设计线性与非线性算法。",
        "challenge": ["平滑要利用未来测量反向约束历史状态，集合逆像计算通常困难。", "非概率框架缺少类似贝叶斯后验的统一最优性定义。", "集合交、逆映射和近似会引入 wrapping 与计算膨胀。"],
        "insight": "用 uncertain variable 的值域条件化定义平滑集合，可把滤波后验与下一时刻平滑集合通过动力学逆像严格连接。",
        "method": ["首次建立最优 SMSing 框架并阐明滤波与平滑关系。", "对线性约束 zonotope 不确定性给出闭式算法。", "面向一类非线性系统构造集合平滑算法。"],
        "principle": "历史状态的平滑范围等于其滤波范围与“能够演化到下一时刻平滑范围”的动力学逆像之交。",
        "formula": r"X_{k|T}=X_{k|k}\cap f_k^{-1}(X_{k+1|T})",
        "flaw": ["非线性逆像和集合并集可能需要保守近似。", "闭式结果依赖特定线性与约束 zonotope 表示。", "长时域反向传播的计算和存储成本需要进一步评估。"],
        "motivation": "滤波只看过去；既然后续测量已经知道，为什么不把它们通过动力学逆向投影回来，删除历史时刻不可能的状态？",
    },
    "1356": {
        "tags": ["Distributed SMF", "Asymptotic Boundedness", "COIT", "Graph Structure"],
        "task": "给出线性离散分布式集合成员滤波估计集渐近有界的可检验条件。",
        "challenge": ["集合近似的 wrapping effect 可使估计集持续膨胀。", "单个传感器不可观并不代表网络整体无法估计，必须结合图结构。", "经典 collective detectability 针对点估计或协方差，不能直接解释集合传播。"],
        "insight": "Collective Observation-Information Tower（COIT）把图的源分量、跨节点信息传播与集合约束的累积联系起来，从而暴露哪些状态方向会被网络持续压缩。",
        "method": ["定义 COIT 描述图结构与估计集合的关系。", "推导一般 DSMF 渐近有界的易验证充分条件。", "证明该条件推广并弱化经典 collective detectability 条件。"],
        "principle": "每个不稳定状态方向都必须在某个源分量被观测，并通过通信路径传播到其他节点；否则该方向的集合宽度会持续增长。",
        "formula": r"X_{i,k}=\Big(AX_{i,k-1}\oplus W\Big)\cap\!\bigcap_{j\in\mathcal N_i} I_{j,k}",
        "flaw": ["当前给出的是充分条件，必要性边界仍可研究。", "分析集中在线性离散系统和固定/受控图结构。", "集合降阶策略可能改变理论条件对应的实际保守性。"],
        "motivation": "若集中式可观性来自多传感器信息互补，那么在分布式网络里，能否沿图追踪每一份观测信息最终约束了哪些状态方向？",
    },
    "1359": {
        "tags": ["Single-Beacon Localization", "Range Measurement", "Constrained Zonotope", "Sliding Window"],
        "task": "在噪声统计未知但界已知时，仅凭单信标距离测量实现移动机器人可靠定位。",
        "challenge": ["单次距离测量只给出圆环约束，具有非凸性和方向歧义。", "单信标缺少瞬时几何可观性，需要运动历史累积信息。", "精确集合传播会快速提高复杂度。"],
        "insight": "将每次距离观测视为必含真值的集合约束，再通过凸松弛、半空间细化与滑动窗口把时间信息转化为逐步收缩的 constrained zonotope。",
        "method": ["以凸优化松弛处理距离圆环的非凸约束。", "增加 halfspace-intersection refinement 提高精度。", "使用滑动窗口递归在精度与效率间折中，并用仿真和场地实验验证。"],
        "principle": "机器人运动让不同时刻的圆环约束发生几何交叠；即使每个圆环单独含糊，多个时刻的交集也能锁定位置。",
        "formula": r"r_k^-\le\|p_k-b\|_2\le r_k^+",
        "flaw": ["性能依赖机器人运动是否提供足够激励。", "信标位置误差和非视距偏差可能破坏“真值在界内”的假设。", "更高维空间和复杂动力学会增加凸松弛保守性。"],
        "motivation": "单个距离只能画一个圆环，但机器人会移动；能否把连续圆环与运动模型相交，让时间替代额外信标？",
    },
    "1360": {
        "tags": ["Formation Stability", "Data Rate", "Veteran Rule", "Directed Topology"],
        "task": "在有限数据率和有界过程噪声下，为离散多智能体系统设计可保证一致有界误差的编队控制。",
        "challenge": ["量化通信使邻居状态只能近似获得。", "有界过程噪声持续扰动编队误差。", "有向拓扑既要分布式构造，又要具备可调的稳定谱性质。"],
        "insight": "借鉴鸽群中的 Veteran Rule，让节点按局部规则形成含有向生成树的层级拓扑；下三角 Laplacian 使非零特征值可由连接权直接配置。",
        "method": ["提出分布式 Veteran-Rule 拓扑构造策略。", "在有限数据率与有界噪声下设计分布式编队控制律。", "用 Jury 稳定判据推导控制增益充分条件并证明一致有界。"],
        "principle": "拓扑决定闭环误差模态；若构造使 Laplacian 谱可控，就能把通信量化和噪声影响纳入每个模态的离散稳定条件。",
        "formula": r"e_i(k)=x_i(k)-h_i,\qquad e(k+1)=A_{cl}(L)e(k)+\eta(k)",
        "flaw": ["拓扑层级化可能牺牲冗余和抗节点失效能力。", "理论基于有界噪声与离散线性模型。", "尚需更真实的物理层时变通信模型和硬件编队实验。"],
        "motivation": "若任意拓扑的谱难以控制，那能否先用一种自然界已验证的层级规则构造拓扑，使稳定性设计变成可直接配置的局部权重问题？",
    },
    "1361": {
        "tags": ["High-order MAS", "Time-delay Consensus", "Kronecker Basis", "Multi-UAV"],
        "task": "完善高阶线性多智能体单/多时延一致性理论，并用于时延通信下的多无人机协同控制。",
        "challenge": ["高阶动力学与多个通信时延共同造成高维耦合。", "既有判据保守，难以给出更大的可容许时延上界。", "平均一致性轨迹、收敛条件与工程控制器需要统一描述。"],
        "insight": "提出张量意义下的 Kronecker Basis，把一致与分歧子空间清晰分解，使高阶时延系统可转化为更易分析的等价子系统。",
        "method": ["定义 Kronecker Basis 并证明基本性质。", "结合 Lyapunov-Krasovskii 泛函和自由权矩阵构造单/多时延 LMI 判据。", "推导时延平均一致的充要条件，并设计多无人机协同控制方案。"],
        "principle": "一致性分析的核心不是直接处理所有智能体状态，而是把网络状态分解为不受耦合影响的一致模态和必须稳定衰减的分歧模态。",
        "formula": r"\dot x_i=Ax_i+\sum_j a_{ij}BK\big[x_j(t-\tau_{ij})-x_i(t-\tau_{ij})\big]",
        "flaw": ["主要基于线性模型、给定时延结构和理想拓扑信息。", "LMI 规模随系统阶次、节点和时延类型增长。", "对丢包、攻击、异构动力学与真实飞行器非线性仍需扩展。"],
        "motivation": "高阶时延系统难，是因为一致方向与分歧方向混在一起；能否先构造一种基把二者彻底拆开，再只对真正需要衰减的模态做时延稳定分析？",
    },
    "1368": {
        "tags": ["Fixed-wing UAV Swarm", "Survey", "Communication", "Command and Control"],
        "task": "系统梳理小型固定翼无人机集群的内涵、典型项目、关键技术与未来发展方向。",
        "challenge": ["固定翼平台不能悬停，速度快、转弯半径和安全间隔约束强。", "集群跨越平台、通信、规划、控制和指挥等多学科层级。", "公开项目指标与验证口径不统一，横向比较困难。"],
        "insight": "用“系统内涵—典型项目—七类关键技术”的多层分类组织领域，把单机能力、群体协同和体系指控置于同一技术地图。",
        "method": ["总结集群协同模式、分布指挥体系、关键技术突破和验证路径。", "从体系架构、通信组网、决策规划、飞机平台、集群飞行、安全、指控七个维度综述。", "据关键瓶颈给出未来研究趋势。"],
        "principle": "固定翼集群的能力不是单项算法相加，而是通信、决策、飞控和安全约束在同一实时闭环中的系统涌现。",
        "formula": r"\text{Swarm capability}=f(\text{platform},\text{network},\text{decision},\text{control},\text{safety})",
        "flaw": ["综述发表于 2020 年，未覆盖近年的基础模型与大规模自主集群进展。", "项目材料的公开程度不同，部分结论难以量化复现。", "七维分类清晰，但缺少统一 benchmark 和成熟度评分。"],
        "motivation": "面对一个跨学科集群系统，与其按论文罗列，能否先拆出完整能力链，再检查每一环的成熟度和最薄弱接口？",
    },
    "1454": {
        "tags": ["Cooperative Estimation", "Set-Membership Filter", "OIT", "Distributed Zonotope"],
        "task": "让多智能体仅用本地绝对/相对测量和邻居通信，分别获得包含真实状态的分布式集合估计。",
        "challenge": ["集中式方法能融合全部信息，但不满足局部通信约束。", "相对测量耦合多个智能体，直接分解会损失信息。", "需要明确分布式方案与集中式基准之间的差距。"],
        "insight": "先用 OIT-inspired 有限时域集中式 constrained-zonotope 方法定义信息充分的基准，再按邻居可得信息拆成分布式集合传播。",
        "method": ["分析集中式 SMF 框架作为分布式性能基准。", "提出 OIT-inspired 有限时域集中式 CZ 算法。", "建立分布式 SMF 框架与 constrained-zonotope 算法，并用仿真验证。"],
        "principle": "绝对测量约束单个状态，相对测量约束状态差；合作估计通过在图上传播这些差分约束，把局部锚定能力传给邻居。",
        "formula": r"X_{i,k}=X_{i,k}^{pred}\cap Y_{i,k}^{abs}\cap\!\bigcap_{j\in\mathcal N_i}Y_{ij,k}^{rel}",
        "flaw": ["验证以仿真为主，通信延迟和异步更新尚未充分体现。", "有限时域和集合降阶会影响长期一致性与保守性。", "算法在大规模稠密相对测量网络中的复杂度需量化。"],
        "motivation": "既然相对测量携带的是两个智能体之间的约束，能否把它当作可沿邻接图传递的集合信息，让每个节点逐步接近集中式估计？",
    },
    "1455": {
        "tags": ["Range Measurement", "Cooperative Filtering", "Extended Constrained Zonotope", "Anchor Agent"],
        "task": "在部分锚节点有高精度绝对测量、其余节点仅有低精度绝对/相对距离时，实现分布式有保证状态估计。",
        "challenge": ["距离测量是非线性非凸约束。", "低精度节点必须从锚节点获益，但不能集中上传全部数据。", "集合算法需兼顾精度、复杂度与沿拓扑传播的稳定性。"],
        "insight": "在链式拓扑中按顺序传播不确定集合，使锚节点的高精度约束逐跳注入；extended constrained zonotope 用额外约束表达距离信息。",
        "method": ["设计 sequential SMFing 框架。", "构造处理相对距离测量的 extended constrained-zonotope 算法。", "通过多组仿真验证低精度节点的估计范围显著收缩。"],
        "principle": "锚节点提供全局坐标基准，相对距离把该基准转成邻居的几何约束；顺序集合交将高精度逐跳扩散。",
        "formula": r"r_{ij}^-\le\|x_i-x_j\|_2\le r_{ij}^+",
        "flaw": ["链式顺序更新对拓扑断裂和传播顺序敏感。", "距离约束近似可能在复杂几何下变保守。", "论文将误差有界性完整分析留作未来工作。"],
        "motivation": "如果只有少数节点知道得准，能否不传原始数据，而是让它们的可信集合沿相对距离链逐跳收紧其他节点？",
    },
}

# The CAJ folder is a second local representation of the same thesis.
FOCUS["1750"] = dict(FOCUS["1361"])
FOCUS["1750"]["tags"] = FOCUS["1361"]["tags"] + ["CAJ mirror"]


CSS = """
:root{--bg:#f8f9fb;--surface:#fff;--border:#e2e5ea;--text:#1a1d23;--muted:#64748b;--blue:#2563eb;--green:#059669;--amber:#d97706;--purple:#7c3aed;--rose:#e11d48}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif;line-height:1.72}nav{position:sticky;top:0;z-index:10;display:flex;gap:4px;align-items:center;flex-wrap:wrap;padding:10px 22px;background:#fffffff2;border-bottom:1px solid var(--border);backdrop-filter:blur(12px)}nav a{font-size:12px;color:#475569;text-decoration:none;padding:5px 8px;border-radius:5px}nav a:hover{background:#dbeafe;color:#1d4ed8}.home{font-weight:800!important;color:#ea580c!important;border:1px solid #fb923c}.brand{font-weight:800;margin:0 8px}.wrap{max-width:1100px;margin:auto;padding:28px 20px 60px}section{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 1px 3px #0000000a;scroll-margin-top:60px}h1{font-size:24px;line-height:1.35;margin:0 0 8px}h2{font-size:18px;margin:0 0 18px}h3{font-size:15px;margin:20px 0 8px}p,li,td,th{font-size:14px;color:#334155}ul,ol{padding-left:22px}.meta{color:var(--muted);font-size:13px}.tag{display:inline-block;margin:3px 5px 3px 0;padding:2px 9px;border-radius:4px;background:#dbeafe;color:#1d4ed8;font-size:11px;font-weight:700}.callout{border-left:4px solid var(--purple);background:#f5f3ff;padding:14px 18px;border-radius:0 8px 8px 0}.info{border-color:var(--blue);background:#eff6ff}.tip{border-color:var(--green);background:#ecfdf5}.warn{border-color:var(--amber);background:#fffbeb}.formula{overflow:auto;background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:15px 18px;margin:12px 0}.mermaid-box{overflow:auto;background:#fafafa;border:1px solid var(--border);border-radius:9px;padding:15px;text-align:center}.figure{border:1px solid var(--border);border-radius:10px;overflow:hidden;margin:16px 0}.figure img{display:block;max-width:100%;max-height:720px;margin:auto}.figcap{padding:10px 14px;background:#f8fafc;color:var(--muted);font-size:12px}.source{white-space:pre-wrap;max-height:260px;overflow:auto;background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:12px;font-size:12px;color:#475569}.placeholder{padding:28px;border:2px dashed var(--border);border-radius:9px;color:var(--muted);text-align:center}table{width:100%;border-collapse:collapse}th,td{padding:9px 11px;border:1px solid var(--border);text-align:left;vertical-align:top}th{background:#f1f5f9}footer{text-align:center;color:#94a3b8;padding:20px;font-size:12px}@media(max-width:650px){section{padding:20px}.wrap{padding:18px 10px}nav{position:static}}
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def items(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in values) + "</ul>"


def extract_figures(pdf: Path, out_dir: Path, limit: int = 4) -> list[Path]:
    exe = shutil.which("pdfimages")
    selected = []
    if exe:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as temp:
            prefix = str(Path(temp) / "asset")
            run = subprocess.run([exe, "-png", str(pdf), prefix], capture_output=True, text=True)
            candidates = []
            if not run.returncode:
                for image_path in Path(temp).glob("asset-*.png"):
                    try:
                        with Image.open(image_path) as image:
                            width, height = image.size
                        area = width * height
                        if width >= 420 and height >= 240 and area >= 180_000:
                            candidates.append((area, width, height, image_path))
                    except Exception:
                        continue
            candidates.sort(reverse=True)
            seen_shapes = set()
            out_dir.mkdir(exist_ok=True)
            for _, width, height, source in candidates:
                shape = (round(width / 100), round(height / 100))
                if shape in seen_shapes and len(candidates) > limit:
                    continue
                seen_shapes.add(shape)
                target = out_dir / f"fig{len(selected)+1}.png"
                shutil.copy2(source, target)
                selected.append(target)
                if len(selected) == limit:
                    break
    # Many robotics/control PDFs draw figures as vectors, so pdfimages sees
    # nothing. Fall back to page snapshots at explicit Fig./图 mentions.
    if not selected:
        try:
            with pdfplumber.open(pdf) as document:
                figure_pages = []
                for page_number, page in enumerate(document.pages):
                    text = page.extract_text() or ""
                    if re.search(r"(?:\bFig(?:ure)?\.?\s*\d+|图\s*\d+)", text, re.I):
                        figure_pages.append(page_number)
                    if len(figure_pages) == min(3, limit):
                        break
                out_dir.mkdir(exist_ok=True)
                for page_number in figure_pages:
                    target = out_dir / f"fig{len(selected)+1}.png"
                    document.pages[page_number].to_image(resolution=120).save(target)
                    selected.append(target)
        except Exception:
            pass
    return selected


def build_note(folder: Path, meta: dict[str, str], focus: dict[str, object], figures: list[Path], asset_note: str = "") -> str:
    title = meta.get("title") or folder.name
    authors = meta.get("authors") or "Metadata unavailable"
    date = meta.get("date") or "Local collection"
    source = meta.get("source") or ""
    abstract = meta.get("abstract") or "该本地条目没有可提取的摘要；以下分析仅依据现有附件和目录信息。"
    local_assets = [p for p in folder.iterdir() if p.is_file() and p.name not in {"index.html", "note.html"}]
    asset_links = " · ".join(f'<a href="{esc(p.name)}">{esc(p.suffix.upper().lstrip(".")) or "FILE"}</a>' for p in local_assets)
    source_link = f' · <a href="{esc(source)}" target="_blank" rel="noopener">Source</a>' if source else ""
    tags = "".join(f'<span class="tag">{esc(tag)}</span>' for tag in focus["tags"])
    diagram = f'''flowchart LR
  A["问题<br/>{esc(focus['task'])}"] --> B["洞察<br/>{esc(focus['insight'])}"]
  B --> C["方法<br/>{esc(focus['method'][0])}"]
  C --> D["验证<br/>理论分析与本地论文中的数值/实验结果"]'''
    figure_html = "".join(f'<div class="figure"><img src="figures/{esc(p.name)}" alt="Representative figure {i}"><div class="figcap">代表性图像 {i}：从本地论文 PDF 内嵌图像提取。图号和精确含义请对照原文图注。</div></div>' for i, p in enumerate(figures, 1))
    if not figure_html:
        figure_html = f'<div class="placeholder">{esc(asset_note or "当前附件未能可靠提取独立论文图；请通过上方本地附件核对原图。")}</div>'
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Paper Notes - {esc(title)}</title><script>MathJax={{tex:{{inlineMath:[["$","$"]],displayMath:[["$$","$$"]]}},options:{{enableMenu:false}}}};</script><script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script><script>mermaid.initialize({{startOnLoad:true,theme:"neutral",securityLevel:"loose"}});</script><style>{CSS}</style></head><body>
<nav><a class="home" href="../../index.html">← SCHOLAR</a><span class="brand">Paper Notes</span><a href="#info">Info</a><a href="#insight">Insight</a><a href="#architecture">Architecture</a><a href="#task">Task</a><a href="#challenge">Challenge</a><a href="#method">Method</a><a href="#principles">Principles</a><a href="#figures">Figures</a><a href="#flaw">Flaw</a><a href="#motivation">Motivation</a></nav><main class="wrap">
<section id="info"><h1>{esc(title)}</h1><p class="meta">{esc(authors)} · {esc(date)}{source_link}</p><div>{tags}</div><h3>TL;DR</h3><div class="callout info">{esc(focus['task'])} 核心路线是：{esc(focus['insight'])}</div><h3>本地材料</h3><p>{asset_links or "No local asset"}</p><h3>Abstract / source-grounded basis</h3><div class="source">{esc(abstract)}</div></section>
<section id="insight"><h2>2. Insight &amp; Novelty</h2><div class="callout">{esc(focus['insight'])}</div><h3>创新链条</h3>{items(["问题 → " + focus['challenge'][0], "洞察 → " + focus['insight']] + ["创新 → " + x for x in focus['method']])}</section>
<section id="architecture"><h2>3. System / Argument Architecture</h2><div class="mermaid-box"><div class="mermaid">{diagram}</div></div><p>该图按“问题—洞察—方法—证据”重构论文逻辑，不替代原论文中的系统框图。</p></section>
<section id="task"><h2>4. Task - 解决什么问题？</h2><div class="callout info">{esc(focus['task'])}</div><p><strong>形式化视角：</strong>在论文给定的动力学、通信/测量与有界不确定性条件下，构造估计或控制映射，并证明目标集合、误差或闭环性质满足论文定义的保证。</p></section>
<section id="challenge"><h2>5. Challenge - 为什么困难？</h2>{items(focus['challenge'])}</section>
<section id="method"><h2>6. Method &amp; Key Formulas</h2>{items(focus['method'])}<div class="formula">$${focus['formula']}$$<p class="meta">概念性核心关系；精确符号、假设与编号以本地论文原文为准。</p></div></section>
<section id="principles"><h2>7. Fundamental Principles - 核心原理</h2><div class="callout tip">{esc(focus['principle'])}</div><p>阅读时应把“集合保证/闭环性质”与具体数值近似区分开：理论对象通常是精确可行集或误差系统，工程算法则需要集合降阶、凸松弛或有限通信。</p></section>
<section id="figures"><h2>8. Paper Figures - 图表解读入口</h2>{figure_html}</section>
<section id="flaw"><h2>9. Potential Flaw &amp; Extensions</h2>{items(focus['flaw'])}<div class="callout warn">可延伸方向应优先验证：模型失配是否破坏保证、规模增长是否仍可计算、以及仿真结论能否在真实通信和传感条件下保持。</div></section>
<section id="motivation"><h2>10. Motivation - 第一性原理推演</h2><div class="callout info"><strong>关键问句：</strong>{esc(focus['motivation'])}</div><ol><li>先识别传统方法真正缺失的可证明性质。</li><li>把问题改写为信息、集合或误差如何传播的基本关系。</li><li>再选择能保留该关系且可计算的表示与算法。</li></ol></section>
</main><footer>UAV-Survey · Yirui Cong · source-grounded local paper notes</footer></body></html>'''


def special_1367(folder: Path) -> str:
    image = next(folder.glob("*.png"))
    focus = {
        "tags": ["Catalog Screenshot", "Thesis Records", "Multi-UAV", "Time-delay Consensus"],
        "task": "整理截图中三项学位论文记录，并明确该目录是文献检索截图而非可全文解析的单篇论文附件。",
        "challenge": ["当前只有检索结果截图，没有论文全文。", "截图同时包含三篇学位论文，不能把其内容混写成一篇。", "除题名、作者、年份和少量关键词外，无法核验公式与实验。"],
        "insight": "将此条目标记为目录证据页，并把可核验信息与不可推断内容分开，避免伪造全文精读。",
        "method": ["识别截图中的题名、作者、学位与年份。", "将第一条与 1361/1750 的同名论文关联。", "保留截图作为来源证据，待补充另外两篇全文后再分别建 paper 目录。"],
        "principle": "没有全文就不能生成全文级方法、公式和实验结论；可靠笔记必须显式区分元数据证据与内容证据。",
        "formula": r"\text{evidence level}:\ \text{metadata}\neq\text{full text}",
        "flaw": ["当前不是独立论文全文。", "截图摘要被截断。", "另外两篇学位论文缺少本地全文与稳定来源映射。"],
        "motivation": "当一个目录只有检索截图时，能否先建立可信的证据边界，而不是为了“补齐”页面去猜测论文内容？",
    }
    meta = {"title": "学位论文检索记录：时延一致性与无人机集群控制", "authors": "丛一睿、马澜、丁宇（截图记录）", "date": "2013 / 2021 / 2019", "abstract": "本页依据目录内截图整理。截图列出三项学位论文记录；其中第一项与本地 1361/1750 条目对应。"}
    return build_note(folder, meta, focus, [], f"原始检索截图：{image.name}").replace('<div class="placeholder">', f'<div class="figure"><img src="{esc(image.name)}" alt="Thesis catalog screenshot"><div class="figcap">本地检索结果截图，仅作为元数据证据。</div></div><div class="placeholder">', 1)


def main() -> None:
    metadata = rdf_metadata(SCHOLAR)
    built = []
    for folder in sorted((p for p in (SCHOLAR / "files").iterdir() if p.is_dir()), key=lambda p: int(p.name)):
        if folder.name == "1367":
            content = special_1367(folder)
        else:
            focus = FOCUS.get(folder.name)
            if not focus:
                raise KeyError(f"No grounded focus data for {folder}")
            pdf = next(folder.glob("*.pdf"), None)
            figures = extract_figures(pdf, folder / "figures") if pdf else []
            if folder.name == "1750" and not figures:
                source_figures = SCHOLAR / "files" / "1361" / "figures"
                if source_figures.is_dir():
                    (folder / "figures").mkdir(exist_ok=True)
                    for src in source_figures.glob("fig*.png"):
                        shutil.copy2(src, folder / "figures" / src.name)
                    figures = sorted((folder / "figures").glob("fig*.png"))
            content = build_note(folder, metadata.get(folder.name, {}), focus, figures, "CAJ 条目与 1361 为同一学位论文的另一种本地格式。" if folder.name == "1750" else "")
        (folder / "note.html").write_text(content, encoding="utf-8", newline="\n")
        built.append(folder.name)
    print(f"Built {len(built)} Yirui Cong notes: {', '.join(built)}")


if __name__ == "__main__":
    main()
