import pandas
import os
import logging
import gzip
import shutil
import getl

from pathlib import Path


@getl.node_process(requires=['download_imdb'])
def unarchive_imdb():

    log = logging.getLogger('getl.etl02_imdb')
    workspace_path = Path('etl02_imdb/raw_extract')
    log.debug(f'workspace_path: {workspace_path.resolve()}')

    raw_path = Path('etl02_imdb/download_dump')
    log.debug(f'raw_path: {raw_path.resolve()}')

    # TODO: uncomment after test of workspace path
    for file in raw_path.iterdir():

        if not file.name.endswith('.gz'):
            continue

        log.debug(f'unarchiving "{file.name}"')
        with gzip.open(file, 'rb') as file_in:
            unarchive_path = workspace_path.joinpath(file.name[:-3])
            with unarchive_path.open('wb') as file_out:
                shutil.copyfileobj(file_in, file_out)