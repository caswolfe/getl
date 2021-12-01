import logging

import networkx

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

    log = logging.getLogger('getl')

    process_graph = networkx.DiGraph()

    np_processed = []
    np_to_process = potential_node_processes.copy()

    while len(np_to_process) > 0:

        (fname, func, requires) = np_to_process.pop()
        generation = 0

        log.debug(f'processing "{fname}", requiring {requires}')

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
        assert fname not in process_graph.nodes, f'node_process name "{fname}" must be unique'
        process_graph.add_node(fname)
        process_graph.nodes[fname]['np_func'] = func
        process_graph.nodes[fname]['np_generation'] = generation

        if len(requires) != 0:
            for requirement in requires:
                process_graph.add_edge(requirement, fname)

        np_processed.append(fname)

    return process_graph

# def custom_wrapper(func):
#     def wrapper_custom_wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper_custom_wrapper
