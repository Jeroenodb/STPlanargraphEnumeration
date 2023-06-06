
import copy
from itertools import count
from random import sample
from typing import List, Tuple

def getSTPlanar(N: int):
    """
    finds all st-planar graphs with <=N nodes.
    Warning: Generates some isomorphic graphs.
    The nodes are labeled in a topological order.
    """
    result = []
    def findGraph(graph: List[List], active: List[Tuple[int,int]], n: int):
        """
        Recursive function that given a prefix of the topological order, extends the graph by adding nodes.
        active is a list of edges that currently have no destination, in order from left to right in some planar embedding.
        """
        need = 1
        for i,j,k in zip(active,active[1:],active[2:]):
            need+=i[0]==j[0]==k[0] # if three adjacent edges in the active list have same parent, middle one definitely needs an extra node.
        if need>n:
            return False
        # if len(active)==1: # some condition to exclude graphs which have bridges.
        #     return True
        A = len(active)
        if len(set(i[0] for i in active))==A:
            # can finish with a t-node now
            t = len(graph)
            graph.append([])
            for f,id in active:
                graph[f][id]=t
            result.append(copy.deepcopy(graph))
            graph.pop()
        newnode = len(graph)
        graph.append([])

        for i in range(A):
            s = set()
            for j in range(i,A):
                if active[j][0] in s:
                    # detected multi-edge when deciding to merge stuff from i:j
                    break
                
                s.add(active[j][0])
                for deg in count(1):
                    graph[newnode] = [None]*deg
                    for f,id in active:
                        graph[f][id] = newnode
                    if not findGraph(graph, active[:i]+[(newnode,i) for i in range(deg)] + active[j+1:],n-1):
                        break
        graph.pop()
        return True
    for deg in count(1):
        graph = [[None]*deg]
        if not findGraph(graph,[(0,i) for i in range(deg)], N-1):
            break
    return result

res = getSTPlanar(5)

print(res)
import networkx as nx
import matplotlib.pyplot as plt

def draw_graphs(adjacency_lists):
    num_graphs = len(adjacency_lists)
    num_cols = min(num_graphs, 3)  # Adjust the number of columns as desired
    num_rows = (num_graphs + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(5*num_cols, 5*num_rows))
    for i, adjacency_list in enumerate(adjacency_lists):
        G = nx.DiGraph()  # Create an empty directed graph

        # Add nodes to the graph
        for node in range(len(adjacency_list)):
            G.add_node(node)

        # Add edges to the graph
        for node, neighbors in enumerate(adjacency_list):
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        # Draw the graph
        pos = nx.planar_layout(G)
        row = i // num_cols
        col = i % num_cols
        ax = axs[row, col] if num_rows > 1 else axs[col]
        ax.set_title(f'Graph {i+1}')
        nx.draw(G, pos, with_labels=True, arrows=True, ax=ax)

    plt.tight_layout()
    plt.show()

draw_graphs(sample(res, 15))
s = input() # so it waits until completion.
