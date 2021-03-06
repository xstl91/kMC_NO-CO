from .constant import Surface,EV
import __main__

x_T = __main__.T/1000.0

# molecule formation energy
E_mol = { 'N2': -10.002*EV,
          'O2':  -5.701*EV,
          'NO':  -6.911*EV,
          'CO': -11.185*EV}


# binding energy of stable adsorption state at zero coverage, J
if Surface == '100':
    E_bind = { 'N' : {'b': -4.596*EV, 'h': -5.093*EV},
               'O' : {'b': -4.465*EV, 'h': -4.554*EV},
               'NO': {'b': -2.208*EV, 'h': -1.943*EV, 't': -1.881*EV},
               'CO': {'b': -1.705*EV, 'h': -1.531*EV, 't': -1.636*EV}}
elif Surface == '111':
    E_bind = { 'N' : {'f': -4.963*EV, 'h': -5.086*EV},
               'O' : {'f': -4.625*EV, 'h': -4.574*EV},
               'NO': {'f': -2.098*EV, 'h': -2.146*EV, 't': -1.669*EV},
               'CO': {'f': -1.627*EV, 'h': -1.682*EV, 't': -1.630*EV}}


# BEP relation: activation energy (J), slope and reaction energy
E_act = {}
def f_T(a,b,c):
    return a*x_T**2 + b*x_T + c
if Surface == '100':
    E_act['dif'] = {'N' :{ 'b-h': (0.007*EV, 0.06, -0.497*EV),
                           'h-b': (0.504*EV, 0.94,  0.497*EV)},
                    'O' :{ 'b-h': (0.032*EV, 0.34, -0.089*EV),
                           'h-b': (0.121*EV, 0.66,  0.089*EV)},
                    'NO':{ 'b-h': (0.294*EV, 0.55,  0.265*EV),
                           'h-b': (0.029*EV, 0.45, -0.265*EV),
                           'b-t': (0.461*EV, 0.79,  0.327*EV),
                           't-b': (0.134*EV, 0.21, -0.327*EV)},
                    'CO':{ 'b-h': (0.197*EV, 0.88,  0.174*EV),
                           'h-b': (0.023*EV, 0.12, -0.174*EV),
                           'b-t': (0.134*EV, 0.53,  0.069*EV),
                           't-b': (0.065*EV, 0.47, -0.069*EV)}}
    E_act['dis'] = {'NO':{ 'brg': (0.774*EV, 0.46,  0.096*EV)}}
    E_act['form']= {'NO' :{ 'N-O_bb' : (0.678*EV, 0.54, -0.096*EV)},
                    'N2' :{ 'N-N_bb' : (0.594*EV, 0.39, -0.858*EV),
                            'N-N_hb' : (1.666*EV, 0.90, -0.496*EV),
                            'N-NO_bb': (f_T(6.8314e-02, -1.0283e-02, 1.0842e+00)*EV, f_T(7.9302e-02, -2.3628e-01, 5.1333e-01), -0.822*EV)},
                    'N2O':{ 'N-NO_bb': (f_T(1.0663e-01, -2.2376e-01, 1.3569e+00)*EV, f_T(8.2343e-02, -2.5011e-01, 7.6552e-01),  1.082*EV)},
                    'CO2':{ 'O-CO_bb': (0.766*EV, 0.48,  0.118*EV)}}
    E_act['des'] = {'O2' :{ 'O-O_bb' : (3.193*EV, 1.00,  3.193*EV)}}
elif Surface == '111':
    E_act['dif'] = {'N' :{ 'f-h': (0.526*EV, 0.39, -0.123*EV),
                           'h-f': (0.649*EV, 0.61,  0.123*EV)},
                    'O' :{ 'f-h': (0.442*EV, 0.43,  0.051*EV),
                           'h-f': (0.391*EV, 0.57, -0.051*EV)},
                    'NO':{ 'f-h': (0.138*EV, 0.48, -0.048*EV),
                           'h-f': (0.186*EV, 0.52,  0.048*EV),
                           'f-t': (0.572*EV, 0.74,  0.429*EV),
                           't-f': (0.143*EV, 0.26, -0.429*EV),
                           'h-t': (0.634*EV, 0.70,  0.477*EV),
                           't-h': (0.157*EV, 0.30, -0.477*EV)},
                    'CO':{ 'f-h': (0.043*EV, 0.40, -0.055*EV),
                           'h-f': (0.098*EV, 0.60,  0.055*EV),
                           'f-t': (0.166*EV, 0.43, -0.003*EV),
                           't-f': (0.169*EV, 0.57,  0.003*EV),
                           'h-t': (0.222*EV, 0.58,  0.052*EV),
                           't-h': (0.170*EV, 0.42, -0.052*EV)}}
    E_act['dis'] = {'NO':{ 'fcc': (1.655*EV, 0.48, -0.373*EV),
                           'hcp': (1.678*EV, 0.56, -0.299*EV)}}
    E_act['form']= {'NO' :{ 'N-O_ff' : (1.977*EV, 0.44,  0.299*EV),
                            'N-O_hh' : (2.028*EV, 0.52,  0.373*EV)},
                    'N2' :{ 'N-N_ff' : (1.942*EV, 0.47, -0.325*EV),
                            'N-N_hh' : (2.104*EV, 0.51, -0.169*EV),
                            'N-NO_ft': (f_T(-6.2321e-02,  3.5146e-01, 1.7735e+00)*EV, f_T(4.2374e-01, -1.1244e+00, 7.3030e-01), -1.106*EV),
                            'N-NO_ht': (f_T(-6.9069e-02,  3.7167e-01, 1.9189e+00)*EV, f_T(4.6900e-01, -1.1577e+00, 7.9202e-01), -1.031*EV)},
                    'N2O':{ 'N-NO_ft': (f_T( 3.6600e-02, -2.6064e-02, 1.4388e+00)*EV, f_T(1.5112e-02,  5.6168e-03, 4.6109e-01),  0.907*EV),
                            'N-NO_ht': (f_T( 3.6475e-02, -3.3715e-02, 1.5910e+00)*EV, f_T(9.7000e-03, -1.2737e-03, 4.8965e-01),  1.033*EV)},
                    'CO2':{ 'O-CO_ft': (1.215*EV, 0.31,  0.212*EV),
                            'O-CO_ht': (1.174*EV, 0.35,  0.148*EV)}}
    E_act['des'] = {'O2' :{ 'O-O_ff' : (3.331*EV, 1.00,  3.331*EV), 
                            'O-O_hh' : (3.211*EV, 1.00,  3.211*EV)}}
    # modification energy
    E_modify  = { 'N' : {'l': -0.047*EV, 'h':  0.128*EV},
                  'O' : {'l': -0.042*EV, 'h':  0.067*EV},
                  'NO': {'l': -0.021*EV, 'h':  0.044*EV},
                  'CO': {'l': -0.018*EV, 'h':  0.012*EV}}
