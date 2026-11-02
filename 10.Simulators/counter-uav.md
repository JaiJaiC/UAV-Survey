# 反无拦截：仿真器与训练栈分开选

> 任务：固定翼 defender（单目 + YOLO v11 + 虚拟平面 + 19-D PPO + PX4）拦截旋翼 intruder。
> 资料核对：2026-10-28

## 两条线，不要混在一起

| 线 | 回答的问题 | 入口 |
|---|---|---|
| **仿真器** | 固定翼气动、PX4 SITL/HITL、相机渲染、多机、吞吐够不够 | [counter-uav-simulators.html](counter-uav-simulators.html) |
| **训练栈** | 环境接口、并行吞吐、感知接入、PX4 部署、固定翼训练路径 | [counter-uav-stacks.html](counter-uav-stacks.html) |

仿真器是「物理/相机/PX4」；训练栈是「环境 + 仿真后端 + 学习器 + 部署 + 评估」。
同一个仿真器可以被不同训练栈使用；同一个训练栈也可以换仿真后端。先分别选，再用同一份 19-D 契约拼起来。

## 仿真器这条线

- **系统闭环/多机/HITL**：Gazebo Sim + PX4（`advanced_plane` + AVL；`rc_cessna` 起步）。
- **工程化固定翼 + 视觉**：RflySim（PX4 + UE + 固定翼配置）。
- **气动基准**：JSBSim / FlightGear / X-Plane。
- **视觉数据**：RflySim / AirSim / UE5 / FlightGoggles。
- **GPU 仿真**：Isaac Lab（固定翼气动需自定义）/ MuJoCo+MJX。
- **Intruder 旋翼**：Aerial Gym / Flightmare / PyBullet。
- **不推荐**：Gazebo Classic（EOL）、AirSim 做固定翼主栈、Aerial Gym 训 defender。

详见 [仿真器 vs 仿真器（19 个）](counter-uav-simulators.html)。

## 训练栈这条线

- **主训练**：Isaac Lab + RSL-RL + 自定义固定翼气动；或 MuJoCo/MJX + Brax/RSL-RL。目标是 GPU 并行 + 19-D 特征 + 噪声。
- **系统闭环**：Gazebo Sim + PX4 + PPO 推理节点；保留 MAVLink/offboard/HITL。
- **工程化**：RflySim + PX4 + Simulink/Python RL。
- **气动可信**：JSBSim + Gym + PPO。
- **视觉验证**：AirSim/RflySim + SB3/RLlib，只做 YOLO 数据与视觉闭环。
- **Intruder**：Aerial Gym / Flightmare，四旋翼专用，不能训练 defender。

详见 [训练栈 vs 训练栈（9 套）](counter-uav-stacks.html)。

## 为什么分开

- **对象不同**：仿真器是物理/渲染/传感器；训练栈是环境接口 + 后端 + 学习器 + 部署 + 评估。
- **指标不同**：仿真器看气动保真、PX4 闭环、相机真实感；训练栈看 env/s、样本效率、特征噪声、部署链路。
- **替换方式不同**：换仿真器只换后端；换训练栈要动环境接口、并行、日志。混在一起会分不清是物理不准还是训练组织不对。

但它们是拼在一起的：一套栈，可替换组件。气动返工换 FDM，视觉返工换渲染，PPO 返工换训练环境，PX4 返工换仿真平台。
怎么拼见 [训练栈是怎么「统一」的](stack-anatomy.html)。

## 一句话

**仿真器回答「够不够真」，训练栈回答「怎么训、怎么部署」。两件事分开选，最后用 19-D 契约拼起来。**
