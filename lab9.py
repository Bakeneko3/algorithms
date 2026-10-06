"""
Лабораторная работа №9.
Рёберная раскраска неориентированного графа (жадный алгоритм).
Поддержка графов с >1000 узлов.
"""

import os
import random
import time
from typing import Dict, Set, Tuple
from common import generate_random_graph, print_adjacency, Adj


def edge_coloring(adj: Adj) -> Dict[Tuple[int, int], int]:
    """
    Жадная рёберная раскраска.
    Возвращает {(u, v): color}, где u < v.
    """
    # Собираем рёбра без дублей
    edges: list = []
    seen: Set[Tuple[int, int]] = set()
    for u in adj:
        for v, _ in adj[u]:
            if u == v:
                continue
            key = (min(u, v), max(u, v))
            if key not in seen:
                seen.add(key)
                edges.append(key)

    # Эвристика: сначала рёбра с большей суммой степеней
    deg = {u: len(adj[u]) for u in adj}
    edges.sort(key=lambda e: -(deg.get(e[0], 0) + deg.get(e[1], 0)))

    color_at_vertex: Dict[int, Set[int]] = {u: set() for u in adj}
    colors: Dict[Tuple[int, int], int] = {}

    for u, v in edges:
        used = color_at_vertex[u] | color_at_vertex[v]
        c = 0
        while c in used:
            c += 1
        colors[(u, v)] = c
        color_at_vertex[u].add(c)
        color_at_vertex[v].add(c)

    return colors


def demo_small():
    print("=== Малый тест ===")
    g = generate_random_graph(8, 0.4, weighted=False)
    print_adjacency(g)
    colors = edge_coloring(g)
    for e, c in sorted(colors.items()):
        print(f"  Ребро {e}: цвет {c}")
    n_colors = max(colors.values()) + 1 if colors else 0
    max_deg = max(len(g[u]) for u in g)
    print(f"Использовано цветов: {n_colors} (Δ={max_deg}, "
          f"оценка Визинга: ≤ {max_deg + 1})")


def demo_large(n: int = 1500, p: float = 0.002, seed: int = 0):
    print(f"\n=== Крупный граф: n={n}, p={p} ===")
    random.seed(seed)
    g = generate_random_graph(n, p, weighted=False)

    t0 = time.perf_counter()
    colors = edge_coloring(g)
    t1 = time.perf_counter()

    n_colors = max(colors.values()) + 1 if colors else 0
    max_deg = max(len(g[u]) for u in g) if g else 0
    print(f"Рёбер: {len(colors)}, цветов: {n_colors}, Δ={max_deg}")
    print(f"Время: {t1 - t0:.3f} c")


if __name__ == "__main__":
    demo_small()
    demo_large(n=1500, p=0.002)