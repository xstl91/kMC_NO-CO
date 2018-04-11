#!/usr/bin/env python

from KMCLib import *


# physical information ----------------------------------------------------------------------------------
T =                              # temperature, K
p = {'NO':       ,               # pressure of NO, Pa
     'CO':       ,               # pressure of CO, Pa
     'O2':       }               # pressure of O2, Pa
#--------------------------------------------------------------------------------------------------------


# starting configuration --------------------------------------------------------------------------------
surface =                        # '100' or '111'
repetitions =                    # supercell size in x and y directions, e.g. (20,20)
init_config =                    # initialize configuration, choose from 'clean', 'random', and 'custom'
if init_config == 'random':
    num_mol = {'N' :  0,         # numbers of molecules to start with, int
               'O' :  0,
               'NO':  0,
               'CO':  0}
elif init_config == 'custom':
    types = []                   # list of types, e.g. ['CO','o','o','o']*20*20;
#--------------------------------------------------------------------------------------------------------


# possible process types --------------------------------------------------------------------------------
process_list = None              # None for including all possible processes
                                 # or customize by list, e.g. (('dif','N'),('dif','O'),...)
#--------------------------------------------------------------------------------------------------------


# rate calculator ---------------------------------------------------------------------------------------
# set on-the-fly rate calculator, True or False
rate_calculator = True

# static acceleration strategy for diffusion  
static_dif = False           # True or False
# parameters for statically slowing down the diffusion rate constants
if static_dif:
    dif_ratio_s = { 'N' :    1,  # ratio between modified and original rate constants
                    'O' :    1,
                    'NO':    1,
                    'CO':    1}

# dynamic acceleration strategy for diffusion, only operates when use rate_calculator
dynamic_dif = 'rate'             # choose from 'rate', 'count', and False
# diffusion process exclude from dynamic scaling
if dynamic_dif:
    dif_exclude = []             # list of molecule name, e.g. ['N']
# parameters for dynamically slowing down the diffusion rate constants
if dynamic_dif == 'rate':
    dif_period = 1000            # rescaling period for diffusion, e.g. 1000
    dif_magnitude = 100          # number to separate fast and slow processes, e.g. 100
elif dynamic_dif == 'count':
    dif_step   = 100             # number of events to slow down certain process, e.g. 100
    dif_factor = 0.5             # diffusion rescaling step, e.g. 0.5

# dynamic acceleration strategy for adsorption and desorption, only operates when use rate_calculator
dynamic_ads = 'rate'             # choose from 'rate', 'count', and False
# parameters for dynamically slowing down the adsorption and desorption rate constants
if dynamic_ads == 'rate':
    ads_length = 50              # length for deciding whether an equilibrium is achieved, e.g. 100
    ads_fluc   = 0.1             # percentage for deciding whether an equilibrium is achieved, e.g. 0.1
    ads_period = 1000            # rescaling period for adsorption and desorption, e.g. 1000
    ads_magnitude = 100          # number to separate fast and slow processes, e.g. 100
elif dynamic_ads == 'count':
    ads_length = 50              # length for deciding whether an equilibrium is achieved, e.g. 100
    ads_fluc   = 0.1             # percentage for deciding whether an equilibrium is achieved, e.g. 0.1
    ads_step   = 100             # number of events to slow down certain process, e.g. 100
    ads_factor = 0.5             # adsorption and desorption rescaling step, e.g. 0.5

# Output for dynamic scaling procedure, dict of True or False
scale_output = {'dif': False,
                'ads': False}
# -------------------------------------------------------------------------------------------------------


# simulation information --------------------------------------------------------------------------------
number_of_steps = 10000000                    # number of steps to run kMC simulation, int
dump_interval =  number_of_steps / 20         # interval to export configuration information, int
analysis_interval = number_of_steps / 5000    # interval to export analysis information, int
suffix = ''                                   # suffix for output files, str, e.g. '_1'
# -------------------------------------------------------------------------------------------------------


# analysis interface ------------------------------------------------------------------------------------
from Model_NOCO import *

coverage = Coverage(
    interval = analysis_interval,
    types = ('N','O','NO','CO'),
    partition = False,
    part_span = None)

process_count = ProcessCount(
    interval = analysis_interval,
    process_list = (('dis','NO'),('form','NO'),('form','N2'),('form','N2O'),('form','CO2'),('des','O2')))

process_rate = ProcessRate(
    process_list = (('dis','NO'),('form','NO'),('form','N2'),('form','N2O'),('form','CO2'),('des','O2')))

graph = Graph(
    interval = dump_interval,
    section = None)
#--------------------------------------------------------------------------------------------------------


# Stop interface ----------------------------------------------------------------------------------------
time_breaker = TimeBreaker( length = 24*60*60 )
file_breaker = FileBreaker( file_name = 'STOP' )
#--------------------------------------------------------------------------------------------------------


# running procedure -------------------------------------------------------------------------------------
model.run(control_parameters  = control_parameters,
          trajectory_filename = 'traj' + suffix + '.py',
          analysis            = [coverage, process_count, process_rate, graph],
          breakers            = [file_breaker],
          analysis_pre        = dynamic)
# end ---------------------------------------------------------------------------------------------------
