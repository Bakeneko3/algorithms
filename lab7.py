"""
Лабораторная работа №7.
Кратчайший путь в транспортной сети. Алгоритм Дейкстры.
Проверка на наличие отрицательных циклов (Беллман-Форд).
Поддержка плотных сетей (E ~ V(V-1)/2).
"""

import heapq
import random
import time
from typing import Dict, List, Optional, Tuple
from common import Adj


def bellman_ford_has_negative_cycle(adj: Adj) -> bool:
    """
    Проверка наличия отрицательного цикла.
    Добавляем фиктивный источник (dist=0 для всех) — стандартный приём.
    """
    n = (max(adj) + 1) if adj else 0
    edges: List[Tuple[int, int, int]] = []
    for u in adj:
        for v, w in adj[u]:
            edges.append((u, v, w))

    dist = [0] * n
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            return False
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return True
    return False


def dijkstra(adj: Adj, src: int, dst: Optional[int] = None
             ) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """Дейкстра (только неотрицательные веса)."""
    dist: Dict[int, float] = {u: float("inf") for u in adj}
    prev: Dict[int, Optional[int]] = {u: None for u in adj}
    dist[src] = 0.0
    pq: List[Tuple[float, int]] = [(0.0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if dst is not None and u == dst:
            break
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


def restore_path(prev: Dict[int, Optional[int]], src: int, dst: int) -> List[int]:
    path: List[int] = []
    cur: Optional[int] = dst
    while cur is not None:
        path.append(cur)
        if cur == src:
            break
        cur = prev.get(cur)
    path.reverse()
    return path if path and path[0] == src else []


def demo_small():
    print("=== Малый тест ===")
    g: Adj = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [],
    }
    dist, prev = dijkstra(g, 0)
    print("dist:", dist)
    print("path 0->3:", restore_path(prev, 0, 3))
    print("Отрицательный цикл?", bellman_ford_has_negative_cycle(g))


def demo_negative():
    print("\n=== Граф с отрицательным циклом ===")
    g: Adj = {
        0: [(1, 1)],
        1: [(2, -2)],
        2: [(1, -2)],
    }
    print("Отрицательный цикл?", bellman_ford_has_negative_cycle(g))


def demo_dense(n: int = 500, seed: int = 0):
    print(f"\n=== Плотный граф: n={n}, E ~ V(V-1)/2 ===")
    random.seed(seed)
    adj: Adj = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v:
                adj[u].append((v, random.randint(1, 100)))
    t0 = time.perf_counter()
    dist, _ = dijkstra(adj, 0)
    t1 = time.perf_counter()
    print(f"Дейкстра от 0: {t1 - t0:.3f} c, "
          f"max dist = {max(d for d in dist.values() if d != float('inf')):.1f}")


if __name__ == "__main__":
    demo_small()
    demo_negative()
    demo_dense(n=500)