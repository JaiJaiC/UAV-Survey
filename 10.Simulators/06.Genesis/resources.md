# Genesis World · 资源索引

> 层级：闭环评估与仿真基础设施（Layer 01）
> 资料核对日期：2026-10-28

## 一手资料

- **Genesis World 1.0 博客**：The role of simulation in scalable robotics, Genesis World 1.0, and the path forward
  - <https://www.genesis.ai/blog/the-role-of-simulation-in-scalable-robotics-genesis-world-10-and-the-path-forward>
  - 发布：2026-05
- **代码**：<https://github.com/Genesis-Embodied-AI/genesis-world>
- **文档**：<https://genesis-world.readthedocs.io/en/latest/>
- **PyPI**：<https://pypi.org/project/genesis-world/>（1.4.5，2026-10-22）
- **Nyx**：<https://github.com/Genesis-Embodied-AI/genesis-nyx>
- **Quadrants**：<https://github.com/Genesis-Embodied-AI/quadrants>

## 核心主张与数字

| 主张 | 数值 | 备注 |
|---|---|---|
| 评估提速 | 约 166–200 小时 → 约 30 分钟 | 厂商口径；中文报道为 166 小时 / 30 分钟，博客转述有 200 小时 / 0.5 小时 |
| 仿真–真机相关性 | 约 89% | 特定任务与模型规模；需独立验证 |
| 评估任务示例 | 约 4 万次独立试验的灵巧手抓取 | 公开报道口径 |
| 定位 | 机器人基础模型的评估与迭代引擎 | 不只是数据生成器 |

> 读这些数字时，务必区分「厂商自报」「特定任务」「特定硬件」三个限定条件。

## 四层系统栈

| 层 | 内容 |
|---|---|
| Simulation Interface | 资产解析（URDF / MJCF / OBJ / GLB / USD）、控制器、传感器、并行/异构环境、GUI |
| Render | Nyx（自研实时光追）、Luisa、Pyrender；3DGS、PBR、多相机 |
| Physics | Rigid、FEM、MPM、PBD/SPH、uipc、Coupler、SAP；共享场景与状态 |
| Compiler | Quadrants（Taichi fork）→ CUDA、ROCm、Metal、Vulkan、x86、ARM64；autodiff、GPU graphs、fastcache |

## 快速开始

```bash
pip install genesis-world

# 运行示例
python examples/rigid/single_franka.py
python examples/tutorials/control_your_robot.py
```

## 评估方法论（比数字更值得学）

1. **分布分离**：策略只用真实数据训练，仿真只做评估，避免「训练/评估同分布」导致的虚高。
2. **并排 rig**：仿真与真机同初始化并行，观测可按层混合（sim / real），用于归因物理、渲染、控制、通信的 gap。
3. **正交扰动轴**：Visual / Behavioral / Semantic 三个轴做单参数扫描，定义各轴 robustness。
4. **闭环回流**：失败样本回流到数据采集与下一轮训练，而不是只出一个分数。

## 名称辨析

- **Genesis（2024-12 开源项目）**：社区/学术起源的通用物理引擎。
- **Genesis World 1.0（2026-05）**：Genesis AI 的全栈仿真基础设施。
- **GENE-26.5**：Genesis AI 的机器人操作基础模型，与仿真栈不是同一事物。

引用时请核对主体，避免把三者混为一谈。

## 相邻项目

- **Isaac Lab**：大平台路线，强在资产、传感、部署与多后端。
- **Newton**：底层物理引擎，强在多物理、可微与治理。
- **MuJoCo / Playground**：轻量物理与快速入口。
- **UniLab**：训练运行时，可与 Genesis 做 sim2sim 评估。

## 阅读顺序建议

1. 先读博客的「评估与迭代引擎」段落，理解它为什么不从「生成训练数据」讲起。
2. 再看四层栈与 Nyx / Quadrants 的设计，理解「全栈」具体指什么。
3. 最后看评估方法论与相关性数字，判断哪些能迁移到自己的任务。
