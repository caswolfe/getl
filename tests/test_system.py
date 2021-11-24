import unittest

from matplotlib import pyplot

import getl


class MyTestCase(unittest.TestCase):

    def test_something(self):

        getl.scan_for_plugins('tests.node_processes')
        getl.getl_graph.draw_process_graph()
        pyplot.show()

        for n in getl.getl_graph.process_graph:
            getl.getl_graph.process_graph.nodes[n]['np_func']()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
