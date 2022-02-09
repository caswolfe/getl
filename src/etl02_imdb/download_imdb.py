import requests
import os
import logging
import getl

from pathlib import Path

file_names = [
    'name.basics',
    'title.akas',
    # 'title.basics',
    # 'title.crew',
    # 'title.episode',
    # 'title.principals',
    # 'title.ratings',
]


@getl.node_process()
def download_imdb():
    """
    Downloads the imdb database
    https://www.imdb.com/interfaces/
    """

    log = logging.getLogger('getl.etl02_imdb')
    workspace_path = Path('download_dump')
    log.debug(f'workspace_path: {workspace_path.resolve()}')

    # TODO: uncomment after test of workspace path
    # for fn in file_names:
    #     download_imdb_file(fn, workspace_path, log)


def download_imdb_file(prefix: str, dump_dir: Path, log: logging.Logger):

    rqst = requests.get(f'https://datasets.imdbws.com/{prefix}.tsv.gz', stream=True)
    log.debug(f'{prefix} rqst.status_code: {rqst.status_code}')
    prefix_fname = f'{prefix.replace(".", "_")}.tsv.gz'

    path_dump = Path(dump_dir).joinpath(prefix_fname)
    with path_dump.open('wb') as f:
        for chunk in rqst.raw.stream(1024, decode_content=False):
            if chunk:
                f.write(chunk)