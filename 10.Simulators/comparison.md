# 训练栈对比表（含 Gazebo）

> 资料核对：2026-10-28 · 对应页面：[comparison.html](comparison.html) · 原始数据：[comparison.csv](comparison.csv)

## 先说结论

1. **Gazebo 不是训练框架**。它提供世界、物理、传感器、ROS 2 通信与多机器人仿真；训练循环要外接 Gym wrapper、SB3、skrl 或 PX4 SITL。
2. **Gazebo Classic 已 EOL**（2025-01-29）。新项目用 Gazebo Sim（Jetty / Harmonic），ROS 2 走 `ros_gz`。
3. **按层比较，而不是按品牌站队**：Gazebo 主要落在 L4/L5（仿真平台 + 物理），Isaac Lab 是 L4 全栈，Playground / mjlab 是 L2 入口，UniLab 是 L3 运行时，Newton 是 L5 引擎，Genesis 是 L1 评估。

## 主表

| 项目 / 版本 | 定位 / 栈层 | 物理引擎 | 并行 / 执行 | 渲染 | ROS / 传感器 / HIL | 可微 | 训练接口 | 许可 / 硬件 |
|---|---|---|---|---|---|---|---|---|
| **Isaac Lab** 3.0 GA（2026-10） | 全栈工作台 · L4 | PhysX / Newton（MJWarp·VBD·MPM）/ OVPhysX | GPU 并行；多 GPU / 多节点 | Isaac RTX / OVRTX / Newton Warp | ROS 2 bridge（经 Isaac Sim）；相机 / 深度 / IMU / 接触 / 力矩；HIL 需外接 | 部分（Newton） | 内置 manager API；RSL-RL / RL-Games / skrl / SB3 / RLinf / TorchRL | BSD-3 / NVIDIA GPU |
| **MuJoCo · Playground** | 物理基座 + 快速入口 · L5/L2 | MuJoCo / MJX / MJWarp | GPU（MJX / MJWarp）+ CPU | 原生 viewer / MJWarp batch renderer | 无原生 ROS；MuJoCo 传感器；HIL 需外接 | 部分（MJX） | Brax PPO / RSL-RL；Gymnasium | Apache-2.0 / CPU·GPU |
| **mjlab** | 轻量任务组织 · L2 | MuJoCo Warp | GPU 并行（示例 4096 envs） | MuJoCo / viser | 无原生 ROS；HIL 需外接 | 无 | manager API + RSL-RL（PPO） | Apache-2.0 / NVIDIA GPU |
| **UniLab** | 异构训练运行时 · L3 | MuJoCoUni / MotrixSim（CPU）+ MJWarp / Newton / IsaacGym / Genesis | CPU 采样 + GPU 学习；同步 / 异步 | Viser / Motrix | 无原生 ROS；HIL 需外接 | 无 | PPO / APPO / FastSAC / FlashSAC；Hydra | Apache-2.0 / CUDA·ROCm·MPS·XPU |
| **Newton** | 物理引擎 / 连接器 · L5 | MuJoCo-Warp / XPBD / Featherstone / VBD / MPM / Kamino | GPU（NVIDIA Warp） | Newton GL / USD / RTX | 无原生 ROS；传感器示例；HIL 需外接 | 是 | 无内置训练器；经 Isaac Lab 或自定义栈 | Apache-2.0 / NVIDIA Turing+ |
| **Genesis World** | 闭环评估基础设施 · L1 | Rigid / FEM / MPM / PBD·SPH / uipc / SAP | GPU 并行 + 异构环境 | Nyx / Luisa / Pyrender | 无原生 ROS；相机 / IMU / 触觉 / 接触 | 是（autodiff） | 无通用 RL 训练器；评估 / 数据引擎 + 示例 | Apache-2.0 / CUDA·ROCm·Metal·CPU |
| **Gazebo Sim** Jetty LTS（2025-09） | ROS 2 仿真平台 · L4/L5 | DART（参考实现）/ Bullet / Bullet-Featherstone / TPE | CPU 物理；多实例 / 多机器人；无 GPU 批量 RL | OGRE 2.x（ogre2） | ROS 2 原生（ros_gz）；丰富传感器；SITL/HIL 经 PX4/ArduPilot | 无 | 无内置 RL；外接 Gym wrapper / SB3 / skrl / PX4 SITL | Apache-2.0 / CPU + GPU 渲染 |
| **Gazebo Classic** 11（EOL 2025-01-29） | 通用仿真平台（维护模式）· L4/L5 | ODE（默认）/ Bullet / DART / Simbody | CPU 物理；多机器人；无 GPU 批量 RL | OGRE 1.x | ROS 1（gazebo_ros）；ROS 2 已转向 Gazebo Sim；HIL 经 PX4/ArduPilot | 无 | 无内置 RL；旧 gym-gazebo 生态 | Apache-2.0 / CPU |

