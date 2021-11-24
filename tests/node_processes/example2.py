from getl.getl_graph import node_process, require_np


@require_np('transform04')
@node_process
def load5():
    print('executing load5...')


@require_np('extract01')
@require_np('transform01')
@node_process
def transform04():
    print('executing transform04...')
