#! /bin/bash

if [ -n "$CMSSW_BASE" ]
then
    curdir=$(pwd)
    cd $CMSSW_BASE/src
    scram b -j 15 -k
    cd $curdir
fi