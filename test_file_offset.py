from NTFS_File_Recover import file_offset

import sys


PORT = 7891


file_offset.run_python_script_as_admin(file_offset.__file__, r"D:\file.txt", PORT)
data = file_offset.listen(PORT)

print(data)

fsutil_file_output = data[0].decode(sys.getdefaultencoding(), "ignore")
fsutil_volume_output = data[1].decode(sys.getdefaultencoding(), "ignore")

print("get_mft_offset_from_fsutil_file_output:",
      file_offset.get_mft_offset_from_fsutil_file_output(fsutil_file_output))
print("get_file_displacement_relative_to_mft_from_fsutil_volume_output",
      file_offset.get_file_displacement_relative_to_mft_from_fsutil_volume_output(fsutil_volume_output))
