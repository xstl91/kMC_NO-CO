#!/bin/sh
# run under coverage directory

getopts af:sh Option
case $Option in
    a) choice='all'; file="whole_N whole_O whole_NO whole_CO whole_all";;
    f) choice='sf'; file=$OPTARG;;
    s) choice='sep'; file="whole_N whole_O whole_NO whole_CO";;
    h) echo "-a for all species; -f file_name for a single file; -s for seperate species"; exit 0;;
   \?) echo "Invalid: $0 -a|f file_name|s|h [ start_line [ end_line ] ]"; exit 1;;
esac

if [ $choice == all -o $choice == sep ]; then
    shift 1
else
    shift 2
fi
if [ $# -eq 0 ];then
    for i in $file; do tail -n +2 $i > .tmp_$i; done
elif [ $# -eq 1 ]; then
    for i in $file; do tail -n +$(($1+1)) $i > .tmp_$i; suffix="_$1"; done
elif [ $# -eq 2 ]; then
    for i in $file; do sed -n "$(($1+1)),${2}p" $i > .tmp_$i ; suffix="_$(($1+1))_${2}"; done
else
    echo "Too much arguments."; exit 1
fi


if [ $choice == all ];then
word=`head -1 whole_N | wc -w`
x_b=`head -1 .tmp_whole_N | awk '{print $2}'`
x_e=`tail -1 .tmp_whole_N | awk '{print $2}'`
y=`sort -nu -k$word,$word .tmp_whole_all | tail -1 | awk '{print $NF}'`
y=`python -c "print max(0.005, $y*1.2)"`
gnuplot<<EOF
set term postscript eps enhanced solid size 3.15,2.2 font "Times,16"
set output "all${suffix}.eps"
set xtics format "%.1t^{%T}" font "Times,12" offset 0,0.3
set ytics format "%.3f" font "Times,12" offset 0.5,0
set key horizontal center top samplen 1.7 font "Times,12"
set xrange [$x_b:$x_e]
set xlabel "time / s" offset 0,0.8
set yrange [0:$y]
set ylabel "coverage / ML" offset 2.5,0
plot ".tmp_whole_all" u 2:$word w l lt 0 lc rgb "black" t "all",\
     ".tmp_whole_N" u 2:$word w l lc rgb "blue" t "N",\
     ".tmp_whole_O" u 2:$word w l lc rgb "red" t "O",\
     ".tmp_whole_NO" u 2:$word w l lc rgb "violet" t "NO",\
     ".tmp_whole_CO" u 2:$word w l lc rgb "forest-green" t "CO"
EOF


elif [ $choice == sf ];then
word=`head -1 $file | wc -w`
x_b=`head -1 .tmp_${file} | awk '{print $2}'`
x_e=`tail -1 .tmp_${file} | awk '{print $2}'`
y=`sort -nu -k$word,$word .tmp_${file} | tail -1 | awk '{print $NF}'`
y=`python -c "print max(0.005, $y*1.2)"`
if [ $word == 7 ]
then
gnuplot<<EOF
set term postscript eps enhanced solid size 3.15,2.2 font "Times,16"
set output "${file}${suffix}.eps"
set xtics format "%.1t^{%T}" font "Times,12" offset 0,0.3
set ytics format "%.3f" font "Times,12" offset 0.5,0
set key horizontal center top samplen 2 font "Times,12"
set xrange [$x_b:$x_e]
set xlabel "time / s" offset 0,0.8
set yrange [0:$y]
set ylabel "coverage / ML"  offset 2.5,0
plot ".tmp_${file}" u 2:7 w l lw 2 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "b1",\
      "" u 2:5 w l lt 0 lc rgb "violet" t "b2",\
      "" u 2:6 w l lt 0 lc rgb "forest-green" t "h"
EOF
else
gnuplot<<EOF
set term postscript eps enhanced solid size 3.15,2.2 font "Times,16"
set output "${file}${suffix}.eps"
set xtics format "%.1t^{%T}" font "Times,12" offset 0,0.3
set ytics format "%.3f" font "Times,12" offset 0.5,0
set key horizontal center top samplen 2 font "Times,12"
set xrange [$x_b:$x_e]
set xlabel "time / s" offset 0,0.8
set yrange [0:$y]
set ylabel "coverage / ML"  offset 2.5,0
plot ".tmp_${file}" u 2:6 w l lw 2 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "f",\
      "" u 2:5 w l lt 0 lc rgb "forest-green" t "h"
EOF
fi


elif [ $choice == sep ];then
word=`head -1 whole_N | wc -w`
x_b=`head -1 .tmp_whole_N | awk '{print $2}'`
x_e=`tail -1 .tmp_whole_N | awk '{print $2}'`
y=`sort -nu -k$word,$word .tmp_whole_N | tail -1 | awk '{print $NF}'`
y_N=`python -c "print max(0.005, $y*1.2)"`
y=`sort -nu -k$word,$word .tmp_whole_O | tail -1 | awk '{print $NF}'`
y_O=`python -c "print max(0.005, $y*1.2)"`
y=`sort -nu -k$word,$word .tmp_whole_NO | tail -1 | awk '{print $NF}'`
y_NO=`python -c "print max(0.005, $y*1.2)"`
y=`sort -nu -k$word,$word .tmp_whole_CO | tail -1 | awk '{print $NF}'`
y_CO=`python -c "print max(0.005, $y*1.2)"`
if [ $word == 7 ]
then
gnuplot<<EOF
set term postscript eps enhanced solid linewidth 0.5 size 3.15,2.2 font "Times,10"
set output "seperate${suffix}.eps"
set multiplot layout 2,2
set xtics format "%.1t^{%T}" font "Times,8" offset 0,0.3
set ytics format "%.3f" font "Times,8" offset 0.5,0
set key horizontal center top samplen 0.4 spacing 0.6 font "Times,8"
set xrange [$x_b:$x_e]
set xlabel "time / s" offset 0,0.8
set yrange [0:$y_N]
set ylabel "N coverage / ML"  offset 2.5,0
plot ".tmp_whole_N" u 2:7 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "b1",\
      "" u 2:5 w l lt 0 lc rgb "violet" t "b2",\
      "" u 2:6 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_O]
set ylabel "O coverage / ML" offset 2.5,0
plot ".tmp_whole_O" u 2:7 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "b1",\
      "" u 2:5 w l lt 0 lc rgb "violet" t "b2",\
      "" u 2:6 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_NO]
set ylabel "NO coverage / ML" offset 2.5,0
plot ".tmp_whole_NO" u 2:7 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "b1",\
      "" u 2:5 w l lt 0 lc rgb "violet" t "b2",\
      "" u 2:6 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_CO]
