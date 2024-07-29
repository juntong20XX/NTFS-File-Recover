---
typora-copy-images-to: ./images
---

# NTFS-File-Recover

It's a tool to recover deleted file on NTFS with FTK Imager.

FTK Imager can be replaced by any other application which can create Raw Images and mount the image as a logical volume.

Script is Windows Only.

## Usage

### Prepare

Install FTK Imager, and create a Raw-Type Image of the logical volume which your target file located.

![Create Raw Image](./images/CreateRawImage.png)

Next, mount the Image as a logical volume.

![Example Raw Image](./images/ExampleRawImage.png)

![Mount Image File](./images/MountImageFile.png)

In this example, the path of Raw Image is `E:\d-test\d-teat.001` and the target file is `F:\fake-log - Copy - Copy - Copy.txt`.

The original content of the file is shown in the left pane of the image below. I copied the file, modified the content and saved it.

![Example File](./images/ExampleFile.png)

### Run Scripts

Clone or download this project. Then change working directory into the project folder.

```bash
git clone https://github.com/juntong20XX/NTFS-File-Recover.git
cd NTFS-File-Recover
```

Next, use python to execute the script. The third-party module is `numpy`. Install it if `numpy` is not in your environment.

```bash
python -m NTFS_File_Recover -f $path_to_target_file -r $path_to_raw_image -o $path_to_output

# In this example:
path_to_target_file = 'F:\fake-log - Copy - Copy - Copy.txt'
path_to_raw_image = 'E:\d-test\d-teat.001'
path_to_output = 'output.txt'
```

You will most likely see a pop-up asking for administrator permissions. That's because `fsutil` command request permissions. So click `Yes`. If not, the script will still listen the port for data, so you should cancel the python process manually.

Finally, if there are no errors occurred, you will find the file at `$path_to_output`. Since the script will still retain binary content such as NTFS end-of-file symbols, you may need to use a hex editor to open the output file.

Run `python -m NTFS-File-Recover --help` for more information.

### Troubleshooting

- `ValueError: too many values to unpack (expected 3)`

  This is because the file storage locations are not consecutive. This situation is beyond the scope of the program can handle.

- `OSError: [WinError 10048] Only one usage of each socket address ...`

  Unfortunately, the default port (7891) has been used by another program. Try again later or specify  a new port by `--port`.

- Antivirus/Firewall Warning

  The script will briefly listen on a local port for communication, please allow this listening request.

- The program has not ended for a long time.

  Open the Task Manager and check the memory usage of the script. If the process usage is very low, there may be an error in the inter-process information transfer process. Kill the process and try to execute the script again.

## Development

The test scripts are named as `test_*`.

All project scripts can be found at `NTFS_File_Recover`.



In the future:

- Test `fsutil` before ask administrator permissions.
- Remove `numpy` depend.

- Supports large files.
