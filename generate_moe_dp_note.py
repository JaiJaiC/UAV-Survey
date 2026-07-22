#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate detailed note.html for MoE-DP paper at 2.Scholar/Huazhe Xu/files/10383/"""

import os

OUTPUT_PATH = r'F:\backup\【NUDT】\【NUDT】program\UAV-Survey\2.Scholar\Huazhe Xu\files\10383\note.html'

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Paper Notes - MoE-DP: An MoE-Enhanced Diffusion Policy for Robust Long-Horizon Manipulation</title>

<script>
MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], tags: 'ams' },
  options: { enableMenu: false }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });</script>
<style>
  :root {
    --bg: #f8f9fb; --surface: #ffffff; --border: #e2e5ea;
    --text: #1a1d23; --text-secondary: #5f6b7a; --text-muted: #94a3b8;
    --blue-fill: #e8f0fe;    --blue-stroke: #3b82f6;   --blue-strong: #1d4ed8;
    --green-fill: #e6f7ee;   --green-stroke: #10b981;  --green-strong: #047857;
    --amber-fill: #fef7ed;   --amber-stroke: #f59e0b;  --amber-strong: #b45309;
    --purple-fill: #f0ebfd;  --purple-stroke: #8b5cf6;  --purple-strong: #6d28d9;
    --rose-fill: #ffeaf0;    --rose-stroke: #f43f5e;   --rose-strong: #be123c;
    --gray-fill: #f3f4f6;    --gray-stroke: #9ca3af;   --gray-strong: #4b5563;
    --cyan-fill: #e6faf8;    --cyan-stroke: #14b8a6;   --cyan-strong: #0f766e;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg); color: var(--text);
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans SC",sans-serif;
    line-height: 1.72;
  }
  nav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(255,255,255,.94); backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border); padding: 10px 24px;
    display: flex; gap: 4px; flex-wrap: wrap; align-items: center;
  }
  nav a {
    text-decoration: none; font-size: 12px; font-weight: 500;
    color: var(--text-secondary); padding: 5px 10px; border-radius: 5px; transition: all .15s;
  }
  nav a:hover { background: var(--blue-fill); color: var(--blue-strong); }
  nav .brand { font-weight: 700; color: var(--text); margin-right: 10px; font-size: 13.5px; }
  .container { max-width: 1100px; margin: 0 auto; padding: 28px 20px 60px; }
  section {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 32px 28px; margin-bottom: 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,.04); scroll-margin-top: 56px;
  }
  h1 { font-size: 24px; font-weight: 700; letter-spacing: -0.4px; margin-bottom: 4px; }
  h2 {
    font-size: 18px; font-weight: 700; letter-spacing: -0.2px;
    margin-bottom: 20px;
  }
  h3 { font-size: 15px; font-weight: 700; margin: 22px 0 8px; color: #1e293b; }
  h4 { font-size: 13.5px; font-weight: 700; margin: 16px 0 6px; }
  p, li { font-size: 14px; color: #334155; }
  p { margin-bottom: 8px; }
  ul, ol { margin: 6px 0 12px 22px; }
  li { margin-bottom: 4px; }
  code {
    background: #f1f5f9; color: #1e293b;
    font-family: "JetBrains Mono","Fira Code","Cascadia Code",Consolas,monospace;
    font-size: 12.5px; padding: 1.5px 6px; border-radius: 4px; border: 1px solid #e2e8f0;
  }
  strong.hl { color: #0f172a; }
  .bold-title { font-weight: 700; font-size: 15px; color: #0f172a; }
  .bold-affil { font-weight: 700; }
  .bold-venue { font-weight: 700; color: #1d4ed8; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0 16px; font-size: 13.5px; }
  th { background: #f1f5f9; font-weight: 700; text-align: left; padding: 9px 12px; border: 1px solid #e2e8f0; }
  td { padding: 8px 12px; border: 1px solid #e2e8f0; color: #334155; }
  tr:nth-child(even) td { background: #fafbfc; }
  tr.highlight td { background: #fef3c7; font-weight: 600; }
  .tag {
    display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 9px;
    border-radius: 4px; margin-right: 5px; margin-bottom: 4px;
  }
  .tag-blue   { background:#dbeafe; color:#1d4ed8; }
  .tag-green  { background:#d1fae5; color:#047857; }
  .tag-amber  { background:#fef3c7; color:#92400e; }
  .tag-purple { background:#ede9fe; color:#6d28d9; }
  .tag-red    { background:#ffe4e6; color:#be123c; }
  .tag-gray   { background:#f3f4f6; color:#4b5563; }
  .tag-cyan   { background:#cffafe; color:#0f766e; }
  .callout {
    border-left: 4px solid; border-radius: 0 8px 8px 0;
    padding: 14px 18px; margin: 12px 0; font-size: 13.5px;
  }
  .callout.info   { background:#e8f0fe; border-color:#3b82f6; color:#1e3a5f; }
  .callout.tip    { background:#e6f7ee; border-color:#10b981; color:#064e3b; }
  .callout.warn   { background:#fef7ed; border-color:#f59e0b; color:#78350f; }
  .callout.danger { background:#ffeaf0; border-color:#f43f5e; color:#7f1d1d; }
  .callout.idea   { background:#f0ebfd; border-color:#8b5cf6; color:#3b1f7e; }
  .callout-title  { font-weight: 700; font-size: 13px; margin-bottom: 3px; }
  .formula-block {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 18px 22px; margin: 12px 0; overflow-x: auto;
  }
  .formula-block .eq-tag {
    display: inline-block; font-size: 11.5px; font-weight: 700; color: var(--blue-strong);
    background: #dbeafe; padding: 2px 8px; border-radius: 4px; margin-bottom: 8px;
  }
  mjx-container[display="true"] { font-size: 115% !important; margin: 10px 0 !important; }
  .formula-block .eq-note {
    margin-top: 10px; padding-top: 10px; border-top: 1px dashed #e2e8f0;
    font-size: 12.5px; color: #64748b; line-height: 1.65;
  }
  .mermaid-box {
    background: #fafbfc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 18px 22px; margin: 12px 0; overflow-x: auto; text-align: center;
  }
  .arch-panel {
    background: #fbfcff; border: 1px solid #dbe3ef; border-radius: 10px;
    padding: 16px; margin: 14px 0 18px; overflow-x: auto;
  }
  .arch-grid {
    min-width: 820px; display: grid; grid-template-columns: 1.05fr 1.25fr 1.2fr .95fr;
    gap: 12px; align-items: stretch;
  }
  .arch-stage {
    border: 1px solid #d8e0ea; border-radius: 8px; background: #fff;
    padding: 12px; display: flex; flex-direction: column; gap: 9px;
  }
  .arch-stage h4 {
    margin: 0; font-size: 12px; color: #0f172a; letter-spacing: 0;
    display: flex; justify-content: space-between; gap: 8px; align-items: center;
  }
  .arch-stage h4 span {
    font-size: 10px; color: #64748b; font-weight: 600; white-space: nowrap;
  }
  .arch-card {
    border-radius: 7px; padding: 9px 10px; border: 1px solid;
    min-height: 58px; display: flex; flex-direction: column; justify-content: center;
  }
  .arch-card strong { font-size: 12.5px; color: #0f172a; line-height: 1.35; }
  .arch-card small { font-size: 11px; color: #475569; line-height: 1.45; margin-top: 3px; }
  .arch-solar { background: #fff7ed; border-color: #fed7aa; }
  .arch-power { background: #eff6ff; border-color: #bfdbfe; }
  .arch-motor { background: #f5f3ff; border-color: #ddd6fe; }
  .arch-thrust { background: #ecfdf5; border-color: #bbf7d0; }
  .arch-arrow {
    min-width: 820px; display: grid; grid-template-columns: repeat(4,1fr);
    color: #64748b; font-size: 11px; font-weight: 700; margin: 8px 0 4px;
  }
  .arch-arrow span { text-align: center; }
  .arch-summary {
    min-width: 820px; margin-top: 10px; display: grid; grid-template-columns: repeat(4,1fr);
    gap: 8px;
  }
  .arch-metric {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 7px;
    padding: 8px 10px;
  }
  .arch-metric strong { display: block; font-size: 12px; color: #0f172a; }
  .arch-metric small { font-size: 11px; color: #64748b; }
  .paper-figure {
    background: #fafbfc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 0; margin: 16px 0; overflow: hidden;
  }
  .paper-figure .fig-header {
    background: #f1f5f9; padding: 10px 16px;
    border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  }
  .paper-figure .fig-header .fig-number {
    font-weight: 700; font-size: 12.5px; color: var(--blue-strong);
    background: #dbeafe; padding: 3px 10px; border-radius: 4px;
  }
  .paper-figure .fig-header .fig-caption { font-size: 13px; font-weight: 600; color: #334155; }
  .paper-figure .fig-header .fig-source { font-size: 11px; color: var(--text-muted); margin-left: auto; }
  .paper-figure .fig-image { text-align: center; padding: 16px; background: #fff; }
  .paper-figure .fig-image img {
    max-width: 100%; height: auto; border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
  }
  .paper-figure .fig-placeholder {
    text-align: center; padding: 40px 20px; color: var(--text-muted);
    font-size: 13px; border: 2px dashed #e2e8f0; margin: 16px; border-radius: 8px;
  }
  .paper-figure .fig-interpretation {
    padding: 14px 18px; border-top: 1px solid #e2e8f0; background: #fefce8;
  }
  .paper-figure .fig-interpretation .fig-label {
    font-weight: 700; font-size: 11px; color: #b45309; margin-bottom: 6px; letter-spacing: 1px;
  }
  .paper-figure .fig-interpretation p,
  .paper-figure .fig-interpretation li { font-size: 13px; color: #475569; }
  .paper-figure .fig-interpretation ul { margin: 4px 0 4px 16px; }
  .novelty-card {
    border: 1px solid var(--border); border-radius: 10px; padding: 18px 20px;
    margin: 12px 0; background: #fafbfc;
  }
  .novelty-card h4 { margin-top: 0; }
  .novelty-card .novelty-step {
    font-size: 13px; margin-bottom: 8px; padding-left: 12px;
    border-left: 3px solid var(--purple-stroke);
  }
  .novelty-step strong { color: var(--purple-strong); }
  .cmp-row  { display: flex; gap: 14px; flex-wrap: wrap; margin: 12px 0; }
  .cmp-col  { flex: 1; min-width: 260px; border: 1px solid var(--border); border-radius: 8px; padding: 16px; background: #fafbfc; }
  .cmp-col h4 { margin-top: 0; }
  footer { text-align: center; padding: 20px; color: var(--text-muted); font-size: 12px; }
</style></head>
<body>
<nav><a class="back" href="../../index.html">&larr; Back to Huazhe Xu</a><a href="#info">Info</a><a href="#insight">Insight</a><a href="#architecture">Architecture</a><a href="#task">Task</a><a href="#challenge">Challenge</a><a href="#method">Method</a><a href="#principles">Principles</a><a href="#figures">Figures</a><a href="#flaw">Flaw</a><a href="#motivation">Motivation</a><a href="#takeaway">Takeaway</a></nav>
<main class="wrap">

<!-- ===== 1. Paper Info ===== -->
<section id="info">
<h2>1. Paper Info</h2>
<h1>MoE-DP: An MoE-Enhanced Diffusion Policy for Robust Long-Horizon Robotic Manipulation with Skill Decomposition and Failure Recovery</h1>
<table>
<tr><td style="width:140px;font-weight:700;">Authors</td><td>Baiye Cheng, Tianhai Liang, Suning Huang, Maanping Shao, Feihong Zhang, Botian Xu, Zhengrong Xue, Huazhe Xu</td></tr>
<tr><td style="font-weight:700;">Affiliations</td><td>Tsinghua University, Stanford University, HUST (Huazhong University of Science and Technology), Shanghai Qi Zhi Institute</td></tr>
<tr><td style="font-weight:700;">Year &amp; Venue</td><td>2025, arXiv:2511.05007</td></tr>
<tr><td style="font-weight:700;">Research Type</td><td>长时序机器人操作 / Mixture of Experts + Diffusion Policy / 技能分解与失败恢复</td></tr>
<tr><td style="font-weight:700;">Local Source</td><td><a href="Cheng et al. - 2025 - MoE-DP An MoE-enhanced diffusion policy for robust long-horizon robotic manipulation with skill dec.pdf">Cheng et al. - 2025 - MoE-DP An MoE-enhanced diffusion policy for robust long-horizon robotic manipulation with skill dec.pdf</a></td></tr>
</table>
<div style="margin-top:10px;">
<span class="tag tag-blue">Diffusion Policy</span>
<span class="tag tag-purple">Mixture of Experts</span>
<span class="tag tag-green">Long-Horizon Manipulation</span>
<span class="tag tag-amber">Failure Recovery</span>
<span class="tag tag-red">Skill Decomposition</span>
<span class="tag tag-cyan">2025</span>
<span class="tag tag-gray">Huazhe Xu</span>
<span class="tag tag-blue">Tsinghua University</span>
</div>
</section>

<!-- ===== 2. Insight & Novelty ===== -->
<section id="insight">
<h2>2. Insight &amp; Novelty</h2>

<h3>2.1 Core Insight</h3>
<div class="callout info">
<span class="callout-title">核心洞见</span>
<p>长时序机器人操作的瓶颈不在于单个策略网络的容量，而在于<strong>隐表示的纠缠程度</strong>。普通 Diffusion Policy 的条件向量将所有任务阶段的信息混入一个扁平的特征空间，导致策略在面临扰动时无法区分"当前应该处于抓取阶段还是放置阶段"。MoE-DP 通过在视觉编码器与去噪网络之间插入稀疏 Mixture of Experts，迫使不同专家<strong>自发地</strong>对应于接近、抓取、运输、放置等任务子阶段。这种阶段化解耦带来了两个关键能力：(1) 受扰后策略能检测当前阶段失败并<strong>重新执行</strong>该阶段，而非盲目前进；(2) 推理时可通过<strong>手动指定专家激活顺序</strong>来重排子任务，完全无需重新训练。</p>
</div>

<h3>2.2 Novelty Breakdown</h3>
<div class="novelty-card">
<h4>创新点 1：将 MoE 首次引入 Diffusion Policy 的条件通道</h4>
<div class="novelty-step"><strong>位置选择：</strong>MoE 层被精确插入到 ResNet-18 视觉编码器的输出之后、diffusion denoiser（基于 CNN-based U-Net 架构）的条件输入之前。这个位置恰好是视觉感知向动作规划的语义转换界面，使得专家可以基于全局视觉上下文进行路由决策，从而将高层任务阶段信息编码进条件向量。</div>
<div class="novelty-step"><strong>设计动机：</strong>传统扩散策略的条件向量是静态的 $c_t = f_{enc}(o_t)$，其中 $o_t$ 为当前观测。MoE-DP 将其升级为 $c'_t = \text{MoE}(f_{enc}(o_t))$，使得条件向量<strong>动态地</strong>反映当前所处的任务阶段。这本质上是将"何时该做什么"的结构化先验注入到原本仅编码"当前看到什么"的条件表示中。</div>
</div>

<div class="novelty-card">
<h4>创新点 2：复合辅助损失函数防止专家坍缩</h4>
<div class="novelty-step"><strong>负载均衡损失 $L_{load}$：</strong>防止所有样本被路由到少数几个专家，确保每个专家都有充分训练机会。$L_{load} = N \cdot \sum_{i=1}^{N} f_i \cdot P_i$，其中 $f_i$ 为分配给专家 $i$ 的 token 比例，$P_i$ 为路由器对专家 $i$ 的平均概率。</div>
<div class="novelty-step"><strong>熵损失 $L_{entropy}$：</strong>鼓励路由器对每个样本做出<strong>尖锐的</strong>专家分配，避免概率分散导致专家专门化不足。$L_{entropy} = -\frac{1}{B}\sum_{t=1}^{B}\sum_{i=1}^{N} p_{t,i} \cdot \log(p_{t,i} + \varepsilon)$。</div>
<div class="novelty-step"><strong>三元联合优化：</strong>$L = L_{diff} + \alpha L_{load} + \beta L_{entropy}$，其中 $L_{diff}$ 是标准扩散策略的行为克隆损失（MSE on noise prediction）。$\alpha$ 和 $\beta$ 控制两种辅助损失的相对权重——$\alpha$ 过大导致专家分配过于均匀丧失专门化，$\beta$ 过大则可能造成路由过于确定而忽略负载均衡。</div>
</div>

<div class="novelty-card">
<h4>创新点 3：推理时技能重排（Inference-Time Skill Reordering）</h4>
<div class="novelty-step"><strong>机制：</strong>在推理阶段，用户可以通过<strong>手动指定 Top-k 专家的激活顺序</strong>来重新编排子任务的执行次序。例如，原本训练数据中"先抓取杯子再抓取壶"的顺序，在推理时可以通过强制激活对应"取壶"的专家来反转顺序，<strong>无需任何额外训练数据或微调</strong>。</div>
<div class="novelty-step"><strong>意义：</strong>这赋予了策略一种零样本的组合泛化能力——学到的技能原语（expert specialization）可以按需重组，应对训练中未见过的任务序列。这为"学会一组技能，组合成任意任务"的通用操作范式提供了初步验证。</div>
</div>

<h3>2.3 与现有工作的本质区别</h3>
<div class="cmp-row">
<div class="cmp-col">
<h4>Standard Diffusion Policy (Chi et al., 2023)</h4>
<ul>
<li>条件向量：单一 MLP 编码观测，无阶段感知</li>
<li>失败恢复：隐式的，依赖扩散模型的随机性"碰巧"回到正确轨迹</li>
<li>任务组合：需要为每个新任务序列收集完整演示数据并重新训练</li>
<li>表示解耦：无显式机制，所有信息混入同一特征空间</li>
</ul>
</div>
<div class="cmp-col">
<h4>MoE-DP (Cheng et al., 2025)</h4>
<ul>
<li>条件向量：稀疏 MoE 动态路由，阶段感知</li>
<li>失败恢复：显式的，通过专家切换检测阶段失败并重新执行当前子任务</li>
<li>任务组合：推理时手动指定专家顺序即可重排，无需重训</li>
<li>表示解耦：稀疏路由 + 负载均衡 + 熵正则自然诱导阶段专门化</li>
</ul>
</div>
</div>

<div class="cmp-row">
<div class="cmp-col">
<h4>ACT / Diffusion Policy with Language (Octo, RT-2)</h4>
<ul>
<li>阶段分解：依赖自然语言指令进行任务分步，需人工标注子任务边界</li>
<li>专家机制：无，单一网络处理所有阶段</li>
<li>训练开销：大模型预训练 + 微调，计算成本高</li>
</ul>
</div>
<div class="cmp-col">
<h4>MoE-DP (无需语言监督)</h4>
<ul>
<li>阶段分解：<strong>完全自发涌现</strong>，无需任何子任务标签或语言标注</li>
<li>专家机制：Top-k 稀疏路由，每个专家 MLP 参数独立</li>
<li>训练开销：仅在 DP 基础上增加 MoE 层（3-4 个专家，每个为 2-3 层 MLP），额外参数量极小</li>
</ul>
</div>
</div>
</section>

<!-- ===== 3. Architecture ===== -->
<section id="architecture">
<h2>3. Architecture</h2>

<h3>3.1 系统总览</h3>
<p>MoE-DP 的整体架构由四个核心阶段组成：<strong>多模态感知编码</strong>、<strong>MoE 条件路由</strong>、<strong>扩散动作去噪</strong>、以及<strong>推理时技能控制</strong>。以下架构面板展示了从原始传感器输入到最终关节动作的完整信息流。</p>

<div class="arch-panel">
<div class="arch-grid">
<div class="arch-stage">
<h4>1. 多模态感知 <span>ResNet-18+MLP</span></h4>
<div class="arch-card arch-solar">
<strong>全局相机 (Global Camera)</strong>
<small>RGB 图像 3×224×224，经 ResNet-18 提取 512-d 特征向量 $v_g \in \mathbb{R}^{512}$</small>
</div>
<div class="arch-card arch-solar">
<strong>腕部相机 (Wrist Camera)</strong>
<small>RGB 图像 3×224×224，经共享权重 ResNet-18 编码为 $v_w \in \mathbb{R}^{512}$</small>
</div>
<div class="arch-card arch-solar">
<strong>本体感知 (Proprioception)</strong>
<small>7-DoF 关节角 + 末端位姿 → MLP → $v_p \in \mathbb{R}^{128}$</small>
</div>
</div>
<div class="arch-stage">
<h4>2. 特征融合 <span>Concat</span></h4>
<div class="arch-card arch-power">
<strong>多模态拼接</strong>
<small>$z_{raw} = [v_g; v_w; v_p] \in \mathbb{R}^{512+512+128} = \mathbb{R}^{1152}$</small>
</div>
<div class="arch-card arch-power">
<strong>投影降维</strong>
<small>线性投影层 → $z_t \in \mathbb{R}^{d_{moe}}$（典型值 $d_{moe}=256$）</small>
</div>
</div>
<div class="arch-stage">
<h4>3. MoE 路由 <span>Top-k Sparse</span></h4>
<div class="arch-card arch-motor">
<strong>路由器 (Router / Gating)</strong>
<small>$g_t = \text{Softmax}(W_g \cdot z_t)$<br/>$W_g \in \mathbb{R}^{N \times d_{moe}}$，N = 专家数量</small>
</div>
<div class="arch-card arch-motor">
<strong>稀疏专家激活</strong>
<small>仅激活 Top-k（k=2）专家：<br/>$z'_t = \sum_{i \in \text{Top-k}(g_t)} g_{t,i} \cdot E_i(z_t)$</small>
</div>
<div class="arch-card arch-motor">
<strong>辅助损失</strong>
<small>$L_{load}$ 平衡专家利用率<br/>$L_{entropy}$ 鼓励尖锐分配</small>
</div>
</div>
<div class="arch-stage">
<h4>4. 扩散去噪 <span>CNN U-Net</span></h4>
<div class="arch-card arch-thrust">
<strong>条件注入</strong>
<small>$z'_t$ 作为条件向量注入 U-Net 各层的 FiLM 模块</small>
</div>
<div class="arch-card arch-thrust">
<strong>动作预测</strong>
<small>预测动作序列 $a_{t:t+H}$，H 为预测时域</small>
</div>
<div class="arch-card arch-thrust">
<strong>推理控制</strong>
<small>可手动指定专家激活顺序 → 技能重排</small>
</div>
</div>
</div>

<div class="arch-arrow">
<span>&#8595; 特征提取</span><span>&#8595; 融合投影</span><span>&#8595; 专家路由</span><span>&#8595; 动作生成</span>
</div>

<div class="arch-summary">
<div class="arch-metric">
<strong>输入维度：1152</strong>
<small>全局 512 + 腕部 512 + 本体 128</small>
</div>
<div class="arch-metric">
<strong>MoE 维度：256</strong>
<small>投影后进入路由器的特征维度</small>
</div>
<div class="arch-metric">
<strong>专家数量：3-8</strong>
<small>仿真 4-8 个，真机仅需 3-4 个</small>
</div>
<div class="arch-metric">
<strong>动作时域：8-16 步</strong>
<small>每步对应 ~0.1s 控制周期</small>
</div>
</div>
</div>

<h3>3.2 MoE 层的数学细节</h3>
<p>MoE 层是本文的核心技术贡献，其设计借鉴了 LLM 中 Mixture of Experts 的稀疏激活思想，但针对机器人操作的特点进行了适配。</p>

<div class="formula-block">
<span class="eq-tag">Router / Gating</span>
$$g_t = \text{Softmax}(W_g \cdot z_t)$$
</div>
<p>其中 $z_t \in \mathbb{R}^{d_{moe}}$ 是融合并投影后的观测特征，$W_g \in \mathbb{R}^{N \times d_{moe}}$ 是路由器的可学习权重矩阵。$g_t \in \mathbb{R}^N$（满足 $\sum_i g_{t,i} = 1$）表示将当前观测分配给 $N$ 个专家的概率分布。</p>

<div class="formula-block">
<span class="eq-tag">Top-k Sparse Activation</span>
$$\text{Top-k}(g_t) = \{i_1, i_2, \ldots, i_k \mid g_{t,i_j} \text{ 是 } g_t \text{ 中前 } k \text{ 大的值}\}$$
$$z'_t = \sum_{i \in \text{Top-k}(g_t)} g_{t,i} \cdot E_i(z_t)$$
</div>
<p>每个专家 $E_i(\cdot)$ 是一个独立的多层感知机（MLP），通常为 2-3 层，隐藏维度 256-512。通过 Top-k 稀疏激活（典型 $k=2$），每个样本仅需计算 $k$ 个专家的前向传播，计算开销远小于全激活。未被激活的专家的梯度为零，保证了负载均衡的必要性。</p>

<div class="formula-block">
<span class="eq-tag">Load Balancing Loss</span>
$$L_{load} = N \cdot \sum_{i=1}^{N} f_i \cdot P_i$$
<div class="eq-note">
<strong>符号说明：</strong><br/>
$f_i = \frac{1}{B} \sum_{x \in \text{batch}} \mathbb{1}[i \in \text{Top-k}(g(x))]$ —— 批次中被分配给专家 $i$ 的样本比例。<br/>
$P_i = \frac{1}{B} \sum_{x \in \text{batch}} g(x)_i$ —— 路由器对专家 $i$ 的平均 softmax 概率。<br/>
当所有专家均匀使用时，$f_i = 1/N$，$P_i = 1/N$，乘积与求和抵消，$L_{load}$ 最小。当路由坍缩到少数专家时，$L_{load}$ 急剧增大。</div>
</div>

<div class="formula-block">
<span class="eq-tag">Entropy Regularization</span>
$$L_{entropy} = -\frac{1}{B} \sum_{t=1}^{B} \sum_{i=1}^{N} p_{t,i} \cdot \log(p_{t,i} + \varepsilon)$$
<div class="eq-note">
<strong>关键设计：</strong>$p_{t,i}$ 是路由器对样本 $t$ 分配给专家 $i$ 的 softmax 概率。由于是负熵，最小化 $L_{entropy}$ 等价于最大化路由概率的熵的相反数——即<strong>鼓励低熵（尖锐）分配</strong>。这与 LLM 中常用的负载均衡损失方向相反：LLM 的 auxiliary loss 通常是鼓励均匀分配的，而这里额外的熵正则项是为了让每个样本的专家分配更加确定，从而促进专家功能的专门化。$\varepsilon = 10^{-8}$ 防止数值溢出。</div>
</div>

<div class="formula-block">
<span class="eq-tag">Composite Training Objective</span>
$$L = L_{diff} + \alpha \cdot L_{load} + \beta \cdot L_{entropy}$$
<div class="eq-note">
<strong>三项损失的博弈关系：</strong><br/>
$L_{diff}$：标准的扩散去噪 MSE 损失，驱动策略学习正确的动作分布。<br/>
$L_{load}$：防止所有样本只使用少数专家（collapsing），$\alpha$ 通常设为 0.01-0.1。<br/>
$L_{entropy}$：防止路由器输出接近均匀分布（无专门化），$\beta$ 通常设为 0.001-0.01。<br/>
这三者形成精巧的制衡：无 $L_{load}$ 时专家坍缩，无 $L_{entropy}$ 时专家无区分度，两者权重不当则训练不稳定。</div>
</div>

<h3>3.3 Diffusion Policy 骨干</h3>
<p>MoE-DP 的扩散骨干与标准 Diffusion Policy (Chi et al., 2023) 基本一致：</p>
<ul>
<li><strong>去噪网络：</strong>基于 1D 卷积的 U-Net 架构，输入为噪声化的动作序列 $a_t^K$（$K$ 为当前去噪步），输出为预测的噪声 $\hat{\epsilon}$。</li>
<li><strong>条件注入：</strong>MoE 输出的条件向量 $z'_t$ 通过 FiLM（Feature-wise Linear Modulation）层注入到 U-Net 的各个下采样和上采样层级。具体而言，$z'_t$ 经过一个小型 MLP 生成每层的 scale $\gamma$ 和 shift $\beta$ 参数，对中间特征图进行仿射变换。</li>
<li><strong>动作表示：</strong>预测未来 $H$ 步的末端执行器位姿变化（6-DoF：位置 $\Delta x, \Delta y, \Delta z$ + 欧拉角 $\Delta roll, \Delta pitch, \Delta yaw$）以及夹爪开合状态。</li>
<li><strong>推理过程：</strong>DDPM 采样，从高斯噪声开始，经 $K=100$ 步迭代去噪，每步将当前动作估计与 MoE 条件向量一起输入 U-Net。</li>
</ul>

<h3>3.4 推理时的专家控制</h3>
<p>这是 MoE-DP 最具特色的功能。在标准推理模式中，路由器根据当前观测自动选择 Top-k 专家。在<strong>手动控制模式</strong>下，用户可以：</p>
<ol>
<li><strong>指定专家序列：</strong>定义 $[e_{i_1}, e_{i_2}, \ldots, e_{i_m}]$，覆盖 $r$ 轮重复。策略在每个推理步按序激活指定专家，忽略路由器的自动选择。</li>
<li><strong>阶段感知重试：</strong>如果某一阶段失败（例如抓取滑落），策略检测到当前状态与阶段目标不匹配，自动重新激活该阶段对应的专家。</li>
<li><strong>组合泛化：</strong>训练中未见过的子任务序列（如先放置再抓取，而非先抓取再放置），通过不同的专家激活顺序即可实现。</li>
</ol>

<div class="mermaid-box">
<div class="mermaid">
graph TD
    A["观测 o_t<br/>全局相机 + 腕部相机 + 本体状态"] --> B["ResNet-18<br/>视觉编码"]
    B --> C["特征拼接<br/>z_raw = [v_g; v_w; v_p]"]
    C --> D["线性投影<br/>z_t = W_proj · z_raw"]
    D --> E{"路由器<br/>g_t = Softmax(W_g · z_t)"}
    E -->|Top-k=2| F["专家 E_1<br/>MLP 256→256"]
    E -->|Top-k=2| G["专家 E_2<br/>MLP 256→256"]
    E -->|未激活| H["专家 E_3<br/>MLP 256→256"]
    E -->|未激活| I["专家 E_4<br/>MLP 256→256"]
    F --> J["加权求和<br/>z'_t = Σ g_i · E_i(z_t)"]
    G --> J
    J --> K["U-Net Denoiser<br/>FiLM 条件注入"]
    K --> L["预测动作序列<br/>a_{t:t+H}"]
    L --> M["机器人执行<br/>Franka Panda"]
    M -->|下一时刻| A

    style A fill:#fff7ed,stroke:#fed7aa
    style E fill:#ede9fe,stroke:#c4b5fd
    style F fill:#d1fae5,stroke:#6ee7b7
    style G fill:#d1fae5,stroke:#6ee7b7
    style H fill:#f3f4f6,stroke:#d1d5db
    style I fill:#f3f4f6,stroke:#d1d5db
    style K fill:#dbeafe,stroke:#93c5fd
    style L fill:#fef3c7,stroke:#fcd34d
</div>
</div>

<h3>3.5 手动专家控制模式流程图</h3>
<div class="mermaid-box">
<div class="mermaid">
graph LR
    subgraph 标准推理
        A1["观测 o_t"] --> A2["路由器自动选择"]
        A2 --> A3["Top-k 专家激活"]
        A3 --> A4["条件向量 z'_t"]
    end
    subgraph 手动控制
        B1["用户指定序列<br/>[E₂, E₁, E₄, E₃]"] --> B2["强制激活 E₂"]
        B2 --> B3["阶段完成?"]
        B3 -->|是| B4["切换到 E₁"]
        B3 -->|否/失败| B2
        B4 --> B5["阶段完成?"]
        B5 -->|是| B6["切换到 E₄"]
        B5 -->|否/失败| B4
    end
    A4 --> C["U-Net 去噪 → 动作"]
    B4 --> C
    B6 --> C

    style A2 fill:#dbeafe,stroke:#3b82f6
    style B1 fill:#fef3c7,stroke:#f59e0b
    style B3 fill:#e6f7ee,stroke:#10b981
    style B5 fill:#e6f7ee,stroke:#10b981
</div>
</div>
</section>

<!-- ===== 4. Task Definition ===== -->
<section id="task">
<h2>4. Task Definition</h2>

<h3>4.1 任务场景总览</h3>
<p>MoE-DP 在 <strong>6 个仿真任务</strong>和 <strong>3 个真实世界任务</strong>上进行了评估。所有任务的共同特征是：<strong>长时序（5-15 个连续子步骤）、需要多阶段协调、容易受外部扰动影响。</strong></p>

<h3>4.2 仿真任务（基于 robosuite / MimicGen）</h3>
<table>
<tr><th>任务名称</th><th>子步骤数</th><th>任务描述</th><th>关键难点</th></tr>
<tr>
<td><strong>Hammer Cleanup</strong></td>
<td>3-4</td>
<td>从桌面上拾取锤子，将其放入指定工具箱，然后关闭工具箱盖子</td>
<td>锤子形状不规则，抓取姿态多样；关闭盖子需要精确的力控制</td>
</tr>
<tr>
<td><strong>Kitchen</strong></td>
<td>4-5</td>
<td>打开柜门，取出锅，将锅放在灶台上，然后打开炉灶开关</td>
<td>柜门铰链运动的非线性；锅的重心变化；开关旋钮的精细操作</td>
</tr>
<tr>
<td><strong>Coffee Preparation</strong></td>
<td>5-6</td>
<td>取咖啡豆，倒入研磨机，研磨，取咖啡粉，放入咖啡机，按下按钮</td>
<td>多物体交互（豆、研磨机、咖啡机）；倒咖啡豆需要倾斜控制</td>
</tr>
<tr>
<td><strong>Mug Cleanup</strong></td>
<td>3-4</td>
<td>拾取杯子，移动到水槽上方，倒出水，将杯子放入碗架</td>
<td>倒水动作涉及旋转腕关节；放置位置需精确对齐</td>
</tr>
<tr>
<td><strong>Kitchen Cleanup</strong></td>
<td>5-7</td>
<td>清理台面：依次拾取多个物体放入垃圾桶，擦拭台面，将抹布放回</td>
<td>物体数量可变、位置随机；抹布的柔性形变；垃圾桶盖的开合</td>
</tr>
<tr>
<td><strong>Table Cleanup</strong></td>
<td>4-6</td>
<td>将桌上的多个物品（杯子、盘子、餐具）分别放入指定收纳区域</td>
<td>多目标分类放置；物品间可能相互遮挡</td>
</tr>
</table>

<h3>4.3 真实世界任务（Franka Panda 平台）</h3>
<table>
<tr><th>任务名称</th><th>子步骤数</th><th>扰动类型</th><th>评估指标</th></tr>
<tr>
<td><strong>Pick-and-Place with Disturbance</strong></td>
<td>2-3</td>
<td>抓取成功后，人为将物体复位到初始位置</td>
<td>策略是否检测到抓取失败并重新执行抓取（而非空手移动到放置位置）</td>
</tr>
<tr>
<td><strong>Multi-Object Sorting</strong></td>
<td>4-6</td>
<td>在运输过程中人为移走或更换物体</td>
<td>策略是否重新定位物体并调整运动轨迹</td>
</tr>
<tr>
<td><strong>Drawer Open-Place-Close</strong></td>
<td>3-4</td>
<td>物体放入抽屉后，人为将物体取出放回桌面</td>
<td>策略是否重新执行"拾取-放入"循环而非直接关闭空抽屉</td>
</tr>
</table>

<h3>4.4 扰动协议</h3>
<div class="callout warn">
<span class="callout-title">扰动定义</span>
<p>本文定义了两类扰动：(1) <strong>状态扰动 (State Disturbance)</strong>——在策略成功完成某个子任务后，人为将物体复位到该子任务开始前的状态。例如抓取杯子成功后，人将杯子放回桌面原位。(2) <strong>轨迹扰动 (Trajectory Disturbance)</strong>——在策略执行过程中，人为推/拉机器人手臂，使其偏离原定轨迹。</p>
<p>扰动测试的核心评估标准是<strong>策略是否能够检测到当前子任务失败，并自动重新执行该子任务</strong>，而非盲目的按预定序列前进。这要求策略具备对当前任务阶段的隐式感知能力。</p>
</div>

<h3>4.5 观测空间与动作空间</h3>
<table>
<tr><th>组成部分</th><th>维度</th><th>说明</th></tr>
<tr><td>全局相机 RGB</td><td>3×224×224</td><td>固定在三脚架上的第三人称视角相机，提供场景级上下文</td></tr>
<tr><td>腕部相机 RGB</td><td>3×224×224</td><td>安装在机械臂末端的眼在手（eye-in-hand）相机，提供精细操作视角</td></tr>
<tr><td>关节角度</td><td>7</td><td>Franka Panda 的 7 个关节角（弧度）</td></tr>
<tr><td>末端执行器位姿</td><td>6</td><td>位置 (x,y,z) + 欧拉角 (roll, pitch, yaw)</td></tr>
<tr><td>夹爪状态</td><td>1</td><td>开合程度 [0, 1]</td></tr>
<tr><td><strong>动作输出</strong></td><td>7</td><td>末端位姿变化 Δx,Δy,Δz,Δroll,Δpitch,Δyaw + 夹爪命令</td></tr>
</table>
</section>

<!-- ===== 5. Key Challenge ===== -->
<section id="challenge">
<h2>5. Key Challenge</h2>

<h3>5.1 长时序操作的核心困难</h3>

<div class="callout danger">
<span class="callout-title">挑战一：隐表示的阶段纠缠 (Latent Entanglement)</span>
<p>标准 Diffusion Policy 的条件向量 $c_t$ 是一个扁平的特征向量，它<strong>同时编码了</strong>所有与当前任务相关的视觉和状态信息。当任务包含多个语义上截然不同的阶段时（如"接近物体"→"抓取"→"抬起"→"运输"→"放置"→"释放"），这些阶段信息在隐空间中高度纠缠。这意味着：</p>
<ul>
<li>策略无法区分"当前靠近物体准备抓取"和"当前已抓取物体准备运输"——两者可能产生相似的隐向量但需要完全不同的动作模式。</li>
<li>当扰动改变了任务状态后，策略无法识别自己处于哪个阶段，从而做出错误的阶段选择——例如抓取失败后继续执行"运输到目标位置"的动作。</li>
</ul>
</div>

<div class="callout danger">
<span class="callout-title">挑战二：失败检测与恢复的缺失</span>
<p>在标准模仿学习框架中，策略从专家演示中学习的是一个<strong>无条件的轨迹分布</strong> $p(a_{1:T} \mid o_1)$。一旦初始观测 $o_1$ 确定，策略生成的轨迹就基本确定了（尽管扩散模型有一定随机性）。这种"开环"特性导致：</p>
<ul>
<li>策略无法感知执行过程中的异常——它不知道抓取是否成功，不知道物体是否在中途滑落。</li>
<li>即使扩散采样的随机性偶尔产生偏离的轨迹，也没有机制引导该偏离"恰好"朝向正确的恢复行为。</li>
</ul>
</div>

<div class="callout danger">
<span class="callout-title">挑战三：专家坍缩与表示坍缩</span>
<p>直接将 MoE 引入 Diffusion Policy 并不能自动解决上述问题。如果缺乏适当的正则化：</p>
<ul>
<li><strong>路由坍缩 (Router Collapse)：</strong>路由器学会将所有样本分配给同一个或少数几个专家，其余专家退化为"死神经元"——此时 MoE 退化为普通 MLP。</li>
<li><strong>表示坍缩 (Representation Collapse)：</strong>即使各专家被均匀使用，如果没有尖锐分配的压力，每个专家的功能边界会模糊化，最终所有专家学习到相似的映射函数——等价于集成而非专门化。</li>
<li>这两个坍缩问题是<strong>相互矛盾的</strong>：负载均衡防止路由坍缩但容易导致表示坍缩，熵正则防止表示坍缩但可能加剧路由坍缩。因此 $L_{load}$ 和 $L_{entropy}$ 必须通过超参数 $\alpha$ 和 $\beta$ 进行精细平衡。</li>
</ul>
</div>

<h3>5.2 任务特定的挑战</h3>
<table>
<tr><th>挑战维度</th><th>具体表现</th><th>对策略的要求</th></tr>
<tr>
<td><strong>多物体顺序依赖</strong></td>
<td>Kitchen Cleanup 中必须先清理台面物品再擦拭，顺序不可颠倒</td>
<td>策略需要有隐式的"进度"表示，能感知已完成和待完成的子任务</td>
</tr>
<tr>
<td><strong>视觉模糊性</strong></td>
<td>全局相机视角下，抓取成功前后的图像差异极小（手部仅移动几厘米）</td>
<td>腕部相机提供补充信息；MoE 路由需要融合多视角判断阶段切换</td>
</tr>
<tr>
<td><strong>接触与非接触切换</strong></td>
<td>从自由空间运动（接近）到接触操作（抓取）的动力学突变</td>
<td>不同阶段需要不同的控制策略特征——接近阶段关注位置精度，抓取阶段关注力/力矩</td>
</tr>
<tr>
<td><strong>部分可观测性</strong></td>
<td>机械臂自身可能遮挡被抓取物体；物体放入抽屉后完全不可见</td>
<td>策略需要依赖记忆和历史信息推断物体状态，而非仅依赖当前帧</td>
</tr>
</table>
</section>

<!-- ===== 6. Method ===== -->
<section id="method">
<h2>6. Method</h2>

<h3>6.1 训练流程</h3>

<div class="mermaid-box">
<div class="mermaid">
graph TD
    A["收集专家演示数据<br/>人类遥操作 / Scripted Policy"] --> B["数据预处理<br/>图像 resize 224×224<br/>动作序列切片 H=16"]
    B --> C["训练循环开始"]
    C --> D["采样批次 (o_t, a_{t:t+H})"]
    D --> E["ResNet-18 编码全局+腕部图像"]
    E --> F["拼接本体状态，线性投影"]
    F --> G["路由器计算 g_t = Softmax(W_g · z_t)"]
    G --> H["Top-k 选择 + 专家前向传播"]
    H --> I["计算 L_diff<br/>噪声预测 MSE"]
    H --> J["计算 L_load<br/>负载均衡"]
    H --> K["计算 L_entropy<br/>熵正则"]
    I --> L["总损失 L = L_diff + α·L_load + β·L_entropy"]
    J --> L
    K --> L
    L --> M["反向传播<br/>更新所有参数"]
    M --> C

    style A fill:#dbeafe,stroke:#3b82f6
    style G fill:#ede9fe,stroke:#8b5cf6
    style L fill:#fef3c7,stroke:#f59e0b
</div>
</div>

<h3>6.2 算法伪代码</h3>
<div class="formula-block">
<span class="eq-tag">Training Algorithm</span>
<pre style="font-family:'JetBrains Mono',Consolas,monospace;font-size:12px;color:#334155;line-height:1.6;">
<strong>Input:</strong> 专家演示数据集 D = {(o_t, a_{t:t+H})}, 专家数量 N, Top-k 值, α, β
<strong>Initialize:</strong> ResNet-18 编码器 φ, 投影矩阵 W_proj, 路由器 W_g,
           专家 MLPs {E_1, ..., E_N}, U-Net 去噪器 ε_θ

<strong>for</strong> epoch = 1 to E:
    <strong>for</strong> batch (o, a) in D:
        # 1. 编码观测
        v_g = φ_global(o_global)      # 全局相机
        v_w = φ_wrist(o_wrist)         # 腕部相机
        v_p = MLP(o_proprio)           # 本体感知
        z_raw = concat([v_g, v_w, v_p])

        # 2. MoE 路由
        z_t = W_proj · z_raw
        g_t = Softmax(W_g · z_t)       # 路由概率 [N]
        top_k_idx = argTopK(g_t, k)
        z'_t = sum(g_t[i] * E_i(z_t) for i in top_k_idx)

        # 3. 扩散损失
        noise = sample_noise()
        a_noisy = sqrt(α_bar) * a + sqrt(1-α_bar) * noise
        noise_pred = ε_θ(a_noisy, condition=z'_t)
        L_diff = MSE(noise_pred, noise)

        # 4. 辅助损失
        f_i = mean(1[i in top_k_idx])  # 分配给专家 i 的样本比例
        P_i = mean(g_t[i])             # 专家 i 的平均路由概率
        L_load = N * sum(f_i * P_i)
        L_entropy = -mean(g_t * log(g_t + ε))

        # 5. 总损失
        L = L_diff + α * L_load + β * L_entropy

        # 6. 更新
        optimizer.zero_grad()
        L.backward()
        optimizer.step()
</pre>
</div>

<h3>6.3 具体实现细节</h3>
<table>
<tr><th>组件</th><th>具体配置</th></tr>
<tr><td>视觉编码器</td><td>ResNet-18（ImageNet 预训练），去掉最后的分类层，输出 512-d 特征。全局和腕部相机<strong>共享权重</strong>，但通过位置编码区分视角。</td></tr>
<tr><td>本体感知编码器</td><td>3 层 MLP，维度 [14 → 64 → 128]，ReLU 激活。输入 14-d = 7 关节角 + 3 末端位置 + 3 欧拉角 + 1 夹爪。</td></tr>
<tr><td>投影层</td><td>线性层 [1152 → 256]，LayerNorm + GELU</td></tr>
<tr><td>路由器 W_g</td><td>线性层 [256 → N]，无 bias。Softmax 温度固定为 1.0</td></tr>
<tr><td>专家 E_i</td><td>2 层 MLP [256 → 512 → 256]，GELU 激活，LayerNorm。每专家独立参数</td></tr>
<tr><td>Top-k</td><td>k=2（仿真和真机均使用）。消融实验测试了 k=1,2,4</td></tr>
<tr><td>U-Net 去噪器</td><td>1D CNN U-Net，下采样 3 层 + 上采样 3 层，每层 2 个残差块。通道数 [256, 512, 1024]</td></tr>
<tr><td>扩散步数</td><td>训练：1000 步（DDPM）；推理：100 步（DDIM 加速）</td></tr>
<tr><td>动作预测时域 H</td><td>16 步（约 1.6 秒）。采用 receding horizon：每次执行前 8 步后重新推理</td></tr>
<tr><td>优化器</td><td>AdamW，lr=1e-4，weight decay=1e-4，cosine schedule</td></tr>
<tr><td>批次大小</td><td>256</td></tr>
<tr><td>训练轮数</td><td>500-1000 epochs（取决于任务复杂度）</td></tr>
<tr><td>α (L_load 权重)</td><td>0.01（仿真）/ 0.02（真机）</td></tr>
<tr><td>β (L_entropy 权重)</td><td>0.005（仿真）/ 0.01（真机）</td></tr>
</table>

<h3>6.4 推理模式</h3>
<div class="cmp-row">
<div class="cmp-col">
<h4>模式 A：自动路由（标准推理）</h4>
<ul>
<li>每步由路由器根据当前观测自动选择 Top-k 专家</li>
<li>条件向量 $z'_t$ 自动反映当前阶段特征</li>
<li>适用于无扰动的正常执行场景</li>
<li>与训练时的推理行为一致</li>
</ul>
</div>
<div class="cmp-col">
<h4>模式 B：手动专家控制（技能重排）</h4>
<ul>
<li>用户指定专家激活序列 [E_i, E_j, E_k, ...]</li>
<li>每步强制执行当前阶段对应的专家，忽略路由器</li>
<li>支持阶段级重试：检测失败后重新激活当前专家</li>
<li>适用于有扰动或需要重排子任务的场景</li>
</ul>
</div>
</div>

<h3>6.5 演示数据收集</h3>
<ul>
<li><strong>仿真：</strong>使用 MimicGen 自动生成演示数据——先通过遥操作采集少量（10-20 条）人工演示，然后用 MimicGen 在物体位置变化的场景中批量生成变体演示（每条人工演示生成 50-100 条变体）。</li>
<li><strong>真机：</strong>使用 3Dconnexion SpaceMouse 进行遥操作，每个任务采集 100-200 条人类演示，覆盖不同的物体初始位置和扰动场景。</li>
<li><strong>数据增强：</strong>训练时随机裁剪 + 颜色抖动，模拟光照和视角变化。</li>
</ul>
</section>

<!-- ===== 7. Principles ===== -->
<section id="principles">
<h2>7. Principles</h2>

<h3>7.1 机制性原理：为什么 MoE 能促进阶段解耦？</h3>

<div class="callout idea">
<span class="callout-title">原理一：稀疏激活 = 条件计算 = 隐式阶段划分</span>
<p>MoE 的稀疏激活机制本质上是一种<strong>输入依赖的条件计算</strong>。对于每个观测 $o_t$，只有 2 个（Top-k=2）专家被激活。由于不同任务阶段产生不同的观测模式（接近阶段：手远离物体，物体在视野中央；抓取阶段：手接触物体，腕部相机中物体消失；运输阶段：物体在手中，全局相机跟踪手部运动），路由器自然学会将不同观测模式映射到不同的专家子集。这是<strong>无监督的阶段分割</strong>——没有人为标注子任务边界，但路由概率 $g_t$ 的变化自然标记了阶段切换点。</p>
</div>

<div class="callout idea">
<span class="callout-title">原理二：负载均衡 + 熵正则 = 专门化动力</span>
<p>$L_{load}$ 和 $L_{entropy}$ 的协同作用创造了一个<strong>专家生态位分化</strong>的优化景观：</p>
<ul>
<li>$L_{load}$：确保所有专家都有"生存权"——每个专家至少被一部分样本使用。类似于生态学中的"资源分配"，防止一个专家垄断所有输入。</li>
<li>$L_{entropy}$：确保专家有"专业化压力"——每个样本的路由概率尽可能尖锐，使得每个专家在其擅长的输入子集上获得高置信度的分配。类似于生态学中的"生态位特化"，促进功能差异化。</li>
<li>两者共同的均衡点：每个专家在数据的某个子集上具有压倒性的高路由概率，同时所有专家在全局数据上被大致均匀地使用。这个均衡状态自然对应<strong>按任务阶段的语义分割</strong>——因为同一阶段内的观测相似（高熵正则推动同一专家），不同阶段间观测差异大（负载均衡推动不同专家）。</li>
</ul>
</div>

<div class="callout idea">
<span class="callout-title">原理三：专家切换信号作为失败检测机制</span>
<p>当任务正常进行时，路由概率 $g_t$ 随时间平滑演变——一个专家的概率逐渐下降，另一个逐渐上升，标志着阶段过渡。当扰动发生时（例如物体被移走），观测突然变化，导致 $g_t$ 发生<strong>不连续的跳变</strong>——可能跳回前一个阶段的专家模式。这种跳变可以被用作隐式的失败检测信号，触发策略重新执行前一阶段。这不需要显式的失败分类器，完全由 MoE 路由的几何结构自然提供。</p>
</div>

<h3>7.2 与认知科学的联系</h3>
<p>MoE-DP 的设计折射出几个认知科学概念：</p>
<ul>
<li><strong>选项框架 (Options Framework, Sutton et al., 1999)：</strong>MoE 的每个专家可以类比为一个"选项"（option）——一个在特定状态下激活并持续一段时间的子策略。路由器的自动切换对应选项的终止条件，手动专家控制对应选项的策略选择。</li>
<li><strong>分块理论 (Chunking Theory)：</strong>人类在执行长序列操作时将连续动作组织成"块"（chunks）。MoE-DP 的专家专门化本质上实现了动作序列的<strong>自适应分块</strong>，每个专家对应一个语义连贯的动作块。</li>
<li><strong>稀疏编码 (Sparse Coding)：</strong>大脑皮层的稀疏编码原则——每个刺激仅激活少数神经元——与 MoE 的 Top-k 稀疏激活高度一致。这可能是 MoE-DP 在生物学意义上的优雅之处。</li>
</ul>

<h3>7.3 设计原则总结</h3>
<table>
<tr><th>原则</th><th>实现</th><th>效果</th></tr>
<tr><td>阶段解耦</td><td>MoE 稀疏路由 + 条件计算</td><td>不同专家自然对应不同任务阶段</td></tr>
<tr><td>专家多样性与利用率平衡</td><td>L_load + L_entropy 协同优化</td><td>所有专家都活跃且有明确专门化</td></tr>
<tr><td>推理灵活性</td><td>手动专家激活序列控制</td><td>零样本任务重排与失败恢复</td></tr>
<tr><td>最小侵入性</td><td>仅在条件通道插入 MoE，不改 DP 骨干</td><td>与现有 Diffusion Policy 框架兼容</td></tr>
<tr><td>无监督阶段发现</td><td>无阶段标签训练，路由概率自然分化</td><td>无需人工标注子任务边界</td></tr>
</table>
</section>

<!-- ===== 8. Figures & Evidence ===== -->
<section id="figures">
<h2>8. Figures &amp; Evidence</h2>

<h3>8.1 关键实验结果</h3>

<h4>仿真扰动测试（核心结果）</h4>
<table>
<tr><th>任务</th><th>Diffusion Policy (DP)</th><th>MoE-DP (ours)</th><th>相对提升</th></tr>
<tr><td>Hammer Cleanup</td><td>21.3%</td><td>58.7%</td><td>+175.6%</td></tr>
<tr><td>Kitchen</td><td>15.2%</td><td>47.8%</td><td>+214.5%</td></tr>
<tr><td>Coffee Preparation</td><td>18.9%</td><td>52.3%</td><td>+176.7%</td></tr>
<tr><td>Mug Cleanup</td><td>22.7%</td><td>61.2%</td><td>+169.6%</td></tr>
<tr><td>Kitchen Cleanup</td><td>12.4%</td><td>44.6%</td><td>+259.7%</td></tr>
<tr><td>Table Cleanup</td><td>16.3%</td><td>58.2%</td><td>+257.1%</td></tr>
<tr class="highlight"><td><strong>平均</strong></td><td><strong>17.8%</strong></td><td><strong>53.8%</strong></td><td><strong>+202.2%（36 pp）</strong></td></tr>
</table>

<div class="callout tip">
<span class="callout-title">关键发现</span>
<p>在所有 6 个仿真任务中，MoE-DP 在扰动条件下的成功率均为 DP 基线的 <strong>2-3.5 倍</strong>。平均绝对提升 36 个百分点。特别值得注意的是 Kitchen Cleanup（+259.7%）和 Table Cleanup（+257.1%）这两个子步骤最多的任务获得了最大幅度的提升，验证了<strong>任务步骤越多、阶段解耦的价值越大</strong>的假设。</p>
</div>

<h4>真实世界扰动测试</h4>
<table>
<tr><th>任务</th><th>Diffusion Policy (DP)</th><th>MoE-DP (ours)</th><th>相对提升</th></tr>
<tr><td>Pick-and-Place + Disturbance</td><td>32.0%</td><td>76.0%</td><td>+137.5%</td></tr>
<tr><td>Multi-Object Sorting</td><td>24.0%</td><td>64.0%</td><td>+166.7%</td></tr>
<tr><td>Drawer Open-Place-Close</td><td>28.0%</td><td>73.0%</td><td>+160.7%</td></tr>
<tr class="highlight"><td><strong>平均</strong></td><td><strong>28.0%</strong></td><td><strong>71.0%</strong></td><td><strong>+153.6%（43 pp）</strong></td></tr>
</table>

<div class="callout tip">
<span class="callout-title">真机验证</span>
<p>真实世界测试的结果趋势与仿真高度一致，且绝对提升幅度（43 pp）甚至超过仿真（36 pp），验证了方法在真实感知噪声和执行不确定性下的鲁棒性。成功率从不到 1/3 提升到超过 2/3，使系统在实际部署中从"不可用"变为"可用"。</p>
</div>

<h4>消融实验</h4>
<table>
<tr><th>配置</th><th>Hammer Cleanup</th><th>Kitchen</th><th>Coffee Prep</th><th>平均</th></tr>
<tr><td>完整 MoE-DP (k=2, 有 L_load + L_entropy)</td><td>58.7%</td><td>47.8%</td><td>52.3%</td><td>52.9%</td></tr>
<tr><td>无 L_load</td><td>35.2%</td><td>28.6%</td><td>31.8%</td><td>31.9%</td></tr>
<tr><td>无 L_entropy</td><td>41.3%</td><td>33.5%</td><td>38.7%</td><td>37.8%</td></tr>
<tr><td>无辅助损失 (纯 MoE, 无正则)</td><td>24.1%</td><td>19.2%</td><td>22.5%</td><td>21.9%</td></tr>
<tr><td>k=1 (单专家)</td><td>48.2%</td><td>38.4%</td><td>43.6%</td><td>43.4%</td></tr>
<tr><td>k=4 (四专家)</td><td>52.6%</td><td>42.1%</td><td>47.2%</td><td>47.3%</td></tr>
<tr><td>DP 基线 (无 MoE)</td><td>21.3%</td><td>15.2%</td><td>18.9%</td><td>18.5%</td></tr>
</table>

<div class="callout warn">
<span class="callout-title">消融分析要点</span>
<ul>
<li><strong>负载均衡损失最为关键：</strong>移除 $L_{load}$ 导致性能从 52.9% 降至 31.9%（降幅最大），说明专家坍缩是最致命的失败模式。没有负载均衡，路由器学会将所有样本分配给同一个专家，MoE 完全失效。</li>
<li><strong>熵正则也很重要：</strong>移除 $L_{entropy}$ 导致约 15 pp 的性能下降。没有熵正则，路由概率趋于均匀，各专家功能边界模糊。</li>
<li><strong>Top-k=2 是最优选择：</strong>k=1 限制了每个样本的表达能力（仅单专家），k=4 引入过多专家导致路由不确定性增加。</li>
<li><strong>无正则的纯 MoE 与 DP 基线相当：</strong>进一步验证了辅助损失设计的必要性。</li>
</ul>
</div>

<h3>8.2 专家专门化可视化</h3>
<p>论文通过分析不同任务阶段中路由概率 $g_t$ 的分布，展示了专家的自发性专门化。</p>

<div class="paper-figure">
<div class="fig-header">
<span class="fig-number">Fig. Expert Specialization</span>
<span class="fig-caption">专家激活模式在任务阶段时序上的分布</span>
<span class="fig-source">Adapted from paper</span>
</div>
<div class="fig-placeholder">[专家专门化热力图/时序图 — 详见原始论文 Fig.4-5]</div>
<div class="fig-interpretation">
<span class="fig-label">关键解读</span>
<ul>
<li><strong>Expert 1（"接近"专家）：</strong>在任务开始阶段（末端靠近物体）路由概率最高，一旦进入接触阶段概率急剧下降。</li>
<li><strong>Expert 2（"抓取"专家）：</strong>在手指接触物体到确认抓取成功的短暂时间窗口内独占式激活。</li>
<li><strong>Expert 3（"运输"专家）：</strong>在物体已被抓取、正在移动到目标位置的阶段持续高概率激活。</li>
<li><strong>Expert 4（"放置/释放"专家）：</strong>在到达目标位置、缓慢释放物体的阶段激活。</li>
<li><strong>阶段切换时的专家概率呈现平滑过渡</strong>（而非硬切换），反映了任务阶段之间的连续过渡特性。</li>
<li>不同随机种子的训练产生了相似的专家功能划分模式，说明这种专门化是<strong>结构性的</strong>而非偶然的。</li>
</ul>
</div>
</div>

<h3>8.3 推理时技能重排实验</h3>
<div class="paper-figure">
<div class="fig-header">
<span class="fig-number">Fig. Skill Reordering</span>
<span class="fig-caption">通过手动专家序列控制实现子任务重排</span>
<span class="fig-source">Adapted from paper</span>
</div>
<div class="fig-placeholder">[技能重排对比图 — 详见原始论文 Fig.7]</div>
<div class="fig-interpretation">
<span class="fig-label">实验结果摘要</span>
<p>论文在 Coffee Preparation 任务中演示了技能重排：</p>
<ul>
<li><strong>训练序列：</strong>取咖啡豆 → 研磨 → 取咖啡粉 → 放入咖啡机 → 按下按钮</li>
<li><strong>重排序列（推理时）：</strong>取咖啡粉 → 放入咖啡机 → 取咖啡豆 → 研磨（颠倒顺序）</li>
<li><strong>结果：</strong>手动专家控制下，重排序列的成功率达到 45.2%，显著高于 DP 基线的 0%（完全失败）和自动路由 MoE-DP 的 12.3%（路由器不理解新的阶段顺序）。</li>
<li>这个实验证明了专家专门化产生了<strong>可重组的技能原语</strong>——每个专家学到的不是"在步骤 3 做什么"，而是"当需要抓取时如何抓取"，因此可以在任意位置被调用。</li>
</ul>
</div>
</div>

<h3>8.4 源文件概览</h3>
<div class="figure">
<img src="figures/overview.png" alt="MoE-DP: An MoE-Enhanced Diffusion Policy for Robust Long-Horizon Manipulation - source overview">
<div class="caption">首页和论文示意图展示 MoE 位于视觉编码与 diffusion 去噪之间，并把连续任务划分为语义动作阶段。涵盖系统架构、仿真和真实世界实验设置以及主要实验结果。</div>
</div>
<p class="source">Rendered directly from page 1 of the local PDF as a source anchor for the title, abstract, and opening overview figure. See the <a href="Cheng et al. - 2025 - MoE-DP An MoE-enhanced diffusion policy for robust long-horizon robotic manipulation with skill dec.pdf">original PDF</a>.</p>
</section>

<!-- ===== 9. Potential Flaw ===== -->
<section id="flaw">
<h2>9. Potential Flaw &amp; Limitations</h2>

<h3>9.1 方法的边界与未解决问题</h3>

<div class="callout warn">
<span class="callout-title">局限一：专家数量的任务依赖性</span>
<p>当前方法中，专家数量 $N$ 是一个需要人为设定的超参数。虽然论文表明仿真任务中 $N=4$ 通常足够，但最优的 $N$ 取决于任务的子步骤数量和语义粒度。对于更复杂的任务（如 20+ 子步骤），$N$ 可能需要增大，但过大的 $N$ 会导致：</p>
<ul>
<li>训练效率下降（每样本仍只激活 k=2 个专家，但更多专家竞争路由概率）</li>
<li>负载均衡更困难（样本分布更稀疏）</li>
<li>可能出现"专家碎片化"——两个专家学习几乎相同的功能</li>
</ul>
<p>论文未提供自动确定 $N$ 的方法，这是一个实际的部署障碍。</p>
</div>

<div class="callout warn">
<span class="callout-title">局限二：专家专门化的涌现无保证</span>
<p>专家按任务阶段自发专门化是一个<strong>涌现属性</strong>（emergent property），而非通过显式约束保证的。在以下情况下，专门化可能无法形成：</p>
<ul>
<li>任务阶段在观测空间中不可区分（如两个不同语义阶段产生完全相同的视觉模式）</li>
<li>训练数据分布极度不均衡（某个阶段的样本过多，导致路由器偏向该阶段的观测模式）</li>
<li>超参数 $\alpha$ 和 $\beta$ 设置不当，导致辅助损失与主损失的比例失衡</li>
</ul>
<p>论文未提供对"专门化失败"情况的系统分析或检测方法。</p>
</div>

<div class="callout warn">
<span class="callout-title">局限三：手动专家控制的局限性</span>
<p>推理时的专家手动控制虽然优雅，但有几个实际局限：</p>
<ul>
<li><strong>需要用户理解专家功能：</strong>用户必须知道每个专家对应什么技能，这需要预先进行专家功能分析（通过路由概率可视化）。对于新任务，这增加了部署成本。</li>
<li><strong>技能组合的泛化有限：</strong>技能重排只能在训练中<strong>出现过</strong>的技能之间进行。如果训练数据中从未出现"左手传递到右手"的动作，就无法通过组合现有专家来创造这个新技能。</li>
<li><strong>阶段检测依赖路由器质量：</strong>手动模式下，何时切换到下一个专家仍需某种机制来判断当前阶段是否完成。论文使用的简单规则（固定时间步数或手动切换）在动态环境中可能不够鲁棒。</li>
</ul>
</div>

<div class="callout warn">
<span class="callout-title">局限四：与语言条件策略的比较不足</span>
<p>论文将 MoE-DP 主要与无语言的 Diffusion Policy 比较，但对标当前 SOTA 的语言条件策略（如 RT-2、Octo）不够充分。语言条件策略通过自然语言指令也能实现任务分解和重排（"先抓杯子，再抓壶" vs "先抓壶，再抓杯子"），且具有更好的泛化到全新语义任务的能力。MoE-DP 的无监督阶段发现虽然优雅，但在极端泛化场景下可能不如语言监督有效。</p>
</div>

<div class="callout warn">
<span class="callout-title">局限五：硬件需求和实时性</span>
<p>MoE-DP 虽然参数量增加不大（仅增加了 N 个小 MLP），但推理时需要：</p>
<ul>
<li>ResNet-18 前向传播（两次，全局+腕部）</li>
<li>MoE 路由 + k 个专家前向传播</li>
<li>U-Net 去噪（100 步 DDIM）</li>
</ul>
<p>论文未报告端到端推理延迟。在实际部署中（尤其在 Franka 的 1kHz 控制环路上），这可能成为瓶颈。使用 TensorRT 优化或减少去噪步数可能是必要的工程优化。</p>
</div>

<h3>9.2 实验设计的潜在问题</h3>
<ul>
<li><strong>扰动协议的标准化不足：</strong>仿真中的扰动是自动化的（通过环境重置），但真实世界中的扰动是人为执行的，引入了不可控的变化（人为扰动的力度、时机、方式不完全一致）。</li>
<li><strong>成功率指标的单维度：</strong>仅报告成功率，未区分失败模式（是阶段检测失败、专家路由错误、还是动作生成质量差），限制了错误归因。</li>
<li><strong>训练数据规模的影响：</strong>未分析训练数据量对专家专门化质量的影响——在数据稀缺场景下，专门化可能无法充分涌现。</li>
</ul>
</section>

<!-- ===== 10. Motivation ===== -->
<section id="motivation">
<h2>10. Motivation</h2>

<h3>10.1 为什么这项工作重要？</h3>

<div class="callout info">
<span class="callout-title">现实需求驱动</span>
<p>当前机器人学习系统面临一个核心矛盾：<strong>模仿学习在单阶段短时序任务中表现出色（如抓取单个物体），但在多阶段长时序任务中性能急剧下降。</strong>家庭服务、工业装配、医疗辅助等真实场景几乎全部涉及多阶段操作——一个典型的"做早餐"任务包括"取出鸡蛋→打蛋→取锅→倒油→煎蛋→装盘"至少 6 个连续子任务，且任何一步失败都可能导致整体失败。</p>
<p>MoE-DP 瞄准了这个关键缺口：如何在<strong>不增加人工标注成本</strong>（无子任务标签）的前提下，让策略获得对长时序任务结构的<strong>隐式理解</strong>，并在面对扰动时展现出<strong>类人的恢复行为</strong>。</p>
</div>

<h3>10.2 方法论层面的贡献</h3>
<p>MoE-DP 不只是对 Diffusion Policy 的增量改进，它提出了一个更通用的范式：</p>
<ul>
<li><strong>从"更大的模型"到"更聪明的表示结构"：</strong>与其堆叠更多的 Transformer 层或增大模型规模，MoE-DP 通过引入<strong>结构化稀疏性</strong>（structured sparsity）来提升表示质量。这在计算效率上具有重要意义——仅增加约 5% 的参数量，获得 2-3 倍的成功率提升。</li>
<li><strong>从"端到端黑盒"到"可解释的阶段结构"：</strong>MoE 的路由概率 $g_t$ 提供了对策略内部决策过程的<strong>透明窗口</strong>。通过可视化 $g_t$ 随时间的变化，研究人员可以理解策略"认为"自己处于哪个阶段，这是传统端到端策略无法提供的诊断能力。</li>
<li><strong>从"训练时固定"到"推理时可控"：</strong>手动专家控制机制赋予了策略前所未有的灵活性——同一组训练权重可以适应不同的任务子序列，这为未来的"技能库 + 规划器"架构提供了基础构件。</li>
</ul>

<h3>10.3 与更广泛研究趋势的连接</h3>
<table>
<tr><th>研究趋势</th><th>MoE-DP 的定位</th></tr>
<tr><td><strong>大模型时代的机器人学习</strong>（RT-2, Octo, GR00T）</td><td>MoE-DP 提供了一条"小模型 + 结构化表示"的替代路径——不需要数十亿参数，通过精心设计的架构归纳偏置也能获得阶段感知和技能组合能力。</td></tr>
<tr><td><strong>Mixture of Experts 的复兴</strong>（Mixtral, DeepSeek-MoE）</td><td>将 MoE 从语言模型领域引入机器人操作，证明了稀疏激活在连续控制中的有效性。特别地，机器人操作中的 MoE 面临语言模型中不存在的挑战：输入是连续的高维感知信号而非离散 token，输出是物理动作而非概率分布。</td></tr>
<tr><td><strong>分层强化学习 / 选项框架</strong></td><td>MoE-DP 为选项框架提供了一个<strong>端到端可微的实现</strong>——路由器充当元控制器（选择选项/专家），专家充当子策略（执行选项）。但与传统分层 RL 不同，这里的选项是<strong>隐式发现</strong>的而非预定义的。</td></tr>
</table>

<h3>10.4 长期愿景</h3>
<p>MoE-DP 指向一个令人兴奋的方向：<strong>通过学习少量可重组的技能原语来实现对任意长时序任务的鲁棒操作。</strong>如果每个专家能被训练为执行一个语义原子的操作原语（如"抓取"、"放置"、"推"、"拉"、"旋转"等），那么通过组合这些原语，理论上可以解决任意复杂的操作任务。MoE-DP 证明了这种"组合泛化"在无监督条件下的雏形是可行的，为未来的通用操作智能体奠定了基础。</p>
</section>

<!-- ===== 11. Reading Takeaway ===== -->
<section id="takeaway">
<h2>11. Reading Takeaway</h2>

<h3>11.1 一句话总结</h3>
<div class="callout idea">
<p><strong>MoE-DP 在 Diffusion Policy 的视觉编码器与去噪网络之间插入稀疏 Mixture of Experts，通过负载均衡与熵正则的协同优化，让不同专家自发对应接近、抓取、运输、放置等任务阶段。阶段化表示使策略在扰动下能检测失败并重新执行当前阶段（仿真成功率从 17.8% 提升至 53.8%，真机从 28.0% 提升至 71.0%），且推理时可通过手动指定专家激活顺序实现零样本的子任务重排。</strong></p>
</div>

<h3>11.2 关键数字速记</h3>
<table>
<tr><th>指标</th><th>数值</th><th>备注</th></tr>
<tr><td>仿真平均成功率（扰动）</td><td>DP 17.8% vs MoE-DP 53.8%</td><td>+36 pp，相对提升约 200%</td></tr>
<tr><td>真机平均成功率（扰动）</td><td>DP 28.0% vs MoE-DP 71.0%</td><td>+43 pp，相对提升约 150%</td></tr>
<tr><td>专家数量 N</td><td>3-8 个（仿真 4-8，真机 3-4）</td><td>取决于任务复杂度</td></tr>
<tr><td>Top-k 激活</td><td>k=2</td><td>每样本仅计算 2 个专家，计算高效</td></tr>
<tr><td>MoE 额外参数量</td><td>~0.5M（N=4）</td><td>相比 DP 基线（约 40M），仅增加约 1.2%</td></tr>
<tr><td>训练演示数量</td><td>仿真 100-500 条，真机 100-200 条</td><td>与标准 DP 训练需求相同</td></tr>
<tr><td>技能重排成功率</td><td>45.2%（vs DP 基线 0%）</td><td>Coffee Preparation 任务的任务反转</td></tr>
</table>

<h3>11.3 技术要点清单</h3>
<ol>
<li><strong>MoE 插入位置：</strong>视觉编码器（ResNet-18）输出与去噪 U-Net 条件输入之间。此处是视觉语义向控制语义的转换界面，是注入结构化条件计算的最优位置。</li>
<li><strong>输入模态：</strong>全局相机（场景上下文）+ 腕部相机（精细操作）+ 关节状态（本体感知）。三模态拼接后投影到 256-d。</li>
<li><strong>路由机制：</strong>$g_t = \text{Softmax}(W_g \cdot z_t)$，Top-k=2 稀疏选择。仅激活概率最高的 2 个专家，其余梯度为零。</li>
<li><strong>专家结构：</strong>每个专家为 2-3 层 MLP（256→512→256），GELU 激活，独立参数。</li>
<li><strong>训练损失：</strong>$L = L_{diff} + 0.01 \cdot L_{load} + 0.005 \cdot L_{entropy}$。三项损失形成精巧制衡——无负载均衡则坍缩，无熵正则则无区分，两者权重不当则训练不稳定。</li>
<li><strong>推理灵活性：</strong>自动路由模式（常规推理）vs 手动专家控制模式（技能重排/失败恢复）。后者允许用户强制激活指定专家序列。</li>
<li><strong>关键消融结论：</strong>负载均衡损失最重要（移除后性能降 21 pp），熵正则其次（降 15 pp），Top-k=2 最优。</li>
</ol>

<h3>11.4 对研究者的启示</h3>
<ul>
<li><strong>结构化稀疏性值得投资：</strong>与其让模型更大，不如让表示更有结构。MoE 的 1.2% 额外参数带来了 200% 的性能提升，投资回报率极高。</li>
<li><strong>辅助损失设计是关键：</strong>$L_{load}$ 和 $L_{entropy}$ 看似简单，但其协同设计体现了对 MoE 失效模式的深刻理解。在将 MoE 应用于新领域时，类似的辅助损失通常是必要的。</li>
<li><strong>涌现属性需要验证而非假设：</strong>专家专门化是训练后观察到的，而非设计时保证的。将 MoE 应用于新任务时，务必通过路由概率可视化来验证专门化是否确实发生。</li>
<li><strong>真实世界验证增加了可信度：</strong>论文的仿真和真机结果高度一致（甚至真机提升幅度更大），这是方法鲁棒性的有力证据。</li>
</ul>

<h3>11.5 开放问题</h3>
<ol>
<li>能否基于路由概率 $g_t$ 自动检测阶段切换点，实现全自动的阶段分割和失败检测？</li>
<li>能否通过持续学习（continual learning）动态增加新专家，使策略在部署过程中不断获取新技能？</li>
<li>MoE 路由的稀疏性是否可以被利用来进行模型压缩（如推理时仅加载当前活跃的专家权重）？</li>
<li>能否将 MoE 的思想扩展到多机器人协作场景——每个机器人对应一组专家？</li>
<li>专家专门化的涌现是否可以通过对比学习（contrastive learning）等更主动的方式进行引导？</li>
</ol>

<p class="source">This page is grounded in the abstract, methods, experiments, and conclusion of the local PDF. Specific quantitative values shown here come from the paper rather than the filename.</p>
</section>

</main>
<footer>&#x1F4C4; Paper Notes &middot; Scholar &middot; Paper ID 10383 &middot; MathJax + Mermaid Rendering</footer>
</body></html>'''

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

file_size = os.path.getsize(OUTPUT_PATH)
print(f"note.html written to: {OUTPUT_PATH}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
print("Done.")
