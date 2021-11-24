from getl.getl_graph import node_process, require_np


@node_process
def extract01():
    print('executing extract01...')


@node_process
def extract02():
    print('executing extract02...')


@require_np('extract01')
@node_process
def transform01():
    print('executing transform01...')


@require_np('extract01')
@require_np('extract02')
@node_process
def transform02():
    print('executing transform02...')


@require_np('extract02')
@node_process
def transform03():
    print('executing transform03...')


@require_np('transform01')
@node_process
def load1():
    print('executing load1...')


@require_np('transform02')
@node_process
def load2():
    print('executing load2...')


@require_np('transform02')
@node_process
def load3():
    print('executing load3...')


@require_np('transform03')
@node_process
def load4():
    print('executing load4...')


