#! /usr/bin/env python

from __future__ import print_function

import argparse
import fnmatch
import re
import os

def testPath(path, regex):
    if regex.match(path):
        print(path)

def fileSearch(file_name, search_dirs):
    regex=re.compile(fnmatch.translate("*"+file_name+"*"))
    for search_dir in search_dirs:
        for root, dirs, files in os.walk(search_dir):
            for d in dirs:
                testPath(os.path.join(root, d), regex)
            for f in files:
                testPath(os.path.join(root, f), regex)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds files matching a given name/pattern within a directory.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file_name",
                        help="File name to search for. This may contain wildcards and will be matched against the full path of files within the search directory.")
    parser.add_argument("search_dirs", default=["."], nargs="*",
                        help="Directory or directories to search for the given file.")
    args = parser.parse_args()

    fileSearch(args.file_name, args.search_dirs)
