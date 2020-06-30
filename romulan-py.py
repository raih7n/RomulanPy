#!/usr/bin/python3

import os
import pefile
import argparse
import pathutils
from rich.console import Console
from rich.traceback import install
from pathlib import Path


def scan_file(path):
    console = Console()

    pe = pefile.PE(path)

    console.print("Checking {}...".format(os.path.basename(path)), end='')

    searched_imports = {  
        "MmMapIoSpace",
        "MmMapIoSpaceEx",
        "MmMapLockedPages",
        "MmMapLockedPagesSpecifyCache",
        "MmMapLockedPagesWithReservedMapping",
        "MmGetPhysicalAddress"}

    ntoskrnl_exe = [n for n in pe.DIRECTORY_ENTRY_IMPORT if n.dll.decode('utf-8') =='ntoskrnl.exe']
    if not ntoskrnl_exe:
        console.print("[[[green]  OK  [/]]]")
        return

    found = [i for i in ntoskrnl_exe[0].imports if i.name.decode('utf-8') in searched_imports]

    if found:
        console.print("[[[bold red] FAIL [/]]]")
        for imp in found:
            console.print("Found {} @ {}\n".format(imp.name.decode('utf-8'), hex(imp.address)))
    else:
        console.print("[[[green]  OK  [/]]]")    


def scan_directory(directory: str):
    paths = Path(directory).glob('**/*.sys')

    for path in paths:
        scan_file(str(path))


def main():
    install()
    console = Console()
    parser = argparse.ArgumentParser(description="Windows driver export scanner")
    parser.add_argument("--dir", '-d', type=str, required=True)
    args = parser.parse_args()
    path = args.dir
    
    #path = "D:\\Program Files (x86)\\EaseUS\\EaseUS Partition Master 11.10\\BUILDPE\\x64\\Windows\\System32\\epmntdrv.sys"

    if not pathutils.is_path_exists_or_creatable(path):
        console.log("Error! '{}' is not a valid path".format(path))
        exit()

    if os.path.isdir(path):
        scan_directory(path)

    elif os.path.isfile(path):
        if Path(path).suffix != ".sys":
            console.log("Error! Not a valid sys file")
            exit()
        scan_file(path)


if __name__ == "__main__":
    main()

    

    
