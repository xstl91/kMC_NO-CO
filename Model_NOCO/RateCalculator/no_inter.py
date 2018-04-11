from ..rate import rate_LH
from ..parameter_E import *
from ..routine import processes
import __main__

def set_fixed_rate():
    for process in processes:
        category,mol,react,point = process.name
        if category == 'des':
            if mol in ('NO','CO'):
                process._KMCProcess__rate_constant = rate_LH(-E_bind[mol][react[0]], process.rateConstant())
            elif mol == 'O2':
                process._KMCProcess__rate_constant = rate_LH(E_act[category][mol][react][0], process.rateConstant())
        elif category in ('dif','dis','form'):
            if category == 'form' and mol == 'N2' and react in ('N-N_ff','N-N_hh'):
                process._KMCProcess__rate_constant = 2*rate_LH(E_act[category][mol][react][0], process.rateConstant())
            else:
                process._KMCProcess__rate_constant = rate_LH(E_act[category][mol][react][0], process.rateConstant())
        if __main__.static_dif and category == 'dif':
            process._KMCProcess__rate_constant *= __main__.dif_ratio_s[mol]
