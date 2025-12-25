# Nob Universe — Hybrid Neural-Symbolic Prototype

This repository demonstrates how symbolic transitions can emerge from coupled fast attractor dynamics and slow structural adaptation interpreted through geometric clustering. The goal is scientific inspectability rather than performance.

## Architecture overview

- **Continuous Attractor Layer (fast):** A rate-based recurrent field on a ring topology (`neural/can_model.py`). Fixed-point and drifting attractors are shaped by a soft structural bias.
- **Stage-H Structural Layer (slow):** A mutable graph whose branching, fusion, and micro-shock operations adjust effective connectivity over longer timescales (`structural/stage_h_graph.py`).
- **Ŋob / N(Z) Symbolic Geometry (emergent):** Points in (λ, Δ, ψ) coherence space are clustered and mapped to emergent labels (`symbolic/nz_classifier.py`) without hand-written symbolic rules.

Timescale separation is explicit: neural dynamics settle within tens of simulation steps, while structural updates happen once per episode and accumulate slowly. Symbol assignment happens only after geometry is inferred from both layers.

## Running the pipeline

1. Ensure Python 3.10+ is available (standard library only).
2. Execute the end-to-end loop:

   ```bash
   python simulation/run_pipeline.py
   ```

   This produces `data/run_logs.json` containing λ-Δ-ψ trajectories, stability metrics, and symbolic labels.

3. Open `visualisation/lambda_delta_psi_plot.html` in a browser to inspect the 3D projection. Use the slider to walk through symbolic transitions over time.

## Interpretation

- **λ (lambda synchrony):** A proxy for network coherence derived from the spread of activity after attractor convergence.
- **Δ (delta variability):** Short-horizon variability of the attractor trajectory reflecting local stability.
- **ψ (psi structural ratio):** A structural ratio of nodes to edges, capturing the current Stage-H topology.
- **Labels:** Assigned by clustering λ-Δ-ψ points (MeanShift) and ordering cluster centroids, allowing labels such as `SU-TI`, `ME-ME`, `FRAG-Δ`, `THE_ONE`, `THE_MANY`, and `COH-REBUILD` to emerge from geometry rather than rules.

Structural mutations feed back into the neural layer through a connectivity bias matrix, altering future attractor stability. The system demonstrates how symbolic cognition can appear when fast neural settling is continually perturbed by slower topological change and then interpreted geometrically.
