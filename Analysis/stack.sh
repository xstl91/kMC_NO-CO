#!/bin/sh
# usage: stack.sh 0 1 2, list suffix number for stacking
# run under main directory

for i in coverage process_count process_rate scale
do
    if [ -e $i ]; then rm -r $i; fi
    if [ -e ${i}_$1 ]; then cp -r ${i}_$1 $i; fi
    rm $i/*.eps 2> /dev/null
done
cp traj_$1.py traj.py
shift

for i in $*
do
    last_step=`grep steps traj.py | tail -1 | awk '{gsub(".*\\\(","",$0);gsub("\\\)","",$0);print $1}'`
    last_time=`grep times traj.py | tail -1 | awk '{gsub(".*\\\(","",$0);gsub("\\\)","",$0);print $1}'`

    # stack for traj
    python << EOF
execfile('traj_$i.py')
times = [ i + $last_time for i in times if i ]
steps = [ i + $last_step for i in steps if i ]
types_list = types[1:]
with open('traj.py','a') as trajectory:
    for (sim_time, step, types) in zip(times, steps, types_list):
        trajectory.write( "times.append(%18.10e)\n"%sim_time )
        trajectory.write( "steps.append(%i)\n"%step )
        types_str = "types.append(["
        indent = " "*14
        row_length = len(types_str)
        for t in types[:-1]:
            row_length += len(t) + 2
            types_str += "\"" + t + "\"" + ","
            if row_length >= 70:
                types_str += "\n" + indent
                row_length = len(indent)
        types_str += "\"" + types[-1] + "\"" + "])\n"
        trajectory.write(types_str)
EOF


    # stack for coverage, process_count, process_rate, scale
    for j in coverage process_count process_rate scale
    do
        if [ -e $j ];then
            cd $j
            for file in *
            do
                cp ../${j}_$i/$file ./tmp
                case $j in
                    "coverage")
                        awk -v l_s=$last_step -v l_t=$last_time 'NR>2{printf "%14d%18.10e",$1+l_s,$2+l_t;\
                            for(x=3;x<=NF;x+=1) printf "%8.4f",$x; printf "\n"}' tmp >> $file;;
                    "process_count")
                        awk -v l_s=$last_step -v l_t=$last_time 'NR>2{printf "%14d%18.10e",$1+l_s,$2+l_t;\
                            for(x=3;x<=NF;x+=1) printf "%14d",$x+ARGV[x+1]; printf "\n"}' tmp `tail -1 $file` 1>>$file 2>/dev/null;;
                    "process_rate")
                        awk -v l_s=$last_step -v l_t=$last_time 'NR>1{printf "%14d%18.10e%18.10e%12.3f\n",$1+l_s,$2+l_t,$3,$4}' tmp >> $file;;
                    "scale")
                        awk -v l_s=$last_step -v l_t=$last_time 'NR>1{printf "%14d%18.10e",$1+l_s,$2+l_t;\
                            for(x=3;x<=NF;x+=1) printf "%12.4e",$x; printf "\n"}' tmp >> $file;;
                esac
            done
            rm tmp
            cd ..
        fi
    done
done
