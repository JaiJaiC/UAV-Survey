#!/usr/bin/env python3
"""Generate customized research dashboards from template for each lab."""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE = (SCRIPT_DIR / "_template.html").read_text(encoding="utf-8")

# ── Lab definitions ──
LABS = [
    {
        "short": "ETH-ASL",
        "full": "ETH Zurich — Autonomous Systems Lab",
        "accent": "#4da6ff",
        "accent_light": "#1a3a5c",
        "store_key": "eth_asl_papers",
        "header_links": [
            ("🌐 Website", "https://asl.ethz.ch/"),
            ("📂 GitHub", "https://github.com/ethz-asl"),
            ("▶️ YouTube", "https://www.youtube.com/@ethzasl"),
            ("📄 Publications", "https://asl.ethz.ch/publications.html"),
        ],
        "quick_searches": [
            "ETH Zurich autonomous drone",
            "Siegwart aerial robot",
            "model predictive control UAV",
            "ASL state estimation SLAM",
        ],
        "research_areas": "Autonomous aerial vehicles, Model predictive control, State estimation & SLAM, Multi-robot systems",
        "folder": "3.Lab/ETH-ASL",
    },
    {
        "short": "UZH-RPG",
        "full": "UZH — Robotics and Perception Group",
        "accent": "#c084fc",
        "accent_light": "#2d1530",
        "store_key": "uzh_rpg_papers",
        "header_links": [
            ("🌐 Website", "https://rpg.ifi.uzh.ch/"),
            ("📂 GitHub", "https://github.com/uzh-rpg"),
            ("▶️ YouTube", "https://www.youtube.com/@RoboticsPerceptionGroup"),
            ("📄 Publications", "https://rpg.ifi.uzh.ch/publications.html"),
        ],
        "quick_searches": [
            "Scaramuzza event camera drone",
            "agile drone flight deep learning",
            "neuromorphic vision robotics",
            "UZH RPG visual odometry",
        ],
        "research_areas": "Event-based vision, Agile drone flight, Deep learning for perception, Neuromorphic computing",
        "folder": "3.Lab/UZH-RPG",
    },
    {
        "short": "UPenn-Kumar",
        "full": "UPenn — Kumar Robotics / GRASP Lab",
        "accent": "#f97316",
        "accent_light": "#3d1f08",
        "store_key": "upenn_kumar_papers",
        "header_links": [
            ("🌐 Kumar Lab", "https://www.kumarrobotics.org/"),
            ("🎓 GRASP", "https://www.grasp.upenn.edu/"),
            ("📂 GitHub", "https://github.com/KumarRobotics"),
            ("📄 Publications", "https://www.kumarrobotics.org/publications/"),
        ],
        "quick_searches": [
            "Vijay Kumar micro aerial vehicle",
            "UPenn GRASP swarm robotics",
            "multi-robot coordination planning",
            "aerial manipulation UPenn",
        ],
        "research_areas": "Micro aerial vehicles, Multi-robot coordination, Control and planning, Swarm robotics",
        "folder": "3.Lab/UPenn-Kumar-GRASP",
    },
    {
        "short": "CMU-AirLab",
        "full": "CMU — AirLab (Autonomous Intelligent Robotics)",
        "accent": "#ff6b6b",
        "accent_light": "#3d1515",
        "store_key": "cmu_airlab_papers",
        "header_links": [
            ("🌐 Website", "https://theairlab.org/"),
            ("📂 GitHub", "https://github.com/castacks"),
            ("▶️ YouTube", "https://www.youtube.com/@AirLabCMU"),
            ("🐦 Twitter", "https://twitter.com/AirLabCMU"),
        ],
        "quick_searches": [
            "Sebastian Scherer autonomous aerial",
            "CMU AirLab field robotics",
            "multi-agent planning drone CMU",
            "airlab perception navigation UAV",
        ],
        "research_areas": "Autonomous aerial vehicles, Field robotics, Perception and planning, Multi-agent systems",
        "folder": "3.Lab/CMU-AirLab",
    },
    {
        "short": "MIT-ACL",
        "full": "MIT — Aerospace Controls Laboratory",
        "accent": "#4ade80",
        "accent_light": "#0f2e1d",
        "store_key": "mit_acl_papers",
        "header_links": [
            ("🌐 Website", "https://acl.mit.edu/"),
            ("📂 GitHub", "https://github.com/mit-acl"),
            ("📄 Publications", "https://acl.mit.edu/publications/"),
        ],
        "quick_searches": [
            "Jonathan How multi-agent MIT",
            "reinforcement learning aerospace UAV",
            "multi-robot planning coordination",
            "MIT ACL autonomous drone",
        ],
        "research_areas": "Multi-agent planning, RL for aerospace, Autonomous UAV systems, Air traffic control automation",
        "folder": "3.Lab/MIT-ACL",
    },
    {
        "short": "TU Delft-MAVLab",
        "full": "TU Delft — Micro Air Vehicle Laboratory",
        "accent": "#38bdf8",
        "accent_light": "#0c2d3d",
        "store_key": "tudelft_mavlab_papers",
        "header_links": [
            ("🌐 Website", "https://mavlab.tudelft.nl/"),
            ("📂 GitHub", "https://github.com/tudelft"),
            ("▶️ YouTube", "https://www.youtube.com/@MAVLabTUDelft"),
        ],
        "quick_searches": [
            "Guido de Croon bio-inspired drone",
            "MAVLab autonomous navigation",
            "neuromorphic AI robotics Delft",
            "swarm intelligence micro air vehicle",
        ],
        "research_areas": "Bio-inspired drones, Autonomous navigation, Swarm intelligence, Neuromorphic AI for robotics",
        "folder": "3.Lab/TUDelft-MAVLab",
    },
    {
        "short": "Imperial-ARL",
        "full": "Imperial College London — Aerial Robotics Lab",
        "accent": "#e879f9",
        "accent_light": "#2d1035",
        "store_key": "imperial_arl_papers",
        "header_links": [
            ("🌐 Aerial Robotics", "https://www.imperial.ac.uk/aerial-robotics"),
            ("🤖 Robotics", "https://www.imperial.ac.uk/robotics"),
        ],
        "quick_searches": [
            "Mirko Kovac aerial robotics",
            "bio-inspired flying robot",
            "soft robotics aerial vehicle",
            "multi-modal drone Imperial",
        ],
        "research_areas": "Bio-inspired aerial robots, Soft robotics for flight, Multi-modal aerial vehicles, Aerial manipulation",
        "folder": "3.Lab/Imperial-ARL",
    },
    {
        "short": "ZJU-FAST",
        "full": "ZJU — FAST Lab (Field Autonomous Systems & compuTing)",
        "accent": "#fbbf24",
        "accent_light": "#3b2f0e",
        "store_key": "zju_fast_papers",
        "header_links": [
            ("🌐 Website", "https://zju-fast-lab.github.io/"),
            ("📂 GitHub", "https://github.com/ZJU-FAST-Lab"),
            ("👤 Fei Gao", "https://feigao-robotics.com/"),
        ],
        "quick_searches": [
            "Fei Gao trajectory planning drone",
            "ego-planner swarm UAV ZJU",
            "FAST-LIO SLAM LiDAR ZJU",
            "aerial manipulation gripper drone",
        ],
        "research_areas": "Autonomous aerial robots, Motion planning (kinodynamic, trajectory optimization), Swarm systems, SLAM and perception, Flying gripper",
        "folder": "3.Lab/ZJU-FAST",
    },
    {
        "short": "BUAA-RFLY",
        "full": "BUAA — Reliable Flight Control Group (RFLY)",
        "accent": "#60a5fa",
        "accent_light": "#1e3a5f",
        "store_key": "buaa_rfly_papers",
        "header_links": [
            ("🌐 Website", "https://rfly.buaa.edu.cn/"),
            ("🔧 RflySim", "https://rflysim.com/"),
        ],
        "quick_searches": [
            "BUAA reliable flight control UAV",
            "RflySim UAV simulation platform",
            "fault-tolerant control drone",
            "UAV safety reliability testing",
        ],
        "research_areas": "Reliable flight control, UAV simulation (RflySim), Fault-tolerant control, UAV safety and reliability",
        "folder": "3.Lab/BUAA-RFLY",
    },
    {
        "short": "Unitree",
        "full": "宇树科技 — Unitree Robotics",
        "accent": "#34d399",
        "accent_light": "#0f2e1d",
        "store_key": "unitree_papers",
        "header_links": [
            ("🌐 Website", "https://www.unitree.com/"),
            ("📂 GitHub", "https://github.com/unitreerobotics"),
            ("▶️ YouTube", "https://www.youtube.com/@UnitreeRobotics"),
            ("📺 Bilibili", "https://space.bilibili.com/"),
        ],
        "quick_searches": [
            "Unitree humanoid locomotion H1",
            "quadruped robot reinforcement learning",
            "sim-to-real transfer legged robot",
            "embodied AI robot manipulation",
        ],
        "research_areas": "Legged robots & humanoids, RL for locomotion, Sim-to-real transfer, Embodied AI",
        "folder": "4.Company/Unitree",
    },
]


