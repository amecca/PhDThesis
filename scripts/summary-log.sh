#!/bin/bash

errors=(  "Compilation" "Error" "LaTeX" "Package" "Overfull hbox" "Underfull vbox" )
patterns=( "^l.[\d]+" "LaTeX(?= Error)" "LaTeX( [^ ]+)*(?= Warning)" "(?<=Package )[^ ]+(?= Warning)" "Overfull \\\\hbox" "Underfull \\\\vbox" )
options=( "-A3" "" "" "" "-q" "-q" )
logfile=${1:-output/AN-21-207_temp.log}

[ -f $logfile ] || { echo "ERROR file not found:" $logfile >&2 ; exit 1; }

for i in "${!errors[@]}" ; do
    printf "%s: %d\n" "${errors[i]}" $(grep -cP "${patterns[i]}" $logfile)
    grep --color=always -P ${options[i]} "${patterns[i]}" $logfile | sed "s/^/\t/g"
done
