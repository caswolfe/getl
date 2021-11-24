import networkx
import networkx as nx
import matplotlib

from matplotlib import pyplot
from typing import List


# process_graph = networkx.DiGraph()
# generation_min = 1
potential_node_processes = []


def node_process(requires: list[str] = []):

    def wrapper_node_process(func):

        global potential_node_processes

        fname = func.__name__
        potential_node_processes.append((fname, func, requires))

        return func

    return wrapper_node_process


def build():

    global potential_node_processes

    process_graph = networkx.DiGraph()

    np_processed = []
    np_to_process = potential_node_processes.copy()

    to_process_names = [name for (name, _, _) in np_to_process]
    print(f'found: {to_process_names}')

    while len(np_to_process) > 0:

        (fname, func, requires) = np_to_process.pop()
        generation = 0

        if len(requires) != 0:
            mpg = -1
            unmet_requirements = requires.copy()

            for requirement in requires:
                if requirement in np_processed:
                    unmet_requirements.remove(requirement)
                    mpg = min(mpg, process_graph.nodes[requirement]['np_generation'] - 1)

            if len(unmet_requirements) > 0:
                np_to_process.insert(0, (fname, func, requires))
                continue
                
            generation = mpg

        assert fname not in process_graph.nodes, 'node_process name must be unique'
        process_graph.add_node(fname)
        process_graph.nodes[fname]['np_func'] = func
        process_graph.nodes[fname]['np_generation'] = generation

        np_processed.append(fname)

    return process_graph


# def draw_etl_process():
#
#     global process_graph
#     global generation_min
#
#     print(nx.get_node_attributes(process_graph, 'np_func'))
#     print(nx.get_node_attributes(process_graph, 'np_generation'))
#
#     pos = networkx.multipartite_layout(
#         process_graph,
#         subset_key='np_generation',
#         align='horizontal',
#     )
#
#     networkx.draw(
#         process_graph,
#         pos=pos,
#         with_labels=True,
#     )
#     pyplot.show()

# def custom_wrapper(func):
#     def wrapper_custom_wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper_custom_wrapper
