#! /bin/bash

# Searches currect directory for a file with a given name and prints full paths to all files found with that name
# Use: search.sh some_file_name_with_unknown_path
# Notes
#  -Searches for regexes should put the searched file name in single quotes (search.sh 'abc*xyz')
#  -Does not search symlinks (to avoid infinite recursion)
#  -Need to add support for searching for directories


shopt -s nullglob

search_recur(){
    cd "$2"
    curdir=$(pwd)

    for i in $(ls -A)
    do
	if [[ $i == $1 ]]
	then
	    echo $curdir/$i
	fi
        if [ -d $i ] && [ -r $i ] && [ -x $i ] && [ ! -L $i ]
        then
            search_recur "$1" "$i"
        fi
    done
    cd ..
}

curdir=$(pwd)
file=$1

search_recur "$file" "$curdir"
