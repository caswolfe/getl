import unittest

import getl

from getl import drawing


class MyTestCase(unittest.TestCase):

    def test_something(self):

        getl.scan_for_plugins('tests.node_processes')

        gg = getl.getl_graph.build()
        drawing.draw_etl_process(gg)

        # for n in getl.getl_graph.process_graph:
        #     getl.getl_graph.process_graph.nodes[n]['np_func']()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
