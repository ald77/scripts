#! /bin/bash

# Recursively removes emacs backup files from current directory
# Note: does not descend into symlinked directories

shopt -s nullglob

clean_recur(){
    cd $1
    rm -f *~ *# .*~ .*#
    for i in $(ls -A)
    do
        if [ -d $i ] && [ ! -L $i ]
        then
            clean_recur $i
        fi
    done
    cd ..
}

clean_recur $(pwd)
