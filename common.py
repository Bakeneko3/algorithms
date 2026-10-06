import csv
import random
from typing import Dict, List, Tuple


# Тип "список смежности": {вершина: [(сосед, вес), ...]}
Adj = Dict[int, List[Tuple[int, int]]]


def generate_random_graph(n: int, p: float, directed: bool = False,
                          weighted: bool = False,
                          w_min: int = 1, w_max: int = 10) -> Adj:
    """Генерация случайного графа G(n, p) по модели Эрдёша–Реньи."""
    adj: Adj = {i: [] for i in range(n)}
    for i in range(n):
        start = i + 1 if not directed else 0
        for j in range(start, n):
            if i == j:
                continue
            if random.random() < p:
                w = random.randint(w_min, w_max) if weighted else 1
                adj[i].append((j, w))
                if not directed:
                    adj[j].append((i, w))
    return adj


def save_adjacency_csv(adj: Adj, filename: str) -> None:
    """Сохраняет список смежности в CSV: src;dst;weight."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["src", "dst", "weight"])
        for u in sorted(adj):
            for v, w in adj[u]:
                writer.writerow([u, v, w])


def load_adjacency_csv(filename: str, directed: bool = False,
                       weighted: bool = True) -> Adj:
    """Загружает список смежности из CSV."""
    adj: Adj = {}
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # пропустить заголовок
        for row in reader:
            if not row:
                continue
            u, v = int(row[0]), int(row[1])
            w = int(row[2]) if weighted and len(row) > 2 else 1
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, [])
            if not directed:
                adj.setdefault(v, []).append((u, w))
    return adj


def print_adjacency(adj: Adj) -> None:
    """Печатает список смежности в консоль."""
    for u in sorted(adj):
        items = ", ".join(f"{v}({w})" for v, w in adj[u])
        print(f"  {u}: {items}")