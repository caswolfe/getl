import unittest
import networkx
import getl

from getl import drawing, executor, graph, graph_util


class MyTestCase(unittest.TestCase):

    def test_something(self):

        getl.scan_for_plugins('tests.node_processes')

        gg: networkx.DiGraph = graph.build()

        rg, run_order = executor.create_linear_run(gg)

        # running the whole process
        print('\n\nrun order 1')
        for np in run_order:
            rg.nodes[np]['np_func']()

        subset_extract02 = graph_util.get_process_starting_at(gg, 'extract02')
        subset_load2 = graph_util.get_process_ending_at(gg, 'load2')

        rg2, run_order2 = executor.create_linear_run(subset_extract02)
        rg3, run_order3 = executor.create_linear_run(subset_load2)

        print('\n\nrun order 1')
        for np in run_order2:
            rg.nodes[np]['np_func']()
        print('\n\nrun order 1')
        for np in run_order3:
            rg.nodes[np]['np_func']()

        drawing.draw_etl_process(gg, 'getl graph')
        drawing.draw_etl_process(subset_extract02, 'process starting at "extract02"')
        drawing.draw_etl_process(subset_load2, 'process ending at "load2"')
        drawing.draw_etl_process(rg, 'running graph')
        drawing.draw_etl_process(rg2, 'running graph of "process starting at "extract02""')
        drawing.draw_etl_process(rg3, 'running graph of "process ending at "load2""')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
