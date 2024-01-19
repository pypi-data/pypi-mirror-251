#!/usr/bin/python3

import argparse
import sys
import os
from pathlib import Path

from file_handler import file_handler

# TODO: these need to be parameterized
# src_path = Path("/home/simsjo")
# src_file = src_path / "server.list"

# des_path = Path("/home/simsjo/tabs")
# des_file = des_path / "batch"

default_batch_size = 6


def main():
    parser = argparse.ArgumentParser(description="Splits single newline seperated host "
                                                 "file into Konsole tab batches",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="fully qualified path to host list - /path/to/list")
    parser.add_argument("dest", help="fully qualified path to output dir - /path/to/output_dir")
    parser.add_argument("-b", "--batch", help="set number of hosts per batch - default is 6")
    parser.add_argument("-n", "--name", help="set name of batches - default is batch#")

    passed_args = vars(parser.parse_args())

    src_path = passed_args["src"]
    dest_path = passed_args["dest"]
    size = passed_args["batch"]
    output_name = str(passed_args["name"])

    # TODO: refactor this to utilize "Path" from pathlib
    if not (os.path.exists(src_path)) or not (os.path.exists(dest_path)):
        print("Source or Destination not reachable")
        sys.exit()

    server_list = str(src_path)
    output_file = str(dest_path)

    file_obj = file_handler.FileHandler
    file_dict = file_obj.file_to_dict(Path(server_list))

    print(file_dict.values())
    print(len(file_dict))

    default_batch_size = len(file_dict)

    file_dict = {
        host: file_obj.text_transform(file_dict[host], "ssh") for host in file_dict
    }

    for item in file_dict.values():
        file_obj.insert_into_file(Path(output_file), item)

    for item in file_dict.items():
        print(item)
    # TODO: need to check this prior to appending to file so that it can be incremented
    # print(file_handler.check_if_file(des_file))


if __name__ == "__main__":
    main()
