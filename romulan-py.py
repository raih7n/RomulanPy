#!/usr/bin/python3

import os
import pefile
import argparse
import pathutils
from rich import Console
from pathlib import Path


def scan_file(path):
    console = Console()

    pe = pefile.PE(path)
    pe.parse_data_directories()

    console.print("[....] Checking  {}".format(os.path.basename(path)), end="\r")

    searched_imports = [  
        "MmMapIoSpace",
        "MmMapIoSpaceEx",
        "MmMapLockedPages",
        "MmMapLockedPagesSpecifyCache",
        "MmMapLockedPagesWithReservedMapping",
        "MmGetPhysicalAddress"]

    ntoskrnl = pe.DIRECTORY_ENTRY_IMPORT["ntoskrnl.exe"]

    found = [i for i in ntoskrnl.imports if i in searched_imports]
    if found:
        console.print("[[bold red] FAIL [/]]", end='')
        for imp in found:
            console.print("Found {} @ {}".format(imp.name, imp.address))
    else:
        console.print("[[green] OK [/]]" , end='')    


def scan_directory(path):
    for root, subdirs, files, in os.walk(path):
        


if __name__ == "__main__":
    console = Console()
    parser = argparse.ArgumentParser(description="Windows driver export scanner")
    parser.add_argument("--dir", '-d', type=str, required=True)
    args = parser.parse_args()
    path = args.dir
    
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
    

    
