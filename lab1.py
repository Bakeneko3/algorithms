"""
Лабораторная работа №1.
Виды и классификация графов. Ориентированные и взвешенные графы.
Генерация случайных графов, список смежности, сохранение в CSV.
"""

import os
import random
from common import generate_random_graph, save_adjacency_csv, print_adjacency


DATA_DIR = "data"


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    random.seed(42)

    n = 10
    p = 0.4

    print("=== Неориентированный взвешенный граф ===")
    g_und = generate_random_graph(n, p, directed=False, weighted=True)
    print_adjacency(g_und)
    save_adjacency_csv(g_und, os.path.join(DATA_DIR, "graph_undirected.csv"))

    print("\n=== Ориентированный взвешенный граф ===")
    g_dir = generate_random_graph(n, p, directed=True, weighted=True)
    print_adjacency(g_dir)
    save_adjacency_csv(g_dir, os.path.join(DATA_DIR, "graph_directed.csv"))

    print("\n=== Неориентированный невзвешенный граф ===")
    g_unw = generate_random_graph(n, p, directed=False, weighted=False)
    print_adjacency(g_unw)
    save_adjacency_csv(g_unw, os.path.join(DATA_DIR, "graph_unweighted.csv"))

    print(f"\nФайлы сохранены в '{DATA_DIR}/'")


if __name__ == "__main__":
    main()