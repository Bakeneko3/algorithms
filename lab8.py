"""
Лабораторная работа №8.
Кратчайшие пути между всеми парами вершин.
Алгоритм Флойда-Уоршалла + проверка отрицательных циклов.
"""

import random
import time
from typing import Dict, List, Tuple
from common import Adj


def floyd_warshall(adj: Adj) -> Tuple[List[int], List[List[float]], bool]:
    """
    Возвращает (vertices, dist_matrix, has_negative_cycle).
    dist_matrix[i][j] — кратчайшее расстояние между vertices[i] и vertices[j].
    """
    vertices = sorted(adj.keys())
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    INF = float("inf")

    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    for u in adj:
        for v, w in adj[u]:
            iu, iv = idx[u], idx[v]
            if w < dist[iu][iv]:
                dist[iu][iv] = w

    # Основной цикл
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    has_neg = any(dist[i][i] < 0 for i in range(n))
    return vertices, dist, has_neg


def demo_small():
    print("=== Малый тест ===")
    g: Adj = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [],
    }
    verts, dist, neg = floyd_warshall(g)
    print("Вершины:", verts)
    for i, row in enumerate(dist):
        print(f"  {verts[i]}: "
              + " ".join("inf" if x == float("inf") else str(x) for x in row))
    print("Отрицательный цикл?", neg)


def demo_negative():
    print("\n=== Граф с отрицательным циклом ===")
    g: Adj = {
        0: [(1, 1)],
        1: [(2, -2)],
        2: [(1, -2)],
    }
    _, _, neg = floyd_warshall(g)
    print("Отрицательный цикл?", neg)


def demo_dense(n: int = 400, seed: int = 0):
    print(f"\n=== Плотный граф: n={n} ===")
    random.seed(seed)
    adj: Adj = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < 0.5:
                adj[u].append((v, random.randint(1, 100)))

    t0 = time.perf_counter()
    _, dist, neg = floyd_warshall(adj)
    t1 = time.perf_counter()
    print(f"Флойд-Уоршалл: {t1 - t0:.3f} c, отрицательный цикл? {neg}")


if __name__ == "__main__":
    demo_small()
    demo_negative()
    demo_dense(n=400)