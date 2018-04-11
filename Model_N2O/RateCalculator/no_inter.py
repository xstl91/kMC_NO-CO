from ..constant import Config, EV
from ..rate import rate_LH
from ..parameter_E import *
from ..routine import processes

config_map = {'Nb-NOb':'NNbhb', 'Nf-NOt':'NNbhtt', 'Nh-NOt':'NNbftt' }

def set_fixed_rate():
    set_fixed_rate.E_diff = 0
    set_fixed_rate.E_bar = E_act['form']['N2O'][config_map[Config]][0] / EV
    for process in processes:
        category,mol,react,o_type = process.name
        if category == 'form' and mol == 'N2O' and react == config_map[Config]:
            set_fixed_rate.prefactor = process.rateConstant()
        process._KMCProcess__rate_constant = rate_LH(E_act[category][mol][react][0], process.rateConstant())
        if category == 'form' and mol == 'N2O' and react == config_map[Config]:
            set_fixed_rate.rate_constant = process.rateConstant()
