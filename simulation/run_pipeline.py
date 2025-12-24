"""End-to-end simulation pipeline for the NobUniverse hybrid architecture."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from random import Random
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from neural.can_model import ContinuousAttractor
from structural.stage_h_graph import StageHGraph
from symbolic.nz_classifier import NZClassifier

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "system_config.json"
LOG_PATH = Path(__file__).resolve().parents[1] / "data" / "run_logs.json"


def load_config(path: Path = CONFIG_PATH) -> Dict:
    with path.open() as f:
        return json.load(f)


def generate_input(prev: List[float], rng: Random, scale: float, drift: float) -> List[float]:
    noise = [rng.gauss(0.0, scale) for _ in prev]
    drift_vector = [rng.gauss(0.0, drift) for _ in prev]
    return [0.8 * p + n + d for p, n, d in zip(prev, noise, drift_vector)]


def extract_lambda_delta_psi(attractor_state, structural_state) -> Dict[str, float]:
    lambda_ = attractor_state.synchrony
    delta_ = structural_state.structural_delta
    psi_ = attractor_state.stability
    return {"lambda": float(lambda_), "delta": float(delta_), "psi": float(psi_)}


def run_pipeline() -> List[Dict]:
    config = load_config()
    rng = Random(config.get("seed"))

    neural_cfg = config.get("neural", {})
    structural_cfg = config.get("structural", {})
    sim_cfg = config.get("simulation", {})

    input_size = neural_cfg.get("size", 16)
    initial_input = [rng.gauss(0.0, sim_cfg.get("input_scale", 0.5)) for _ in range(input_size)]

    attractor = ContinuousAttractor(
        size=input_size,
        leak=neural_cfg.get("leak", 0.1),
        noise_level=neural_cfg.get("noise", 0.02),
        recurrent_scale=neural_cfg.get("recurrent_scale", 1.0),
        seed=config.get("seed"),
    )
    structure = StageHGraph(seed=config.get("seed"), **structural_cfg)
    classifier = NZClassifier()

    steps = sim_cfg.get("steps", 20)
    logs: List[Dict] = []
    current_input = initial_input

    for step in range(steps):
        attractor_result = attractor.run_attractor(current_input, neural_cfg.get("timesteps", 50))

        structural_state = structure.update_structure(
            {"stability": attractor_result.stability, "synchrony": attractor_result.synchrony}
        )

        attractor.adjust_recurrence(structural_state.connectivity_scale)

        lambda_delta_psi = extract_lambda_delta_psi(attractor_result, structural_state)
        label_state = classifier.classify_state(
            lambda_delta_psi["lambda"], lambda_delta_psi["delta"], lambda_delta_psi["psi"]
        )

        log_entry = {
            "step": step,
            "lambda": lambda_delta_psi["lambda"],
            "delta": lambda_delta_psi["delta"],
            "psi": lambda_delta_psi["psi"],
            "label": label_state.label,
            "stability": float(attractor_result.stability),
            "synchrony": float(attractor_result.synchrony),
            "structural_metrics": structural_state.metrics,
        }
        logs.append(log_entry)

        current_input = generate_input(
            attractor_result.final_state,
            rng,
            sim_cfg.get("input_scale", 0.5),
            sim_cfg.get("input_drift", 0.1),
        )

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("w") as f:
        json.dump({"trajectory": logs}, f, indent=2)

    return logs


if __name__ == "__main__":
    run_pipeline()
    print(f"Logged simulation to {LOG_PATH}")
