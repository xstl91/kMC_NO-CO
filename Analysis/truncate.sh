#!/bin/sh
# usage: truncate.sh 0 1 2, list suffix number for truncation
# run under main directory

for i in $*
do
    last_step=`grep steps traj_$i.py | tail -1 | awk '{gsub(".*\\\(","",$0);gsub("\\\)","",$0);print $1}'`
    for j in coverage process_count process_rate scale
    do
        if [ -e ${j}_$i ]; then
            cd ${j}_$i
            for file in *
            do
                awk -v l_s=$last_step 'NR==1 || NR>1 && $1<=l_s {print $0}' $file > ${file}_tmp
                mv ${file}_tmp $file
            done
            cd ..
        fi
    done
done
