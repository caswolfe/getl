import networkx

from typing import Any


def get_process_starting_at(graph: networkx.DiGraph, node: Any):

    subset_include = list(networkx.descendants(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        subset_graph.remove_node(subset_exclude.pop())

    return subset_graph


def get_process_ending_at(graph: networkx.DiGraph, node: Any):

    subset_include = list(networkx.ancestors(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        subset_graph.remove_node(subset_exclude.pop())

    return subset_graph
