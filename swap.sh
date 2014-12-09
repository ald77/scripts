#! /usr/bin/env bash

if [ $# -eq 2 ]
then
    if [ -f $1 ] && [ -f $2 ]
    then
	tmp_file=mktemp
	mv $1 $tmp_file
	mv $2 $1
	mv $tmp_file $2
	rm -f $tmp_file
    elif [ -d $1 ] && [ -d $2 ]
    then
	tmp_dir=mktemp -d
	mv $1 $tmp_dir
	mv $2 $1
	mv $tmp_dir $2
	rm -f $tmp_dir
    fi
fi
