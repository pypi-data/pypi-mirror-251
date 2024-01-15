from collections import defaultdict
from heapq import heappush, heappop
import networkx as nx
import matplotlib.pyplot as plt

class WeightedGraph:
    def __init__(self, matrix=None):
        self.graph = defaultdict(list)
        self.adjacency_matrix = matrix

        if matrix is not None:
            self.__construct_graph_from_matrix()

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # Make the graph undirected

    def __construct_graph_from_matrix(self):
        vertices = range(len(self.adjacency_matrix))
        self.graph = defaultdict(list)

        for i, u in enumerate(vertices):
            for j, v in enumerate(vertices):
                if u == v or self.adjacency_matrix[i][j] == float('inf'):
                    continue

                self.add_edge(u, v, self.adjacency_matrix[i][j])

    def print_graph(self):
        for k, neighbors in self.graph.items():
            print(f"{k} -> {neighbors}")

    def prim_mst(self, start):
        if start not in self.graph:
            raise ValueError(f"Start vertex {start} is not in the graph.")
        
        visited = set()
        min_heap = [(0, start, None)]
        mst_edges = []
        mst_cost = 0

        while min_heap:
            weight, current_vertex, parent = heappop(min_heap)
            if current_vertex not in visited:
                visited.add(current_vertex)
                if parent is not None:
                    mst_edges.append((parent, current_vertex, weight))
                    mst_cost += weight
                for neighbor, edge_weight in self.graph[current_vertex]:
                    if neighbor not in visited:
                        heappush(min_heap, (edge_weight, neighbor, current_vertex))
        return mst_edges, mst_cost
    
    def draw_graph(self):
        G = nx.Graph()
        for u, neighbors in self.graph.items():
            for v, weight in neighbors:
                G.add_edge(u, v, weight=weight)
        pos = nx.spring_layout(G)  # You can choose different layout algorithms
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue", font_color="black", font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()