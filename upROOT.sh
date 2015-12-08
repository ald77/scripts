#! /bin/bash

mydir=$(pwd)

cd $ROOTSYS
sudo git pull
sudo ./configure --all --build=debug --cxxflags="-g -pg -O2" --cflags="-g -pg -O2"
sudo nice -n 19 make -k
source bin/thisroot.sh

cd $mydir