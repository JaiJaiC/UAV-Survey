# 两页版 · 讲稿提纲

> 2 页 / 约 3 分钟  
> 核心：P1 只讲仿真器，P2 只讲训练栈。

## P1 · 仿真器：三条互补线

**一句话开场**：仿真器不选全能冠军，按角色选三条线。

| 线 | 首选 | 什么时候用 | 边界 |
|---|---|---|---|
| 系统闭环 | Gazebo Sim + PX4 / RflySim | PX4、两机、MAVLink、HITL | 视觉中等、CPU 单实例 |
| 气动复核 | JSBSim + FlightGear / X-Plane | 配平、失速、侧滑、风扰 | 无 RL、多机弱 |
| 视觉验证 | RflySim / AirSim / UE5 | YOLO 数据、相机内参、虚拟平面 | 固定翼弱、单实例 |

**收尾**：三条线互补，不是三选一；系统闭环优先，气动/视觉单独验证。

**四个不要**：
- Gazebo Classic 已 EOL
- AirSim 固定翼弱
- Aerial Gym 只训旋翼
- 能加载模型 ≠ 气动可信

## P2 · 训练栈：三种运行模式

**一句话开场**：仿真器选完，再决定怎么训、怎么部署；不要一个栈硬扛。

| 模式 | 栈 | 关键 | 验收 |
|---|---|---|---|
| 训练 | Isaac Lab + RSL-RL / MuJoCo + MJX | 19-D 特征 + 噪声、GPU 并行 | env/s、样本效率、命中率 |
| 系统 | Gazebo Sim + PX4 + PPO 推理 | MAVLink、offboard、两机、HITL | offboard 切换、指令延迟、时钟 |
| 视觉 | RflySim / AirSim / UE5 + YOLO | 只做数据与视觉闭环 | mAP、s1/s2 误差、漏检率 |

**连接**：共用一份 19-D 契约（observation.py / action.py / scenario.yaml / metrics.py）。

**路线**：0–4 周基线 → 1–3 月提速 → 2–4 月视觉 → 4–6 月 HITL。

**收尾**：同一份 19-D 契约，三种执行循环；换组件，不重写任务。

## 讲稿长度

- P1：60–90 秒
- P2：90–120 秒
- 总：3 分钟左右
