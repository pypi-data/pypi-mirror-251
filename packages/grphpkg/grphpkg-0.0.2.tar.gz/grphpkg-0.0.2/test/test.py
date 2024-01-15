# main_script.py
import sys
import os

# Add the parent directory to the Python path
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(project_path)

from graph.graph import Graph
from graph.weighted_graph import WeightedGraph

matrix_representation = [
    [0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0]
]

# g = Graph(matrix_representation)
# g.print_graph()
# g.dfs(0, lambda x: print(str(x)+" ", end=""))
# g.draw_graph()

# g2 = Graph()
# g2.add_edge(0, 1)
# g2.print_graph()

matrix = [
    [0, 2, 3, float('inf')],
    [2, 0, 1, 4],
    [3, 1, 0, 5],
    [float('inf'), 4, 5, 0]
]

weighted_graph = WeightedGraph(matrix)
weighted_graph.print_graph()
print(weighted_graph.prim_mst(0))
weighted_graph.draw_graph()



