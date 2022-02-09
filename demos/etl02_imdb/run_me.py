import getl
from getl import drawing, executor, graph, helper
import networkx

helper.set_logger_to_console('getl')
# helper.set_logger_to_console('getl.etl02_imdb')

getl.scan_for_plugins('demos.etl02_imdb.etl')

gg: networkx.DiGraph = graph.build()
rg, run_order = executor.create_linear_run(gg)

# drawing.draw_etl_process(gg, 'getl graph')

for np in run_order:
    rg.nodes[np]['np_func']()
