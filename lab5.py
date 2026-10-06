"""
Лабораторная работа №5.
Максимальный поток в транспортной сети. Алгоритм Диница.
Поддерживает сети с >1000 узлов.
"""

import random
from collections import deque
from typing import List
from common import Adj


class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.graph: List[List[List[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        # [to, cap, reverse_index]
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0

    def _dfs(self, u: int, t: int, f: int) -> int:
        if u == t:
            return f
        while self.it[u] < len(self.graph[u]):
            e = self.graph[u][self.it[u]]
            v, cap, rev = e
            if cap > 0 and self.level[v] == self.level[u] + 1:
                d = self._dfs(v, t, min(f, cap))
                if d > 0:
                    e[1] -= d
                    self.graph[v][rev][1] += d
                    return d
            self.it[u] += 1
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        INF = float("inf")
        while self._bfs(s, t):
            self.it = [0] * self.n
            while True:
                f = self._dfs(s, t, INF)
                if f == 0:
                    break
                flow += f
        return flow


def max_flow_from_adj(adj: Adj, s: int, t: int) -> int:
    n = (max(adj) + 1) if adj else 0
    d = Dinic(n)
    for u in adj:
        for v, cap in adj[u]:
            d.add_edge(u, v, cap)
    return d.max_flow(s, t)


def demo_small():
    print("=== Малый тест (классическая сеть) ===")
    net: Adj = {i: [] for i in range(6)}
    edges_cap = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4),
                 (1, 3, 12), (3, 2, 9), (2, 4, 14), (4, 3, 7),
                 (3, 5, 20), (4, 5, 4)]
    for u, v, c in edges_cap:
        net[u].append((v, c))
    print("Max flow (ожидается 23):", max_flow_from_adj(net, 0, 5))


def demo_large(n: int = 1500, avg_out_degree: int = 4, seed: int = 0):
    print(f"=== Крупная сеть: {n} узлов ===")
    random.seed(seed)
    net: Adj = {i: [] for i in range(n)}
    for u in range(n - 1):
        for _ in range(avg_out_degree):
            v = random.randint(u + 1, n - 1)
            cap = random.randint(1, 100)
            net[u].append((v, cap))
    # исток 0, сток n-1
    import time
    t0 = time.perf_counter()
    flow = max_flow_from_adj(net, 0, n - 1)
    t1 = time.perf_counter()
    print(f"Max flow = {flow} за {t1 - t0:.3f} c")


if __name__ == "__main__":
    demo_small()
    demo_large(n=1500, avg_out_degree=4)