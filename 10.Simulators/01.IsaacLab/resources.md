# Isaac Lab · 资源索引

> 层级：大平台 / 统一工作台（Layer 04）
> 资料核对日期：2026-10-28

## 一手资料

- **论文**：Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning
  - arXiv: <https://arxiv.org/abs/2511.04831>
  - PDF: <https://arxiv.org/pdf/2511.04831>
  - 作者：NVIDIA（Mayank Mittal, Pascal Roth, James Tigue 等）
  - 提交：2025-11-06
- **代码**：<https://github.com/isaac-sim/IsaacLab>
- **文档**：<https://isaac-sim.github.io/IsaacLab/>
- **3.0 Release Notes**：<https://github.com/isaac-sim/IsaacLab/releases/tag/v3.0.0>

## 关键版本节点

| 时间 | 事件 | 说明 |
|---|---|---|
| 2021 | Isaac Gym | GPU 并行仿真 + RL 的起点 |
| 2025-11 | Isaac Lab 论文 | 多模态、传感器、数据采集、域随机化统一 |
| 2026-03 | 3.0 Beta | 多后端、Newton、kit-less、Warp 数据通路 |
| 2026-10-20 | 3.0 GA | PhysX / Newton / OVPhysX 可选；统一 `isaaclab` CLI |

## 3.0 需要记住的 API 变化

- 四元数：`(w, x, y, z)` → `(x, y, z, w)`
- 数据属性：返回 `ProxyArray`，显式取 `.torch` / `.warp`
- schema：组合配置 → 可组合 fragment（`UsdPhysicsRigidBodyCfg` + `PhysxRigidBodyCfg`）
- 训练入口：`scripts/reinforcement_learning/*/train.py` → `isaaclab train --rl_library ...`
- 可视化：`--headless` → `--viz` / `--viz none`
- 传感器：2.x 的 `IMU` → `PVA`；新 `IMU` 只报角速度与线加速度

## 复现入口

```bash
# 最小验证：Newton 后端 + MuJoCo-Warp，无需 Isaac Sim
git clone --branch v3.0.0 --depth 1 https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

uv run isaaclab train \
  --rl_library rsl_rl \
  --task Isaac-Cartpole \
  --viz newton_gl \
  physics=newton_mjwarp

# 完整 Isaac Sim / PhysX 路径
uv run --extra isaacsim isaaclab train \
  --rl_library rsl_rl \
  --task Isaac-Cartpole \
  --viz kit \
  physics=isaacsim_physx
```

## 生态与相邻项目

- **Newton**：<https://github.com/newton-physics/newton>（3.0 的一等物理后端）
- **MuJoCo Warp**：<https://github.com/google-deepmind/mujoco_warp>
- **OpenUSD**：<https://openusd.org/>
- **NVIDIA Warp**：<https://github.com/NVIDIA/warp>
- **RSL-RL**：<https://github.com/leggedrobotics/rsl_rl>
- **Isaac Sim**：<https://developer.nvidia.com/isaac-sim>

## 阅读顺序建议

1. 先读论文摘要 + 第 3 节（系统设计），建立「平台」而不是「仿真器」的心智模型。
2. 再读 3.0 release notes 的 Highlights，理解多后端与 kit-less 的动机。
3. 最后看 `Backends and Presets` 文档，确认你的任务支持哪些 `physics=` / `renderer=` 组合。
