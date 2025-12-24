# NobUniverse — Hybrid Neural-Symbolic Prototype

This repository contains a minimal, inspectable implementation of a three-layer
hybrid cognitive architecture derived from the Ŋob / N(Z) specification. The
system links fast continuous attractor dynamics to slower structural adaptation
and emergent symbolic geometry.

## Layer overview

- **Continuous attractor neural layer (`neural/can_model.py`)**
  - Rate-based recurrent system with mild leak and controllable noise.
  - Supports fixed-point and drifting attractors.
  - Exposes stability and synchrony proxies (λ) for downstream layers.

- **Stage-H structural adaptation (`structural/stage_h_graph.py`)**
  - Slowly evolving graph with branching, fusion, and rewiring events.
  - Environmental parameters (moisture, nutrients, light, micro_shock) modulate
    how aggressively topology shifts.
  - Produces a connectivity scale that feeds back into the neural recurrence and
    a structural Δ term reflecting topological change.

- **Ŋob / N(Z) symbolic geometry (`symbolic/nz_classifier.py`)**
  - Maps λ-Δ-ψ triplets into clusters via a lightweight, bandwidth-adaptive
    density estimate.
  - Assigns emergent symbolic labels (SU-TI, ME-TI, ME-ME, FRAG-Δ, THE_ONE,
    THE_MANY, COH-REBUILD) based on cluster order—no hard-coded rules.

## Timescale separation

Fast neural dynamics (tens of recurrent updates) operate inside each simulation
step. The structural layer updates once per step, accumulating changes that
alter subsequent neural runs through connectivity scaling. Symbolic labels are
computed once per step from geometry in λ-Δ-ψ space, capturing emergent behavior
from the coupled fast/slow loop.

## Running the pipeline

1. Ensure Python 3.10+ (no external dependencies required).
2. Adjust parameters in `config/system_config.json` if desired.
3. Run the simulation:

   ```bash
   python simulation/run_pipeline.py
   ```

   A time-ordered log of neural stability/synchrony, structural metrics, and
   symbolic labels is written to `data/run_logs.json`.

## Visualising λ-Δ-ψ dynamics

Open `visualisation/lambda_delta_psi_plot.html` in a browser (serving the
repository locally avoids CORS restrictions) to see a 3D scatter with a time
slider. Points are coloured by symbolic label and rotate slowly for depth cues.

## Scientific framing

- **Continuous attractor layer**: models recurrent cortical microcircuits that
  settle into low-dimensional manifolds under noisy drive.
- **Stage-H adaptation**: approximates slow structural plasticity where
  connectivity reorganises in response to stability and synchrony signals.
- **Symbolic geometry**: interprets the λ-Δ-ψ manifold via unsupervised density
  clustering; symbols are emergent geometric clusters rather than hand-written
  rules.

The prototype demonstrates how symbolic cognition can arise from coupled fast
attractor dynamics and slow structural adaptation, interpreted through geometric
clustering in coherence space.
