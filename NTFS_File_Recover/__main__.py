"""

"""
from . import get_bytes

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--raw", "--raw_path", type=Path,
                    help="path of Raw Image")
parser.add_argument("-f", "--file", "--file_path", type=Path,
                    help="path to Target File on mounted logical volume")
parser.add_argument("-o", "--output", type=Path,
                    help="path to dump output")
parser.add_argument("--encoding", default="ascii", type=str,
                    help="encode of NTFS")
parser.add_argument("--port", default="7891", type=int,
                    help="port for TCP server")


def main(parse: argparse.Namespace):
    b = get_bytes(raw_path=parse.raw, file_path=parse.file, port=parse.port, encoding=parse.encoding)
    with open(parse.output, "wb") as fp:
        fp.write(b)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
