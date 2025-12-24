"""Continuous attractor network implementation (dependency-free)."""
from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random
from typing import Dict, List


Vector = List[float]
Matrix = List[List[float]]


def _tanh_vec(vec: Vector) -> Vector:
    return [math.tanh(v) for v in vec]


def _add_vec(a: Vector, b: Vector) -> Vector:
    return [x + y for x, y in zip(a, b)]


def _scale_vec(vec: Vector, scale: float) -> Vector:
    return [scale * v for v in vec]


def _matvec(mat: Matrix, vec: Vector) -> Vector:
    return [sum(m_ij * v_j for m_ij, v_j in zip(row, vec)) for row in mat]


def _norm(vec: Vector) -> float:
    return math.sqrt(sum(v * v for v in vec))


def _mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


@dataclass
class AttractorResult:
    state_trajectory: List[Vector]
    stability: float
    synchrony: float
    final_state: Vector


class ContinuousAttractor:
    def __init__(
        self,
        size: int,
        leak: float = 0.1,
        noise_level: float = 0.02,
        recurrent_scale: float = 1.0,
        seed: int | None = None,
    ) -> None:
        self.rng = Random(seed)
        self.size = size
        self.leak = leak
        self.noise_level = noise_level
        self.recurrent_scale = recurrent_scale
        self.weights = self._make_weights()
        self.bias = [self.rng.gauss(0.0, 0.1) for _ in range(size)]

    def _make_weights(self) -> Matrix:
        weights: Matrix = []
        for i in range(self.size):
            row: Vector = []
            for j in range(self.size):
                symmetric = self.rng.gauss(0.0, 0.4)
                skew = self.rng.gauss(0.0, 0.05)
                value = symmetric + (skew - (-skew))
                row.append(self.recurrent_scale * value / math.sqrt(self.size))
            weights.append(row)
        # Symmetrise lightly to encourage fixed points.
        for i in range(self.size):
            for j in range(i + 1, self.size):
                avg = 0.5 * (weights[i][j] + weights[j][i])
                weights[i][j] = avg
                weights[j][i] = avg
        return weights

    def adjust_recurrence(self, scale: float) -> None:
        if scale <= 0:
            return
        factor = scale / max(self.recurrent_scale, 1e-6)
        for i in range(self.size):
            for j in range(self.size):
                self.weights[i][j] *= factor
        self.recurrent_scale = scale

    def step(self, state: Vector, drive: Vector) -> Vector:
        noise = [self.rng.gauss(0.0, self.noise_level) for _ in range(self.size)]
        recurrent = _matvec(self.weights, _tanh_vec(state))
        updated = _add_vec(_scale_vec(state, 1 - self.leak), drive)
        updated = _add_vec(updated, recurrent)
        updated = _add_vec(updated, self.bias)
        updated = _add_vec(updated, noise)
        return updated

    def _stability_metric(self, trajectory: List[Vector]) -> float:
        if len(trajectory) < 2:
            return 0.0
        last_diff = _norm(
            [a - b for a, b in zip(trajectory[-1], trajectory[-2])]
        )
        return math.exp(-last_diff)

    def _synchrony_metric(self, trajectory: List[Vector]) -> float:
        # Mean absolute correlation across units.
        t = len(trajectory)
        if t < 3:
            return 0.0
        n_units = len(trajectory[0])
        # Collect time-series per unit.
        series = [[trajectory[k][i] for k in range(t)] for i in range(n_units)]
        corrs: List[float] = []
        for i in range(n_units):
            for j in range(i + 1, n_units):
                a, b = series[i], series[j]
                mean_a, mean_b = _mean(a), _mean(b)
                cov = _mean([(x - mean_a) * (y - mean_b) for x, y in zip(a, b)])
                var_a = _mean([(x - mean_a) ** 2 for x in a])
                var_b = _mean([(y - mean_b) ** 2 for y in b])
                if var_a <= 0 or var_b <= 0:
                    continue
                corr = cov / math.sqrt(var_a * var_b)
                corrs.append(abs(corr))
        return _mean(corrs) if corrs else 0.0

    def run_attractor(
        self, input_vector: Vector, timesteps: int
    ) -> AttractorResult:
        state = list(input_vector)
        trajectory: List[Vector] = [list(state)]
        for _ in range(timesteps):
            state = self.step(state, input_vector)
            trajectory.append(list(state))
        stability = self._stability_metric(trajectory)
        synchrony = self._synchrony_metric(trajectory)
        return AttractorResult(
            state_trajectory=trajectory,
            stability=stability,
            synchrony=synchrony,
            final_state=state,
        )


def run_attractor(
    input_vector: Vector, timesteps: int, *, config: Dict[str, float]
) -> AttractorResult:
    net = ContinuousAttractor(
        size=config.get("size", len(input_vector)),
        leak=config.get("leak", 0.1),
        noise_level=config.get("noise", 0.02),
        recurrent_scale=config.get("recurrent_scale", 1.0),
    )
    return net.run_attractor(list(input_vector), timesteps)
