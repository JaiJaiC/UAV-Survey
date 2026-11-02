# Newton · 资源索引

> 层级：底层物理引擎 / 连接器（Layer 05）
> 资料核对日期：2026-10-28

## 一手资料

- **代码**：<https://github.com/newton-physics/newton>
- **文档**：<https://newton-physics.github.io/newton/latest/guide/overview.html>
- **安装/兼容性**：<https://newton-physics.github.io/newton/latest/guide/installation.html>
- **Linux Foundation 公告**：<https://www.linuxfoundation.org/press/linux-foundation-announces-contribution-of-newton-by-disney-research-google-deepmind-and-nvidia-to-accelerate-open-robot-learning>
- **NVIDIA 发布博客**：<https://developer.nvidia.com/blog/announcing-newton-an-open-source-physics-engine-for-robotics-simulation/>
- **NVIDIA 教程（Isaac Lab + Newton）**：<https://developer.nvidia.com/blog/train-a-quadruped-locomotion-policy-and-simulate-cloth-manipulation-with-nvidia-isaac-lab-and-newton/>
- **Isaac Lab Newton 后端**：<https://isaac-sim.github.io/IsaacLab/v3.0.0/source/concepts/physics-backends/newton.html>

## 关键事实

| 项 | 内容 |
|---|---|
| 发起方 | Disney Research、Google DeepMind、NVIDIA |
| 治理 | Linux Foundation |
| 许可 | Apache-2.0；文档 CC-BY-4.0 |
| 计算基座 | NVIDIA Warp（泛化 `warp.sim`） |
| 主后端 | MuJoCo Warp |
| 场景表达 | OpenUSD |
| 求解器 | MuJoCo-Warp、XPBD、Featherstone、VBD、MPM、Kamino |
| 能力 | 刚体、可变形、布料、线缆、肌腱、颗粒、多物理耦合、可微 |
| 平台 | Linux x86-64/aarch64、Windows x86-64、macOS（CPU） |
| GPU 要求 | Turing+（compute capability 7.5+），驱动 R580+（Warp 1.18） |
| Python | 3.10+（3.10 已弃用，建议 3.11+） |

## 快速开始

```bash
pip install "newton[examples]"
python -m newton.examples --list
python -m newton.examples basic_pendulum
python -m newton.examples robot_g1 --device cuda:0
```

## 在 Isaac Lab 中使用

```bash
# 3.0 GA：Newton + MuJoCo-Warp，无需 Isaac Sim
uv run isaaclab train \
  --rl_library rsl_rl \
  --task Isaac-Cartpole \
  --viz newton_gl \
  physics=newton_mjwarp
```

- `isaaclab_newton` 是 3.0 的后端扩展包。
- 支持 MJWarp、VBD、MPM、Kamino 等求解路径；具体任务支持需查 `--show_presets`。
- GA 提供 PhysX↔Newton 策略迁移指南，可用于 sim2sim 验证。

## 阅读顺序建议

1. 先读 README 的定位段：Warp、warp.sim、MuJoCo Warp、USD、可微、Linux Foundation。
2. 再看 example 列表，判断你关心的物理类型（刚体/布料/MPM/线缆）当前覆盖到什么程度。
3. 如果用在 Isaac Lab 里，先读 3.0 的 Newton backend 文档与 supported features，再动手迁移任务。
4. 最后看 release notes / known limitations，确认哪些功能仍是 backend-specific。

## 相邻项目

- **Isaac Lab**：<https://github.com/isaac-sim/IsaacLab>
- **MuJoCo Warp**：<https://github.com/google-deepmind/mujoco_warp>
- **NVIDIA Warp**：<https://github.com/NVIDIA/warp>
- **OpenUSD**：<https://openusd.org/>
- **Kamino**：Newton 生态中的求解器/示例方向，见仓库 `newton/examples/kamino/`
