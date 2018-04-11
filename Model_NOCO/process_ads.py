from KMCLib import *
import numpy as np
from .constant import *
from .rate import pre_ads
import __main__

# rate_constant set here refers to actual rate constant

p_ads = { x:{} for x in ('NO', 'CO', 'O2') }

# adsorption of NO and CO
if Surface == '100':
    surround = N1.values() + N2.values()
    multi = 4
elif Surface == '111':
    surround = N1.values()
    multi = 3
len_s = len(surround)
for mol in ('NO','CO'):
    for point in Bp_map:
        p_ads[mol][point] = [KMCProcess(
                                 coordinates     = [Origin] + surround,
                                 elements_before = ['o'] + ['o']*len_s,
                                 elements_after  = [mol] + ['o']*len_s,
                                 basis_sites     = [Bp_map[point]],
                                 rate_constant   = pre_ads(mol, __main__.p[mol], A_uc/multi))]
        p_ads[mol][point][-1].name = ('ads', mol, point[0], point)

# adsorption of O2
def site_include(site1, sites):
    for site2 in sites:
        diff = sum(abs(np.array(site1) - np.array(site2)))
        if diff < 1e-3:
            return True
    return False
def get_surround(sites, offsets):
    surround = []
    for center in sites:
        for offset in offsets:
            site = [ center[x] + offset[x] for x in range(3) ]
            if not site_include(site, surround) and not site_include(site, sites):
                surround.append(site)
    return surround
if Surface == '100':
    p_ads['O2']['O-O_bb'] = []
    for point,d in (('b1','u'),('b2','r')):
        surround = get_surround( [Origin, N3[d]], N1.values() + N2.values() )
        len_s = len(surround)
        p_ads['O2']['O-O_bb'].append( KMCProcess(
                                          coordinates     = [Origin, N3[d]] + surround,
                                          elements_before = ['o','o'] + ['o']*len_s,
                                          elements_after  = ['O','O'] + ['o']*len_s,
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_ads('O2', __main__.p['O2'], A_uc/2)))
        p_ads['O2']['O-O_bb'][-1].name = ('ads', 'O2', 'O-O_bb', point)
elif Surface == '111':
    for name in ('O-O_ff','O-O_hh'):
        p_ads['O2'][name] = []
        point = name[-1]
        for d in ('ul','ur','r'):
            surround = get_surround( [Origin, N2[d]], N1.values() )
            len_s = len(surround)
            p_ads['O2'][name].append( KMCProcess(
                                          coordinates     = [Origin, N2[d]] + surround,
                                          elements_before = ['o','o'] + ['o']*len_s,
                                          elements_after  = ['O','O'] + ['o']*len_s,
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_ads('O2', __main__.p['O2'], A_uc/6)))
            p_ads['O2'][name][-1].name = ('ads', 'O2', name, point)
