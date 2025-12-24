"""Ŋob / N(Z) symbolic geometry classifier without external libraries."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

SUPPORTED_LABELS = [
    "SU-TI",
    "ME-TI",
    "ME-ME",
    "FRAG-Δ",
    "THE_ONE",
    "THE_MANY",
    "COH-REBUILD",
]


def _distance(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


@dataclass
class SymbolicState:
    lambda_delta_psi: Tuple[float, float, float]
    label: str
    cluster_centers: Optional[List[Tuple[float, float, float]]] = None


@dataclass
class NZClassifier:
    centers: List[Tuple[float, float, float]] = field(default_factory=list)
    counts: List[int] = field(default_factory=list)

    def _bandwidth(self) -> float:
        if len(self.centers) < 2:
            return 0.4
        dists = []
        for i, a in enumerate(self.centers):
            for b in self.centers[i + 1 :]:
                dists.append(_distance(a, b))
        return max(0.2, sum(dists) / len(dists))

    def classify_state(self, lambda_: float, delta_: float, psi_: float) -> SymbolicState:
        point = (lambda_, delta_, psi_)
        if not self.centers:
            self.centers.append(point)
            self.counts.append(1)
            return SymbolicState(point, SUPPORTED_LABELS[0], self.centers.copy())

        bandwidth = self._bandwidth()
        distances = [_distance(point, c) for c in self.centers]
        min_idx = int(distances.index(min(distances)))
        if distances[min_idx] > bandwidth:
            self.centers.append(point)
            self.counts.append(1)
            min_idx = len(self.centers) - 1
        else:
            count = self.counts[min_idx]
            cx, cy, cz = self.centers[min_idx]
            new_center = (
                (cx * count + point[0]) / (count + 1),
                (cy * count + point[1]) / (count + 1),
                (cz * count + point[2]) / (count + 1),
            )
            self.centers[min_idx] = new_center
            self.counts[min_idx] = count + 1

        # Emergent mapping: sort centers by radius and map to labels in order.
        order = sorted(range(len(self.centers)), key=lambda i: math.sqrt(sum(c * c for c in self.centers[i])))
        label_map = {cluster_idx: SUPPORTED_LABELS[i % len(SUPPORTED_LABELS)] for i, cluster_idx in enumerate(order)}
        label = label_map[min_idx]

        return SymbolicState(point, label, self.centers.copy())


def classify_state(lambda_: float, delta_: float, psi_: float) -> SymbolicState:
    classifier = NZClassifier()
    return classifier.classify_state(lambda_, delta_, psi_)
