"""
Get file offset.
Run this file as administrator, with [file_path] [PORT], to send command output as a connector.
"""
import re
import sys
import time
import ctypes
import socket
import pathlib
import socketserver
import subprocess as sp
from threading import Thread


def is_admin() -> bool:
    """
    Windows Only
    :return:
    """
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_python_script_as_admin(script_path: str, *parameters):
    parameter = script_path + " " + " ".join(str(i) for i in parameters)
    return run_as_admin(sys.executable, parameter)


def run_as_admin(exe: str, parameters: str = ""):
    return ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, parameters, None, 1)


class Handler(socketserver.StreamRequestHandler):
    """
    """

    def handle(self):
        timing = time.time()
        while True:
            lines = self.rfile.readline().strip()
            data = b""
            for i in range(int(lines.decode("ascii")) + 1):
                data += self.rfile.readline()
            data = data[:-1]
            self.server.data.append(data)
            # print(data)
            self.wfile.write(data[:1024])
            self.wfile.flush()
            if self.rfile.readline().strip() == b"y":
                self.wfile.write(b"quit")
                self.wfile.flush()
                break
        if data == b"%d<->quit" % int(timing):
            self.shutdown()

    def shutdown(self, seconds=2):
        """
        Start a thread which call `self.server.shutdown` after `seconds` seconds.
        """

        def target():
            time.sleep(seconds)
            self.server.shutdown()

        thread = Thread(target=target)
        thread.start()
        return thread


def listen(port: int) -> list[bytes]:
    """
    Return the data sent by `sand_data` or `send_output`.
    :param port: TCP port
    :return:
    """
    with socketserver.TCPServer(("localhost", port), Handler) as server:
        server.data = data = []
        server.serve_forever()
        return data


def send_output(port: int, command: str):
    """
    send output to server at "localhost:{port}"
    """
    data = sp.run(command, shell=True, stdout=sp.PIPE, timeout=10)
    send_data(port, data.stdout)


def send_data(port, data: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", port))
        while True:
            sock.sendall(str(data.count(b"\n")).encode("ascii") + b"\n" + data + b"\n")
            if sock.recv(1024) == data[:1024]:
                sock.send(b"y\n")
                if sock.recv(1024) == b"quit":
                    break
            else:
                sock.send(b"n\n")


def send_quit(port):
    send_data(port, b"%d<->quit" % int(time.time()))


def get_mft_offset_from_fsutil_file_output(output: str):
    vcn, clusters, lcn = re.findall(r" 0x([\dabcdef]+)", output)
    return int(lcn, 16) * 4096


def get_file_displacement_relative_to_mft_from_fsutil_volume_output(output: str):
    ref_number = output.splitlines()[2]
    count = int(ref_number[-4:], 16)
    return count * 1024


def get_file_offset(data):
    """
    Get file offset from data.
    :param data: `listen` returned.
    :return:
    """
    fsutil_file_output = data[0].decode(sys.getdefaultencoding(), "ignore")
    fsutil_volume_output = data[1].decode(sys.getdefaultencoding(), "ignore")
    return (get_mft_offset_from_fsutil_file_output(fsutil_file_output) +
            get_file_displacement_relative_to_mft_from_fsutil_volume_output(fsutil_volume_output))


if __name__ == "__main__":
    if not is_admin():
        print("please run as administrator")
        exit()
    server_port = sys.argv[-1]
    assert server_port.isnumeric(), ValueError(f"{server_port} is not numeric")
    file_path = sys.argv[-2]  # eg: "F:\log.txt"
    drive = pathlib.Path(file_path).drive
    server_port = int(server_port)
    send_output(server_port, " ".join(["fs""util", "file", "queryExtents", drive]))
    send_output(server_port, " ".join(["fs""util", "volume", "fileLayout", file_path]))
    send_quit(server_port)
