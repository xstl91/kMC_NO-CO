from .process_ads import p_ads
from .process_dif import p_dif
from .process_des import p_des
from .process_dis import p_dis
from .process_form import p_form

Process = {}
Process['ads'] = p_ads     # adsorption
Process['dif'] = p_dif     # diffusion
Process['des'] = p_des     # desorption
Process['dis'] = p_dis     # dissociation
Process['form'] = p_form   # formation
