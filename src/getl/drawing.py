import networkx
from matplotlib import pyplot


def draw_etl_process(graph: networkx.Graph):

    pos = networkx.multipartite_layout(
        graph,
        subset_key='np_generation',
        align='horizontal',
    )
    networkx.draw(
        graph,
        pos=pos,
        with_labels=True,
    )
    pyplot.show()
