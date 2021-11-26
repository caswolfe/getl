import networkx

from typing import Any


def get_process_starting_at(graph: networkx.DiGraph, node: Any):
    # TODO: iterate through the nodes and find any parents which might need to be added and so forth
    subset_include = list(networkx.descendants(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()
    for n in subset_exclude:
        subset_graph.remove_node(n)
    return subset_graph
