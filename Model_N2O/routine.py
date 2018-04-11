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

possible_types = [ 'o', 'N', 'O', 'NO', 'CO', 'top']
if Surface == '100':
    possible_types.extend(['flat-N', 'flat-mN', 'flat-mO', 'falt-O'])
    for config in ('NNbhb', 'NNtbt', 'NOtbt', 'NOtht'):
        possible_types.extend([config+'-N', config+'-m', config+'-O'])
elif Surface == '111':
    for config in ('NNbftt', 'NNbhtt', 'NObft', 'NObht'):
        possible_types.extend([config+'-N', config+'-m', config+'-O'])
    for config in ('NNtbt', 'NOtbt'):
        possible_types.extend([config+'-N', config+'-O'])

from .get_init import types

configuration = KMCConfiguration(
    lattice        = lattice,
    types          = types,
    possible_types = possible_types)

processes = []
for react,mol in __main__.process_list:
    for x in Process[react][mol].values():
        processes.extend(x)

interactions = KMCInteractions(
    processes          = processes,
    implicit_wildcards = True)

from .RateCalculator import *

if __main__.rate_calculator:
    interactions.setRateCalculator(Pairwise)
else:
    set_fixed_rate()

model = KMCLatticeModel(
    configuration = configuration,
    interactions  = interactions)

control_parameters = KMCControlParameters(
    number_of_steps   = 100000000,
    dump_interval     = 100000000,
    analysis_interval = 100000000,
    seed              = None)

from .breaker import Breaker
breaker = Breaker()