> 「可微」指该栈是否提供可用的可微物理路径；「无」不等于不能做，而是需要外接或自己实现。
> Gazebo 的 HIL 能力来自 PX4 / ArduPilot SITL/HITL 工作流，不是 Gazebo 自身提供的训练接口。

## 能力矩阵

| 项目 | GPU 批量 RL | 内置任务 API | 批量渲染 | ROS 2 | SITL / HIL | 多物理 | 可微 | 跨厂商硬件 |
|---|---|---|---|---|---|---|---|---|
| Isaac Lab | ✓ | ✓ | ✓ | ~ | ~ | ✓ | ~ | ✗ |
| MuJoCo / Playground | ✓ | ~ | ✓ | ✗ | ✗ | ✗ | ~ | ✓ |
| mjlab | ✓ | ✓ | ~ | ✗ | ✗ | ✗ | ✗ | ✗ |
| UniLab | ~ | ✓ | ~ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Newton | ✓ | ✗ | ~ | ✗ | ✗ | ✓ | ✓ | ✗ |
| Genesis World | ✓ | ~ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Gazebo Sim | ✗ | ✗ | ✗ | ✓ | ~ | ✗ | ✗ | ✓ |
| Gazebo Classic | ✗ | ✗ | ✗ | ✗ | ~ | ✗ | ✗ | ✓ |

**图例**：✓ 原生 / 一等支持；~ 部分支持或需要外接；✗ 非目标 / 不支持。

## Gazebo 补的是哪一段

**强在系统集成**：
- ROS 2 原生：`ros_gz` bridge、launch、composition、QoS。
- SDF / URDF 资产与 Fuel 模型库，多机器人、复杂场景、传感器仿真。
- PX4 / ArduPilot 的 SITL/HITL 默认后端之一。
- 插件机制可扩展传感器噪声、执行器模型、环境控制。

**不负责训练循环**：
- 没有 manager API、reward 组合、curriculum、域随机化的统一抽象。
- 物理默认 CPU，缺少 GPU tensorized 批量环境，大规模 RL 吞吐不占优。
- 没有内置批量渲染 / 可微物理 / 多物理耦合。
- 训练要外接 Gym wrapper、SB3、skrl、RLlib，或 PX4 的 RL 工具链。

一句话：**Gazebo 更像「ROS 2 的操作系统 + 物理/传感器外设」，Isaac Lab 更像「机器人学习的 IDE + 运行时」。**

## 按任务选

| 你的任务 | 首选 | 组合建议 | 不建议 |
|---|---|---|---|
| UAV / ROS 2 / 多机器人 / HIL | Gazebo Sim（Jetty） | Gazebo + PX4 SITL + `ros_gz` + SB3 / skrl | Gazebo Classic（已 EOL） |
| 人形 / 四足全身控制 | Isaac Lab | Isaac Lab（PhysX + Newton）+ mjlab 快速消融 | 只靠 Gazebo 做大规模 RL |
| 快速验证 reward / 动作空间 | Playground / mjlab | Playground 起步 → mjlab 组织任务 → Isaac Lab 扩规模 | 一上来就搭最重平台 |
| 端到端训练吞吐瓶颈 | UniLab | UniLab + MuJoCoUni / MotrixSim + PPO / SAC 系列 | 视觉主导或软体任务 |
| 复杂接触 / 软体 / 可微 | Newton | Newton + Isaac Lab；先用双后端做 sim2sim | 要求开箱即用的稳定 baseline |
| 基础模型 / VLA 评估 | Genesis World | Genesis 做 real-to-sim 评估 + 真机日志回流 | 把厂商相关性当验收标准 |

## 数据口径

- Gazebo 版本以 2026-10 官方文档为准：Jetty LTS（2025-09 至 2031-05）；Classic 11 EOL 2025-01-29。
- 物理引擎与渲染信息来自 `gz-physics` / `gz-rendering` 文档：Gazebo Sim 支持 DART、Bullet、Bullet-Featherstone、TPE；渲染支持 OGRE 与 OGRE-Next（ogre2）。
- 表中「能力矩阵」是定性判断，不是 benchmark；未引用任何厂商性能数字。
- 训练栈项目的版本与数据口径见 [README.md](README.md) 与 [PDF 报告](sim-training-stack-report.pdf)。
