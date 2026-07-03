# 多无人机灵活编队控制 — 学习笔记摘要

> 论文: Flexible multi-UAV formation control via integrating deep reinforcement learning and affine transformations
> 期刊: Aerospace Science and Technology (2025) · NUDT

---

## 核心创新：模型-数据混合驱动框架

将编队约束拆解为两个子问题，分别用不同范式解决：

| 层级 | 方法 | 机制 | 解决问题 |
|------|------|------|----------|
| 决策层 | **模型驱动** | 仿射变换 + 应力矩阵 + Leader-Follower | 编队结构完整性 |
| 执行层 | **数据驱动** | DRL (PPO) per UAV · CNN+FC 网络 | 安全导航 + 避障 |

---

## 决策层关键公式

**仿射变换 (Eq.5)**：`x'(t) = (A(t) ⊗ I_d) · x + [1_N ⊗ I_d] · b(t)`

- A(t): 旋转 · 缩放 · 剪切
- b(t): 平移
- 保持共线性 → 结构完整性

**跟随者目标 (Eq.8)**：`p_f*(t) = −Ω_ff⁻¹ · Ω_fl · p_l(t)`

- 每个 follower 独立计算 → 分布式无中心节点

---

## 执行层关键设计

- **观测**：LiDAR 270° × 3层 + 速度[v,ω] + 相对目标位置Δp
- **网络**：CNN(3层Conv1D) → Concat(v,ω,Δp) → FC(128)+ReLU → Actor/Critic
- **动作**：a = [v_cmd, ω_cmd] 端到端速度控制
- **UAV模型**：独轮车运动学 (Unicycle)

---

## 奖励设计

`r = r_target + r_collision + r_smooth1 + r_smooth2`

- r_target: 到达奖励(+15) + 过程奖励(Δ距离)
- r_collision: 碰撞惩罚(-15)
- r_smooth1: 大角速度惩罚(|ω|>0.7)
- r_smooth2: heading偏差惩罚/距离权重（自适应——远距离允许绕路，近距离强制对准）

---

## 训练策略

1. **两阶段课程学习**：Stage 1 无障碍(~70k iter) → Stage 2 复杂障碍
2. **PPO KL-penalty 变体**：自适应KL惩罚系数
3. **邻居=动态障碍物**：训练时只有静态障碍物，UAV间自然充当动态障碍
4. **硬件**：Ubuntu 20.04 · 32GB · RTX 3090 · ~24h

---

## 实验结果亮点

- A-F方法编队精度最高但**全部碰撞**(50/50)——纯模型驱动无法避障
- 本文方法综合最优：飞行时间最短、运动最平滑(Jerk最小)、编队误差有竞争力
- 可扩展到4~10架UAV

---

## 8个科研Tricks

1. 混合驱动：数学模型处理结构约束 + DRL处理难以建模的部分
2. 邻居=动态障碍物：巧妙的训练策略，无需专门生成动态障碍物
3. 两阶段课程学习：简单→复杂，大幅加速收敛
4. Eq.(8)的分布式优雅性：每个follower独立计算目标，无需中心节点
5. 自适应heading惩罚：距离相关权重（远→自由探索，近→精确对准）
6. PPO KL-penalty变体：多智能体训练可能更稳定
7. 多维度评价指标：安全+编队质量+运动质量
8. 充分调优的baseline对比：让对比方法也充分发挥

---

## 与OpenFlight的对比

| 维度 | OpenFlight | 本文 |
|------|-----------|------|
| 核心哲学 | "Less is more" | "Model-Data Hybrid" |
| UAV数量 | 单机 | 多机(4~10) |
| 动力学 | 6-DOF 高保真 | 独轮车(简化) |
| 控制层级 | 三级(速度→姿态→舵面) | 两层(决策→执行) |
| DRL位置 | 全部层级可替换 | 仅执行层 |
| 模型驱动部分 | PID自动驾驶仪 | 仿射变换+应力矩阵 |
| 核心贡献 | RL首次直接控制舵面 | 混合驱动框架灵活编队避障 |

---

## 改进方向

- 独轮车 → 6-DOF固定翼（结合OpenFlight的JSBSim）
- 2D → 3D空间编队
- 引入Attention处理可变数量UAV
- CTDE + 参数共享
- 通信约束（延迟/丢包/带宽）
- Sim-to-Real 实机部署
