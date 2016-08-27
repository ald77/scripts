#! /usr/bin/env python

import argparse
import os
import subprocess
import errno
import multiprocessing
import glob
import sys

def fullPath(path):
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))

def ensureDir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def updateSource(source_dir):
    orig_dir = os.getcwd()
    os.chdir(source_dir)
    try: subprocess.check_call(["git","pull"])
    finally: os.chdir(orig_dir)

def includeDir():
    base_path = os.path.join(sys.prefix,"include")
    version = sys.version_info
    subdir = "python"+str(version.major)+"."+str(version.minor)+"*"
    return glob.glob(os.path.join(base_path,subdir))[-1]

def libFile():
    base_path = os.path.join(sys.prefix,"lib")
    version = sys.version_info
    filename = "libpython"+str(version.major)+"."+str(version.minor)+"*.dylib"
    return glob.glob(os.path.join(base_path,filename))[-1]

def build(source_dir, build_dir):
    ensureDir(build_dir)
    orig_dir = os.getcwd()
    os.chdir(build_dir)
    try:
        config = ["cmake"]
        if sys.version_info.major >= 3 and sys.version_info.minor >= 1:
            config.append("-Dpython3:BOOL=ON")
        config.extend(["-DPYTHON_EXECUTABLE:PATH="+sys.executable,
                       "-DPYTHON_INCLUDE_DIR:PATH="+includeDir(),
                       "-DPYTHON_LIBRARY:PATH="+libFile(),
                       "-Droofit:BOOL=ON","-Dminuit2:BOOL=ON",
                       "-Drpath:BOOL=ON","-Dlibcxx:BOOL=ON",
                       source_dir])

        subprocess.check_call(config)
        subprocess.call(["cmake","--build",".","--","-k","-j",str(multiprocessing.cpu_count())])
    finally:
        os.chdir(build_dir)

def fixLinks(build_dir):
    lib_dir = os.path.join(sys.prefix,"lib")
    for f in glob.glob(os.path.join(build_dir, "lib/*.so")):
        out=subprocess.check_output(["otool","-L",f])
        for line in out.decode("utf-8").splitlines():
            if not line.startswith("\t"): continue
            if line.startswith("\t@rpath") or line.startswith("\t/"): continue
            libname = line.split()[0]
            subprocess.call(["install_name_tool","-change",
                              libname, os.path.join(lib_dir, libname), f])

def upROOT(source_dir, build_dir):
    source_dir = fullPath(source_dir)
    build_dir = fullPath(build_dir)

    try: subprocess.check_call(["git","clone","http://root.cern.ch/git/root.git", source_dir])
    except subprocess.CalledProcessError as e:
        updateSource(source_dir)

    build(source_dir, build_dir)
    fixLinks(build_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Updates ROOT, installing if necessary",
                                      formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--source", default="~/root/source",
                        help="Directory for ROOT source code")
    parser.add_argument("--build", default="~/root/build",
                        help="Directory for ROOT build files")
    args = parser.parse_args()

    upROOT(args.source, args.build)
