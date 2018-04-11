#!/usr/bin/env python
from copy import deepcopy
from random import randint
import numpy as np
try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FormatStrFormatter
    visual = True
except:
    visual = False


# starting configuration --------------------------------------------------------------------------------
config =                         # starting configuration, choose from 'Nb-NOb', 'Nf-NOt', and 'Nh-NOt'
num_O =                          # number for surrounding O atoms, int
num_CO =                         # number for surronding CO molecules, int
repetitions = (12,12)            # supercell size in x and y directions, e.g. (12,12)
#--------------------------------------------------------------------------------------------------------


# physical information ----------------------------------------------------------------------------------
T =                              # temperature in K
#--------------------------------------------------------------------------------------------------------


# simulation information --------------------------------------------------------------------------------
loop_number = 2000               # number of loops to be run, int, e.g. 1000000
suffix = ''                      # suffix for output files, str, e.g. '_1'
#--------------------------------------------------------------------------------------------------------


# model information -------------------------------------------------------------------------------------
from KMCLib import *
# set possible process types, e.g. (('form','N2O'),('back','N2O'),...)
process_list = [ (x,'N2O') for x in ('form','back','trans','des','dis') ]
# set processes to break simulation, e.g. ('des','dis')
end_list = ['des','dis']
# set on-the-fly rate calculator, True or False
rate_calculator = True
#--------------------------------------------------------------------------------------------------------


# running procedure -------------------------------------------------------------------------------------
from Model_N2O import *

record = { y:{ x:0 for x in Process[y]['N2O'] } for y in end_list}
times = []

control_parameters._KMCControlParameters__time_seed = False
f = open('trace'+suffix,'w',1)
for i in range(loop_number):
    control_parameters._KMCControlParameters__seed = randint(1,1000000000)
    if i == loop_number-1:
        model_copy = model
    else:
        model_copy = deepcopy(model)
    model_copy.run(control_parameters  = control_parameters,
                   trajectory_filename = None,
                   breakers            = [breaker])
    category,react = breaker.end_process
    record[category][react] += 1
    times.append(breaker.end_time)
    if (i+1) % (loop_number/100) == 0:
        f.write('{:8}:  '.format(i+1))
        rate = 1 / np.average(times)
        f.write('{} Hz\n'.format(rate))
f.close()
#--------------------------------------------------------------------------------------------------------


# output files ------------------------------------------------------------------------------------------
rate = 1 / np.average(times)
rate_calculator = interactions.rateCalculator() if rate_calculator else set_fixed_rate
with open('summary'+suffix,'w') as f:
    f.write('Number of loops: {}\n'.format(loop_number))
    f.write('Temperature: {} K\n'.format(T))
    f.write('Formation-step information:\n')
    f.write('    Reaction energy difference: {:.3f} eV\n'.format(rate_calculator.E_diff))
    f.write('    Activation energy: {:.3f} eV\n'.format(rate_calculator.E_bar))
    f.write('    Prefactor: {} Hz\n'.format(rate_calculator.prefactor))
    f.write('    Rate constant: {} Hz\n'.format(rate_calculator.rate_constant))
    f.write('End process:\n')
    num = {}
    for i in end_list:
        num[i] = sum( y for x,y in record[i].items() )
        f.write('    '+i+': {}\n'.format(num[i]))
        for x in sorted(record[i].keys()):
            f.write('        {}: {}\n'.format(x,record[i][x]))
    f.write('Fitted rate constant:\n')
    f.write('    all: {} Hz\n'.format(rate))
    for i in end_list:
        if num[i]:
            f.write('    '+ i +': {} Hz\n'.format(rate*num[i]/loop_number))
    f.write('Fitted activation energy:\n')
    for i in end_list:
        if num[i]:
            E_active = -np.log(rate*num[i]/loop_number/rate_calculator.prefactor) * (K*T/EV)
            f.write('    '+ i +': {:.3f} eV\n'.format(E_active))
#--------------------------------------------------------------------------------------------------------


# time distribution function image ----------------------------------------------------------------------
if visual:
    times.sort()
    times = np.array(times)
    accum = np.linspace(0,1,times.size,False)
    xmajorFormatter = FormatStrFormatter('%.1e')
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(1,1,1)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    plt.plot(times,accum,'ro')
    plt.plot(times,1-np.exp(-rate*times),'r-')
    plt.xlabel('time / s')
    plt.ylabel('accumulation')
    fig.savefig('fitting'+suffix+'.png',dpi=100,bbox_inches='tight')
# end ---------------------------------------------------------------------------------------------------
