import networkx
import networkx as nx
import matplotlib

from matplotlib import pyplot


process_graph = networkx.DiGraph()
generation_min = 1


def draw_etl_process():

    global process_graph
    global generation_min

    print(nx.get_node_attributes(process_graph, 'np_func'))
    print(nx.get_node_attributes(process_graph, 'np_generation'))

    pos = networkx.multipartite_layout(
        process_graph,
        subset_key='np_generation',
        align='horizontal',
    )

    networkx.draw(
        process_graph,
        pos=pos,
        # node_color=list(nx.get_node_attributes(process_graph, 'np_generation').values()),
        # vmin=generation_min,
        # vmax=0,
        # cmap=matplotlib.cm.get_cmap('summer'),
        with_labels=True,
    )
    pyplot.show()


# def custom_wrapper(func):
#     def wrapper_custom_wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper_custom_wrapper


def node_process(func):

    global process_graph

    fname = func.__name__

    assert fname not in process_graph.nodes, 'node_process name must be unique'

    process_graph.add_node(fname)
    process_graph.nodes[fname]['np_func'] = func
    process_graph.nodes[fname]['np_generation'] = 0

    return func


def require_np(np_name: str):

    def decorator_require_np(func):

        global process_graph
        global generation_min

        fname = func.__name__

        # assert np_name in process_graph.nodes, 'provided node_process does not exist'

        process_graph.add_edge(np_name, fname)

        generation = min(
            process_graph.nodes[fname]['np_generation'],
            process_graph.nodes[np_name]['np_generation'] - 1,
        )
        process_graph.nodes[fname]['np_generation'] = generation
        generation_min = min(generation_min, generation)

        return func

    return decorator_require_np
