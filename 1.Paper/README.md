# 1. Paper Deep Dive

Single-paper in-depth study and analysis. Each paper gets its own folder with:

- Original PDF
- Reading notes (`note.html`) — 11-section deep dive (info, insight, architecture, task, challenge, method, principles, figures, flaws, motivation, takeaways) rendered with MathJax + Mermaid
- Paper figures under `figures/` (`fig1.png` … `figN.png`), cropped from the PDF and interpreted one by one
- Related code or experiments (where applicable)

## Papers

| # | Paper | Venue | Folder | Figures | Status |
|---|-------|-------|--------|---------|--------|
| 00 | CoulombFly — Sunlight-powered sustained flight of an ultralight MAV | Nature 2024 | `0.Fracture/` | 4 | Notes |
| 01 | Image-Based Visual Servoing of Quadrotors to Arbitrary Flight Targets | IEEE RA-L 2023 | `1.Image-Based Visual Servoing of Quadrotors to Arbitrary Flight Targets/` | 13 | Notes |
| 02 | Actor-Critic Model Predictive Control | IEEE ICRA 2024 | `2.Actor-Critic Model Predictive Control/` | 5 | Notes |
| 03 | Learning Vision-Based Agile Flight via Differentiable Physics | Nature Machine Intelligence 2025 | `3.Learning vision-based agile flight via differentiable physics/` | 8 | Notes |
| 04 | High-Speed Interception Multicopter Control by Image-Based Visual Servoing | IEEE TCST 2025 | `4. High-Speed Interception Multicopter Control by Image-Based Visual Servoing/` | 13 | Notes |
| 05 | Perception-Aware Image-Based Visual Servoing of Aggressive Quadrotor UAVs | IEEE/ASME TMECH 2023 | `5. Perception-Aware Image-Based Visual Servoing of Aggressive Quadrotor UAVs/` | 11 | Notes |
| 06 | A Bearing-Angle Approach for Unknown Target Motion Analysis | arXiv 2024 | `6. A Bearing-Angle Approach for Unknown Target Motion Analysis Based on Visual Measurements/` | 13 | Notes |
| 07 | Flexible multi-UAV formation control via DRL and affine transformations | Aerospace Science and Technology 2025 | `Flexible multi-UAV formation control via integrating deep reinforcement learning and affine transformations/` | 16 | Notes + code |
| 08 | Learning Agile Intruder Interception using Differentiable Quadrotor Dynamics | arXiv 2026 | `Learning Agile Intruder Interception using Differentiable Quadrotor Dynamics/` | 10 | Notes |
| 09 | OpenFlight — Learning minimum-time flight control for fixed-wing UAVs | Journal of Automation and Intelligence 2025 | `OpenFlight/` | 6 | Notes + code |
| 10 | DiffAero — A GPU-Accelerated Differentiable Simulation Framework for Quadrotor Policy Learning | IEEE RA-L 2025 (arXiv 2509.10247) | `Diffaero/` | 1 | Notes + code |
| 11 | VisFly — An Efficient and Versatile Simulator for Training Vision-based Flight | arXiv 2024 (2407.14783) | `VisFly/` | 4 | Notes + code |
| 12 | Model-Free vs. Model-Based RL for Fixed-Wing UAV Attitude Control Under Varying Wind | ICINCO 2024 (JSBSim framework: FW-JSBGym) | `FW-JSBGym/` | 0 | Notes + code |
| 13 | YOPO — You Only Plan Once: A Learning-Based One-Stage Planner With Guidance Learning | IEEE RA-L 2024 | `YOPO/` | 2 | Notes + code |
| 14 | NavRL — Learning Safe Flight in Dynamic Environments | IEEE RA-L 2025 (arXiv 2409.15634) | `NavRL/` | 6 | Notes + code |
| 15 | NeuralPlane — An Efficiently Parallelizable Platform for Fixed-Wing Aircraft Control with RL | NeurIPS 2024 (D&B Track) | `Neuralplane/` | 5 | Notes + code |

## Themes

The collection is organised around four threads that keep recurring in the notes:

1. **Visual servoing / bearing-only interception** (01, 04, 05, 06, 08) — what can be done with a monocular camera alone, how to handle latency and field-of-view, and how observability changes when bearing is augmented with a bearing angle.
2. **Learning-based flight with differentiable physics** (02, 03, 08, 14) — analytic policy gradients vs. model-free RL, model fidelity (point mass vs. full rigid body), safety shielding, sim-to-real.
3. **Aerial platforms and multi-agent systems** (00, 07, 09) — ultralight solar MAV, formation control, and high-fidelity fixed-wing simulation.
4. **Simulators, benchmarks and learned planners** (10, 11, 12, 13, 15) — GPU-parallel differentiable physics and rendering, high-throughput vision-based training, JSBSim-based fixed-wing RL, one-stage learned planning, and `10^6`-agent parallel FDM benchmarks. Every folder in this thread ships a runnable code repository.

## Adding a new paper

1. Create `1.Paper/<Paper Title>/` with the PDF.
2. Add `note.html` (copy the head/CSS of an existing note, then write the 11 sections) and `figures/figN.png`.
3. Add a card to `index.html` and a row to the table above.
