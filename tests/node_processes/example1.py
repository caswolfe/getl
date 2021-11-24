from getl.getl_graph import node_process, require_np


@node_process
def extract01():
    print('executing extract01...')


@node_process
def extract02():
    print('executing extract02...')


@node_process
@require_np('extract01')
def transform01():
    print('executing transform01...')


@node_process
@require_np('extract01')
@require_np('extract02')
def transform02():
    print('executing transform02...')


@node_process
@require_np('extract02')
def transform03():
    print('executing transform03...')


@node_process
@require_np('transform01')
def load1():
    print('executing load1...')


@node_process
@require_np('transform02')
def load2():
    print('executing load2...')


@node_process
@require_np('transform02')
def load3():
    print('executing load3...')


@node_process
@require_np('transform03')
def load4():
    print('executing load4...')


