"""Stage-H structural adaptation layer without external dependencies."""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Dict, List, Optional, Tuple


@dataclass
class StructuralState:
    graph: "SimpleGraph"
    connectivity_scale: float
    structural_delta: float
    metrics: Dict[str, float]


class SimpleGraph:
    def __init__(self) -> None:
        self.nodes: Dict[int, Dict[str, float]] = {}
        self.edges: Dict[Tuple[int, int], float] = {}

    def add_node(self, node: int, **attrs: float) -> None:
        self.nodes[node] = attrs

    def add_edge(self, a: int, b: int, weight: float = 0.3) -> None:
        key = tuple(sorted((a, b)))
        self.edges[key] = weight

    def remove_edge(self, a: int, b: int) -> None:
        key = tuple(sorted((a, b)))
        if key in self.edges:
            del self.edges[key]

    def has_edge(self, a: int, b: int) -> bool:
        return tuple(sorted((a, b))) in self.edges

    def number_of_edges(self) -> int:
        return len(self.edges)

    def number_of_nodes(self) -> int:
        return len(self.nodes)

    def copy(self) -> "SimpleGraph":
        g = SimpleGraph()
        g.nodes = {k: dict(v) for k, v in self.nodes.items()}
        g.edges = dict(self.edges)
        return g

    def degree(self) -> List[Tuple[int, int]]:
        counts: Dict[int, int] = {n: 0 for n in self.nodes}
        for (a, b) in self.edges:
            counts[a] += 1
            counts[b] += 1
        return list(counts.items())

    def average_clustering(self) -> float:
        # Approximate clustering using triangle counts.
        if self.number_of_nodes() < 3:
            return 0.0
        triangles = 0
        triples = 0
        nodes = list(self.nodes.keys())
        for i, a in enumerate(nodes):
            for j in range(i + 1, len(nodes)):
                b = nodes[j]
                for c in nodes[j + 1 :]:
                    if self.has_edge(a, b) and self.has_edge(b, c) and self.has_edge(a, c):
                        triangles += 1
                    triples += 1
        return triangles / triples if triples else 0.0


@dataclass
class StageHGraph:
    moisture: float
    nutrients: float
    light: float
    micro_shock: float
    rewire_prob: float
    seed: Optional[int] = None
    graph: SimpleGraph = field(init=False)

    def __post_init__(self) -> None:
        self.rng = Random(self.seed)
        self.graph = SimpleGraph()
        for i in range(4):
            self.graph.add_node(i, resource=self._initial_resource())
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 0)

    def _initial_resource(self) -> float:
        env_drive = (self.moisture + self.nutrients + self.light) / 3
        return env_drive + self.rng.gauss(0, 0.05)

    def _maybe_branch(self) -> None:
        if self.rng.random() < self.moisture:
            new_node = max(self.graph.nodes) + 1 if self.graph.nodes else 0
            anchor = self.rng.choice(list(self.graph.nodes)) if self.graph.nodes else 0
            self.graph.add_node(new_node, resource=self._initial_resource())
            self.graph.add_edge(anchor, new_node, weight=self.rng.uniform(0.2, 1.0))

    def _maybe_fuse(self) -> None:
        if len(self.graph.nodes) < 3:
            return
        if self.rng.random() < self.nutrients:
            nodes = list(self.graph.nodes.keys())
            a = self.rng.choice(nodes)
            b = self.rng.choice(nodes)
            if a != b and not self.graph.has_edge(a, b):
                self.graph.add_edge(a, b, weight=self.rng.uniform(0.3, 1.2))

    def _maybe_rewire(self) -> None:
        edges = list(self.graph.edges.keys())
        for a, b in edges:
            if self.rng.random() < self.rewire_prob + self.micro_shock:
                self.graph.remove_edge(a, b)
                self._maybe_branch()

    def update_structure(self, attractor_state: Dict[str, float]) -> StructuralState:
        prev_edges = self.graph.number_of_edges()
        prev_nodes = self.graph.number_of_nodes()
        stability = attractor_state.get("stability", 0.0)
        synchrony = attractor_state.get("synchrony", 0.0)

        if stability < 0.8:
            self._maybe_branch()
        if synchrony > 0.3:
            self._maybe_fuse()
        self._maybe_rewire()

        # Adjust edge weights subtly using light and synchrony cues.
        for key in list(self.graph.edges.keys()):
            jitter = self.rng.gauss(0, 0.02)
            self.graph.edges[key] = max(0.05, self.graph.edges[key] + jitter + 0.05 * ((self.light + synchrony) / 2))

        avg_degree = sum(deg for _, deg in self.graph.degree()) / max(1, self.graph.number_of_nodes())
        clustering = self.graph.average_clustering()
        edge_count = self.graph.number_of_edges()
        node_count = self.graph.number_of_nodes()

        structural_delta = abs(edge_count - prev_edges) + abs(node_count - prev_nodes)
        connectivity_scale = 1.0 + 0.1 * (avg_degree + clustering)

        metrics = {
            "avg_degree": float(avg_degree),
            "clustering": float(clustering),
            "edge_count": float(edge_count),
            "node_count": float(node_count),
        }

        return StructuralState(
            graph=self.graph.copy(),
            connectivity_scale=connectivity_scale,
            structural_delta=float(structural_delta),
            metrics=metrics,
        )


def update_structure(attractor_state: Dict[str, float], *, config: Dict[str, float]) -> StructuralState:
    layer = StageHGraph(
        moisture=config.get("moisture", 0.5),
        nutrients=config.get("nutrients", 0.5),
        light=config.get("light", 0.5),
        micro_shock=config.get("micro_shock", 0.0),
        rewire_prob=config.get("rewire_prob", 0.1),
    )
    return layer.update_structure(attractor_state)
