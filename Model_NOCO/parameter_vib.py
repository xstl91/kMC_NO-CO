from .constant import *

# structure for molecules
# conventional weight, kg
Mass = {'C' : M_C,
        'N' : M_N,
        'O' : M_O,
        'CO': M_C + M_O,
        'NO': M_N + M_O,
        'N2': M_N * 2,
        'O2': M_O * 2}
# bond distance for gas, m
Bond_l = {'CO': 1.14347e-10,
          'NO': 1.17232e-10,
          'N2': 1.11735e-10,
          'O2': 1.23608e-10}
# vibrational frequency for gas, Hz
Vib_gas = {'CO': [63.494798e12],
           'NO': [57.328453e12],
           'N2': [72.600932e12],
           'O2': [46.565965e12]}

# Get vibrational frequency for species on surface from (2x2) supercell
# vibrational frequency for stable adsorption state, Hz
Vib_ad = {}
# vibrational frequency for transition state of diffusion, Hz
Vib_dif = {}
# vibrational frequency for transition state of dissociation, Hz
Vib_dis = {}
# vibrational frequency for transition state of formation, Hz
Vib_form = {}
if Surface == '100':
    Vib_ad['N']    = {'b' : [18.518569e12, 16.703956e12,  2.478041e12],
                      'h' : [10.394186e12,  9.965291e12,  9.944956e12]}
    Vib_dif['N']   = {'bh': [18.301402e12, 16.252577e12]}
    Vib_ad['O']    = {'b' : [15.713888e12, 13.095904e12,  3.121071e12],
                      'h' : [11.250526e12,  5.281000e12,  5.262782e12]}
    Vib_dif['O']   = {'bh': [15.438793e12, 12.100397e12]}
    Vib_ad['NO']   = {'b' : [49.076663e12, 13.443827e12, 11.083520e12,
                              8.798510e12,  5.287027e12,  1.814127e12],
                      'h' : [43.388592e12,  9.885589e12,  9.866367e12,
                              7.631836e12,  3.485812e12,  3.433351e12],
                      't' : [55.343506e12, 14.609526e12,  7.793795e12,
                              7.779889e12,  1.350153e12,  1.309455e12]}
    Vib_dif['NO']  = {'bh': [45.594074e12, 11.309055e12,  9.441879e12,
                              5.875395e12,  4.309584e12],
                      'bt': [53.489889e12, 13.495543e12,  7.353492e12,
                              4.822443e12,  1.777636e12]}
    Vib_ad['CO']   = {'b' : [55.372769e12, 10.587345e12, 10.498931e12,
                              8.586661e12,  5.389030e12,  2.273925e12],
                      'h' : [50.097132e12,  7.698714e12,  6.160419e12,
                              6.147794e12,  3.919511e12,  3.871913e12],
                      't' : [59.673781e12, 13.490089e12, 10.838161e12,
                             10.835423e12,  2.007085e12,  1.927059e12]}
    Vib_dif['CO']  = {'bh': [51.261132e12,  8.768710e12,  6.919244e12,
                              5.199504e12,  4.292606e12],
                      'bt': [58.119809e12, 12.724090e12, 10.622712e12,
                              6.958356e12,  1.798331e12]}
    Vib_dis['NO']  = {'brg':[15.797894e12, 14.479149e12, 13.404828e12,
                             10.970114e12,  7.916673e12]}
    Vib_form['N2'] = {'N-N_bb' :[16.770332e12, 15.660210e12, 14.797506e12,
                                 14.246567e12,  5.991422e12],
                      'N-N_hb' :[19.063975e12, 17.093616e12, 12.514244e12,
                                 10.089118e12,  4.328790e12]}
    Vib_form['N2O']= {'N-NO_bb':[46.011885e12, 17.902125e12, 13.817403e12,
                                 10.714597e12, 10.129264e12,  7.393209e12,
                                  5.069095e12,  4.087923e12]}
    Vib_form['CO2']= {'O-CO_bb':[53.334983e12, 17.117226e12, 10.994955e12,
                                 10.607553e12,  8.030856e12,  6.866818e12,
                                  4.727634e12,  3.997399e12]}

