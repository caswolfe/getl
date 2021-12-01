from getl.graph import node_process


@node_process()
def E1():
    print('executing extract01...')


@node_process()
def E2():
    print('executing extract02...')


@node_process(requires=['E1'])
def T1():
    print('executing transform01...')


@node_process(requires=['E1', 'E2'])
def T2():
    print('executing transform02...')


@node_process(requires=['E2'])
def T3():
    print('executing transform03...')


@node_process(requires=['T1'])
def L1():
    print('executing load1...')


@node_process(requires=['T2'])
def L2():
    print('executing load2...')


@node_process(requires=['T2'])
def L3():
    print('executing load3...')


@node_process(requires=['T3'])
def L4():
    print('executing load4...')
