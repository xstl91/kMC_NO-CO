#!/usr/bin/env python
# usage: cov_ave.py 0.5 1000 0.3
# run under coverage directory

import numpy as np
import sys

try:
    threshold = float(sys.argv[1])  # threshold value for acceptable correlation
except:
    threshold = 0.5
try:
    max_step = int(sys.argv[2])     # maximum step length for calculating local correlation
except:
    max_step = 1000
try:
    percent = float(sys.argv[3])    # minimum percentage for staying at equilibrium
except:
    percent = 0.3

# read coverage files
step_list = []
time_list = []
cov_list = { x:[] for x in ('N','O','NO','CO') }
for mol in ('N','O','NO','CO'):
    with open('whole_'+mol) as f:
        f.readline()
        for line in f:
            line = line.split()
            if mol == 'N':
                step_list.append(int(line[0]))
                time_list.append(float(line[1]))
            cov_list[mol].append(float(line[-1]))

# decide whether equilibrium is reached
for num in range( max(0, int(len(time_list) - max_step*percent)) ):
    x_l = np.array(time_list[num:(num+max_step)])
    x_g = np.array(time_list[num:])
    for mol in ('N','O','NO','CO'):
        y_l = np.array(cov_list[mol][num:(num+max_step)])
        y_g = np.array(cov_list[mol][num:])
        cor_l = np.corrcoef(np.vstack((x_l,y_l)))[0][1]
        cor_g = np.corrcoef(np.vstack((x_g,y_g)))[0][1]
        if abs(cor_l) > threshold or abs(cor_g) > threshold:
            break
    else:
        print "Equilibrium is reached at line {}.".format(num+1)
        break
else:
    print "Equilibrium is not reached."
    exit()

# calculate average coverage
time_dif_list = np.array([time_list[i+1] - time_list[i] for i in range(num,len(time_list)-1)])
cov_ave = {}
cov_std = {}
for mol in ('N','O','NO','CO'):
    cov_list[mol] = np.array(cov_list[mol][num:-1])
    cov_ave[mol] = np.average(cov_list[mol], weights=time_dif_list)
    cov_std[mol] = np.sqrt( np.average((cov_list[mol]-cov_ave[mol])**2, weights=time_dif_list))
with open('average_cov','w') as f:
    f.write('Start line: {}\n'.format(num+1))
    f.write('Start step: {}\n'.format(step_list[num]))
    f.write('Start time: {:e} s\n'.format(time_list[num]))
    f.write('Coverage:\n    mol     ave     std\n')
    for mol in ('N','O','NO','CO'):
        f.write('{:>7s}{:>8.4f}{:8.4f}\n'.format(mol,cov_ave[mol],cov_std[mol]))
