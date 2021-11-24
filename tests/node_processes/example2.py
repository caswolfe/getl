from getl.getl_graph import node_process


@node_process(requires=['transform04'])
def load5():
    print('executing load5...')


@node_process(requires=['extract01', 'transform01'])
def transform04():
    print('executing transform04...')
