#!/bin/bash

errors=( "Error" "LaTeX" "Package" )
patterns=( "LaTeX(?= Error)" "LaTeX(?= Warning)" "(?<=Package )[^ ]+(?= Warning)" )
logfile=${1:-output/AN-21-207_temp.log}

[ -f $logfile ] || { echo "ERROR file not found:" $logfile >&2 ; exit 1; }

for i in "${!errors[@]}" ; do
    printf "%s: %d\n" "${errors[i]}" $(grep -cP "${patterns[i]}" $logfile)
    grep --color=always -P "${patterns[i]}" $logfile | sed "s/^/\t/g"
done
