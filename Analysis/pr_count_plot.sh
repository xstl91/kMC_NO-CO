#!/bin/sh
# run under process_count directory

getopts f:sh Option
case $Option in
    f) choice='sf'; file=$OPTARG;;
    s) choice='sep'; file=dis_NO;;
    h) echo "-f file_name for a single file; -s for seperate processes"; exit 0;;
   \?) echo "Invalid: $0 -f file_name|s|h"; exit 1;;
esac

word=`head -1 $file | wc -w`
x=`tail -1 $file | awk '{print $2}'`

if [ $choice == sf ];then
y=`tail -1 $file | awk '{for(x=3;x<=NF;x+=1) a+=$x; print a}'`
y=`python -c "print max(5, $y*1.1)"`
gnuplot<<EOF
set term postscript eps solid size 3.15,2.2 font "Times,16"
set output "${file}.eps"
set xtics format "%.1t^%T" font "Times,12" offset 0,0.3
set ytics font "Times,12" offset 0.5,0
set key left top font "Times,12"
set xrange [0:$x]
set yrange [0:$y]
set xlabel "time / s" offset 0,0.8
set ylabel "frequency"  offset 2.5,0
if ($word == 3)\
plot "${file}" u 2:3 w l lc rgb "red" t columnhead;\
else if ($word == 4)\
plot "${file}" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t columnhead,\
      "" u 2:4 w l lc rgb "blue" t columnhead;\
else if ($word == 5)\
plot "${file}" u 2:(\$3+\$4+\$5) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t columnhead,\
      "" u 2:4 w l lc rgb "blue" t columnhead,\
      "" u 2:5 w l lc rgb "forest-green" t columnhead;\
else if ($word == 6)\
plot "${file}" u 2:(\$3+\$4+\$5+\$6) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t columnhead,\
      "" u 2:4 w l lc rgb "blue" t columnhead,\
      "" u 2:5 w l lc rgb "forest-green" t columnhead,\
      "" u 2:6 w l lc rgb "violet" t columnhead
EOF

elif [ $choice == sep ];then
arr=()
for file in dis_NO form_NO form_N2 form_N2O form_CO2 des_O2
do
y=`tail -1 $file | awk '{for(x=3;x<=NF;x+=1) a+=$x; print a}'`
y=`python -c "print max(5, $y*1.1)"`
arr=(${arr[*]} $y)
done
if [ $word -eq 3 ];then
gnuplot<<EOF
set term postscript eps enhanced solid linewidth 0.5 size 4.5,2.2 font "Times,10"
set output "seperate.eps"
set multiplot layout 2,3
set xtics format "%.1t^{%T}" font "Times,8" offset 0,0.3
set ytics format "%4.0f" font "Times,8" offset 0.5,0
set key left top samplen 2 spacing 0.8 font "Times,8"
set xrange [0:$x]
set xlabel "time / s" offset 0,0.8
set ylabel "frequency"  offset 2.5,0
set yrange [0:${arr[0]}]
set title "NO dissociation"
plot "dis_NO" u 2:3 w l lc rgb "red" t "brg"
set yrange [0:${arr[1]}]
set title "NO formation"
plot "form_NO" u 2:3 w l lc rgb "red" t "N-O-bb"
set yrange [0:${arr[2]}]
set title "N_2 formation"
plot "form_N2" u 2:(\$3+\$4+\$5) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "N-NO-bb",\
      "" u 2:4 w l lc rgb "blue" t "N-N-bb",\
      "" u 2:5 w l lc rgb "forest-green" t "N-N-hb"
set yrange [0:${arr[3]}]
set title "N_2O formation"
plot "form_N2O" u 2:3 w l lc rgb "red" t "N-NO-bb"
set yrange [0:${arr[4]}]
set title "CO_2 formation"
plot "form_CO2" u 2:3 w l lc rgb "red" t "O-CO-bb"
set yrange [0:${arr[5]}]
set title "O_2 desorption"
plot "des_O2" u 2:3 w l lc rgb "red" t "O-O-bb"
unset multiplot
EOF

elif [ $word -eq 4 ];then
gnuplot<<EOF
set term postscript eps enhanced solid linewidth 0.5 size 4.5,2.2 font "Times,10"
set output "seperate.eps"
set multiplot layout 2,3
set xtics format "%.1t^{%T}" font "Times,8" offset 0,0.3
set ytics format "%4.0f" font "Times,8" offset 0.5,0
set key left top samplen 2 spacing 0.8 font "Times,8"
set xrange [0:$x]
set xlabel "time / s" offset 0,0.8
set ylabel "frequency"  offset 2.5,0
set yrange [0:${arr[0]}]
set title "NO dissociation"
plot "dis_NO" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "fcc",\
      "" u 2:4 w l lc rgb "blue" t "hcp"
set yrange [0:${arr[1]}]
set title "NO formation"
plot "form_NO" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "N-O-ff",\
      "" u 2:4 w l lc rgb "blue" t "N-O-hh"
set yrange [0:${arr[2]}]
set title "N_2 formation"
plot "form_N2" u 2:(\$3+\$4+\$5+\$6) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "N-NO-ft",\
      "" u 2:4 w l lc rgb "blue" t "N-NO-ht",\
      "" u 2:5 w l lc rgb "forest-green" t "N-N-ff",\
      "" u 2:6 w l lc rgb "violet" t "N-N-hh"
set yrange [0:${arr[3]}]
set title "N_2O formation"
plot "form_N2O" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "N-NO-ft",\
      "" u 2:4 w l lc rgb "blue" t "N-NO-ht"
set yrange [0:${arr[4]}]
set title "CO_2 formation"
plot "form_CO2" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "O-CO-ft",\
      "" u 2:4 w l lc rgb "blue" t "O-CO-ht"
set yrange [0:${arr[5]}]
set title "O_2 desorption"
plot "des_O2" u 2:(\$3+\$4) w l lc rgb "black" t 'all',\
      "" u 2:3 w l lc rgb "red" t "O-O-ff",\
      "" u 2:4 w l lc rgb "blue" t "O-O-hh"
unset multiplot
EOF
fi
fi
