# UAV-Survey 架构技术文档

> **版本**: v2.0 | **更新**: 2026-07-22 | **维护者**: JaiJaiC

---

## 目录

1. [项目概述](#1-项目概述)
2. [层级架构](#2-层级架构)
3. [目录结构](#3-目录结构)
4. [子系统详解](#4-子系统详解)
5. [数据流与自动化](#5-数据流与自动化)
6. [模板与样式体系](#6-模板与样式体系)
7. [如何添加新内容](#7-如何添加新内容)
8. [技术栈与依赖](#8-技术栈与依赖)
9. [协议、版权与合规](#9-协议版权与合规)
10. [维护清单](#10-维护清单)

---

## 1. 项目概述

UAV-Survey 是一个**个人学术研究追踪系统**，用于系统化管理无人机（UAV）与机器人领域的论文阅读笔记、学者追踪、实验室动态监控、公司技术跟踪和竞赛资料。

### 核心设计理念

- **静态HTML优先**：所有页面为纯静态HTML，无需服务器端渲染，可直接通过文件系统或任何HTTP服务器访问
- **去中心化架构**：每个子系统独立维护，通过相对路径链接形成整体
- **模板驱动**：统一的CSS/HTML模板确保样式一致性
- **自动化辅助**：Python脚本负责批量操作（论文爬取、RSS监控、格式升级）
- **本地优先**：所有数据存储在本地文件系统中，PDF论文作为一手证据

---

## 2. 层级架构

```
                        ┌─────────────────────────────┐
                        │     index.html (总入口)       │
                        │  search.html (全局搜索)        │
                        │  track.py (研究追踪器)         │
                        └─────────────┬───────────────┘
                                      │
        ┌─────────┬─────────┬─────────┼─────────┬─────────┬─────────┐
        ▼         ▼         ▼         ▼         ▼         ▼         ▼
   ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
   │1.Paper  ││2.Scholar││ 3.Lab   ││4.Company││5.UAV    ││6.Compe- ││7.Tools  │
   │深度论文  ││学者追踪  ││实验室追踪││企业追踪  ││Field    ││tition   ││工具资料  │
   └────┬────┘└────┬────┘└────┬────┘└────┬────┘│领域综述  ││竞赛资料  │└─────────┘
        │         │         │         │        └─────────┘└─────────┘
   ┌────▼────┐┌───▼────┐┌───▼────┐┌───▼────┐
   │note.html││Scholar ││  Lab   ││Company │
   │(每篇论文 ││index   ││dashboard││index   │
   │ 独立笔记)││+ files/││+ RSS   ││+ papers│
   └─────────┘│  index ││  爬取   ││  .json │
              └────────┘└────────┘└────────┘
```

### 数据流向

```
外部数据源                     本地处理                         展示层
─────────────────────────────────────────────────────────────────
arXiv API ──→ track.py ──→ reports/*.md (周报)
RSS Feeds ──→ crawl脚本 ──→ 3.Lab/*/papers.json ──→ search.html
Google Scholar ──→ 手动整理 ──→ 2.Scholar/*/index.html
PDF论文 ──→ Agent辅助 ──→ 2.Scholar/*/files/*/index.html (深度笔记)
GitHub API ──→ track.py ──→ 活动监控
```

---

## 3. 目录结构

```
UAV-Survey/
│
├── index.html                 # 🏠 总入口：7大板块导航 + 拖拽排序
├── search.html                # 🔍 全局论文搜索引擎
├── ARCHITECTURE.md            # 📋 本文档
├── track.py                   # 🤖 研究追踪器 (arXiv + GitHub)
├── last_updated.json          # 📊 统计元数据
│
├── 1.Paper/                   # 📄 深度论文笔记 (精选精读)
│   ├── 0.Fracture/            #    模板参考：CoulombFly (Nature 2024)
│   │   ├── note.html          #       ← 所有2.Scholar笔记的模板源头
│   │   └── figures/           #       论文图表截图
│   ├── 1.Image-Based Visual Servoing.../
│   ├── 2.Actor-Critic Model Predictive Control/
│   └── ...                    #    共 ~9 篇精选深度论文
│
├── 2.Scholar/                 # 👤 学者论文笔记库 (核心)
│   ├── Chao Yan/              #    以学者为单位的文件夹
│   │   ├── index.html         #      学者首页 (Chao Yan风格)
│   │   └── files/             #      论文笔记目录
│   │       ├── 5476/          #        每篇论文一个子目录
│   │       │   ├── index.html #          论文深度笔记 (~60-90KB)
│   │       │   ├── *.pdf      #          论文PDF (一手证据)
│   │       │   └── figures/   #          图表截图
│   │       └── ...
│   ├── Fei Gao/
│   ├── Vijay Kumar/
│   └── ...                    #    共 16 位学者
│
├── 3.Lab/                     # 🏛️ 大学实验室追踪
│   ├── index.html             #    实验室总览页
│   ├── ETH-ASL/               #    ETH Autonomous Systems Lab
│   │   ├── dashboard.html     #      动态仪表盘
│   │   └── papers.json        #      爬取论文数据
│   ├── UZH-RPG/
│   ├── ZJU-FAST/
│   └── ...                    #    共 9 个实验室
│
├── 4.Company/                 # 🏢 企业技术追踪
│   ├── index.html             #    企业总览页
│   ├── DJI/
│   ├── Unitree/
│   ├── Skydio/
│   └── ...                    #    共 14 家公司
│
├── 5.UAV Field/               # 📚 UAV领域综述
│   ├── Anti-UAV/
│   ├── Swarm Intelligence/
│   └── UAV+RL/
│
├── 6.Competition/             # 🏆 竞赛资料
│   ├── RoboCup无人机挑战赛/
│   └── 中国研究生未来飞行器创新大赛/
│
├── 7.Tools/                   # 🔧 工具资料
│
└── reports/                   # 📊 自动生成周报
    └── report-YYYY-MM-DD.md
```

---

## 4. 子系统详解

### 4.1 总入口 (`index.html`)

**功能**：7大板块导航，拖拽排序卡片，实时时钟

**技术特点**：
- HTML5 Drag & Drop API 实现卡片排序
- localStorage 持久化用户排序偏好
- 动态加载 Scholar 卡片（从内嵌JSON渲染）
- 深色主题 (dark mode)，CSS变量体系

**关键代码段**：
- `data-sortable` 属性标记可排序网格
- `draggable-card` 类启用拖拽
- `initDragAndDrop()` 函数处理拖拽事件

### 4.2 论文笔记 (`1.Paper/` + `2.Scholar/*/files/`)

**模板标准** (以 `1.Paper/0.Fracture/note.html` 为基准)：

每个论文笔记包含 **11个固定章节**：

| # | 章节 | 内容要求 |
|---|------|----------|
| 1 | 论文信息 | 标题、作者、机构、期刊/会议、DOI、TL;DR、标签 |
| 2 | 核心洞察与创新点 | Q&A式核心洞察 + 灵感映射表 + 3张创新卡片 |
| 3 | 系统架构 | 架构面板 + 2-3个Mermaid流程图 |
| 4 | 任务定义 | LaTeX公式形式化 + 输入/输出表 |
| 5 | 核心挑战 | 第一性原理诊断 + 先前方法对比表 |
| 6 | 关键方法 | 3-4组LaTeX公式 + 参数表 + 对比框 |
| 7 | 基本原理 | 2-3个深层机制解释 + 对比表 |
| 8 | 论文图表 | 图表解读 + figures/占位 |
| 9 | 缺陷与扩展 | 局限性 + 扩展方向 + 数据敏感度表 |
| 10 | 动机推导 | 5步推导链 + 一句话动机 |
| 11 | 核心收获 | 经验教训 + UAV研究应用 + 关键参考文献 |

**样式规范**：
- MathJax 3 渲染LaTeX公式 (`$$...$$`, `$...$`)
- Mermaid 10 渲染流程图
- 7种彩色标签 (blue/green/amber/purple/red/cyan/gray)
- 5种callout框 (info/tip/warn/danger/idea)
- 响应式设计 (max-width: 1100px)
- 中英混杂：章节标题/分析用中文，论文名/公式/术语保留英文

### 4.3 学者追踪 (`2.Scholar/`)

**两层结构**：
1. **学者首页** (`scholar/index.html`)：Chao Yan风格，包含Abstract、统计面板、研究路线图、论文卡片网格
2. **论文笔记** (`scholar/files/XXXX/index.html`)：完整11章节笔记

**series-nav**：每篇论文笔记顶部有学者内导航栏，可在该学者所有论文间快速跳转

**特殊处理**：
- NUDT同事（Chao Yan, Xiangke Wang, Yirui Cong, Guanzheng Wang, Zhihong Liu）：不包含Abstract
- 无笔记学者（Boyu Zhou, Kaiming He, Shaojie Shen, Ángel Romero）：显示占位状态

### 4.4 实验室追踪 (`3.Lab/`)

**数据来源**：
- 各实验室的 `papers.json`（由爬虫自动生成）
- RSS feed 监控
- 手动添加的重要论文

**页面层级**：
- `3.Lab/index.html` — 总览页（大卡片 + 实验室介绍）
- `3.Lab/{Lab}/dashboard.html` — 各实验室独立仪表盘
- `3.Lab/{Lab}/papers.json` — 论文数据

### 4.5 企业追踪 (`4.Company/`)

14家公司，分类为：
- **Drones**: DJI, Skydio, Autel, Parrot, Quantum Systems, JOUAV, XAG
- **Robotics**: Unitree
- **Defense**: Anduril, Shield AI, AeroVironment
- **Delivery/UAM**: EHang, Wing, Zipline

### 4.6 搜索系统 (`search.html`)

**数据源**：从各Lab/Company/UAV Field目录加载 `papers.json`

**功能**：
- 全文搜索（标题、作者、摘要、标签）
- 多维度筛选（实验室、期刊/会议、CCF等级、CAS分区、年份）
- 多种排序（最新、质量分、引用数、标题）
- Badge可视化（CCF等级、CAS分区、IF影响因子、引用数）

---

## 5. 数据流与自动化

### 5.1 研究追踪器 (`track.py`)

```
python track.py --days 14 -o reports/report-$(date +%Y-%m-%d).md
```

- 查询 arXiv API：按关键词检索各实验室/公司的最新论文
- 查询 GitHub API：监控组织和仓库的最新活动
- 生成Markdown周报

### 5.2 批量脚本体系

| 脚本用途 | 典型操作 |
|----------|----------|
| CSS/JS基础设施注入 | 为缺失MathJax/Mermaid的文件添加CDN脚本和模板CSS |
| 结构修复 | 修复minified HTML、统一container/nav/HOME按钮 |
| IF/期刊标注 | 匹配期刊数据库，为每篇论文添加IF/分区badge |
| 重命名迁移 | note.html → index.html 批量重命名 + 链接更新 |
| 学者首页生成 | 统一生成Chao Yan风格的学者index.html |

### 5.3 Agent辅助

使用Claude Agent进行：
- 论文PDF深度阅读 + 笔记生成
- 全英文笔记中文化翻译
- 内容质量增强（补充缺失的分析章节）

---

## 6. 模板与样式体系

### 6.1 CSS变量体系

**总入口深色主题**：
```css
--bg:#0f1117; --bg-card:#1a1d27; --text:#e1e4ea;
--text-dim:#8b8fa3; --border:#2a2d3a;
```

**论文笔记浅色主题**：
```css
--bg:#f8f9fb; --surface:#ffffff; --border:#e2e5ea;
--text:#1a1d23; --text-secondary:#5f6b7a;
```

### 6.2 色彩系统

- `accent-blue` (ETH-ASL), `accent-purple` (UZH-RPG), `accent-orange` (UPenn/DJI)
- 标签：`.tag-blue`, `.tag-green`, `.tag-amber`, `.tag-purple`, `.tag-red`, `.tag-cyan`, `.tag-gray`
- IF badge: `.if-q1` (绿色), `.if-q2` (黄色), `.if-q3` (橙色), `.if-q4` (红色)

### 6.3 响应式断点

- 总入口：`@media (max-width: 768px)` → 单列布局
- 论文笔记：`@media (max-width: 800px)` → hero单列
- 学者首页：`@media (max-width: 800px)` → hero + roadmap 单列

---

## 7. 如何添加新内容

### 添加新学者

1. 在 `2.Scholar/` 下创建 `{Name}/` 目录
2. 创建 `files/` 子目录
3. 运行 `regenerate_all_index.py` 生成学者首页
4. 在 `index.html` 的 `scholars` 数组中添加条目

### 添加新论文笔记

1. 在 `2.Scholar/{Scholar}/files/` 下创建数字ID目录
2. 放入论文PDF
3. 复制 `1.Paper/0.Fracture/note.html` 作为模板
4. 填充11个章节内容（可借助Agent辅助）
5. 重命名为 `index.html`

### 添加新实验室

1. 在 `3.Lab/` 下创建目录
2. 创建 `dashboard.html` 和 `papers.json`
3. 在 `3.Lab/index.html` 和总 `index.html` 中添加卡片

### 更新已有笔记

使用 `enrich_papers.py` 脚本批量更新IF/期刊标注。

---

## 8. 技术栈与依赖

| 组件 | 技术 | 说明 |
|------|------|------|
| 页面渲染 | 纯静态HTML5 + CSS3 | 无框架依赖 |
| 数学公式 | MathJax 3 (CDN) | `tex-chtml.js` |
| 流程图 | Mermaid 10 (CDN) | `mermaid.min.js` |
| 搜索 | 原生JavaScript fetch API | 加载本地JSON |
| 拖拽排序 | HTML5 Drag & Drop API | localStorage持久化 |
| 批量处理 | Python 3 | 文件操作、正则、JSON |
| 外部数据 | arXiv API, GitHub API | 通过 track.py |
| 字体 | 系统原生字体栈 | `-apple-system, "Noto Sans SC"` |

### CDN依赖
```
cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js
cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js
```

---

## 9. 协议、版权与合规

### 9.1 代码许可

本项目为**个人学术用途**（Personal Academic Use）。所有HTML/CSS/JavaScript代码为原创编写。

### 9.2 论文PDF

**重要法律声明**：

- 本项目中存储的论文PDF文件仅供**个人学术研究和学习**使用
- 所有论文版权归原作者和出版机构所有
- PDF文件通过合法渠道获取（arXiv开放获取、作者主页、机构订阅）
- **不得**将PDF文件公开发布、商业分发或用于任何侵犯版权的用途
- 如需引用，请直接访问出版社官方DOI链接

### 9.3 arXiv 论文

arXiv上的论文遵循arXiv的使用条款：
- 多数论文为开放获取（Open Access）
- 允许个人下载和学术引用
- 引用时应标注arXiv ID和官方链接

### 9.4 付费期刊论文 (IEEE, Springer, Elsevier等)

- 仅存储通过**机构订阅**合法获取的PDF
- 这些PDF**不应**被公开分享或上传至公共仓库
- 建议在 `.gitignore` 中排除PDF文件：
  ```
  **/*.pdf
  ```
- 笔记HTML文件仅包含论文的**分析性内容**（原创），不包含论文全文

### 9.5 图片与图表

- `figures/` 目录中的截图为论文原图
- 使用受**合理使用 (Fair Use)** 原则保护：用于学术评论和批评
- 每张图片标注来源（论文Figure编号）
- 如版权方要求移除，将立即删除

### 9.6 商标与名称

- 公司名称（DJI, Unitree, Skydio等）为其各自所有者的商标
- 实验室名称（ETH-ASL, UZH-RPG等）为其所属大学的名称
- 本项目仅用于**学术参考和追踪**，不暗示任何背书或关联

### 9.7 第三方API使用

- **arXiv API**: 免费开放，无API密钥要求，请求间隔>1秒
- **GitHub API**: 免费层级，可选Token提升限额
- **Google Scholar**: 仅存储公开链接，不进行大规模爬取

### 9.8 推荐做法

1. **不要将PDF文件加入Git**：在 `.gitignore` 中添加 `**/*.pdf`
2. **使用相对路径**：确保项目可移植
3. **标注来源**：每篇笔记标注DOI和arXiv链接
4. **尊重robots.txt**：自动化脚本遵守网站的爬取规则
5. **定期审查**：移除不再需要的版权内容

### 9.9 Disclaimer

```
本项目 (UAV-Survey) 是一个个人学术研究追踪工具。
所有论文版权归原作者和出版机构所有。
论文PDF文件仅供个人学习使用，不应公开发布。
如需使用论文内容，请通过官方渠道获取并正确引用。
```

---

## 10. 维护清单

### 每周
- [ ] 运行 `track.py --days 7` 生成周报
- [ ] 检查RSS爬取是否正常

### 每月
- [ ] 添加新发表的论文笔记
- [ ] 更新学者信息（Google Scholar、主页链接）
- [ ] 检查外部链接是否有效

### 每季度
- [ ] 审查并更新期刊IF数据
- [ ] 备份整个项目目录
- [ ] 清理过时的临时文件

### 架构调整时
- [ ] 先在测试学者上验证脚本
- [ ] 备份 `2.Scholar/` 目录
- [ ] 运行批量脚本后逐学者检查
- [ ] 确保总入口index.html链接正确

---

> **文档维护**: 架构变更时同步更新本文档。最后更新: 2026-07-22
