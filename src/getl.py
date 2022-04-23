import logging
import networkx
import os
import pandas
import re
import sys

from matplotlib import pyplot
from pathlib import Path
from typing import Any, Dict, List

_potential_node_processes = []

# ---------------
# -- FUNCTIONS --
# ---------------


def build() -> networkx.DiGraph:
    """
    Creates a getl graph from functions stored in the global
    "potential_node_processes" variable, respecting given requirements.
    (Functions will exist in potential_node_processes if
    they are loaded with the @node_process function decorator)

    Returns:
        a getl graph
    """
    global _potential_node_processes

    log = logging.getLogger('getl')
    log.info('building...')

    process_graph = networkx.DiGraph()

    np_processed = []
    np_to_process = _potential_node_processes.copy()

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


def clear_dir_recurse(directory: Path):
    """
    Recursively clears a directory of all files but leaves folders.

    Args:
        directory: path of the top-level folder to clean
    """

    if str(directory) == '':
        return

    for root, subdirs, files in os.walk(directory):
        for file in files:
            if file != '.gitignore':
                os.unlink(os.path.join(root, file))


def create_linear_run(process_graph: networkx.DiGraph) -> List[str]:
    """
    Iterates through a graph and creates a run order based off of 'np_generation'.

    Args:
        process_graph: a getl graph

    Returns:
        a list of all nodes in a pathed order
    """
    node_gen_dict = dict()

    for node in process_graph.nodes:
        node_gen = process_graph.nodes[node]['np_generation']
        if node_gen not in node_gen_dict.keys():
            node_gen_dict[node_gen] = [node]
        else:
            node_gen_dict[node_gen].append(node)

    node_master_list: List[str] = []
    gen_high = max(node_gen_dict.keys())
    gen_low = min(node_gen_dict.keys()) - 1
    for i in range(gen_high, gen_low, -1):
        for np in node_gen_dict[i]:
            node_master_list.append(np)

    return node_master_list


def create_linear_run_graph(process_graph: networkx.DiGraph, node_master_list) -> networkx.DiGraph:
    """
    Creates a new graph with new edges from the run order.

    Args:
        process_graph: a getl graph
        node_master_list: a linear run from create_linear_run

    Returns:
        a getl graph reorganized to a single path
    """
    run_graph: networkx.DiGraph = networkx.create_empty_copy(process_graph)
    for i in range(1, len(node_master_list)):
        run_graph.add_edge(
            node_master_list[i-1],
            node_master_list[i]
        )

    return run_graph


def draw_etl_process(graph: networkx.Graph, title='', node_color='#1f78b4'):
    """
    using pyplot, create & show the graph sorted by each node's 'np_generation'

    Args:
        graph: a getl graph
        title: for the graph
        node_color: color of the nodes
    """
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


def find_in_csv(workspace_path: Path, column_name: str, obj: str) -> Dict[str, pandas.DataFrame]:
    """
    Searches all csv files in the workspace_path for lines with the matching obj in the specified column.

    Args:
        workspace_path: directory to search
        column_name: column name to search under
        obj: target to find

    Returns:
        a dictionary with the keys of the dataframe file names and the values those dataframes themselves
    """

    log = logging.getLogger('getl')

    match_dict = dict()

    for root, sub_dirs, files in os.walk(workspace_path):
        for filename in files:

            if '.csv' not in filename:
                continue

            file_path = Path(os.path.join(root, filename))
            log.debug(f'touching {file_path.resolve()}')
            with file_path.open() as file_obj:

                line = file_obj.readline()
                column_matches = re.match(column_name, line)
                if not column_matches:
                    continue

                log.debug(f'column match!')
                df_matches = pandas.read_csv(file_path, dtype=str)
                df_matches = df_matches[df_matches[column_name].str.match(obj)]

            match_dict.update({file_path.name: df_matches.copy()})

    return match_dict


def get_process_starting_at(graph: networkx.DiGraph, node: Any) -> networkx.DiGraph:
    """
    Extracts the node and all its descendants from the graph.

    Args:
        graph: a getl graph
        node: the node to act as a root in the subset graph

    Returns:
        the subset graph
    """
    subset_include = list(networkx.descendants(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        subset_graph.remove_node(subset_exclude.pop())

    return subset_graph


def get_process_ending_at(graph: networkx.DiGraph, node: Any):
    """
    Extracts the node and all its ancestors from the graph.

    Args:
        graph: a getl graph
        node: the node to act as a root in the subset graph

    Returns:
        the subset graph
    """
    subset_include = list(networkx.ancestors(graph, node)) + [node]
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        subset_graph.remove_node(subset_exclude.pop())

    return subset_graph


def get_process_between(graph: networkx.DiGraph, node_start, node_end):
    """
    Extracts the start, end, and all nodes from start to end.

    Args:
        graph: a getl graph
        node_start: the graph node to start from
        node_end: the graph node to end at

    Returns:
        the subset graph
    """
    graph_path = networkx.all_simple_paths(graph, source=node_start, target=node_end)
    subset_include = set()
    for gp in graph_path:
        subset_include.update(gp)
    subset_exclude = [n for n in graph.nodes if n not in subset_include]
    subset_graph = graph.copy()

    while len(subset_exclude) > 0:
        subset_graph.remove_node(subset_exclude.pop())

    return subset_graph


def get_processes_between(graph: networkx.DiGraph, start_nodes=[], end_nodes=[]):
    """
    Extracts the start, end, and all nodes from start to end - for any number of starts & ends (including 0)

    Args:
        graph: a getl graph
        start_nodes: the graph nodes to start from
        end_nodes: the graph nodes to end at

    Returns:
        the subset graph
    """
    if len(start_nodes) == 0 and len(end_nodes) == 0:
        return graph.copy()
    elif len(start_nodes) == 0:
        grouping_sets = [('', end_node) for end_node in end_nodes]
    elif len(end_nodes) == 0:
        grouping_sets = [(start_node, '') for start_node in start_nodes]
    else:
        grouping_sets = [(start_node, end_node) for end_node in end_nodes for start_node in start_nodes]

    subset_graphs = []
    for (start_node, end_node) in grouping_sets:

        if start_node == '':
            gs_graph = get_process_ending_at(graph, end_node)
        elif end_node == '':
            gs_graph = get_process_starting_at(graph, start_node)
        else:
            gs_graph = get_process_between(graph, start_node, end_node)

        subset_graphs.append(gs_graph)

    return networkx.compose_all(subset_graphs)


def scan_for_plugins(namespace):
    """
    https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/

    Args:
        namespace:
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


def set_logger_to_console(log_name: str, log_level=logging.DEBUG):
    """
    sets the log to print to the console, with some formatting

    Args:
        log_name: log name
        log_level: default logging.DEBUG, see https://docs.python.org/3/library/logging.html#logging-levels
    """
    log = logging.getLogger(log_name)
    log.setLevel(log_level)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d] %(message)s"
    )

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)


# -------------------------
# -- FUNCTION DECORATORS --
# -------------------------


def node_process(requires: list[str] = []):
    """
    function decorator to add a function to the node_process graph, will be a child of all required nodes

    Args:
        requires: a list of function names of node processes

    Returns:
        the wrapper function
    """

    def wrapper_node_process(func):

        global _potential_node_processes

        fname = func.__name__
        _potential_node_processes.append((fname, func, requires))

        return func

    return wrapper_node_process

