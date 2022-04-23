import argparse
import getl
import networkx
import logging


def main():

    parser = argparse.ArgumentParser(description='run getl')

    parser.add_argument('namespace')
    parser.add_argument('--start', nargs='*', default=[])
    parser.add_argument('--end', nargs='*', default=[])

    pg_lists = parser.add_mutually_exclusive_group()
    pg_lists.add_argument('--whitelist', '--only', nargs='*', default=[])
    pg_lists.add_argument('--blacklist', nargs='*', default=[])

    parser.add_argument('--log', action='store_true', default=False)

    args = parser.parse_args()

    if args.log:
        getl.set_logger_to_console('getl')

    run(
        namespace=args.namespace,
        start_nodes=args.start,
        end_nodes=args.end,
        whitelist=args.whitelist,
        blacklist=args.blacklist,
    )


def run(namespace, start_nodes=[], end_nodes=[], whitelist=[], blacklist=[]):

    log = logging.getLogger('getl')
    log.info('running:')
    log.info(f'\tnamespace: {namespace}')
    log.info(f'\tstart_nodes: {start_nodes}')
    log.info(f'\tend_nodes: {end_nodes}')
    log.info(f'\twhitelist: {whitelist}')
    log.info(f'\tblacklist: {blacklist}')

    assert (len(whitelist) == 0 and len(blacklist) >= 0) \
        or (len(whitelist) >= 0 and len(blacklist) == 0), \
        "whitelist and blacklist are mutually exclusive!"

    getl.scan_for_plugins(namespace)
    gg: networkx.DiGraph = getl.build()
    graph = getl.get_processes_between(gg, start_nodes=start_nodes, end_nodes=end_nodes)

    if len(blacklist) != 0:
        nodes_to_remove = blacklist.copy()
    elif len(whitelist) != 0:
        node_list = [i for i in graph.nodes]
        nodes_to_remove = [i for i in node_list if i not in whitelist]
    else:
        nodes_to_remove = []

    subset_graph = graph.copy()
    while len(nodes_to_remove) > 0:
        subset_graph.remove_node(nodes_to_remove.pop())

    run_order = getl.create_linear_run(subset_graph)
    for np in run_order:
        log.debug(f'running {np}')
        subset_graph.nodes[np]['np_func']()

    # getl.draw_etl_process(gg, '1) gg')
    # getl.draw_etl_process(graph, '2) graph')
    # getl.draw_etl_process(subset_graph, '3) subset_graph')
    # getl.draw_etl_process(rg, '4) rg')


if __name__ == '__main__':
    main()
