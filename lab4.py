"""
Лабораторная работа №4.
Поиск маршрута в связном графе.
Выделение максимальной (слабо) связной компоненты в ориентированном графе.
Вход/выход: CSV со списком смежности.
"""

import os
import random
from collections import deque
from typing import Dict, Set
from common import (generate_random_graph, save_adjacency_csv,
                    load_adjacency_csv, print_adjacency, Adj)


def largest_weak_component(adj: Adj) -> Adj:
    """Возвращает подграф максимальной слабо связной компоненты."""
    # Строим неориентированный вариант для поиска компонент
    undirected: Dict[int, Set[int]] = {u: set() for u in adj}
    for u in adj:
        for v, _ in adj[u]:
            undirected.setdefault(v, set())
            undirected[u].add(v)
            undirected[v].add(u)

    visited: Set[int] = set()
    best: Set[int] = set()
    for s in undirected:
        if s in visited:
            continue
        comp: Set[int] = set()
        q = deque([s])
        visited.add(s)
        while q:
            u = q.popleft()
            comp.add(u)
            for v in undirected[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        if len(comp) > len(best):
            best = comp

    # Подграф только по вершинам из best
    result: Adj = {u: [] for u in best}
    for u in best:
        for v, w in adj.get(u, []):
            if v in best:
                result[u].append((v, w))
    return result


def main():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    random.seed(3)

    in_file = os.path.join(data_dir, "graph_directed.csv")
    out_file = os.path.join(data_dir, "largest_component.csv")

    if not os.path.exists(in_file):
        print(f"Файл {in_file} не найден. Генерируем пример...")
        # низкая p, чтобы получилось несколько компонент
        g = generate_random_graph(20, 0.08, directed=True, weighted=True)
        save_adjacency_csv(g, in_file)

    print(f"Загрузка ориентированного графа из {in_file}")
    g = load_adjacency_csv(in_file, directed=True, weighted=True)

    print("Исходный граф:")
    print_adjacency(g)

    comp = largest_weak_component(g)
    print("\nМаксимальная слабо связная компонента:")
    print_adjacency(comp)

    save_adjacency_csv(comp, out_file)
    print(f"\nКомпонента сохранена в {out_file}")


if __name__ == "__main__":
    main()