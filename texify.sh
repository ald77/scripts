#! /bin/bash

shopt -s nullglob

texify(){
    orig_dir=$(pwd)
    cd $1
    for i in $(ls -A)
    do
	if [ -f $i ] && [ "${i: -4}" == ".tex" ]
	then
            pdfname=$(basename "$i" .tex).pdf
	    if [ ! -f $pdfname ] || [ $i -nt $pdfname ]
	    then
		echo "Compiling $i"
		pdflatex --shell-escape $i 1> /dev/null
		auxname=$(basename "$i" .tex).aux
		logname=$(basename "$i" .tex).log
		rm -f $auxname $logname
	    else
		echo "Skipping $i"
	    fi
	fi
    done
    cd $orig_dir
}

if [ $# == 0 ]
then
    texify .
else
    for i in $@
    do
	texify $i
    done
fi
