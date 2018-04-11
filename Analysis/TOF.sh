#!/bin/sh
# usage: TOF.sh 400, give the number of sites
# run under process_count directory

if [ $# -ne 1 ]; then echo "Provide the number of sites as an argument."; exit 1;fi

site=$1
for file in dis_NO form_NO form_N2 form_N2O form_CO2 des_O2
do
    if [ -e $file ]; then
        word=`head -1 $file | wc -w`
        if [ $word == 3 ];then
            tail -1 $file | awk -v name=$file -v site=$site '{printf "%11s%11.3e\n",name,$3/$2/site}'
        elif [ $word == 4 ];then
            tail -1 $file | awk -v name=$file -v site=$site '{printf "%11s%11.3e\n",name,($3+$4)/$2/site}'
        elif [ $word == 5 ];then
            tail -1 $file | awk -v site=$site '{printf "form_N2_N2O%11.3e\n form_N2_2N%11.3e\n",$3/$2/site,($4+$5)/$2/site}'
        elif [ $word == 6 ];then
            tail -1 $file | awk -v site=$site '{printf "form_N2_N2O%11.3e\n form_N2_2N%11.3e\n",($3+$4)/$2/site,($5+$6)/$2/site}'
        fi
    fi
done 
