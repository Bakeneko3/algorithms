"""
Лабораторная работа №3.
Минимальное остовное дерево (МОД) во взвешенном
неориентированном графе. Алгоритм Крускала.
Вход: CSV со списком смежности.
Выход: CSV со списком смежности остовного дерева.
"""

import os
import random
import sys
from typing import List, Tuple
from common import (generate_random_graph, save_adjacency_csv,
                    load_adjacency_csv, print_adjacency, Adj)


class DSU:
    """Система непересекающихся множеств (Union-Find)."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal_mst(adj: Adj) -> Adj:
    """Алгоритм Крускала. Возвращает список смежности МОД."""
    n = (max(adj) + 1) if adj else 0

    # Собираем рёбра без дублей
    edges: List[Tuple[int, int, int]] = []
    seen = set()
    for u in adj:
        for v, w in adj[u]:
            if u == v:
                continue
            key = (min(u, v), max(u, v))
            if key in seen:
                continue
            seen.add(key)
            edges.append((w, u, v))

    edges.sort()

    dsu = DSU(n)
    mst: Adj = {i: [] for i in range(n)}
    for w, u, v in edges:
        if dsu.union(u, v):
            mst[u].append((v, w))
            mst[v].append((u, w))
    return mst


def main():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    random.seed(7)

    in_file = os.path.join(data_dir, "graph_undirected.csv")
    out_file = os.path.join(data_dir, "mst.csv")

    if not os.path.exists(in_file):
        print(f"Файл {in_file} не найден. Генерируем пример...")
        g = generate_random_graph(15, 0.35, weighted=True, w_min=1, w_max=20)
        save_adjacency_csv(g, in_file)

    print(f"Загрузка графа из {in_file}")
    g = load_adjacency_csv(in_file, directed=False, weighted=True)

    print("Исходный граф:")
    print_adjacency(g)

    mst = kruskal_mst(g)
    print("\nМинимальное остовное дерево (Крускал):")
    print_adjacency(mst)

    save_adjacency_csv(mst, out_file)
    print(f"\nМОД сохранено в {out_file}")


if __name__ == "__main__":
    main()