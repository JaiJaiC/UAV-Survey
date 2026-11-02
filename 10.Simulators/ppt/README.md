# 反无拦截 · PPT 汇报版

> 16:9 / 两套：**2 页浓缩版**（推荐汇报）+ **14 页详细版**（备用）  
> 源页面：[反无选型导航](../counter-uav.html) · [只看仿真器](../counter-uav-simulators.html) · [只看训练栈](../counter-uav-stacks.html)

## 文件

| 文件 | 说明 |
|---|---|
| `counter-uav-2p-deck.pptx` | **2 页浓缩版**：P1 仿真器三条线，P2 训练栈三种模式 |
| `counter-uav-simulator-stack-deck.pptx` | 14 页详细版，含完整 narrative 与备注 |
| `build_2p.py` | 生成 2 页版 |
| `build_deck.py` | 生成 14 页版 |
| `ppt-outline-2p.md` | 2 页版讲稿提纲 |
| `ppt-outline.md` | 14 页版逐页提纲 |

## 两页版结构

### P1 · 仿真器：三条互补线
- 系统闭环：Gazebo Sim + PX4 / RflySim
- 气动复核：JSBSim + FlightGear / X-Plane
- 视觉验证：RflySim / AirSim / UE5
- 底部：四个“不要”

### P2 · 训练栈：三种运行模式
- 训练模式：Isaac Lab + RSL-RL / MuJoCo + MJX
- 系统模式：Gazebo Sim + PX4 + PPO 推理
- 视觉模式：RflySim / AirSim / UE5 + YOLO
- 底部：19-D 契约 + 四阶段路线

## 生成

```bash
python build_2p.py     # 2 页版
python build_deck.py   # 14 页版
```

字体：Microsoft YaHei。两套都带演讲者备注。

## 使用建议

- **3 分钟汇报**：直接用 2 页版，P1 讲“三条线”，P2 讲“三种模式”。
- **10–12 分钟**：用 14 页版，2 页版作为开场/收尾。
- 2 页版适合放在答辩 PPT 的“前期调研”或“技术路线”一页；14 页版适合组会/技术评审。
