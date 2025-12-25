"""Continuous Attractor Network implementation without external dependencies."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AttractorState:
    trajectory: List[List[float]]
    final_state: List[float]
    stability: float
    lambda_synchrony: float


class ContinuousAttractorNetwork:
    def __init__(
        self,
        size: int = 48,
        dt: float = 0.05,
        noise_std: float = 0.01,
        baseline_connectivity_strength: float = 1.2,
        structural_influence: float = 0.25,
    ) -> None:
        self.size = size
        self.dt = dt
        self.noise_std = noise_std
        self.baseline_connectivity_strength = baseline_connectivity_strength
        self.structural_influence = structural_influence
        self.base_connectivity = self._build_ring_connectivity()

    def _build_ring_connectivity(self) -> List[List[float]]:
        positions = [2 * math.pi * i / self.size for i in range(self.size)]
        weights = [[0.0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    continue
                distance = abs(math.sin(0.5 * (positions[i] - positions[j])))
                weights[i][j] = math.exp(-(distance**2) / 0.15)
        for i in range(self.size):
            total = sum(weights[i]) or 1e-9
            weights[i] = [self.baseline_connectivity_strength * w / total for w in weights[i]]
        return weights

    def _matvec(self, matrix: List[List[float]], vector: List[float]) -> List[float]:
        return [sum(mij * vj for mij, vj in zip(mi, vector)) for mi in matrix]

    def run(
        self, input_vector: List[float], timesteps: int, connectivity_bias: Optional[List[List[float]]] = None
    ) -> AttractorState:
        if len(input_vector) != self.size:
            raise ValueError(f"Input vector size {len(input_vector)} does not match network size {self.size}.")

        weight_matrix = [row[:] for row in self.base_connectivity]
        if connectivity_bias is not None:
            for i in range(self.size):
                for j in range(self.size):
                    bias = max(min(connectivity_bias[i][j], 1.0), -1.0)
                    weight_matrix[i][j] += self.structural_influence * bias

        state = [0.0 for _ in range(self.size)]
        trajectory: List[List[float]] = []

        for _ in range(timesteps):
            recurrent_drive = self._matvec(weight_matrix, state)
            next_state: List[float] = []
            for drive, stimulus in zip(recurrent_drive, input_vector):
                noise = random.gauss(0.0, self.noise_std)
                pre_activation = drive + stimulus + noise
                updated = state[len(next_state)] + self.dt * (-state[len(next_state)] + math.tanh(pre_activation))
                next_state.append(updated)
            state = next_state
            trajectory.append(state[:])

        stability = 0.0
        if timesteps >= 5:
            avg_recent = [sum(values) / len(values) for values in zip(*trajectory[-5:])]
            diff = math.sqrt(sum((trajectory[-1][i] - avg_recent[i]) ** 2 for i in range(self.size)))
            stability = 1.0 / (1.0 + diff)

        mean_activity = sum(state) / len(state)
        global_activity = [x - mean_activity for x in state]
        variance = sum(g**2 for g in global_activity) / len(global_activity)
        lambda_synchrony = 1.0 - math.sqrt(variance)

        return AttractorState(
            trajectory=trajectory,
            final_state=state,
            stability=stability,
            lambda_synchrony=lambda_synchrony,
        )


def run_attractor(input_vector: List[float], timesteps: int, **kwargs: Dict) -> AttractorState:
    network = ContinuousAttractorNetwork(
        size=kwargs.get("size", 48),
        dt=kwargs.get("dt", 0.05),
        noise_std=kwargs.get("noise_std", 0.01),
        baseline_connectivity_strength=kwargs.get("baseline_connectivity_strength", 1.2),
        structural_influence=kwargs.get("structural_influence", 0.25),
    )
    connectivity_bias = kwargs.get("connectivity_bias")
    return network.run(input_vector=input_vector, timesteps=timesteps, connectivity_bias=connectivity_bias)


__all__ = ["AttractorState", "ContinuousAttractorNetwork", "run_attractor"]
