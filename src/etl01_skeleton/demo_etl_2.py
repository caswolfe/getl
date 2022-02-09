import getl


@getl.node_process(requires=['T4'])
def L5():
    print('executing load5...')


@getl.node_process(requires=['E1', 'T1'])
def T4():
    print('executing transform04...')
