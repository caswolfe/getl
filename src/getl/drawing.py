import networkx
from matplotlib import pyplot


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
