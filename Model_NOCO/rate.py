from .constant import *
from .parameter_vib import *
import __main__
from numpy import pi,exp


T = __main__.T
kT = K*T


# partition function for translation
def _q_trans(mol, A_st):
    '''
    Calculate the partition function for 2D translation.
    :param mol:  molecule name
    :type  mol:  string
    :param A_st: area for per site, m^2
    :type  A_st: float
    '''
    return 2*pi*Mass[mol]*kT*A_st / H**2 


# partition function for rotation
def _q_rot(mol):
    '''
    Calculate the partition function for rotation.
    :param mol: molecule name
    :type  mol: string
    '''
    if mol in ('NO', 'CO'):
        m_a, m_b, r, multi = Mass[mol[0]],  Mass[mol[1]], Bond_l[mol], 1
    elif mol in ('N2', 'O2'):
        m_a, m_b, r, multi = Mass[mol[0]],  Mass[mol[0]], Bond_l[mol], 2
    else:
        raise Exception('Unsupported choice for calculating rotational partition function.')
    reduced_m = m_a*m_b / (m_a+m_b)               # reduced mass
    moment    = reduced_m * r**2                  # moment of inertia
    rot_T     = H**2 / (8 * pi**2 * moment * K)   # rotational temperature
    partition = T / (multi * rot_T)               # partition function
    return partition


# partition function for vibration
def _q_vib(freq_list):
    '''
    Calculate the partition function for rotation.
    :param freq_list: list of frequencies for vibration, Hz
    :type  freq_list: list of float
    '''
    accum = 1
    for freq in freq_list:
        vib_T     = H * freq / K
        partition = exp(-vib_T / (2*T)) / (1-exp(-vib_T / T))
        accum *= partition
    return accum


# prefactor for non-activated adsorption, i.e. rate constant
def pre_ads(mol, p, A_st):
    '''
    Calculate the rate constant for non-activated adsorption.
    :param mol: molecule name
    :type  mol: string
    :param p:   pressure, Pa
    :type  p:   float
    :param A_st: area for per site, m^2
    :type  A_st: float
    '''
    return p*A_st / (2*pi*Mass[mol]*kT)**0.5


# prefactor for desorption of non-activated adsorption
def pre_des(mol, A_st, *freq_l_i):
    '''
    Calculate the rate constant for desorption of non-activated adsorption.
    :param mol: molecule name
    :type  mol: string
    :param A_st: area for per site, m^2
    :type  A_st: float
    :param freq_l_i: list of vibrational frequencies for initial state, Hz
    :type  freq_l_i: list of float
    '''
    q_t_t = _q_trans(mol, A_st)    # partition function for transition state
    q_r_t = _q_rot(mol)
    q_v_t = _q_vib(Vib_gas[mol])
    freq_i = [ i for x in freq_l_i for i in x ]
    q_v_i = _q_vib(freq_i)         # partition function for initial state
    prefactor = kT/H * q_t_t*q_r_t*q_v_t/q_v_i
    return prefactor


# prefactor for L-H surface reaction
def pre_sur(freq_l_t, *freq_l_i):
    '''
    Calculate the rate constant for L-H surface reaction.
    :param freq_l_t: list of vibrational frequencies for transition state, Hz
    :type  freq_l_t: list of float
    :param freq_l_i: list of vibrational frequencies for initial state, Hz
    :type  freq_l_i: list of float
    '''
    q_v_t = _q_vib(freq_l_t)       # partition function for transition state
    freq_i = [ i for x in freq_l_i for i in x ]
    q_v_i = _q_vib(freq_i)         # partition function for initial state
    prefactor = kT/H * q_v_t/q_v_i
    return prefactor


# rate constant for L-H surface reaction
def rate_LH(E_bar, prefactor = 1e13):
    '''
    Calculate the rate constant.
    :param E_bar: energy barrier, without zero point energy, J
    :type  E_bar: float
    :param prefactor: pre-exponential factor
    :type  prefactor: float
    '''
    return prefactor * exp( -E_bar/kT )
