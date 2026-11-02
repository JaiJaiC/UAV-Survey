# 10.Simulators · 仿真与训练栈

> 从「仿真器对比」升级为「训练栈分层」：六个训练栈项目、Gazebo 对照、六层位置、一份 PDF 报告。
> 资料核对：2026-10-28

## 先看什么

| 入口 | 内容 |
|---|---|
| [index.html](index.html) | 总览：分层图、对比矩阵、五个「为什么」、成本模型、三套组合 |
| [comparison.html](comparison.html) | **完整对比表（8 个对象，含 Gazebo Sim / Classic）** + 能力矩阵 |
| [comparison.md](comparison.md) / [comparison.csv](comparison.csv) | 同一张表的 Markdown 版与原始数据 |
| [counter-uav.html](counter-uav.html) | **反无拦截选型导航**：仿真器与训练栈两条线分开看 |
| [counter-uav-simulators.html](counter-uav-simulators.html) | **只看仿真器**：19 个仿真器的固定翼/PX4/相机/多机/吞吐对比 |
| [counter-uav-stacks.html](counter-uav-stacks.html) | **只看训练栈**：9 套训练栈的环境接口/并行/感知/部署/固定翼对比 |
| [stack-anatomy.html](stack-anatomy.html) | **训练栈是怎么「统一」的**：一个命令、多个进程、三份契约 |
| [ppt/](ppt/) | **PPT 汇报版**：2 页浓缩版 + 14 页详细版，含提纲与备注 |
| [counter-uav.md](counter-uav.md) | 反无选型的 Markdown 导航摘要 |
| [sim-training-stack-report.pdf](sim-training-stack-report.pdf) | LaTeX 报告：23 页，完整论证与参考文献 |
| [uav/index.html](uav/index.html) | 原有 UAV 仿真平台对比（Gazebo / AirSim / Flightmare / RflySim 等） |

## 目录结构

```
10.Simulators/
├── index.html                     # 本板块总览
├── README.md                      # 本文件
├── comparison.html                # 完整对比表（8 个对象，含 Gazebo）
├── comparison.md                  # 对比表 Markdown 版
├── comparison.csv                 # 对比表原始数据
├── counter-uav.html               # 反无选型导航（两条线）
├── counter-uav-simulators.html    # 只看仿真器（19 个）
├── counter-uav-stacks.html        # 只看训练栈（9 套）
├── counter-uav.md                 # 反无选型导航摘要
├── stack-anatomy.html             # 训练栈怎么「统一」：一个命令、多进程、三份契约
├── ppt/                           # PPT 汇报版（14 页）
│   ├── counter-uav-simulator-stack-deck.pptx
│   ├── build_deck.py
│   └── ppt-outline.md
├── sim-training-stack-report.pdf  # 最终报告（根目录副本）
├── assets/sim.css                 # 共享样式
├── uav/index.html                 # 原有 UAV 仿真对比（保留）
├── report/
│   ├── main.tex                   # 报告源码
│   ├── references.bib             # 参考文献（BibTeX 条目库）
│   └── sim-training-stack-report.pdf
├── 01.IsaacLab/
│   ├── index.html                 # 项目档案
│   └── resources.md               # 资源与复现入口
├── 02.MuJoCo/
├── 03.mjlab/
├── 04.UniLab/
├── 05.Newton/
└── 06.Genesis/
```

## 核心判断

1. **不是框架洗牌，是训练栈分层。** Isaac Lab、MuJoCo、Playground、mjlab、UniLab、Newton、Genesis 分别占据平台、物理、入口、运行时、引擎、评估等不同位置。
2. **竞争单位从 FPS 变成「每次有效验证的返工成本」。** 峰值仿真速度只影响训练时间的一段；任务搭建、sim2sim、评估与真机返工往往更贵。
3. **闭环能力才是分水岭。** 谁能把真机失败更快、更稳定地带回训练，谁更接近 Sim2Real；单个工具只是闭环上的一段。
4. **Gazebo 是仿真平台，不是训练框架。** 它补的是 ROS 2 / HIL / 多机器人 / 传感器集成；训练要外接 Gym wrapper、SB3、skrl 或 PX4 SITL。Gazebo Classic 已 EOL（2025-01-29），新项目用 Gazebo Sim（Jetty / Harmonic）。

## 六个训练栈项目 + Gazebo

| 项目 | 主层 | 一句话 |
|---|---|---|
| Isaac Lab | L4 平台 | 把资产、物理、传感、训练、部署收进同一工作台；3.0 起多后端、kit-less |
| MuJoCo / Playground | L5 物理 + L2 入口 | 可读的物理基座；Playground 把 time-to-robot 压短 |
| mjlab | L2 入口 | Isaac Lab 的 manager API + MuJoCo Warp，轻量、可组合、可调试 |
| UniLab | L3 运行时 | CPU 采样 + GPU 学习，统一运行时；3–10× 端到端提升 |
| Newton | L5 引擎 | Warp + MuJoCo Warp + OpenUSD；多物理、可微、LF 治理 |
| Genesis World | L1 评估 | 把仿真做成机器人基础模型的评估与迭代引擎 |
| **Gazebo Sim / Classic** | **L4/L5 仿真平台** | **ROS 2 / HIL / 多机器人强；不含训练循环；Classic 已 EOL（2025-01-29）** |

## 如何编译报告

需要 XeLaTeX（MiKTeX / TeX Live 均可）：

```bash
cd report
xelatex main.tex
xelatex main.tex
xelatex main.tex
```

生成 `sim-training-stack-report.pdf`（在 `report/` 内），再复制到板块根目录：

```bash
copy sim-training-stack-report.pdf ..
```

中文字体使用 `ctex` 的 Windows 字库（SimSun / SimHei / KaiTi）。
参考文献采用 `thebibliography` 手工条目，不依赖 Biber；`references.bib` 保留为可复用的 BibTeX 条目库。

> 注：仓库 `.gitignore` 忽略 `*.pdf`，因此 PDF 仅本地保留；HTML、Markdown 与 LaTeX 源码可正常提交。

## 数据口径

- 论文与版本信息以 arXiv、GitHub release、官方文档为准。
- UniLab 的 3–10×、Genesis 的 89%、mjlab 的「单命令」均为作者/厂商报告，带任务与硬件限定条件。
- 本目录中的「生态成熟度」是主观判断，不是量化指标。
