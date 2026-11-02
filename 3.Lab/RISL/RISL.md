# CMU - RISLab (Resilient Intelligent Systems Lab)

- **Institution**: Carnegie Mellon University — Robotics Institute (RI)
- **PI**: Prof. Wennie Tabib
- **Website**: https://rislab.org/
- **GitHub**: https://github.com/rislab
- **Publications**: https://rislab.org/publications.html
- **Code**: https://rislab.org/code.html
- **Blog / News**: https://rislab.org/blog.html
- **Contact**: wtabib@cmu.edu
- **Location**: Pittsburgh, PA, USA

> 中文：卡内基梅隆大学机器人研究所 **韧性智能系统实验室（RISLab）**，由 Wennie Tabib 教授领导。
> 研究目标是"让自主系统更可靠"——在洞穴、森林、废墟等退化/非结构化环境中，同时保证
> **感知的紧凑性（低带宽可通信）**、**规划的安全性（概率化碰撞）** 与 **飞行的敏捷性**。

## 中文速览

| 维度 | 内容 |
|---|---|
| 一句话定位 | 用高斯混合模型（GMM）做统一感知表示，配合信息论主动探索与学习控制，实现退化环境下的韧性自主飞行 |
| 技术主线 | SOGMM/GIRA（连续概率地图）→ 信息论探索/主动搜索 → 概率碰撞与安全规划 → 可微仿真强化学习控制 |
| 代表成果 | 洞穴自主测绘（T-RO 2021，King-Sun Fu 最佳论文荣誉提名）；快速四旋翼导航（SSRR 2024 最佳论文）；分层避障遥操作（SSRR 2022 最佳论文） |
| 2025-2026 热点 | 可微四旋翼动力学 RL 拦截（10 m/s 空中拦截）、双向推力特技翻转（AcroRL）、特权信息 RL 越野导航（ICRA 2026）、零样本单目度量深度（ICRA 2026） |
| 开源资产 | GIRA 框架与教程（RSS 2023 tutorial）、`rislab/depthnav`（44★）、`rislab/acrorl`、`rislab/mono_depth_rescaler` |
| 对 UAV 综述的价值 | "概率地图 + 信息论探索 + 安全约束 + 学习控制"四位一体的少数团队，且几乎全部开源 |

## Key Research Areas

1. **Compact probabilistic perception** — 以 GMM/自组织 GMM（SOGMM）表示几何与强度，兼顾高分辨率重建与低带宽传输。
2. **Information-theoretic exploration & active search** — 实时信息增益规划、条件互信息、多模态传感器、未知目标数量的主动搜索。
3. **Resilient / safe navigation** — 概率碰撞检测（椭球机器人 vs 高斯表面）、自适应速度、无通信退化下的安全策略。
4. **Learning-based agile flight** — 可微仿真 + 解析策略梯度、特权信息（privileged information）、sim-to-real 外场验证。
5. **Aerial robotic field autonomy** — 洞穴、森林、矿区等 GPS-denied、无光/弱光环境的整机系统集成。
6. **Human-robot teaming** — 头盔深度相机隐式协同探索、自适应速度遥操作。

## Research Projects

