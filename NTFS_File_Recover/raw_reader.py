"""
functions for parsing Raw Images
"""
import numpy as np

import sys

END_FLAG = bytes.fromhex('ffffffff82794711')  # It's the file-end-flag of NTFS.
END_FLAG_ARRAY = np.array(bytearray(END_FLAG), dtype=np.uint8)


def get_file_name_flag(file_name: str, encoding: str = sys.getdefaultencoding()) -> bytearray:
    """

    :param file_name:
    :param encoding: the system encoding
    :return:
    """
    b = bytes(file_name, encoding=encoding)
    # 0x2100 "!\x00" is the start flag
    ba = bytearray()
    ba.append(0x21)
    ba.append(0x00)
    # 'f' will be saved as 'f\x00'
    for i in b:
        j = i << (16 - (i.bit_length() // 4 + (i.bit_length() % 4 != 0)) * 4)
        ba.append(j >> 8)
        ba.append(j & 0xff)
    return ba


def find_subsequence(source: np.array, target: np.array, times: int = 1) -> int:
    """
    :param source:
    :param target:
    :param times: Returns the index of the target when it appears `times` times. The default is 1.
    :return: Then index of target first include source.
    :raise: ValueError, if not found.
    """
    length = len(target)
    gen = match_subsequence_maybe(source, target)
    for index in gen:
        if np.all(source[index:index + length] == target):
            times -= 1
            if times == 0:
                return index
    raise ValueError


def match_subsequence_maybe(source: np.array, target: np.array):
    """
    Yield the start index, which is **maybe** target in source.
    :param source:
    :param target:
    :return:
    """
    step = len(target)
    target_start = target[0]
    start = 0
    end = 0
    for _ in range(0, len(source), step):
        start, end = end, end + step

        chunk = source[start:end]
        isin = np.isin(chunk, target_start)
        if not isin.any():
            continue
        target_maybe_relative_starts = np.arange(step)[isin]
        for i in target_maybe_relative_starts:
            if np.all(chunk[i:] == target[:step - i]):
                yield i + start
