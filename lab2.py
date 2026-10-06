"""
Лабораторная работа №2.
Обход графа в ширину (BFS) и в глубину (DFS).
Используются deque и list как очередь/стек из стандартной библиотеки.
"""

import os
import random
import time
from collections import deque
from typing import List, Set
from common import generate_random_graph, Adj


def bfs(adj: Adj, start: int) -> List[int]:
    """Обход в ширину. Возвращает порядок посещения вершин."""
    visited: Set[int] = {start}
    order: List[int] = []
    q = deque([start])
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj.get(u, []):
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order


def dfs(adj: Adj, start: int) -> List[int]:
    """Обход в глубину (итеративный, через стек)."""
    visited: Set[int] = set()
    order: List[int] = []
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        # реверс — чтобы порядок совпадал с рекурсивным DFS
        for v, _ in reversed(adj.get(u, [])):
            if v not in visited:
                stack.append(v)
    return order


def time_traversal(adj: Adj, start: int = 0) -> None:
    t0 = time.perf_counter()
    o_bfs = bfs(adj, start)
    t1 = time.perf_counter()
    o_dfs = dfs(adj, start)
    t2 = time.perf_counter()
    print(f"  BFS: посещено {len(o_bfs)} вершин за {t1 - t0:.6f} c")
    print(f"  DFS: посещено {len(o_dfs)} вершин за {t2 - t1:.6f} c")


def main():
    random.seed(1)

    print("=== Небольшой граф (n=10) ===")
    g = generate_random_graph(10, 0.4)
    print("BFS от 0:", bfs(g, 0))
    print("DFS от 0:", dfs(g, 0))
    time_traversal(g, 0)

    print("\n=== Крупный граф (n=5000, p=0.001) ===")
    big = generate_random_graph(5000, 0.001)
    time_traversal(big, 0)


if __name__ == "__main__":
    main()