from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_form = { 'NO':{}, 'N2':{}, 'N2O':{}, 'CO2':{} }

if Surface == '100':
    # formation of NO
    mol,name = 'NO','N-O_bb'
    p_form[mol][name] = []
    for point,d in (('b1', 'u'), ('b1', 'd'), ('b2', 'r'), ('b2', 'l')):
        p_form[mol][name].append( KMCProcess(
                                        coordinates     = [Origin, N3[d]],
                                        elements_before = ['N', 'O'],
                                        elements_after  = ['NO','o'],
                                        basis_sites     = [Bp_map[point]],
                                        rate_constant   = pre_sur(Vib_dis['NO']['brg'], Vib_ad['N']['b'], Vib_ad['O']['b']) ))
        p_form[mol][name][-1].name = ('form', mol, name, point)

    # formation of N2
    mol = 'N2'
    name = 'N-N_bb'
    p_form[mol][name] = []
    for point,d in (('b1', 'u'), ('b2', 'r')):
        p_form[mol][name].append( KMCProcess(
                                      coordinates     = [Origin, N3[d]],
                                      elements_before = ['N', 'N'],
                                      elements_after  = ['o', 'o'],
                                      basis_sites     = [Bp_map[point]],
                                      rate_constant   = pre_sur(Vib_form[mol][name], Vib_ad['N']['b'], Vib_ad['N']['b']) ))
        p_form[mol][name][-1].name = ('form', mol, name, point)
    name = 'N-N_hb'
    p_form[mol][name] = []
    for end in N4.values():
        p_form[mol][name].append( KMCProcess(
                                      coordinates     = [Origin, end],
                                      elements_before = ['N', 'N'],
                                      elements_after  = ['o', 'o'],
                                      basis_sites     = [Bp_map['h']],
                                      rate_constant   = pre_sur(Vib_form[mol][name], Vib_ad['N']['h'], Vib_ad['N']['b']) ))
        p_form[mol][name][-1].name = ('form', mol, name, 'h')

    # formation of N2O
    name = 'N-NO_bb'
    for mol,atom in (('N2','O'),('N2O','o')):
        p_form[mol][name] = []
        for point,d in (('b1', 'u'), ('b1', 'd'), ('b2', 'r'), ('b2', 'l')):
            p_form[mol][name].append( KMCProcess(
                                          coordinates     = [Origin, N3[d]],
                                          elements_before = ['N', 'NO'],
                                          elements_after  = ['o',atom],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N']['b'], Vib_ad['NO']['b']) ))
            p_form[mol][name][-1].name = ('form', mol, name, point)

    # formation of CO2
    mol,name = 'CO2','O-CO_bb'
    p_form[mol][name] = []
    for point,d in (('b1', 'u'), ('b1', 'd'), ('b2', 'r'), ('b2', 'l')):
        p_form[mol][name].append( KMCProcess(
                                      coordinates     = [Origin, N3[d]],
                                      elements_before = ['O', 'CO'],
                                      elements_after  = ['o', 'o'],
                                      basis_sites     = [Bp_map[point]],
                                      rate_constant   = pre_sur(Vib_form[mol][name], Vib_ad['O']['b'], Vib_ad['CO']['b']) ))
        p_form[mol][name][-1].name = ('form', mol, name, point)


elif Surface == '111':
    # formation of NO
    mol = 'NO'
    for name,TS,near in (('N-O_ff','hcp',('d','ur','ul')), ('N-O_hh','fcc',('u','dr','dl'))):
        p_form[mol][name] = []
        point = TS[0]
        for d_N,d_O,b in ( (x,y,z) for x in near for y in near for z in near if (x!=y and x!=z and y!=z) ):
            p_form[mol][name].append( KMCProcess(
                                          coordinates     = [Origin, N1[d_N], N1[d_O], N1[b]],
                                          elements_before = ['o','N','O','o'],
                                          elements_after  = ['NO','o','o','o'],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_sur(Vib_dis['NO'][TS], Vib_ad['N'][name[-1]], Vib_ad['O'][name[-1]]) ))
            p_form[mol][name][-1].name = ('form', mol, name, point)

    # formation of N2
    mol = 'N2'
    for name,point,near in (('N-N_ff','h',('d','ur','ul')), ('N-N_hh','f',('u','dr','dl'))):
        p_form[mol][name] = []
        for d1,d2,b in ( (near[x],near[y],near[z]) for x in range(3) for y in range(x+1,3) for z in range(3) if (z!=x and z!=y) ):
            p_form[mol][name].append( KMCProcess(
                                          coordinates     = [Origin, N1[d1], N1[d2], N1[b]],
                                          elements_before = ['o','N','N','o'],
                                          elements_after  = ['o','o','o','o'],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_sur(Vib_form['N2'][name], Vib_ad['N'][name[-1]], Vib_ad['N'][name[-1]]) ))
            p_form[mol][name][-1].name = ('form', mol, name, point)

    # formation of N2O
    for mol,atom in (('N2','O'),('N2O','o')):
        for name,near in (('N-NO_ft',('u','dr','dl')),('N-NO_ht',('d','ur','ul'))):
            p_form[mol][name] = []
            point = name[5]
            for d in near:
                p_form[mol][name].append( KMCProcess(
                                              coordinates     = [Origin, N3[d], N1[d]],
                                              elements_before = ['N', 'NO', 'o'],
                                              elements_after  = ['o', 'o', atom],
                                              basis_sites     = [Bp_map[point]],
                                              rate_constant   = pre_sur(Vib_form['N2O'][name], Vib_ad['N'][point], Vib_ad['NO']['t']) ))
                p_form[mol][name][-1].name = ('form', mol, name, point)

    # formation of CO2
    mol = 'CO2'
    for name,near in (('O-CO_ft',('u','dr','dl')),('O-CO_ht',('d','ur','ul'))):
        p_form[mol][name] = []
        point = name[5]
        for d in near:
            p_form[mol][name].append( KMCProcess(
                                          coordinates     = [Origin, N3[d]],
                                          elements_before = ['O', 'CO'],
                                          elements_after  = ['o', 'o'],
                                          basis_sites     = [Bp_map[point]],
                                          rate_constant   = pre_sur(Vib_form[mol][name], Vib_ad['O'][point], Vib_ad['CO']['t']) ))
            p_form[mol][name][-1].name = ('form', mol, name, point)
