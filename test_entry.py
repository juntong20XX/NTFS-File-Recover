"""
The test entry.
"""

from NTFS_File_Recover import main

raw_path = r"E:\d-test\d-test.001.raw"
file_name = r"F:\fake-log - Copy - Copy - Copy.txt"

b = main(raw_path, file_name)

with open("output.txt", "wb") as fp:
    fp.write(b)

print(b.decode("utf-8"))
