from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_form = { 'N2O':{} }
p_back = { 'N2O':{} }

if Surface == '100':
    name = 'NNbhb'
    p_form['N2O'][name] = []
    p_back['N2O'][name] = []
    for point,d in (('b1', 'u'), ('b1', 'd'), ('b2', 'r'), ('b2', 'l')):
        p_form['N2O'][name].append( KMCProcess(
                                        coordinates     = [Origin, N1[d], N3[d]],
                                        elements_before = ['N', 'o', 'NO'],
                                        elements_after  = ['NNbhb-N', 'NNbhb-m', 'NNbhb-O'],
                                        basis_sites     = [Bp_map[point]],
                                        rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N']['b'], Vib_ad['NO']['b']) ))
        p_form['N2O'][name][-1].name = ('form', 'N2O', name, point)
        p_back['N2O'][name].append( KMCProcess(
                                        coordinates     = [Origin, N1[d], N3[d]],
                                        elements_before = ['NNbhb-N', 'NNbhb-m', 'NNbhb-O'],
                                        elements_after  = ['N', 'o', 'NO'],
                                        basis_sites     = [Bp_map[point]],
                                        rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N2O'][name]) ))
        p_back['N2O'][name][-1].name = ('back', 'N2O', name, point)


elif Surface == '111':
    p_form['N2O'] = { 'NNbftt': [], 'NNbhtt': [] }
    p_back['N2O'] = { 'NNbftt': [], 'NNbhtt': [] }
    for name,point,d in (('NNbhtt','f','u'), ('NNbhtt','f','dr'), ('NNbhtt','f','dl'),
                         ('NNbftt','h','d'), ('NNbftt','h','ur'), ('NNbftt','h','ul')):
        p_form['N2O'][name].append( KMCProcess(
                                        coordinates     = [Origin, N1[d], N3[d]],
                                        elements_before = ['N', 'o', 'NO'],
                                        elements_after  = [name+'-N', name+'-m', name+'-O'],
                                        basis_sites     = [Bp_map[point]],
                                        rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N'][point], Vib_ad['NO']['t']) ))
        p_form['N2O'][name][-1].name = ('form', 'N2O', name, point)
        p_back['N2O'][name].append( KMCProcess(
                                        coordinates     = [Origin, N1[d], N3[d]],
                                        elements_before = [name+'-N', name+'-m', name+'-O'],
                                        elements_after  = ['N', 'o', 'NO'],
                                        basis_sites     = [Bp_map[point]],
                                        rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N2O'][name]) ))
        p_back['N2O'][name][-1].name = ('back', 'N2O', name, point)
