# UniLab · 资源索引

> 层级：运行时与异构调度（Layer 03）
> 资料核对日期：2026-10-28

## 一手资料

- **论文**：UniLab: A Heterogeneous Architecture for Robot RL Beyond GPU-Dominant Paradigms
  - arXiv: <https://arxiv.org/abs/2605.30313>
  - 项目页（含完整 HTML、图表、附录）: <https://unilabsim.github.io/paper/index.html>
  - 会议：CoRL 2026
  - 通讯：Yufei Jia（THU）
- **代码**：<https://github.com/unilabsim/UniLab>
- **文档**：<https://unilabsim.github.io/UniLab-doc/>
- **项目主页**：<https://unilabsim.github.io/>

## 核心数字

| 项目 | 数值 | 出处 |
|---|---|---|
| 端到端效率提升 | 3–10× | 论文摘要 |
| G1 Flip（PPO） | 3.3× | 论文第 4.3 节 |
| G1 Walk Flat（FastSAC） | 8.4× | 论文第 4.3 节 |
| G1 Motion Tracking（FlashSAC） | 11.0× | 论文第 4.3 节 |
| 受控硬件 | RTX 4090 + Ryzen 9 9950X3D + 64 GB | 论文第 4.1 节 |
| CPU 吞吐（Go2, 9950X3D） | MJ 246k / Motrix 704k steps/s | 论文表 2 |
| 跨平台 | macOS、ROCm、XPU | 论文第 4.5 节 |

## 复现入口

```bash
# 安装
git clone https://github.com/unilabsim/UniLab.git
cd UniLab
make setup

# 训练 + 回放（MuJoCo）
uv run train --algo sac --task g1_walk_flat --sim mujoco
uv run eval  --algo sac --task g1_walk_flat --sim mujoco --render-mode viser

# 换后端做 sim2sim
uv run --extra motrix  eval --algo sac --task g1_walk_flat --sim motrix  --load-run -1
uv run --extra newton  eval --algo sac --task g1_walk_flat --sim newton  --load-run -1
uv run --extra isaacgym eval --algo sac --task g1_walk_flat --sim isaacgym --load-run -1

# MuJoCo Warp 训练 + Genesis 评估
uv run --extra mjwarp  train --algo flashsac --task g1_motion_tracking --sim mjwarp
uv run --extra genesis eval  --algo flashsac --task g1_motion_tracking --sim genesis --load-run -1
```

## 支持矩阵与后端

| 后端 | 角色 | 备注 |
|---|---|---|
| MuJoCoUni | CPU 批量物理 | 论文主力后端 |
| MotrixSim | CPU 批量物理 + 渲染 | Motphys 提供 |
| MuJoCo Warp | GPU 物理 | 训练/评估 |
| Newton | GPU 物理 | sim2sim |
| Isaac Gym | GPU 物理 | 兼容旧栈 |
| Genesis | GPU 物理 + 渲染 | sim2sim / 评估 |

## 相邻项目

- **mjlab**：UniLab 明确致谢其轻量实现与工程实践。
- **Isaac Lab**：manager API 与 Hydra 任务组织的思想来源之一。
- **MuJoCoUni**：<https://arxiv.org/abs/2605.24922>
- **MotrixSim**：Motphys 的机器人仿真引擎。

## 阅读顺序建议

1. 先看论文第 1 节的「systems framing」，理解它为什么不是算法论文。
2. 看第 3.2 节的 execution architecture 与 Figure 3 的时序图。
3. 再看第 4.3 节的训练周期放置消融，理解「谁在等谁」。
4. 最后读 Limitations，确认自己的任务是否落在「仿真主导 + 可解耦」范围内。
