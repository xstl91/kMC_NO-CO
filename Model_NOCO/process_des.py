from KMCLib import *
from .constant import *
from .parameter_vib import Vib_ad
from .rate import pre_des

# rate_constant set here refers to prefactor

p_des = { x:{} for x in ('NO', 'CO', 'O2') }

# desorption of NO and CO
multi = 4 if Surface == '100' else 3
for mol in ('NO','CO'):
    for point in Bp_map:
        p_des[mol][point] = [KMCProcess(
                                 coordinates     = [Origin],
                                 elements_before = [mol],
                                 elements_after  = ['o'],
                                 basis_sites     = [Bp_map[point]],
                                 rate_constant   = pre_des(mol, A_uc/multi, Vib_ad[mol][point[0]]))]
        p_des[mol][point][-1].name = ('des', mol, point[0], point)

# desorption of O2
if Surface == '100':
    p_des['O2']['O-O_bb'] = []
    for point,d in (('b1','u'),('b2','r')):
        p_des['O2']['O-O_bb'].append( KMCProcess(
                                          coordinates     = [Origin, N3[d]],
                                          elements_before = ['O','O'],
                                          elements_after  = ['o','o'],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_des('O2', A_uc/2, Vib_ad['O']['b'], Vib_ad['O']['b'])))
        p_des['O2']['O-O_bb'][-1].name = ('des', 'O2', 'O-O_bb', point)
elif Surface == '111':
    for name in ('O-O_ff','O-O_hh'):
        p_des['O2'][name] = []
        point = name[-1]
        for d in ('ul','ur','r'):
            p_des['O2'][name].append( KMCProcess(
                                          coordinates     = [Origin, N2[d]],
                                          elements_before = ['O','O'],
                                          elements_after  = ['o','o'],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_des('O2', A_uc/6, Vib_ad['O'][point], Vib_ad['O'][point])))
            p_des['O2'][name][-1].name = ('des', 'O2', name, point)
