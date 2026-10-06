"""
Лабораторная работа №6.
Максимальное паросочетание в двудольном графе.
Алгоритм Куна (венгерский).
Поддерживает двудольные графы с >2000 узлов.
"""

import random
import sys
import time
from typing import Dict, Iterable, Set
from common import Adj

# Увеличим лимит рекурсии (Кун — рекурсивный)
sys.setrecursionlimit(10000)


def kuhn_matching(adj: Adj, left: Iterable[int]) -> Dict[int, int]:
    """
    Возвращает {left_vertex: right_vertex}.
    adj — список смежности для вершин левой доли
    (рёбра left -> right с любым весом, вес игнорируется).
    """
    left = list(left)
    match_r: Dict[int, int] = {}  # right -> left

    def try_kuhn(u: int, used: Set[int]) -> bool:
        for v, _ in adj.get(u, []):
            if v in used:
                continue
            used.add(v)
            if v not in match_r or try_kuhn(match_r[v], used):
                match_r[v] = u
                return True
        return False

    for u in left:
        try_kuhn(u, set())

    return {u: v for v, u in match_r.items()}


def demo_small():
    print("=== Малый тест ===")
    bg: Adj = {
        0: [(10, 1), (11, 1)],
        1: [(10, 1), (12, 1)],
        2: [(11, 1), (12, 1)],
        3: [(10, 1)],
    }
    m = kuhn_matching(bg, left=[0, 1, 2, 3])
    print("Паросочетание:", m)
    print("Размер:", len(m))


def demo_large(n_left: int = 1000, n_right: int = 1000,
               edges_per_left: int = 3, seed: int = 0):
    print(f"\n=== Крупный тест: L={n_left}, R={n_right}, "
          f"~{edges_per_left} рёбер на вершину ===")
    random.seed(seed)
    adj: Adj = {u: [] for u in range(n_left)}
    for u in range(n_left):
        targets = random.sample(range(n_right), min(edges_per_left, n_right))
        for v in targets:
            # правая доля кодируется как n_left + v
            adj[u].append((n_left + v, 1))

    t0 = time.perf_counter()
    # Кун работает с настоящими номерами правых вершин, поэтому
    # передаём их «как есть» (в adj уже лежат числа >= n_left)
    m = kuhn_matching(adj, left=range(n_left))
    t1 = time.perf_counter()
    print(f"Размер паросочетания = {len(m)} за {t1 - t0:.3f} c")


if __name__ == "__main__":
    demo_small()
    demo_large(n_left=1000, n_right=1000, edges_per_left=3)