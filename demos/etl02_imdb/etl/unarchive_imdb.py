import pandas
import os
import logging
import gzip
import shutil

from getl import helper
from getl.graph import node_process
from pathlib import Path


@node_process(requires=['download_imdb'])
def unarchive_imdb():

    log = logging.getLogger('getl.etl02_imdb')
    workspace_path = Path(os.path.join(os.getcwd(), 'demos/_workspace/etl02_imdb/raw_extract'))
    log.debug(f'workspace_path: {workspace_path.resolve()}')
    helper.set_workspace(workspace_path)

    raw_path = Path(os.path.join(os.getcwd(), 'demos/_workspace/etl02_imdb/raw'))

    for file in raw_path.iterdir():

        if not file.name.endswith('.gz'):
            continue

        log.debug(f'unarchiving "{file.name}"')
        with gzip.open(file, 'rb') as file_in:
            unarchive_path = workspace_path.joinpath(file.name[:-3])
            with unarchive_path.open('wb') as file_out:
                shutil.copyfileobj(file_in, file_out)

