#! /bin/bash

mydir=$(pwd)

cd $ROOTSYS
sudo git pull
sudo ./configure --all
sudo nice -n 19 make -k
source bin/thisroot.sh

cd $mydir