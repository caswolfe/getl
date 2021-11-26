import networkx

from typing import Any


def get_process_starting_at(graph: networkx.DiGraph, node: Any):

    subset_include = list(networkx.descendants(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        n = subset_exclude.pop()
        se_children = list(networkx.descendants(subset_graph, n))

        # If there is an intersection in the children of the "node to remove", and
        # the subset of "nodes to include", it is a parent of a node to include.
        if len([i for i in se_children if i in subset_include]) > 0:
            subset_include.append(n)
        else:
            subset_graph.remove_node(n)

    return subset_graph
