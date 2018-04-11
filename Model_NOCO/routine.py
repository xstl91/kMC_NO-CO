from KMCLib import *
from .constant import *
from .process import Process
import __main__

unit_cell = KMCUnitCell(
    cell_vectors = Cell_vectors,
    basis_points = Basis_points)

lattice = KMCLattice(
    unit_cell   = unit_cell,
    repetitions = (__main__.repetitions[0],__main__.repetitions[1],1),
    periodic    = (True, True, False))

if __main__.init_config not in ('clean', 'random', 'custom'):
    raise Exception('Unsupported starting configuration.')
elif __main__.init_config == 'clean':
    types = ['o']*len(lattice.sites())
elif __main__.init_config == 'random':
    from .get_init import types

configuration = KMCConfiguration(
    lattice        = lattice,
    types          = types,
    possible_types = ['o','N','O','NO','CO'])

if 'process_list' in dir(__main__) and __main__.process_list:
    process_list = __main__.process_list
else:
    process_list = (('ads','NO'),('ads','CO'),('ads','O2'),
                    ('dif','N'),('dif','O'),('dif','NO'),('dif','CO'),
                    ('dis','NO'),
                    ('form','NO'),('form','N2'),('form','N2O'),('form','CO2'),
                    ('des','NO'),('des','CO'),('des','O2'))
processes = []
for category,mol in process_list:
    for x in Process[category][mol].values():
        processes.extend(x)

interactions = KMCInteractions(
    processes          = processes,
    implicit_wildcards = True)

from .RateCalculator import *

dynamic = [ x for x in [dif_ratio, ads_ratio] if not isinstance(x, dict) ]
if not dynamic:
    dynamic = None

if __main__.rate_calculator:
    interactions.setRateCalculator(Pairwise)
else:
    set_fixed_rate()

model = KMCLatticeModel(
    configuration = configuration,
    interactions  = interactions)

control_parameters = KMCControlParameters(
    number_of_steps   = __main__.number_of_steps,
    dump_interval     = __main__.dump_interval,
    analysis_interval = 1,
    seed              = None)
