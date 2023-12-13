#!/bin/bash

errors=(  "Compilation" "Error" "LaTeX" "Package" )
patterns=( "^l.[\d]+" "LaTeX(?= Error)" "LaTeX( [^ ]+)*(?= Warning)" "(?<=Package )[^ ]+(?= Warning)" )
options=( "-A3" "" "" "" "" )
logfile=${1:-output/AN-21-207_temp.log}

[ -f $logfile ] || { echo "ERROR file not found:" $logfile >&2 ; exit 1; }

for i in "${!errors[@]}" ; do
    printf "%s: %d\n" "${errors[i]}" $(grep -cP "${patterns[i]}" $logfile)
    grep --color=always -P ${options[i]} "${patterns[i]}" $logfile | sed "s/^/\t/g"
done
