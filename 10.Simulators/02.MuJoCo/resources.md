# MuJoCo / MuJoCo Playground · 资源索引

> 层级：物理基座（Layer 05）+ 快速入口（Layer 02）
> 资料核对日期：2026-10-28

## 一手资料

- **Playground 论文**：MuJoCo Playground
  - arXiv: <https://arxiv.org/abs/2502.08844>
  - PDF: <https://arxiv.org/pdf/2502.08844>
  - 作者：Kevin Zakka, Baruch Tabanpour, Qiayuan Liao 等
  - 提交：2025-02-12
  - 荣誉：RSS 2025 Outstanding Demo Paper Award
- **Playground 项目页**：<https://playground.mujoco.org/>
- **Playground 代码**：<https://github.com/google-deepmind/mujoco_playground>
- **MuJoCo 代码**：<https://github.com/google-deepmind/mujoco>
- **MuJoCo 文档**：<https://mujoco.readthedocs.io/>
- **MuJoCo Warp**：<https://github.com/google-deepmind/mujoco_warp>
- **MJX 文档**：<https://mujoco.readthedocs.io/en/stable/mjx.html>

## 关键论文与历史节点

| 时间 | 事件 | 说明 |
|---|---|---|
| 2012 | MuJoCo 论文 | Todorov, Erez, Tassa, IROS 2012 |
| 2021 | DeepMind 开源 MuJoCo | Apache-2.0，社区生态迅速扩大 |
| 2024 | MJX 成熟 | JAX 后端，GPU/TPU 批量仿真 |
| 2025-02 | MuJoCo Playground | MJX + 批量渲染 + 训练环境 + sim2real |
| 2025 | MJWarp 接入 Playground | 支持 `--impl warp`，与 Isaac Lab / Newton 共用 Warp 路线 |

## 复现入口

```bash
# 安装
pip install playground

# 训练（MJX）
train-jax-ppo --env_name CartpoleBalance

# 训练（MuJoCo Warp）
train-jax-ppo --env_name CartpoleBalance --impl warp
train-rsl-ppo --env_name CartpoleBalance --impl warp

# 从源码（推荐，获取最新环境）
git clone https://github.com/google-deepmind/mujoco_playground.git
cd mujoco_playground
uv venv --python 3.12
uv pip install -U "jax[cuda12]"
uv --no-config sync --all-extras
```

## 推荐阅读顺序

1. Playground 项目页的真机视频：先建立「这套东西能上真机」的直觉。
2. 论文第 3 节：看它如何把物理、渲染、训练环境打包成一条链路。
3. 代码里的 `locomotion/` 与 `manipulation/`：挑一个最接近自己任务的环境，改 reward 跑通。
4. 再回到 MuJoCo 文档的接触模型与执行器章节，理解 sim2sim 差异从哪里来。

## 相邻项目

- **mjlab**：把 Isaac Lab 的 manager API 接到 MuJoCo Warp，见 `../03.mjlab/`
- **Newton**：以 MuJoCo Warp 为主要后端，见 `../05.Newton/`
- **UniLab**：把 MuJoCo（MuJoCoUni）作为 CPU 批量后端之一，见 `../04.UniLab/`
- **Isaac Lab**：3.0 的 Newton 后端同样走 MuJoCo Warp，见 `../01.IsaacLab/`
