# getl (graphical etl)

## Purpose & Goals
- modular definition of an ETL process 
- simple decleration of requirements
- automatic sorting of each modular process to accodimate requirements

## Summary
- Definitions  
    - node process
        - a modular unit of python code contained within a single function
    - getl graph
        - the collection of all node processes
- The Process (see [etl01_overview.ipynb](src/etl01_overview.ipynb) and [demo_etl_1.py](src/etl01_skeleton/demo_etl_1.py) for example)
    1. define a node process withen a Python function marked by the `@node_process()` decorator
    1. load all the definitions via the `getl.scan_for_plugins` function
    1. extract the desired run graph
    1. run each function in the provided order
