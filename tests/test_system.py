import unittest

import networkx

import getl

from getl import drawing, gg_executor
from getl import graph_util


class MyTestCase(unittest.TestCase):

    def test_something(self):

        getl.scan_for_plugins('tests.node_processes')

        gg: networkx.DiGraph = getl.getl_graph.build()

        rg, run_order = gg_executor.create_linear_run(gg)

        # running the whole process
        for np in run_order:
            rg.nodes[np]['np_func']()

        subset_extract02 = graph_util.get_process_starting_at(gg, 'extract02')
        subset_load2 = graph_util.get_process_ending_at(gg, 'load2')

        rg2, run_order2 = gg_executor.create_linear_run(subset_extract02)
        rg3, run_order3 = gg_executor.create_linear_run(subset_load2)

        drawing.draw_etl_process(gg)
        drawing.draw_etl_process(rg)
        drawing.draw_etl_process(subset_extract02)
        drawing.draw_etl_process(rg2)
        drawing.draw_etl_process(subset_load2)
        drawing.draw_etl_process(rg3)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
