#! /usr/bin/env python

import argparse
import os
import subprocess

def EnsureDirectory(dir_path):
    real_path = os.path.expanduser(dir_path)
    if not os.path.exists(real_path):
        os.makedirs(real_path)
    return real_path

def GetSource(source_path):
    if os.listdir(source_path):
        cwd = os.getcwd()
        os.chdir(source_path)
        subprocess.call(["git","pull"])
        os.chdir(cwd)
    else:
        subprocess.call(["git","clone","http://root.cern.ch/git/root.git",source_path])

def Build(build_path, enable_all):
    cwd = os.getcwd()
    os.chdir(build_path)

    if os.path.isfile("CMakeCache.txt"):
        os.remove("CMakeCache.txt")

    cmake_args = ["cmake","-Dall:BOOL=ON"]
    if not enable_all:
        cmake_args.extend(["-Dqt:BOOL=OFF","-Dqtgsi:BOOL=OFF","-Dr:BOOL=OFF"])
    cmake_args.extend(["/usr/local/root"])
    subprocess.call(cmake_args)
    
    subprocess.call(["cmake","--build","."])
    
    os.chdir(cwd)

def main():
    parser = argparse.ArgumentParser(description="Updates ROOT, installing if necessary")
    parser.add_argument("-s", "--source", default="~/root/source", help="Directory for ROOT source code")
    parser.add_argument("-b", "--build", default="~/root/build", help="Directory for ROOT build files")
    parser.add_argument("-a", "--enable_all", action="store_true", help="Enable all packages, including those which conflict with anaconda")
    args = parser.parse_args()

    real_source = EnsureDirectory(args.source)
    real_build = EnsureDirectory(args.build)

    GetSource(real_source)
    Build(real_build, args.enable_all)

if __name__ == "__main__":
    main()
