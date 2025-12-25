"""Stage-H slow structural adaptation layer without external dependencies."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List

import math


@dataclass
class StructuralState:
    graph: Dict[int, Dict[int, float]]
    connectivity_bias: List[List[float]]
    metrics: Dict[str, float] = field(default_factory=dict)


class StageHGraph:
    def __init__(
        self,
        size: int,
        moisture: float = 0.5,
        nutrients: float = 0.5,
        light: float = 0.5,
        micro_shock: float = 0.1,
        branch_threshold: float = 6.5,
        fusion_threshold: float = 2.0,
    ) -> None:
        self.size = size
        self.maturity = 1.0
        self.env = {
            "moisture": moisture,
            "nutrients": nutrients,
            "light": light,
            "micro_shock": micro_shock,
        }
        self.branch_threshold = branch_threshold
        self.fusion_threshold = fusion_threshold
        self.graph = self._initial_graph()

    def _initial_graph(self) -> Dict[int, Dict[int, float]]:
        g: Dict[int, Dict[int, float]] = {i: {} for i in range(self.size)}
        for i in range(self.size):
            j = (i + 1) % self.size
            g[i][j] = g[j].get(i, 1.0)
            g[j][i] = g[i][j]
        return g

    def _environmental_modulation(self) -> float:
        field = (
            0.4 * self.env["moisture"]
            + 0.3 * self.env["nutrients"]
            + 0.2 * self.env["light"]
            - 0.2 * self.env["micro_shock"]
        )
        return max(0.1, field)

    def _branch(self, g: Dict[int, Dict[int, float]], energy: float) -> None:
        candidate = max(g.keys()) + 1 if g else 0
        g[candidate] = {}
        target = random.choice(list(g.keys()))
        weight = 1.0 + 0.1 * energy
        g[candidate][target] = weight
        g[target][candidate] = weight

    def _fuse(self, g: Dict[int, Dict[int, float]]) -> None:
        nodes = list(g.keys())
        if len(nodes) < 2:
            return
        a, b = random.sample(nodes, 2)
        weight = g[a].get(b, 0.8) + 0.2
        g[a][b] = weight
        g[b][a] = weight

    def _shock(self, g: Dict[int, Dict[int, float]]) -> None:
        if random.random() < self.env["micro_shock"]:
            edges = [(u, v) for u in g for v in g[u] if u < v]
            if edges:
                u, v = random.choice(edges)
                g[u].pop(v, None)
                g[v].pop(u, None)

    def _graph_to_matrix(self, g: Dict[int, Dict[int, float]]) -> List[List[float]]:
        matrix = [[0.0 for _ in range(self.size)] for _ in range(self.size)]
        for u, neighbors in g.items():
            for v, weight in neighbors.items():
                if u < self.size and v < self.size:
                    matrix[u][v] = matrix[v][u] = weight
        for i in range(self.size):
            row_sum = sum(matrix[i]) or 1e-9
            matrix[i] = [w / row_sum for w in matrix[i]]
        return matrix

    def graph_to_matrix(self) -> List[List[float]]:
        return self._graph_to_matrix(self.graph)

    def _metrics(self, g: Dict[int, Dict[int, float]], energy: float, stability: float) -> Dict[str, float]:
        edge_count = sum(len(neigh) for neigh in g.values()) / 2
        return {
            "energy": energy,
            "stability": stability,
            "nodes": float(len(g)),
            "edges": float(edge_count),
            "maturity": self.maturity,
        }

    def update_structure(self, attractor_state: Dict) -> StructuralState:
        final_state = attractor_state.get("final_state", [])
        energy = math.sqrt(sum(v * v for v in final_state))
        stability = float(attractor_state.get("stability", 0.0))
        modulation = self._environmental_modulation()

        g = {node: neighbors.copy() for node, neighbors in self.graph.items()}
        if energy > self.branch_threshold * modulation:
            self._branch(g, energy)
        if energy < self.fusion_threshold:
            self._fuse(g)
        self._shock(g)

        self.graph = g
        bias_matrix = self._graph_to_matrix(g)
        metrics = self._metrics(g, energy, stability)
        self.maturity = min(2.0, self.maturity + 0.01 * modulation)

        return StructuralState(graph=g, connectivity_bias=bias_matrix, metrics=metrics)


def update_structure(attractor_state: Dict, **kwargs: Dict) -> StructuralState:
    graph = StageHGraph(
        size=kwargs.get("size", 48),
        moisture=kwargs.get("moisture", 0.5),
        nutrients=kwargs.get("nutrients", 0.5),
        light=kwargs.get("light", 0.5),
        micro_shock=kwargs.get("micro_shock", 0.1),
        branch_threshold=kwargs.get("branch_threshold", 6.5),
        fusion_threshold=kwargs.get("fusion_threshold", 2.0),
    )
    return graph.update_structure(attractor_state)


__all__ = ["StructuralState", "StageHGraph", "update_structure"]
