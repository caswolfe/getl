import networkx


def create_linear_run(process_graph: networkx.DiGraph):  # , flags=util.get_default_flags()

    node_gen_dict = dict()
    run_graph: networkx.DiGraph = networkx.create_empty_copy(process_graph)

    for node in process_graph.nodes:
        print(f'node: {node}')
        node_gen = process_graph.nodes[node]['np_generation']
        print(f'gen: {node_gen}')
        if node_gen not in node_gen_dict.keys():
            node_gen_dict[node_gen] = [node]
        else:
            node_gen_dict[node_gen].append(node)

    node_master_list = []
    gen_high = max(node_gen_dict.keys())
    gen_low = min(node_gen_dict.keys()) - 1
    for i in range(gen_high, gen_low, -1):
        for np in node_gen_dict[i]:
            node_master_list.append(np)

    for i in range(1, len(node_master_list)):
        run_graph.add_edge(
            node_master_list[i-1],
            node_master_list[i]
        )

    return run_graph, node_master_list
