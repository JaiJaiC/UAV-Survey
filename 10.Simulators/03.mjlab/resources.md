# mjlab · 资源索引

> 层级：任务与环境入口（Layer 02）
> 资料核对日期：2026-10-28

## 一手资料

- **论文**：mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning
  - arXiv: <https://arxiv.org/abs/2601.22074>（v1 2026-01-29，v2 2026-02-25）
  - PDF: <https://arxiv.org/pdf/2601.22074>
  - 作者：Kevin Zakka, Qiayuan Liao, Brent Yi, Louis Le Lay, Koushil Sreenath, Pieter Abbeel
- **代码**：<https://github.com/mujocolab/mjlab>
- **文档**：<https://mujocolab.github.io/mjlab/>

## 关键设计

| 设计 | 作用 |
|---|---|
| manager-based API | observation / reward / event / command / curriculum / metrics 可组合 |
| MjSpec → MjModel | 保留 MuJoCo 原生模型编译链路 |
| MuJoCo Warp | GPU 并行物理，示例单卡 4096 envs |
| 原生数据访问 | 出问题能按 MuJoCo 的方式排查 |
| 单命令安装 | `uvx --from mjlab --refresh demo` |
| dummy agents | `--agent zero` / `--agent random` 做 MDP sanity check |
| 多 GPU | `--gpu-ids "[0, 1]"` |

## 复现入口

```bash
# 零安装 demo
uvx --from mjlab --refresh demo

# 源码安装
git clone https://github.com/mujocolab/mjlab.git && cd mjlab
uv run demo

# 速度跟踪（G1，4096 envs）
uv run train Mjlab-Velocity-Flat-Unitree-G1 --env.scene.num-envs 4096

# 动作模仿
uv run train Mjlab-Tracking-Flat-Unitree-G1 \
  --registry-name your-org/motions/motion-name \
  --env.scene.num-envs 4096

# MDP 自检
uv run play Mjlab-Your-Task-Id --agent zero
uv run play Mjlab-Your-Task-Id --agent random
```

## Unitree 生态

- **unitree_rl_mjlab**：<https://github.com/unitreerobotics/unitree_rl_mjlab>
- 支持机型：Go2、A2、As2、G1、R1、H1_2、H2
- 流程：Train → Play → Sim2Real
- 训练时导出 `policy.onnx` / `policy.onnx.data`；部署前用 <code>unitree_mujoco</code> 做仿真验证
- 机型任务：`Unitree-Go2-Flat`、`Unitree-G1-Flat`、`Unitree-G1-23Dof-Flat`、`Unitree-H1_2-Flat`、`Unitree-A2-Flat`、`Unitree-R1-Flat`

## 与相邻项目的关系

- **Isaac Lab**：mjlab 复用其 manager API 设计；Isaac Lab 的 Newton 后端同样基于 MuJoCo Warp。
- **MuJoCo Playground**：都基于 MuJoCo，但 Playground 更偏「环境库 + 训练脚本」，mjlab 更偏「任务组织框架」。
- **UniLab**：UniLab 的 Hydra + manager term 设计明确参考了 Isaac Lab 与 mjlab。

## 阅读顺序建议

1. 先跑 `uvx --from mjlab --refresh demo`，感受启动成本。
2. 读论文第 3 节与架构图，理解 `MjSpec → MjModel → MjWarp` 的链路。
3. 用 `--agent zero/random` 检查一个任务，再改 reward 做一次消融。
4. 如果要上真机，直接看 `unitree_rl_mjlab` 的 Train / Play / Sim2Real 流程。
