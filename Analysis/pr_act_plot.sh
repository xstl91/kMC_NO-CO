#!/bin/sh
# usage: pr_act_plot.sh 1000
# run under process_rate directory

if [ $# -ne 1 ]; then echo "Provide a temperature in K as an argument."; exit 1;fi

if [ -f dis_NO_brg ]; then
act_N2_bb=`python -c "print 6.8314e-02*($1/1000.)**2 - 1.0283e-02*($1/1000.) + 1.0842"`
act_N2O_bb=`python -c "print 1.0663e-01*($1/1000.)**2 - 2.2376e-01*($1/1000.) + 1.3569"`
for file_o in dis_NO_brg form_NO_N-O_bb form_N2_N-N_bb form_N2_N-N_hb form_N2_N-NO_bb form_N2O_N-NO_bb form_CO2_O-CO_bb des_O2_O-O_bb
do
if [ `wc -l $file_o | cut -d " " -f 1` -ne 1 ];then file_l="$file_l $file_o";fi
done
for file in $file_l
do
gnuplot > /dev/null <<EOF
set term postscript eps enhanced solid size 3.15,2.2 font "Times,16"
set xtics font "Times,12" offset 0,0.3
set ytics font "Times,12" offset 0.5,0
set key font "Times,12"
set xlabel "Activation energy / eV" offset 0,0.8
set ylabel "Frequency"  offset 2.5,0
set yrange [0:]
bin(x)=0.05*floor(x/0.05)+0.025
set boxwidth 0.05

if ("$file" eq "dis_NO_brg")\
set title "NO dissociation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'brg';\
act=0.774;\
else if ("$file" eq "form_NO_N-O_bb")\
set title "NO formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'N-O-bb';\
act=0.678;\
else if ("$file" eq "form_N2_N-N_bb")\
set title "N_2 formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'N-N-bb';\
act=0.594;\
else if ("$file" eq "form_N2_N-N_hb")\
set title "N_2 formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'N-N-hb';\
act=1.666;\
else if ("$file" eq "form_N2_N-NO_bb")\
set title "N_2 formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'N-NO-bb';\
act=$act_N2_bb;\
else if ("$file" eq "form_N2O_N-NO_bb")\
set title "N_2O formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'N-NO-bb';\
act=$act_N2O_bb;\
else if ("$file" eq "form_CO2_O-CO_bb")\
set title "CO_2 formation";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'O-CO-bb';\
act=0.766;\
else if ("$file" eq "des_O2_O-O_bb")\
set title "O_2 desorption";\
plot "$file" u (bin(\$4)):(1) s f w boxes fill transparent pattern 1 lw 3 lc rgb 'red' t 'O-O-bb';\
act=3.193

set output "${file}.eps"
set arrow 1 from act,0 to act,(GPVAL_Y_MAX*1.2) nohead front lt 0 lw 3 lc rgb 'red';
set yrange [0:(GPVAL_Y_MAX*1.2)]
if (GPVAL_X_MAX < (act+(act-GPVAL_X_MIN)/5)) set xrange [(GPVAL_X_MIN-0.05):(act+(act-GPVAL_X_MIN)/5)];\
else if (GPVAL_X_MIN > (act-(GPVAL_X_MAX-act)/5)) set xrange [(act-(GPVAL_X_MAX-act)/5):(GPVAL_X_MAX+0.05)];\
else set xrange [(GPVAL_X_MIN-0.05):(GPVAL_X_MAX+0.05)]
replot
EOF
done


elif [ -f dis_NO_fcc ]; then
act_N2_ft=`python -c "print -6.2321e-02*($1/1000.)**2 + 3.5146e-01*($1/1000.) + 1.7735"`
act_N2_ht=`python -c "print -6.9069e-02*($1/1000.)**2 + 3.7167e-01*($1/1000.) + 1.9189"`
act_N2O_ft=`python -c "print 3.6600e-02*($1/1000.)**2 - 2.6064e-02*($1/1000.) + 1.4388"`
act_N2O_ht=`python -c "print 3.6475e-02*($1/1000.)**2 - 3.3715e-02*($1/1000.) + 1.5910"`
if [ $((`wc -l dis_NO_fcc | cut -d " " -f 1`+`wc -l dis_NO_hcp | cut -d " " -f 1`)) -ne 2 ];then file_l="dis_NO"; fi
for file_o in form_NO_N-O form_N2_N-N des_O2_O-O
do
if [ $((`wc -l ${file_o}_ff | cut -d " " -f 1`+`wc -l ${file_o}_hh | cut -d " " -f 1`)) -ne 2 ];then file_l="$file_l $file_o";fi
done
for file_o in form_N2_N-NO form_N2O_N-NO form_CO2_O-CO
do
if [ $((`wc -l ${file_o}_ft | cut -d " " -f 1`+`wc -l ${file_o}_ht | cut -d " " -f 1`)) -ne 2 ];then file_l="$file_l $file_o";fi
done

for file in $file_l
do
gnuplot > /dev/null <<EOF
set term postscript eps enhanced solid size 3.15,2.2 font "Times,16"
set xtics font "Times,12" offset 0,0.3
set ytics font "Times,12" offset 0.5,0
set key font "Times,12"
set xlabel "Activation energy / eV" offset 0,0.8
set ylabel "Frequency"  offset 2.5,0
set yrange [0:]
bin(x)=0.05*floor(x/0.05)+0.025
set boxwidth 0.05

if ("$file" eq "dis_NO")\
set title "NO dissociation";\
plot "${file}_fcc" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'fcc',\
     "${file}_hcp" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'hcp';\
act1=1.655; act2=1.678; act_l=act1; act_h=act2;\
else if ("$file" eq "form_NO_N-O")\
set title "NO formation";\
plot "${file}_ff" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'N-O-ff',\
     "${file}_hh" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'N-O-hh';\
act1=1.977; act2=2.028; act_l=act1; act_h=act2;\
else if ("$file" eq "form_N2_N-N")\
set title "N_2 formation";\
plot "${file}_ff" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'N-N-ff',\
     "${file}_hh" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'N-N-hh';\
act1=1.942; act2=2.104; act_l=act1; act_h=act2;\
else if ("$file" eq "form_N2_N-NO")\
set title "N_2 formation";\
plot "${file}_ft" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'N-NO-ft',\
     "${file}_ht" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'N-NO-ht';\
act1=$act_N2_ft; act2=$act_N2_ht; act_l=act1; act_h=act2;\
else if ("$file" eq "form_N2O_N-NO")\
set title "N_2O formation";\
plot "${file}_ft" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'N-NO-ft',\
     "${file}_ht" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'N-NO-ht';\
act1=$act_N2O_ft; act2=$act_N2O_ht; act_l=act1; act_h=act2;\
else if ("$file" eq "form_CO2_O-CO")\
set title "CO_2 formation";\
plot "${file}_ft" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'O-CO-ft',\
     "${file}_ht" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'O-CO-ht';\
act1=1.215; act2=1.174; act_l=act2; act_h=act1;\
else if ("$file" eq "des_O2_O-O")\
set title "O_2 desorption";\
plot "${file}_ff" u (bin(\$4)):(1) s f w boxes fill transparent pattern 4 lw 3 lc rgb 'red' t 'O-O-ff',\
     "${file}_hh" u (bin(\$4)):(1) s f w boxes fill transparent pattern 5 lw 3 lc rgb 'blue' t 'O-O-hh';\
act1=3.331; act2=3.211; act_l=act1; act_h=act2

set output "${file}.eps"
set arrow 1 from act1,0 to act1,(GPVAL_Y_MAX*1.2) nohead front lt 0 lw 3 lc rgb 'red';
set arrow 2 from act2,0 to act2,(GPVAL_Y_MAX*1.2) nohead front lt 0 lw 3 lc rgb 'blue';
set yrange [0:(GPVAL_Y_MAX*1.2)]
if (GPVAL_X_MAX < (act_h+(act_h-GPVAL_X_MIN)/5)) set xrange [(GPVAL_X_MIN-0.05):(act_h+(act_h-GPVAL_X_MIN)/5)];\
else if (GPVAL_X_MIN > (act_l-(GPVAL_X_MAX-act_l)/5)) set xrange [(act_l-(GPVAL_X_MAX-act_l)/5):(GPVAL_X_MAX+0.05)];\
else set xrange [(GPVAL_X_MIN-0.05):(GPVAL_X_MAX+0.05)]
replot
EOF
done

fi