def generate_link_html(links):
    return "\n      ".join(
        f'<a href="{url}" target="_blank">{label}</a>'
        for label, url in links
    )


def generate_search_buttons(searches):
    return " | ".join(
        f'<button class="btn" style="font-size:0.78rem;padding:6px 12px;" onclick="document.getElementById(\'arxivQuery\').value=\'{kw}\';fetchArxiv()">{kw}</button>'
        for kw in searches
    )


def main():
    for lab in LABS:
        html = TEMPLATE
        html = html.replace("__LAB_SHORT_NAME__", lab["short"])
        html = html.replace("__LAB_FULL_NAME__", lab["full"])
        html = html.replace("__ACCENT_COLOR__", lab["accent"])
        html = html.replace("__ACCENT_LIGHT__", lab["accent_light"])
        html = html.replace("__LAB_STORE_KEY__", lab["store_key"])
        html = html.replace("__HEADER_LINKS__", generate_link_html(lab["header_links"]))
        html = html.replace("__QUICK_SEARCH_BUTTONS__", generate_search_buttons(lab["quick_searches"]))

        out_path = SCRIPT_DIR / lab["folder"] / "dashboard.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  ✅ {lab['folder']}/dashboard.html")

    print(f"\nDone! Generated {len(LABS)} dashboards.")


if __name__ == "__main__":
    main()
