"""

"""
from . import file_offset
from .file_offset import run_as_admin, listen, get_file_offset
from .raw_reader import get_file_name_flag, find_subsequence, END_FLAG_ARRAY

import os
import numpy as np


def get_bytes(raw_path: str, file_path: str, port: int = 7891, encoding="ascii") -> bytes:
    """
    Get the binary of the file.
    :param raw_path:
    :param file_path:
    :param port:
    :param encoding:
    :return:
    """
    file_offset.run_python_script_as_admin(file_offset.__file__, file_path, port)
    data = listen(port)
    offset = get_file_offset(data)

    file = np.fromfile(raw_path, dtype=np.uint8)[offset:]
    file_name_flag = np.array(get_file_name_flag(os.path.basename(file_path), encoding), dtype=np.uint8)
    find = find_subsequence(file, file_name_flag)
    length = len(file_name_flag)
    ending = find_subsequence(file[find + length:], END_FLAG_ARRAY, times=2) + find
    return file[find + length:ending].tobytes()
