"""
仿射变换 + 多UAV编队控制 交互式演示
====================================================
演示内容:
  1. 标称编队(预设形状)的六种基本仿射变换
  2. 论文两层框架中"避障"到底发生在哪一层
  3. Leader驱动 + Follower自动跟随的动画

运行: python affine_demo.py
依赖: pip install numpy matplotlib

操作说明:
  拖拽 Leader (红色大圆) → 编队实时响应
  拖拽障碍物 → 观察编队如何"尝试"变形躲避
  键盘: r=旋转 s=缩放 h=剪切 t=平移 空格=暂停
====================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon
from matplotlib.widgets import Button, Slider
import matplotlib.animation as animation

# ============================================================
# 第0部分: 基础工具函数
# ============================================================

def rotation_matrix(theta):
    """旋转矩阵"""
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta),  np.cos(theta)]])

def scaling_matrix(sx, sy):
    """缩放矩阵"""
    return np.array([[sx, 0],
                     [0, sy]])

def shear_matrix(hx, hy):
    """剪切矩阵"""
    return np.array([[1, hx],
                     [hy, 1]])

def affine_transform(points, A, b):
    """
    对一组点施加仿射变换
    points: shape (N, 2) — N个2D点
    A: shape (2, 2) — 线性变换部分
    b: shape (2,)  — 平移部分
    返回: shape (N, 2)
    """
    return points @ A.T + b  # (N,2) @ (2,2)^T + (2,) = (N,2)


def create_formation(shape='diamond', scale=2.0):
    """创建标称编队构型 (预设形状)"""
    if shape == 'diamond':
        # 菱形: 5架UAV
        return scale * np.array([
            [0, 0],     # Leader 1 (中心)
            [1, 0],     # Leader 2 (右侧)
            [-1, 0],    # Follower 1 (左侧)
            [0, 1],     # Follower 2 (上方)
            [0, -1],    # Follower 3 (下方)
        ])

    elif shape == 'arrow':
        # 箭头形: 5架UAV
        return scale * np.array([
            [0, 0],     # Leader 1 (顶点)
            [-1, -1],   # Follower
            [0, -1],    # Leader 2
            [1, -1],    # Follower
            [0, -2],    # Follower (尾部)
        ])

    elif shape == 'v':
        # V字形: 5架UAV
        return scale * np.array([
            [0, 0],     # Leader 1 (顶点)
            [1, -1],    # Follower
            [2, -2],    # Follower
            [-1, -1],   # Follower
            [-2, -2],   # Follower
        ])

    elif shape == 'line':
        # 一字形
        return scale * np.array([
            [0, 0],     # Leader
            [1, 0],     # Follower
            [2, 0],     # Follower
            [-1, 0],    # Follower
            [-2, 0],    # Follower
        ])

    else:  # 'square'
        return scale * np.array([
            [0, 0],     # Leader
            [2, 0],     # Follower
            [2, 2],     # Follower
            [0, 2],     # Follower
            [1, 1],     # Follower (中心)
        ])


def compute_affine_from_leaders(nominal_leaders, current_leaders):
    """
    从两对leader位置反推仿射变换参数 (A, b)
    这就是论文中 A 和 b 的来源

    对于2D, 至少需要3个不共线点确定仿射变换
    这里简化: 用2个leader + 假设无剪切, 计算旋转+缩放+平移
    """
    # 用2个leader估计旋转和缩放
    nominal_vec = nominal_leaders[1] - nominal_leaders[0]
    current_vec = current_leaders[1] - current_leaders[0]

    # 旋转角 = 当前方向角 - 标称方向角
    theta_nom = np.arctan2(nominal_vec[1], nominal_vec[0])
    theta_cur = np.arctan2(current_vec[1], current_vec[0])
    theta = theta_cur - theta_nom

    # 缩放 = 当前长度 / 标称长度
    s = np.linalg.norm(current_vec) / (np.linalg.norm(nominal_vec) + 1e-8)

    R = rotation_matrix(theta)
    S = scaling_matrix(s, s)
    A = R @ S  # 先缩放再旋转

    # 平移 = Leader1当前 - (旋转缩放后的标称Leader1)
    b = current_leaders[0] - A @ nominal_leaders[0]

    return A, b


# ============================================================
# 第1部分: 静态演示 — 六种基本仿射变换
# ============================================================

def demo_static_transforms():
    """演示六种基本仿射变换在一个编队上的效果"""
    nominal = create_formation('diamond', scale=1.5)

    # 六种变换
    transforms = {
        '(a) Nominal (标称)': {
            'A': np.eye(2),
            'b': np.array([0, 0]),
            'color': '#333333'
        },
        '(b) Rotation 旋转 30°': {
            'A': rotation_matrix(np.pi/6),
            'b': np.array([0, 0]),
            'color': '#e74c3c'
        },
        '(c) Scaling 缩放 (0.5x, 0.7y)': {
            'A': scaling_matrix(0.5, 0.7),
            'b': np.array([0, 0]),
            'color': '#2ecc71'
        },
        '(d) Shear X 剪切 (hx=0.6)': {
            'A': shear_matrix(0.6, 0),
            'b': np.array([0, 0]),
            'color': '#3498db'
        },
        '(e) Shear Y 剪切 (hy=0.5)': {
            'A': shear_matrix(0, 0.5),
            'b': np.array([0, 0]),
            'color': '#9b59b6'
        },
        '(f) Full Affine 综合变换': {
            'A': rotation_matrix(np.pi/6) @ scaling_matrix(0.6, 0.8) @ shear_matrix(0.3, 0),
            'b': np.array([3, 2]),
            'color': '#e67e22'
        },
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for ax, (title, params) in zip(axes, transforms.items()):
        A, b = params['A'], params['b']
        color = params['color']

        transformed = affine_transform(nominal, A, b)

        # 绘制标称编队 (虚线)
        ax.plot(nominal[:, 0], nominal[:, 1], 'o--', color='gray',
                markersize=8, alpha=0.4, label='Nominal')
        # 标称编队连线
        for i in range(len(nominal)):
            for j in range(i+1, len(nominal)):
                ax.plot([nominal[i, 0], nominal[j, 0]],
                        [nominal[i, 1], nominal[j, 1]],
                        '--', color='gray', alpha=0.2, linewidth=0.8)

        # 绘制变换后编队
        ax.plot(transformed[:, 0], transformed[:, 1], 's-', color=color,
                markersize=10, linewidth=2, label='Transformed')
        # 变换后编队连线
        for i in range(len(transformed)):
            for j in range(i+1, len(transformed)):
                ax.plot([transformed[i, 0], transformed[j, 0]],
                        [transformed[i, 1], transformed[j, 1]],
                        '-', color=color, alpha=0.4, linewidth=1.2)

        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5)

        # 设置一致的显示范围
        ax.set_xlim(-4, 6)
        ax.set_ylim(-4, 6)

    fig.suptitle('Affine Transformations on a 5-UAV Formation\n'
                 '灰色虚线=标称编队  彩色实线=变换后编队  连线=结构关系',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ============================================================
# 第2部分: 交互式演示 — Leader驱动编队 + 避障原理
# ============================================================

class FormationSimulator:
    """
    交互式仿真: 拖拽Leader, 观察编队如何实时响应
    同时展示"避障到底发生在哪"
    """

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.fig.canvas.manager.set_window_title(
            'Multi-UAV Affine Formation — Drag Leaders to See Response')

        # 标称编队
        self.nominal = create_formation('diamond', scale=2.0)

        # Leader索引 (前2个是leader, 其余是follower)
        self.leader_indices = [0, 1]
        self.follower_indices = [2, 3, 4]

        # 当前leader位置 (初始等于标称位置)
        self.current_leaders = self.nominal[self.leader_indices].copy()

        # 当前A, b
        self.A = np.eye(2)
        self.b = np.array([0.0, 0.0])

        # 障碍物
        self.obstacles = [
            {'pos': np.array([3.0, 2.5]), 'r': 0.8},
            {'pos': np.array([-2.0, 4.0]), 'r': 0.6},
        ]

        # 动画状态
        self.paused = False
        self.dragging_leader = None
        self.dragging_obstacle = None
        self.time = 0

        # 记录轨迹
        self.trail_length = 80
        self.trails = {i: [] for i in range(len(self.nominal))}

        # 预定义路径: leaders绕圈 + 通过狭窄通道
        self.auto_mode = True
        self.auto_phase = 0
        self.auto_time = 0

        self._setup_plot()
        self._connect_events()

    def _setup_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-6, 8)
        self.ax.set_ylim(-6, 8)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_xlabel('X (m)', fontsize=11)
        self.ax.set_ylabel('Y (m)', fontsize=11)

        # 标题区 — 解释信息
        self.title_text = self.ax.set_title(
            '', fontsize=13, fontweight='bold', pad=20)

        # 信息文本框
        self.info_text = self.ax.text(
            0.02, 0.98, '', transform=self.ax.transAxes,
            fontsize=10, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

        # ===== 绘制元素 =====

        # 标称编队 (灰色虚线)
        self.nominal_scatter = self.ax.scatter(
            [], [], c='gray', marker='o', s=60, alpha=0.3, zorder=1,
            label='Nominal Formation')
        self.nominal_lines = []

        # 变换后编队
        self.formation_scatter = self.ax.scatter(
            [], [], c=[], marker='o', s=100, zorder=5,
            edgecolors='black', linewidth=1.5,
            label='Current Position')
        self.formation_lines = []

        # 目标位置 (决策层输出 p_i*)
        self.target_scatter = self.ax.scatter(
            [], [], c='gold', marker='x', s=80, zorder=4,
            linewidth=2, label='Target p_i*(t) [Decision Layer]')

        # Leader特殊标记
        self.leader_highlight = self.ax.scatter(
            [], [], c='none', marker='o', s=300, zorder=3,
            edgecolors='red', linewidth=3, alpha=0.8,
            label='Leaders')

        # Follower到目标的连线 (表示DRL需要追踪的方向)
        self.tracking_arrows = []

        # 障碍物
        self.obstacle_patches = []
        for obs in self.obstacles:
            circle = Circle(obs['pos'], obs['r'],
                          fill=True, color='#555555', alpha=0.6,
                          zorder=2, label='' if self.obstacle_patches else 'Obstacle')
            self.ax.add_patch(circle)
            self.obstacle_patches.append(circle)

        # 轨迹
        self.trail_lines = {}
        colors_trail = ['#ff6b6b', '#ff6b6b', '#4ecdc4', '#4ecdc4', '#4ecdc4']
        for i in range(len(self.nominal)):
            line, = self.ax.plot([], [], '-', color=colors_trail[i],
                                alpha=0.3, linewidth=1, zorder=1)
            self.trail_lines[i] = line

        # 安全距离圈 (每架UAV周围)
        self.safety_circles = []

        self.ax.legend(loc='upper right', fontsize=8, ncol=2)

    def _connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)

    def _find_nearby(self, x, y):
        """查找鼠标附近的拖拽对象"""
        pt = np.array([x, y])
        # 检查leader
        for idx in self.leader_indices:
            if np.linalg.norm(self.current_leaders[
                self.leader_indices.index(idx)] - pt) < 0.5:
                return ('leader', self.leader_indices.index(idx))
        # 检查障碍物
        for i, obs in enumerate(self.obstacles):
            if np.linalg.norm(obs['pos'] - pt) < obs['r'] + 0.3:
                return ('obstacle', i)
        return (None, None)

    def _on_press(self, event):
        if event.inaxes != self.ax:
            return
        obj_type, idx = self._find_nearby(event.xdata, event.ydata)
        if obj_type == 'leader':
            self.dragging_leader = idx
            self.auto_mode = False  # 手动了就退出自动模式
        elif obj_type == 'obstacle':
            self.dragging_obstacle = idx

    def _on_release(self, event):
        self.dragging_leader = None
        self.dragging_obstacle = None

    def _on_motion(self, event):
        if event.inaxes != self.ax:
            return
        if self.dragging_leader is not None:
            self.current_leaders[self.dragging_leader] = [
                event.xdata, event.ydata]
        elif self.dragging_obstacle is not None:
            self.obstacles[self.dragging_obstacle]['pos'] = np.array(
                [event.xdata, event.ydata])

    def _on_key(self, event):
        if event.key == ' ':
            self.paused = not self.paused
            print(f"{'⏸ Paused' if self.paused else '▶ Running'}")
        elif event.key == 'r':
            self.auto_mode = not self.auto_mode
            if self.auto_mode:
                self.auto_time = 0
                self.auto_phase = 0
            print(f"Auto mode: {'ON' if self.auto_mode else 'OFF (drag leaders manually)'}")
        elif event.key == 'c':
            # 清空轨迹
            for i in self.trails:
                self.trails[i].clear()
            print("Trails cleared")
        elif event.key == '1':
            self.nominal = create_formation('diamond', scale=2.0)
            self._reset_formation()
        elif event.key == '2':
            self.nominal = create_formation('arrow', scale=2.0)
            self._reset_formation()
        elif event.key == '3':
            self.nominal = create_formation('v', scale=2.0)
            self._reset_formation()
        elif event.key == '4':
            self.nominal = create_formation('line', scale=2.0)
            self._reset_formation()
        elif event.key == '5':
            self.nominal = create_formation('square', scale=1.5)
            self._reset_formation()

    def _reset_formation(self):
        self.current_leaders = self.nominal[self.leader_indices].copy()
        self.A = np.eye(2)
        self.b = np.array([0.0, 0.0])
        for i in self.trails:
            self.trails[i].clear()
        print(f"Shape changed. Leaders reset.")

    def _auto_leader_trajectory(self):
        """
        自动生成一条"通过狭窄通道"的leader轨迹
        演示编队如何旋转+缩放来适应环境

        路径设计:
          阶段0 (0-3s):   编队向通道入口飞行, 保持大编队
          阶段1 (3-7s):   接近通道 → 编队旋转对准通道方向 + 缩放变窄
          阶段2 (7-10s):  通过通道 → 编队保持窄长
          阶段3 (10-14s): 通过后 → 编队恢复大小 + 平移绕过前方障碍
          阶段4 (14-18s): 到达目标区域
        """
        self.auto_time += 0.04  # 25fps
        t = self.auto_time

        # 通道入口位置和方向
        channel_center = np.array([1.5, 3.0])
        channel_angle = np.pi / 4  # 45度通道
        channel_width = 1.5

        # --- 阶段判定 ---
        if t < 3:
            phase = 0
        elif t < 7:
            phase = 1
        elif t < 10:
            phase = 2
        elif t < 14:
            phase = 3
        else:
            phase = 4

        self.auto_phase = phase

        if phase == 0:
            # 从起点出发, 保持原有队形向通道入口前进
            progress = t / 3
            start = np.array([-3.0, -2.0])
            end = channel_center - np.array([3.0, 1.0])
            center = start + progress * (end - start)
            # Leader1在编队中心, Leader2在右侧
            self.current_leaders[0] = center
            self.current_leaders[1] = center + np.array([2.0, 0.0])

        elif phase == 1:
            # 接近通道 → 旋转 + 缩放
            progress = (t - 3) / 4
            center = channel_center - np.array([1.0, 0.5]) + progress * np.array([2.5, 1.5])

            # 旋转: 从0度逐渐转到通道方向45度
            angle = progress * channel_angle
            # 缩放: 从1.0逐渐缩到0.4 (变窄通过通道)
            scale = 1.0 - progress * 0.6

            R = rotation_matrix(angle)
            # Leader2方向: 相对于Leader1, 旋转+缩放
            dir_vec = R @ np.array([2.0 * scale, 0.0])
            self.current_leaders[0] = center
            self.current_leaders[1] = center + dir_vec

        elif phase == 2:
            # 通过通道 → 保持窄长, 沿通道方向移动
            progress = (t - 7) / 3
            start_pos = channel_center + np.array([1.5, 1.0])
            end_pos = channel_center + np.array([4.0, 3.5])
            center = start_pos + progress * (end_pos - start_pos)

            R = rotation_matrix(channel_angle)
            dir_vec = R @ np.array([2.0 * 0.4, 0.0])  # 保持scale=0.4
            self.current_leaders[0] = center
            self.current_leaders[1] = center + dir_vec

        elif phase == 3:
            # 通过通道后 → 恢复大小, 绕过障碍
            progress = (t - 10) / 4
            center = np.array([5.5, 4.5]) + progress * np.array([1.5, -1.0])

            # 恢复缩放
            scale = 0.4 + progress * 0.6
            angle = channel_angle * (1 - progress * 0.5)  # 慢慢回正

            R = rotation_matrix(angle)
            dir_vec = R @ np.array([2.0 * scale, 0.0])
            self.current_leaders[0] = center
            self.current_leaders[1] = center + dir_vec

        else:  # phase == 4
            # 到达目标区域, 恢复标称编队
            progress = min((t - 14) / 4, 0.99)
            center = np.array([7.0, 3.5])
            self.current_leaders[0] = center + np.array([-0.5, 0])
            self.current_leaders[1] = center + np.array([1.5, 0])

        # 循环
        if t > 18:
            self.auto_time = 0
            for i in self.trails:
                self.trails[i].clear()

    def update(self, frame):
        if self.paused:
            return

        # 自动模式: 更新leader位置
        if self.auto_mode:
            self._auto_leader_trajectory()

        # ===== 核心计算: 从Leader位置反推仿射变换 =====
        nominal_leaders = self.nominal[self.leader_indices]
        self.A, self.b = compute_affine_from_leaders(
            nominal_leaders, self.current_leaders)

        # 计算所有UAV的目标位置 (仿射变换后)
        target_positions = affine_transform(self.nominal, self.A, self.b)

        # ===== 模拟DRL执行层: "追踪目标 + 避障" =====
        # 实际论文中这是PPO策略网络, 这里简化为:
        #   actual_pos = target_pos + 避障偏移
        actual_positions = target_positions.copy()

        # 模拟每架UAV的局部避障
        for i in range(len(self.nominal)):
            uav_pos = actual_positions[i]
            total_repulsion = np.zeros(2)

            # 障碍物排斥力 (模拟LiDAR感知)
            for obs in self.obstacles:
                vec = uav_pos - obs['pos']
                dist = np.linalg.norm(vec)
                safe_dist = obs['r'] + 0.8  # r_safe = 0.8m
                if dist < safe_dist * 2 and dist > 1e-6:
                    # 越近斥力越大 (模拟DRL学到的避障行为)
                    repulsion = vec / dist * np.exp(-dist / safe_dist) * 0.3
                    total_repulsion += repulsion

            # UAV间互斥 (邻居=动态障碍物!)
            for j in range(len(self.nominal)):
                if i == j:
                    continue
                vec = uav_pos - actual_positions[j]
                dist = np.linalg.norm(vec)
                safe_dist = 0.8
                if dist < safe_dist * 1.5 and dist > 1e-6:
                    repulsion = vec / dist * np.exp(-dist / safe_dist) * 0.2
                    total_repulsion += repulsion

            actual_positions[i] += total_repulsion

        # 记录轨迹
        for i in range(len(self.nominal)):
            self.trails[i].append(actual_positions[i].copy())
            if len(self.trails[i]) > self.trail_length:
                self.trails[i].pop(0)

        # ===== 更新绘图 =====
        # 轨迹
        for i in range(len(self.nominal)):
            if self.trails[i]:
                trail_arr = np.array(self.trails[i])
                self.trail_lines[i].set_data(trail_arr[:, 0], trail_arr[:, 1])

        # 目标位置 (决策层输出) — 金色X
        self.target_scatter.set_offsets(target_positions)

        # 实际位置
        colors = ['red', 'red'] + ['#2196F3'] * (len(self.nominal) - 2)
        self.formation_scatter.set_offsets(actual_positions)
        self.formation_scatter.set_facecolor(colors)

        # Leader高亮圈
        self.leader_highlight.set_offsets(actual_positions[self.leader_indices])

        # 画Follower到目标的追踪箭头 (DRL需要干的事)
        for arrow in self.tracking_arrows:
            arrow.remove()
        self.tracking_arrows.clear()
        for idx in self.follower_indices:
            arrow = FancyArrowPatch(
                actual_positions[idx], target_positions[idx],
                arrowstyle='->', color='orange', linewidth=1.2,
                alpha=0.6, mutation_scale=12, zorder=3,
                linestyle='dashed')
            self.ax.add_patch(arrow)
            self.tracking_arrows.append(arrow)

        # 画编队内部连线 (结构关系)
        for line in self.formation_lines:
            line.remove()
        self.formation_lines.clear()
        for i in range(len(self.nominal)):
            for j in range(i+1, len(self.nominal)):
                line, = self.ax.plot(
                    [actual_positions[i, 0], actual_positions[j, 0]],
                    [actual_positions[i, 1], actual_positions[j, 1]],
                    '-', color='#90CAF9', alpha=0.4, linewidth=1, zorder=2)
                self.formation_lines.append(line)

        # 更新障碍物位置
        for patch, obs in zip(self.obstacle_patches, self.obstacles):
            patch.center = obs['pos']

        # 清除旧安全圈
        for c in self.safety_circles:
            c.remove()
        self.safety_circles.clear()
        for i in range(len(self.nominal)):
            circle = Circle(actual_positions[i], 0.8,
                          fill=False, color='red', alpha=0.15,
                          linestyle='--', linewidth=0.8)
            self.ax.add_patch(circle)
            self.safety_circles.append(circle)

        # 更新信息
        self._update_info(actual_positions, target_positions)

        return []

    def _update_info(self, actual, target):
        """更新屏幕上的文字信息"""

        # 检查碰撞
        collision = False
        for i in range(len(actual)):
            for j in range(i+1, len(actual)):
                if np.linalg.norm(actual[i] - actual[j]) < 0.3:
                    collision = True

        for obs in self.obstacles:
            for i in range(len(actual)):
                if np.linalg.norm(actual[i] - obs['pos']) < obs['r'] + 0.2:
                    collision = True

        # 位置误差
        errors = np.linalg.norm(actual - target, axis=1)
        mean_error = np.mean(errors)

        # Leader间距 (反映缩放)
        leader_dist = np.linalg.norm(
            self.current_leaders[1] - self.current_leaders[0])

        info_lines = [
            f"Phase: {['出发','旋转缩放','通过通道','恢复','到达'][self.auto_phase]}",
            f"Leader间距: {leader_dist:.2f}m (标称=2.0m)",
            f"平均位置误差: {mean_error:.3f}m",
            f"碰撞: {'⚠ YES!' if collision else '✅ Safe'}",
            f"",
            f"=== 键盘控制 ===",
            f"  Space: 暂停",
            f"  R: 自动/手动切换",
            f"  1-5: 切换编队形状",
            f"  C: 清除轨迹",
            f"",
            f"=== 鼠标操作 ===",
            f"  拖拽红色Leader → 编队跟随",
            f"  拖拽灰色障碍物 → 改变环境",
            f"",
            f"金色✚ = 决策层目标",
            f"虚线箭头 = DRL需追踪的方向",
            f"红色圈 = 安全距离(0.8m)",
        ]

        self.info_text.set_text('\n'.join(info_lines))

        # 标题根据phase变化
        phase_titles = [
            'Phase 0: Formation Approaches Channel (Normal Size)',
            'Phase 1: Rotating + Scaling to Fit Narrow Passage!',
            'Phase 2: Passing Through Channel (Scaled 40%)',
            'Phase 3: Recovering Size + Avoiding Obstacle',
            'Phase 4: Reaching Target Area (Normal Formation)',
        ]
        self.title_text.set_text(phase_titles[self.auto_phase])

    def run(self):
        """启动交互动画"""
        ani = animation.FuncAnimation(
            self.fig, self.update, frames=None,
            interval=40, blit=False, cache_frame_data=False)
        plt.tight_layout()
        plt.show()


# ============================================================
# 第3部分: 避障机制详解 (单独一图)
# ============================================================

def demo_avoidance_principle():
    """
    画一张图解释"仿射变换写死了, 那怎么避障?"
    回答核心疑感
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # ----- 子图1: 没有避障的情况 (纯仿射变换 = A-F方法) -----
    ax = axes[0]
    nominal = create_formation('diamond', scale=1.5)

    # Leader穿过障碍物中间
    leader_positions = np.array([[0, -1], [1.5, -1]])
    A, b = compute_affine_from_leaders(nominal[:2], leader_positions)
    targets = affine_transform(nominal, A, b)

    # 假定UAV完美追踪目标 → 全部撞上障碍物
    ax.plot([-2, 4], [0.5, 0.5], 'k-', linewidth=3, label='Obstacle Wall')
    ax.fill_between([-2, 4], [0.3, 0.3], [0.7, 0.7], color='gray', alpha=0.5)
    ax.scatter(targets[:, 0], targets[:, 1], c='red', s=120, zorder=5,
               marker='X', edgecolors='darkred', linewidth=2)
    for i in range(len(targets)):
        for j in range(i+1, len(targets)):
            ax.plot([targets[i, 0], targets[j, 0]],
                    [targets[i, 1], targets[j, 1]],
                    'r-', alpha=0.3)

    ax.text(0.75, 1.5, 'ALL CRASH!\nA-F method: 50/50 collisions',
            fontsize=13, color='red', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.9))

    ax.set_xlim(-2.5, 4)
    ax.set_ylim(-2.5, 3)
    ax.set_aspect('equal')
    ax.set_title('(a) Pure Affine Formation (A-F method)\n'
                 'Targets on obstacle → NO avoidance mechanism',
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # ----- 子图2: 论文方案 —— 两层分工 -----
    ax = axes[1]

    # 决策层: 仿射变换计算目标位置 (金色X)
    targets_shifted = affine_transform(nominal, A, b + np.array([0, 1.5]))

    # 执行层DRL: 实际轨迹绕开障碍物
    actual_positions = targets_shifted.copy()
    for i in range(len(actual_positions)):
        if actual_positions[i, 1] > 0 and actual_positions[i, 1] < 1.2:
            actual_positions[i, 1] += 0.6  # DRL绕开
        if i > 1:  # follower多加一些偏移
            actual_positions[i, 0] += 0.3

    ax.plot([-2, 4], [0.5, 0.5], 'k-', linewidth=3, label='Obstacle Wall')
    ax.fill_between([-2, 4], [0.3, 0.3], [0.7, 0.7], color='gray', alpha=0.5)

    # 目标位置
    ax.scatter(targets_shifted[:, 0], targets_shifted[:, 1],
               c='gold', s=100, marker='X', zorder=4,
               edgecolors='orange', linewidth=1.5, label='Target (Decision Layer)')
    # 实际位置
    colors = ['red', 'red', '#2196F3', '#2196F3', '#2196F3']
    ax.scatter(actual_positions[:, 0], actual_positions[:, 1],
               c=colors, s=120, zorder=5, edgecolors='black', linewidth=1.5,
               label='Actual (Execution Layer)')

    # 连线: 目标→实际 (DRL的追踪偏差)
    for i in range(len(actual_positions)):
        ax.annotate('', xy=actual_positions[i], xytext=targets_shifted[i],
                    arrowprops=dict(arrowstyle='->', color='orange',
                                   lw=1.5, alpha=0.6, linestyle='dashed'))

    # 画编队连线 (实际)
    for i in range(len(actual_positions)):
        for j in range(i+1, len(actual_positions)):
            ax.plot([actual_positions[i, 0], actual_positions[j, 0]],
                    [actual_positions[i, 1], actual_positions[j, 1]],
                    '-', color='#90CAF9', alpha=0.4, linewidth=1.2)

    ax.text(0.75, 2.8, 'SAFE!\nDRL deviates from target\nbut structure mostly kept',
            fontsize=13, color='green', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='#ccffcc', alpha=0.9))
    ax.set_xlim(-2.5, 4)
    ax.set_ylim(-2.5, 3.5)
    ax.set_aspect('equal')
    ax.set_title('(b) This Paper: Two-Layer Hybrid\n'
                 'Decision → targets, Execution → avoid obstacles + track',
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc='lower right')

    # ----- 子图3: 关键图解 —— 避障的自由度从哪来 -----
    ax = axes[2]

    # 画图说明自由度
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.axis('off')

    y = 9
    ax.text(5, y, 'WHERE DOES AVOIDANCE COME FROM?', fontsize=14,
            fontweight='bold', ha='center', color='#333')
    y -= 1.2

    # 自由度1: Leaders
    ax.text(0.5, y, '1. LEADERS STEER THE FORMATION', fontsize=12,
            fontweight='bold', color='#c0392b')
    y -= 0.4
    ax.text(1, y, 'Leaders can choose ANY trajectory.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → If path is blocked, leaders go around.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Followers targets auto-update via Eq.(8).', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → The whole formation "flows" around the obstacle.', fontsize=11,
            color='#555')
    y -= 0.8

    # 自由度2: Leaders改变间距
    ax.text(0.5, y, '2. LEADERS CHANGE SPACING → SCALING', fontsize=12,
            fontweight='bold', color='#c0392b')
    y -= 0.4
    ax.text(1, y, 'Leaders move closer = narrower formation.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Formation squeezes through narrow passages.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Eq.(8) automatically scales ALL followers.', fontsize=11,
            color='#555')
    y -= 0.8

    # 自由度3: 执行层DRL微调
    ax.text(0.5, y, '3. DRL EXECUTION LAYER FINE-TUNES', fontsize=12,
            fontweight='bold', color='#2196F3')
    y -= 0.4
    ax.text(1, y, 'Each UAV has its OWN PPO policy.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → If LiDAR sees nearby obstacle, deviate from target.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Reward: reach target (+15) vs collision (-15).', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Automatic trade-off learned via training!', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → Once obstacle cleared, return to target.', fontsize=11,
            color='#555')
    y -= 0.8

    # 自由度4: 邻居=动态障碍物
    ax.text(0.5, y, '4. INTER-UAV COLLISION AVOIDANCE', fontsize=12,
            fontweight='bold', color='#2196F3')
    y -= 0.4
    ax.text(1, y, 'Other UAVs appear in LiDAR → treated as dynamic obstacles.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → No need to generate extra dynamic obstacles in training.', fontsize=11)
    y -= 0.3
    ax.text(1, y, '  → UAVs learn to avoid each other naturally.', fontsize=11,
            color='#555')
    y -= 1.0

    # 总结
    ax.text(5, y, 'KEY INSIGHT:', fontsize=13, fontweight='bold',
            ha='center', color='#8e44ad')
    y -= 0.5
    ax.text(5, y,
            'Affine transformation defines WHERE UAVs SHOULD BE.\n'
            'DRL execution layer decides HOW to GET THERE safely.\n'
            'The "rigidity" of affine transform is the GOAL, not the PATH.',
            fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='#f3e5f5', alpha=0.9))

    fig.suptitle('How Obstacle Avoidance Works in the Hybrid Framework\n'
                 '(Affine transformation is the TARGET, not the CONSTRAINT)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


# ============================================================
# 第4部分: 缩放编队通过狭窄通道 — 最直观的演示
# ============================================================

def demo_narrow_passage():
    """
    演示编队如何通过缩放 (Scale) 来通过狭窄通道
    这是仿射变换"灵活性"最经典的场景
    """
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    nominal = create_formation('diamond', scale=2.0)

    # 通道: y方向宽度只有1.5m
    channel_y_min, channel_y_max = 0.8, 2.3
    channel_x_range = [0, 4]

    scenes = [
        {
            'title': '(a) Full Size Formation\nWIDTH = 4.0m > CHANNEL 1.5m',
            'A': np.eye(2),  # 无缩放
            'b': np.array([0, 0]),
            'color': 'red',
            'status': 'BLOCKED!'
        },
        {
            'title': '(b) Scale X to 0.5\nWIDTH = 2.0m > CHANNEL 1.5m',
            'A': scaling_matrix(0.5, 1.0),
            'b': np.array([0, 0]),
            'color': 'orange',
            'status': 'STILL BLOCKED'
        },
        {
            'title': '(c) Scale X to 0.3\nWIDTH = 1.2m < CHANNEL 1.5m',
            'A': scaling_matrix(0.3, 1.0),
            'b': np.array([0, 0]),
            'color': '#2ecc71',
            'status': 'FITS! ✅'
        },
        {
            'title': '(d) Scale X=0.3 + Rotate + Shift\nOptimally aligned!',
            'A': rotation_matrix(np.pi/6) @ scaling_matrix(0.3, 0.8),
            'b': np.array([2.0, 1.55]),
            'color': '#2196F3',
            'status': 'PASSING ✅'
        },
    ]

    for ax, scene in zip(axes, scenes):
        A, b = scene['A'], scene['b']
        transformed = affine_transform(nominal, A, b)

        # 画通道
        ax.fill_between(channel_x_range,
                        [channel_y_min, channel_y_min],
                        [channel_y_max, channel_y_max],
                        color='#E8E8E8', zorder=0)
        ax.plot([channel_x_range[0], channel_x_range[1]],
                [channel_y_min, channel_y_min], 'k-', linewidth=3)
        ax.plot([channel_x_range[0], channel_x_range[1]],
                [channel_y_max, channel_y_max], 'k-', linewidth=3)
        ax.text(2, channel_y_max + 0.3, f'CHANNEL {channel_y_max-channel_y_min:.1f}m',
                ha='center', fontsize=9, fontweight='bold')

        # 画编队
        for i in range(len(transformed)):
            for j in range(i+1, len(transformed)):
                ax.plot([transformed[i, 0], transformed[j, 0]],
                        [transformed[i, 1], transformed[j, 1]],
                        '-', color=scene['color'], alpha=0.4, linewidth=1.2)
        colors_pts = ['red', 'red'] + ['#2196F3'] * (len(transformed) - 2)
        ax.scatter(transformed[:, 0], transformed[:, 1],
                  c=colors_pts, s=80, edgecolors='black',
                  linewidth=1.2, zorder=5)

        # 画编队宽度标注
        xs = transformed[:, 0]
        x_min, x_max = xs.min(), xs.max()
        ax.annotate('', xy=(x_max, transformed[0, 1]),
                   xytext=(x_min, transformed[0, 1]),
                   arrowprops=dict(arrowstyle='<->', color=scene['color'],
                                  lw=2, linestyle='dashed'))
        width = x_max - x_min
        ax.text((x_min + x_max) / 2, transformed[0, 1] - 0.4,
                f'Width={width:.1f}m',
                ha='center', fontsize=9, color=scene['color'], fontweight='bold')

        ax.set_title(scene['title'], fontsize=12, fontweight='bold')
        ax.set_xlim(-3, 6)
        ax.set_ylim(-2, 5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)

        # 状态标记
        if 'FITS' in scene['status'] or 'PASSING' in scene['status']:
            bg_color = '#ccffcc'
        else:
            bg_color = '#ffcccc'
        ax.text(1.5, -1.3, scene['status'], fontsize=13,
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round', facecolor=bg_color, alpha=0.9))

    fig.suptitle('How Affine Scaling Allows Formation to Pass Narrow Passages\n'
                 'Same 5-UAV diamond formation → different scale factors → fit or not fit',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ============================================================
# 运行入口
# ============================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║    Multi-UAV Affine Formation Visual Demo               ║
    ║    仿射变换 + 多UAV编队 交互式演示                      ║
    ╚══════════════════════════════════════════════════════════╝

    请选择演示:
      0 — 全跑一遍 (推荐!)
      1 — 静态变换演示 (6种基本仿射变换)
      2 — 交互式仿真 (拖拽Leader, 编队实时响应+避障)
      3 — 避障机制图解 (仿射变换写死了, 怎么避障?)
      4 — 狭窄通道缩放演示 (编队缩放通过通道)
    """)

    try:
        choice = input("输入数字 (0-4), 直接回车=0: ").strip()
        if choice == '':
            choice = '0'
    except (EOFError, KeyboardInterrupt):
        choice = '0'

    if choice == '0':
        print("\n>>> Running all demos...\n")
        print("=== DEMO 1: Static Affine Transforms ===")
        demo_static_transforms()

        print("\n=== DEMO 2: Avoidance Principle ===")
        demo_avoidance_principle()

        print("\n=== DEMO 3: Narrow Passage Scaling ===")
        demo_narrow_passage()

        print("\n=== DEMO 4: Interactive Simulator ===")
        print("(Close the window to continue)")
        sim = FormationSimulator()
        sim.run()

    elif choice == '1':
        demo_static_transforms()
    elif choice == '2':
        sim = FormationSimulator()
        sim.run()
    elif choice == '3':
        demo_avoidance_principle()
    elif choice == '4':
        demo_narrow_passage()
    else:
        print("Invalid choice, running all...")
        demo_static_transforms()
        demo_avoidance_principle()
        demo_narrow_passage()
