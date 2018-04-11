from .process_form import p_form
from .process_form import p_back
from .process_trans import p_trans
from .process_dis import p_dis
from .process_des import p_des

Process = {}
Process['form'] = p_form     # formation
Process['back'] = p_back     # reverse of formation
Process['trans'] = p_trans   # transformation
Process['dis'] = p_dis       # dissociation
Process['des'] = p_des       # desorption
