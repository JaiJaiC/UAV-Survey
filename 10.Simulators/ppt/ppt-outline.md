# 反无拦截：仿真器与训练栈调研 · PPT 提纲

> 14 页 / 16:9 / 约 10–12 分钟  
> 主线：**先分开（仿真器 / 训练栈）→ 各自 shortlist → 各自结论 → 用 19-D 契约拼起来 → 落地路线**

## 叙事逻辑

1. **先给判断**：不选全能冠军，选可替换组件。
2. **再给约束**：固定翼气动、旋翼目标、单目视觉、PX4 闭环。
3. **仿真器只比仿真器**：按角色分四类，再收敛到七个候选。
4. **训练栈只比训练栈**：五个部件，六个候选，三种模式。
5. **最后拼接**：一个命令、五个进程、一套契约。
6. **落地与风险**：四个阶段、六个不要。

## 逐页

### 1. 封面
- 标题：反无拦截：仿真器与训练栈调研
- 副标题：固定翼 defender × 旋翼 intruder × 单目视觉 × PX4
- 一句话：两条线分开选，一套 19-D 契约拼起来。
- 讲稿：今天不选“全能冠军”，而是把两条线拆开，最后用契约拼接。

### 2. 一页结论
- 01 仿真器：回答“够不够真”。
- 02 训练栈：回答“训得快不快、部署通不通”。
- 03 连接：一套 19-D 契约。
- 底部：不选全能冠军，选可替换组件。
- 讲稿：如果只记一页，就记这一页。

### 3. 任务约束
- 四条链路：固定翼气动 / 旋翼 intruder / 单目视觉 / PX4 闭环。
- 流程：世界+PX4 → 单目 → YOLO+虚拟平面 → 19-D PPO → PX4 offboard。
- 19-D = 7 视觉 + 4 运动学 + 4 姿态 + 3 历史动作 + 1 高度。
- 关键：PPO 输入是特征，不是像素。
- 讲稿：这决定了训练不必每一步照片级渲染。

### 4. 为什么分开
- 仿真器：世界/物理/相机/PX4，回答“够不够真”。
- 训练栈：环境/并行/学习器/部署，回答“快不快、通不通”。
- 一个命令 ≠ 一个进程：launcher → Gazebo / PX4×2 / YOLO / PPO / MCAP。
- 金句：统一在契约，不在二进制。
- 讲稿：消除“为什么不塞进一个软件”的误解。

### 5. 仿真器全景
- 系统闭环：Gazebo Sim、RflySim、XTDrone、Gazebo Classic（EOL）。
- 气动基准：JSBSim、FlightGear、X-Plane。
- 视觉渲染：AirSim、FlightGoggles、Flightmare、UE5。
- GPU/物理：Isaac Lab、MuJoCo/MJX、Genesis、Aerial Gym（仅旋翼）。
- 每类给一个“首选”。
- 讲稿：先建地图，不急着排名。

### 6. 仿真器 shortlist
- 七个候选：Gazebo Sim、RflySim、JSBSim+FlightGear、AirSim/UE5、Isaac Lab、MuJoCo/MJX、Aerial Gym/Flightmare。
- 每个只讲：强在哪、代价是什么、用在哪。
- 讲稿：Aerial Gym/Flightmare 只适合 intruder，不能训 defender。

### 7. 仿真器结论
- 系统闭环：Gazebo Sim + PX4（advanced_plane + AVL）。
- 气动复核：JSBSim + FlightGear（X-Plane 可选）。
- 视觉验证：RflySim / AirSim / UE5。
- 四条“不要”：Gazebo Classic EOL、AirSim 固定翼弱、Aerial Gym 只训旋翼、能加载 ≠ 气动可信。
- 讲稿：三条互补线，不是三选一。

### 8. 训练栈是什么
- 五个部件：环境接口 → 仿真后端 → 学习器 → 感知桥 → 部署评估。
- RSL-RL 是学习器，不是仿真器/飞控。
- 三条判断：接口稳定→任务可迁移；后端可换→不锁定；学习器独立→算法可对照。
- 讲稿：训练栈比的是组织方式。

### 9. 训练栈 shortlist
- 六个候选：当前 Gazebo+PX4+PPO、RflySim+Simulink、Isaac Lab+RSL-RL、MuJoCo+MJX、JSBSim+Gym、Aerial Gym/Flightmare。
- 维度：吞吐、视觉、PX4、固定翼、适合阶段。
- 讲稿：当前栈不是不能用，是吞吐低；Isaac Lab 吞吐高但没 PX4。

### 10. 训练栈结论
- 训练模式：Isaac Lab+RSL-RL / MuJoCo+MJX；19-D 特征 + 噪声。
- 系统模式：Gazebo Sim+PX4+PPO 推理；MAVLink/HITL。
- 视觉模式：RflySim/AirSim/UE5+YOLO；不进 PPO 训练循环。
- 金句：同一份 19-D 契约，三种执行循环。
- 讲稿：不要一个栈硬扛三种模式。

### 11. 两条线怎么拼
- scenario.yaml → launcher → 三种模式。
- 共用契约：observation.py / action.py / scenario.yaml / metrics.py / MCAP。
- 金句：换仿真器只换“执行器”，不重写任务。
- 讲稿：气动返工换 FDM，视觉返工换渲染，PPO 返工换训练环境，PX4 返工换平台。

### 12. 落地路线
- 0–4 周：基线，Gazebo Sim + PX4 advanced_plane；两机；19-D logger。
- 1–3 月：提速，Isaac Lab/MuJoCo 特征级 PPO。
- 2–4 月：视觉，RflySim/AirSim 生成 YOLO 数据。
- 4–6 月：闭环，HITL + 真机 + JSBSim 复核。
- 讲稿：每个阶段只换一层。

### 13. 六个不要
- 不要一个栈硬扛训练/系统/视觉。
- 不要用 Gazebo Classic 开新项目。
- 不要指望 AirSim 固定翼。
- 不要用 Aerial Gym 训 defender。
- 不要只看 FPS / 厂商数字。
- 不要把 PPO 训练绑在照片级渲染上。
- 讲稿：这些比“选错仿真器”更常见。

### 14. 总结
- 2 条线、3 种模式、1 套契约。
- 仿真器回答“够不够真”，训练栈回答“怎么训、怎么部署”。
- 谢谢 / Q&A。

## 时间控制

- **8 分钟版**：1、2、3、4、6、7、9、10、11、14。
- **12 分钟版**：全讲，5/8/12 各 40 秒。
- **15 分钟版**：全讲，加 6/9 的边界讨论。

## 关键句（可背）

- 不选全能冠军，选可替换组件。
- 仿真器看“真不真”，训练栈看“快不快、通不通”。
- 一个命令，五个进程；五个进程，一套契约。
- 同一份 19-D 契约，三种执行循环。
- 先跑通，再提速；先拆链路，再选组件。