set ylabel "CO coverage / ML" offset 2.5,0
plot ".tmp_whole_CO" u 2:7 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "b1",\
      "" u 2:5 w l lt 0 lc rgb "violet" t "b2",\
      "" u 2:6 w l lt 0 lc rgb "forest-green" t "h"
unset multiplot
EOF
else
gnuplot<<EOF
set term postscript eps enhanced solid linewidth 0.5 size 3.15,2.2 font "Times,10"
set output "seperate${suffix}.eps"
set multiplot layout 2,2
set xtics format "%.1t^{%T}" font "Times,8" offset 0,0.3
set ytics format "%.3f" font "Times,8" offset 0.5,0
set key horizontal center top samplen 0.3 spacing 0.6 font "Times,8"
set xrange [$x_b:$x_e]
set xlabel "time / s" offset 0,0.8
set yrange [0:$y_N]
set ylabel "N coverage / ML"  offset 2.5,0
plot ".tmp_whole_N" u 2:6 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "f",\
      "" u 2:5 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_O]
set ylabel "O coverage / ML"  offset 2.5,0
plot ".tmp_whole_O" u 2:6 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "f",\
      "" u 2:5 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_NO]
set ylabel "NO coverage / ML"  offset 2.5,0
plot ".tmp_whole_NO" u 2:6 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "f",\
      "" u 2:5 w l lt 0 lc rgb "forest-green" t "h"
set yrange [0:$y_CO]
set ylabel "CO coverage / ML"  offset 2.5,0
plot ".tmp_whole_CO" u 2:6 w l lw 3 lc rgb "black" t "a",\
      "" u 2:3 w l lt 0 lc rgb "red" t "t",\
      "" u 2:4 w l lt 0 lc rgb "blue" t "f",\
      "" u 2:5 w l lt 0 lc rgb "forest-green" t "h"
unset multiplot
EOF
fi


fi
rm .tmp*