elif Surface == '111':
    Vib_ad['N']    = {'f' : [15.489026e12, 12.933185e12, 12.919833e12],
                      'h' : [15.877149e12, 12.975680e12, 12.945329e12]}
    Vib_dif['N']   = {'fh': [18.735513e12, 16.101440e12]}
    Vib_ad['O']    = {'f' : [14.318462e12, 10.529161e12, 10.490579e12],
                      'h' : [14.297974e12, 10.015344e12,  9.976111e12]}
    Vib_dif['O']   = {'fh': [15.850534e12, 11.721845e12]}
    Vib_ad['NO']   = {'f' : [46.599826e12,  9.882411e12,  9.851651e12,
                              9.791210e12,  3.744262e12,  3.473197e12],
                      'h' : [46.492560e12, 11.129754e12, 11.120694e12,
                             10.136189e12,  4.227303e12,  4.192900e12],
                      't' : [55.907343e12, 14.528206e12,  7.491485e12,
                              7.422356e12,  1.565460e12,  1.182730e12]}
    Vib_dif['NO']  = {'fh': [48.718968e12, 13.291988e12, 10.736823e12,
                              6.095976e12,  5.243794e12],    # b-h for TS 
                      'ft': [53.172067e12, 13.087445e12,  4.948218e12,
                              4.157678e12,  1e12],  # one more f/i, set to 1e12
                      'ht': [52.962908e12, 12.984452e12,  4.066997e12,
                              3.932034e12,  1e12]}  # one more f/i, set to 1e12
    Vib_ad['CO']   = {'f' : [53.300149e12,  9.669118e12,  6.253180e12,
                              6.218388e12,  3.238900e12,  3.175964e12],
                      'h' : [52.896896e12, 10.008173e12,  7.584936e12,
                              7.545438e12,  3.969956e12,  3.875542e12],
                      't' : [60.128952e12, 13.581979e12, 11.952567e12,
                             11.937563e12,  1.614249e12,  1.364234e12]}
    Vib_dif['CO']  = {'fh': [53.938474e12, 10.155034e12,  8.062177e12,
                              7.038350e12,  4.880644e12],
                      'ft': [57.052263e12, 12.389149e12,  8.446128e12,
                              6.271867e12,  1e12],  # one more f/i, set to 1e12
                      'ht': [57.331472e12, 12.558485e12,  8.203419e12,
                              6.143468e12,  1e12]}  # one more f/i, set to 1e12
    Vib_dis['NO']  = {'fcc':[17.339607e12, 14.618672e12, 11.983936e12,
                              8.690146e12,  6.052976e12],
                      'hcp':[17.920375e12, 14.719577e12, 11.616459e12,
                              8.665347e12,  6.587738e12]}
    Vib_form['N2'] = {'N-N_ff' :[17.385188e12, 16.438426e12, 12.416260e12,
                                 10.802966e12,  6.276882e12],
                      'N-N_hh' :[17.225915e12, 15.921602e12, 12.246919e12,
                                 10.503985e12,  5.899589e12]}
    Vib_form['N2O']= {'N-NO_ft':[51.728761e12, 17.193977e12, 12.419070e12,
                                 12.074288e12,  9.526192e12,  7.931204e12,
                                  4.056887e12,  2.210329e12],
                      'N-NO_ht':[51.930543e12, 17.277082e12, 12.573051e12,
                                 11.926747e12, 10.178933e12,  7.630031e12,
                                  3.533290e12,  2.138662e12]}
    Vib_form['CO2']= {'O-CO_ft':[57.252504e12, 17.129088e12, 12.967747e12,
                                 12.021592e12,  8.687262e12,  8.562862e12,
                                  3.962540e12,  2.537505e12],
                      'O-CO_ht':[57.720238e12, 16.942411e12, 13.441371e12,
                                 11.952009e12,  8.497839e12,  8.288978e12,
                                  3.611881e12,  2.171511e12]}
