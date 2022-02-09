import os
import sys
import logging
import re
import pandas

from typing import Dict
from pathlib import Path


def find_in_csv(workspace_path: Path, column_name: str, obj: str) -> Dict[str, pandas.DataFrame]:
    """
    Searches all csv files in the workspace_path for lines with the matching obj in the specified column.

    :param workspace_path:
    :param column_name:
    :param obj:
    :return:
    """

    log = logging.getLogger('getl')

    match_dict = dict()

    for root, sub_dirs, files in os.walk(workspace_path):
        for filename in files:

            if '.csv' not in filename:
                continue

            file_path = Path(os.path.join(root, filename))
            log.debug(f'touching {file_path.resolve()}')
            with file_path.open() as file_obj:

                line = file_obj.readline()
                column_matches = re.match(column_name, line)
                if not column_matches:
                    continue

                log.debug(f'column match!')
                df_matches = pandas.read_csv(file_path, dtype=str)
                df_matches = df_matches[df_matches[column_name].str.match(obj)]

            match_dict.update({file_path.name: df_matches.copy()})

    return match_dict


def set_logger_to_console(log_name: str):

    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d] %(message)s"
    )

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)


def set_workspace(workspace: Path):

    print(workspace.resolve())

    if not workspace.exists():
        workspace.mkdir()
    else:
        clear_dir_recurse(workspace)


def clear_dir_recurse(directory: Path) -> None:
    """ Recursively clears a directory of all files but leaves directories."""

    for root, subdirs, files in os.walk(directory):
        for file in files:
            os.unlink(os.path.join(root, file))
