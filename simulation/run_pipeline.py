"""End-to-end simulation pipeline for NobUniverse prototype (dependency-free)."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural.can_model import ContinuousAttractorNetwork
from structural.stage_h_graph import StageHGraph
from symbolic.nz_classifier import NZClassifier

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "system_config.json"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "run_logs.json"


def load_config(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def rolling_std(trajectory: List[List[float]]) -> float:
    window = trajectory[-5:]
    flattened = list(zip(*window))
    mean_vector = [sum(values) / len(values) for values in flattened]
    variance = 0.0
    count = 0
    for state in window:
        for val, mean in zip(state, mean_vector):
            variance += (val - mean) ** 2
            count += 1
    return (variance / (count or 1)) ** 0.5


def derive_geometry(attractor_state: Dict, structural_metrics: Dict) -> Dict[str, float]:
    lambda_ = attractor_state["lambda_synchrony"]
    delta_ = rolling_std(attractor_state["trajectory"]) if attractor_state.get("trajectory") else 0.0
    psi_ = float(structural_metrics.get("nodes", 0)) / (structural_metrics.get("edges", 1) + 1e-6)
    return {"lambda": lambda_, "delta": delta_, "psi": psi_}


def blend_connectivity(base: List[List[float]], bias: List[List[float]], rate: float = 0.1) -> List[List[float]]:
    blended = []
    for base_row, bias_row in zip(base, bias):
        blended.append([0.9 * b + rate * (b + br) for b, br in zip(base_row, bias_row)])
    return blended


def run_simulation(config: Dict) -> List[Dict]:
    random.seed(config["simulation"].get("seed", 0))
    neural_cfg = config["neural"]
    structural_cfg = config["structural"]

    network = ContinuousAttractorNetwork(**neural_cfg)
    stage_h = StageHGraph(size=neural_cfg["size"], **structural_cfg)
    classifier = NZClassifier(bandwidth=0.18)

    trajectories: List[Dict] = []
    for step in range(config["simulation"]["runs"]):
        stimulus = [random.uniform(-1, 1) for _ in range(neural_cfg["size"])]
        attractor_state = network.run(
            input_vector=stimulus,
            timesteps=config["simulation"]["timesteps"],
            connectivity_bias=stage_h.graph_to_matrix(),
        )

        structural_state = stage_h.update_structure(attractor_state.__dict__)
        geometry = derive_geometry(attractor_state.__dict__, structural_state.metrics)
        label = classifier.classify_state(geometry["lambda"], geometry["delta"], geometry["psi"])

        trajectories.append(
            {
                "step": step,
                "lambda": geometry["lambda"],
                "delta": geometry["delta"],
                "psi": geometry["psi"],
                "label": label,
                "stability": attractor_state.stability,
                "structural": structural_state.metrics,
            }
        )

        network.base_connectivity = blend_connectivity(network.base_connectivity, structural_state.connectivity_bias)

    return trajectories


def save_logs(logs: List[Dict]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as log_file:
        json.dump(logs, log_file, indent=2)


def main() -> None:
    config = load_config(CONFIG_PATH)
    logs = run_simulation(config)
    save_logs(logs)
    print(f"Saved {len(logs)} steps to {DATA_PATH}")


if __name__ == "__main__":
    main()
