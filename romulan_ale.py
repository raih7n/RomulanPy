#!/usr/bin/python3

import os
import sys
import argparse
import pathlib
import pefile

import rich.traceback
from rich.console import Console

import pathutils

def scan_file(path: str):
    console = Console(width=40)
    driver = pefile.PE(path)

    console.print("Checking {}...".format(os.path.basename(path)), end='', justify="left")
    searched_imports = {
        "MmMapIoSpace",
        "MmMapIoSpaceEx",
        "MmMapLockedPages",
        "MmMapLockedPagesSpecifyCache",
        "MmMapLockedPagesWithReservedMapping",
        "MmGetPhysicalAddress"}

    ntoskrnl_exe = [n for n in driver.DIRECTORY_ENTRY_IMPORT
                    if n.dll.decode('utf-8') == 'ntoskrnl.exe']

    if not ntoskrnl_exe:
        console.print("[[[green]  OK  [/]]]", justify="right")
        return

    found = [i for i in ntoskrnl_exe[0].imports if i.name.decode('utf-8') in searched_imports]

    if found:
        console.print("[[[bold red] FAIL [/]]]", justify="right")
        for imp in found:
            console.print("Found {} @ {}\n\n".format(
                imp.name.decode('utf-8'), hex(imp.address)))
    else:
        console.print("[[[green]  OK  [/]]]", justify="right")


def scan_directory(directory: str):
    paths = pathlib.Path(directory).glob('**/*.sys')

    for path in paths:
        scan_file(str(path))


def main():
    rich.traceback.install()
    console = Console()

    parser = argparse.ArgumentParser(description="Windows driver export scanner")
    parser.add_argument('--path', '-p', type=str, required=True, help="File or directory to scan")
    args = parser.parse_args()
    path =  args.path

    if not pathutils.is_path_exists_or_creatable(path):
        console.print("Error! '{}' is not a valid path".format(path))
        sys.exit()

    if os.path.isdir(path):
        scan_directory(path)

    elif os.path.isfile(path):
        if pathlib.Path(path).suffix != ".sys":
            console.print("Error! Not a valid sys file")
            sys.exit()
        scan_file(path)


if __name__ == "__main__":
    main()
