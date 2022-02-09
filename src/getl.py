import logging
import networkx

from matplotlib import pyplot
from typing import Any

potential_node_processes = []

# functions


def build():

    global potential_node_processes

    log = logging.getLogger('getl')

    process_graph = networkx.DiGraph()

    np_processed = []
    np_to_process = potential_node_processes.copy()

    while len(np_to_process) > 0:

        (fname, func, requires) = np_to_process.pop()
        assert fname not in process_graph.nodes, f'node_process name "{fname}" must be unique'

        log.debug(f'processing "{fname}", requiring {requires}')

        generation = 0
        if len(requires) != 0:
            mpg = -1
            unmet_requirements = requires.copy()

            for requirement in requires:
                if requirement in np_processed:
                    unmet_requirements.remove(requirement)
                    mpg = min(mpg, process_graph.nodes[requirement]['np_generation'] - 1)

            if len(unmet_requirements) > 0:
                # TODO: detect when requirement is not present, currently runs forever...
                np_to_process.insert(0, (fname, func, requires))
                continue
            generation = mpg

        log.debug(f'adding "{fname}"')
        process_graph.add_node(fname)
        process_graph.nodes[fname]['np_func'] = func
        process_graph.nodes[fname]['np_generation'] = generation

        # if len(requires) != 0:
        for requirement in requires:  # this will not iterate at all if len(requires) == 0
            process_graph.add_edge(requirement, fname)

        np_processed.append(fname)

    return process_graph


def create_linear_run(process_graph: networkx.DiGraph):

    node_gen_dict = dict()
    run_graph: networkx.DiGraph = networkx.create_empty_copy(process_graph)

    for node in process_graph.nodes:
        node_gen = process_graph.nodes[node]['np_generation']
        if node_gen not in node_gen_dict.keys():
            node_gen_dict[node_gen] = [node]
        else:
            node_gen_dict[node_gen].append(node)

    node_master_list = []
    gen_high = max(node_gen_dict.keys())
    gen_low = min(node_gen_dict.keys()) - 1
    for i in range(gen_high, gen_low, -1):
        for np in node_gen_dict[i]:
            node_master_list.append(np)

    for i in range(1, len(node_master_list)):
        run_graph.add_edge(
            node_master_list[i-1],
            node_master_list[i]
        )

    return run_graph, node_master_list


def draw_etl_process(graph: networkx.Graph, title='', node_color='#1f78b4'):

    pyplot.figure(figsize=(7, 5))
    ax = pyplot.gca()
    ax.set_title(title)
    pos = networkx.multipartite_layout(
        graph,
        subset_key='np_generation',
        align='horizontal',
    )
    networkx.draw(
        graph,
        pos=pos,
        with_labels=True,
        node_color=node_color,
    )
    pyplot.show()


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


def scan_for_plugins(namespace):
    """
    https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/

    :param namespace:
    :return:
    """

    import importlib
    import pkgutil

    name = importlib.util.resolve_name(namespace, package=__package__)
    spec = importlib.util.find_spec(name)

    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for finder, name, ispkg in pkgutil.iter_modules(module.__path__):
            spec = finder.find_spec(name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


# function decorators


def node_process(requires: list[str] = []):

    def wrapper_node_process(func):

        global potential_node_processes

        fname = func.__name__
        potential_node_processes.append((fname, func, requires))

        return func

    return wrapper_node_process
