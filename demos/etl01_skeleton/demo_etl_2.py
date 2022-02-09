from getl.graph import node_process


@node_process(requires=['T4'])
def L5():
    print('executing load5...')


@node_process(requires=['E1', 'T1'])
def T4():
    print('executing transform04...')