| Project | Year | One-line |
|---|---|---|
| [Learning Agile Intruder Interception using Differentiable Quadrotor Dynamics](https://rislab.org/projects/catchrl.html) | 2026 | 仅用 3D 方向单位向量 + 可微四旋翼动力学做解析策略梯度，实现 10 m/s 空中拦截，比点质量基线高约 30% |
| [AcroRL: Aggressive Quadrotor Inversion using Bidirectional Thrust](https://rislab.org/projects/2026-05-14-acro-rl.html) | 2026 | RL 调制参考轨迹，实现位置受限的双向推力翻转；位置 RMSE −32%、调节时间 −57% |
| [Rapid Navigation in Diverse Environments](https://rislab.org/projects/2024-11-07-high-speed-flight.html) | 2024 | 机载深度相机的反应式前向弧运动基元，洞穴/森林高速安全飞行，成功率 +24% |
| [Large-Scale Decentralized Multirobot Active Search](https://rislab.org/projects/2024-02-02-decentralized-multirobot-active-search.html) | 2024 | 去中心化、不确定性驱动的多机主动搜索，通信拒止下仍可扩展 |
| [Collaborative Human-Robot Exploration via Implicit Coordination](https://rislab.org/projects/2022-09-24-human-robot-collaborative-exploration-ydkg.html) | 2022 | 头盔深度相机隐式传达感兴趣区域，机器人进入人无法到达的空间 |
| [Scalable and Adaptive Aerial Robotic Exploration](https://rislab.org/projects/2022-09-24-scalable-adaptive-robot-exploration-kgwt.html) | 2022 | 内存高效的多旋翼建图与规划，生成高保真环境地图 |
| [Assistive Adaptive-Speed Multirotor Teleoperation](https://rislab.org/projects/2022-09-24-hierarchical-collision-avoidance-kgyd.html) | 2022 | 分层碰撞检测自适应调整地图分辨率与最大速度，穿越狭窄间隙/隧道 |
| [Autonomous Cave Surveying](https://rislab.org/projects/2021-09-15-autonomous-cave-surveying-wtks.html) | 2021 | 全黑洞穴自主测绘：深度相机建图 + 下视相机状态估计 + 前后照明 |
| [Variable Resolution Occupancy Mapping using GMMs](https://rislab.org/projects/2018-12-24-variable-resolution-cowt.html) | 2018 | 从 GMM 采样并光线投射得到变分辨率占据，避免稠密多分辨率栅格存储 |
| [On-Manifold GMM Registration](https://rislab.org/projects/2018-07-16-on-manifold-gmm-wtco.html) | 2018 | 把深度/LiDAR 观测当作连续信念分布，在流形上做 GMM 配准 |
| [Efficient Multi-Sensor Exploration using Conditional Mutual Information](https://rislab.org/projects/2016-10-09-computationally-efficient-wtmc.html) | 2016 | 用条件互信息处理异构传感器的相关观测，避免信息重复计数 |

## Awards & Recognition

- **IEEE T-RO King-Sun Fu Memorial Best Paper Award — Honorable Mention** (2023)：*Autonomous Cave Surveying with an Aerial Robot*
- **Best Paper Award, IEEE SSRR 2024**：*Rapid Quadrotor Navigation in Diverse Environments using an Onboard Depth Camera*
- **Best Paper Award, IEEE SSRR 2022**：*Hierarchical Collision Avoidance for Adaptive-Speed Multirotor Teleoperation*
- **ICRA 2026**：2 篇（特权信息 RL 导航、零样本单目度量深度）
- **IROS 2025 / ISER 2025**：高斯表面距离与碰撞概率估计；去中心化主动搜索
- **RSS 2025 Workshop**（与 MIT 合办）：Gaussian Representations for Autonomy
- **RSS 2023 Tutorial**：GIRA — Gaussian Mixture Models for Inference and Robot Autonomy

## Robots / Platforms

Lab-site platforms: **Rocky**（洞穴测绘项目所用平台，系统配深度相机、下视相机与前后照明）、**Omicron**（遥操作/探索项目中出现）、**Acerodon**、**Danaus**、**Crazyflie**（小型/室内平台）。
机载计算强调 SWaP 约束：单线程低功耗 CPU 上微秒级椭球碰撞估计、15 Hz 机载度量深度。

## Open-Source Code

| Repo | What it is |
|---|---|
| [rislab/depthnav](https://github.com/rislab/depthnav) | 深度相机自主导航策略的研究框架（Python, 44★, MIT） |
| [rislab/acrorl](https://github.com/rislab/acrorl) | AcroRL 双向推力翻转的 RL 实现（JAX 仿真 + 硬件） |
| [rislab/mono_depth_rescaler](https://github.com/rislab/mono_depth_rescaler) | 单目相对深度 → 度量深度的视觉惯性重标定 |
| [rislab/catchrl](https://github.com/rislab/catchrl) | 可微四旋翼动力学拦截策略 |
| [gira3d](https://gira3d.github.io) / [github.com/gira3d](https://github.com/gira3d) | GIRA 教程、文档与代码（RSS 2023 tutorial）；GIRA 框架见 ICRA 2023 |
| [rislab/D-Map](https://github.com/rislab/D-Map)、CopperTag、AAMED | 占据建图 / 基准标记 / 椭圆检测等 fork（工程依赖） |

## People

- **Faculty**: Wennie Tabib
- **Staff / Research**: Abhishek Rathod, John Stecklein, Edsel Burkholder, Kshitij Goel, Nishanth Bobbili
- **PhD**: Mike Anoruo
- **MS**: Johnny (Xiaoyu) Tian, Gabriel Rodriguez, Michael Allen
- **Undergrad**: Steven Yang, Henri Sayag, Aaron Ding
- **Alumni**: Nicole Chan (M.S. 2026), Jonathan Lee (M.S. 2025 → Nimble Robotics), Akshay Chekuri (→ Shield AI), Lucky Kant Nayak (→ CMU MSR), Ankit Khandelwal (→ Viam), Rohan Dhesikan (→ Tesla Autopilot), Yves Georgy Daoud (→ Agility Robotics)

## Collaborations / Funding Signals

- **CMU NREC**（SSRR 2024 最佳论文合作）
- **MIT**（RSS 2025 GMM workshop 共同组织）
- 项目致谢中出现 **AI2C Seed grant**、**NVIDIA Academic Grant Program**

## Why Track This Lab (UAV survey relevance)

1. **地图表示**：GMM 是 voxel/TSDF/NeRF 之外的一条"紧凑连续表示"路线，可直接对比内存-精度权衡。
2. **探索与主动感知**：信息论目标 + 去中心化多机，是"大范围未知环境搜索"的强基线。
3. **安全规划**：概率碰撞 + 椭球机体 + 自适应速度，填补"高速飞行"与"搜救安全"之间的空白。
4. **学习控制**：可微仿真下的解析策略梯度是对 PPO 类 model-free RL 的替代方案，样本效率更高。
5. **可复现性**：论文配套代码/视频齐全，适合作为综述中的"开源系统"案例。

## Tracking Feeds

- arXiv: `au:"Wennie Tabib"`；`au:"Kshitij Goel" AND (all:quadrotor OR all:exploration OR all:mapping)`
- Lab blog: https://rislab.org/blog.html （有大事才更新，配合 `crawl_labs.py` 周更）
- GitHub org: https://github.com/rislab （新仓库 = 新论文信号；`depthnav`、`acrorl` 均在论文前后放出）
- Per-paper videos on YouTube（各项目页内嵌）

## Sources

- Home: https://rislab.org/
- Research: https://rislab.org/research.html
- Publications: https://rislab.org/publications.html
- Code: https://rislab.org/code.html
- Blog: https://rislab.org/blog.html
- Openings: https://rislab.org/openings.html
- GitHub org API: https://api.github.com/orgs/rislab/repos
