"""Ŋob / N(Z) symbolic geometry layer without external dependencies."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List

SYMBOLS = [
    "SU-TI",
    "ME-TI",
    "ME-ME",
    "FRAG-Δ",
    "THE_ONE",
    "THE_MANY",
    "COH-REBUILD",
]


@dataclass
class GeometryPoint:
    lambda_: float
    delta_: float
    psi_: float
    label: str


@dataclass
class NZClassifier:
    bandwidth: float = 0.15
    history: List[GeometryPoint] = field(default_factory=list)

    def _distance(self, a, b) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

    def _cluster(self, samples: List[List[float]]):
        clusters: List[dict] = []
        for point in samples:
            attached = False
            for cluster in clusters:
                if self._distance(point, cluster["center"]) <= self.bandwidth:
                    cluster["points"].append(point)
                    attached = True
                    break
            if not attached:
                clusters.append({"points": [point], "center": point[:]})

            for cluster in clusters:
                px, py, pz = zip(*cluster["points"])
                cluster["center"] = [sum(px) / len(px), sum(py) / len(py), sum(pz) / len(pz)]
        return clusters

    def classify_state(self, lambda_: float, delta_: float, psi_: float) -> str:
        point = [lambda_, delta_, psi_]
        samples = [[p.lambda_, p.delta_, p.psi_] for p in self.history] + [point]
        clusters = self._cluster(samples)

        ordering = sorted(range(len(clusters)), key=lambda idx: self._distance(clusters[idx]["center"], [0, 0, 0]))
        label_lookup = {cluster_idx: SYMBOLS[i % len(SYMBOLS)] for i, cluster_idx in enumerate(ordering)}

        containing_cluster = None
        for idx, cluster in enumerate(clusters):
            if any(self._distance(point, member) < 1e-9 for member in cluster["points"]):
                containing_cluster = idx
                break
        assigned_label = label_lookup.get(containing_cluster, SYMBOLS[0])

        self.history.append(GeometryPoint(lambda_, delta_, psi_, assigned_label))
        return assigned_label

    def export_points(self) -> List[GeometryPoint]:
        return self.history


__all__ = ["NZClassifier", "GeometryPoint"]
