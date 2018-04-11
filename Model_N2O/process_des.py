from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_des = { 'N2O':{} }
p_des['N2O']['top'] = [KMCProcess(
                           coordinates     = [Origin],
                           elements_before = ['top'],
                           elements_after  = ['o'],
                           basis_sites     = [Bp_map['t']],
                           rate_constant   = pre_des('N2O', A_uc, Vib_ad['N2O']['top']))]
p_des['N2O']['top'][-1].name = ('des', 'N2O', 'top', 't')
