import functools
import networkx

from matplotlib import pyplot


process_graph = networkx.DiGraph()


def draw_process_graph():
    networkx.draw(process_graph, with_labels=True)
    pyplot.show()


# def custom_wrapper(func):
#     def wrapper_custom_wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper_custom_wrapper


def node_process(func):
    fname = func.__name__
    # TODO: assert name is unique
    process_graph.add_node(fname)
    process_graph.nodes[fname]['np_func'] = func
    return func


def require_np(np_name: str):
    def decorator_require_np(func):
        fname = func.__name__
        # TODO: assert required node process exists
        process_graph.add_edge(np_name, fname)
        return func
    return decorator_require_np
