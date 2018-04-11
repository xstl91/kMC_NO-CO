from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_dis = { 'NO':{} }

if Surface == '100':
    p_dis['NO']['brg'] = []
    for point,d in (('b1', 'u'), ('b1', 'd'), ('b2', 'r'), ('b2', 'l')):
        b1,b2 = [ d+x+d for x in ('r','l') ] if point == 'b1' else [ x+d*2 for x in ('u','d') ]
        p_dis['NO']['brg'].append( KMCProcess(
                                       coordinates     = [Origin, N3[d], N4[b1], N4[b2], N6[d], N7[b1], N7[b2]],
                                       elements_before = ['NO','o','o','o','o','o','o'],
                                       elements_after  = ['N' ,'O', 'o','o','o','o','o'],
                                       basis_sites     = [Bp_map[point]],
                                       rate_constant   = pre_sur(Vib_dis['NO']['brg'], Vib_ad['NO']['b']) ))
        p_dis['NO']['brg'][-1].name = ('dis', 'NO', 'brg', point)

elif Surface == '111':
    ends = { 'u': [N1['u'], N2['ur'], N2['ul'], N3['u']],
            'ur': [N1['ur'], N2['r'], N2['ur'], N3['ur']],
            'dr': [N1['dr'], N2['r'], N2['dr'], N3['dr']],
             'd': [N1['d'], N2['dr'], N2['dl'], N3['d']],
            'dl': [N1['dl'], N2['l'], N2['dl'], N3['dl']],
            'ul': [N1['ul'], N2['l'], N2['ul'], N3['ul']]}
    for name,near in (('fcc',('u','dr','dl')),('hcp',('d','ur','ul'))):
        p_dis['NO'][name] = []
        for d_1,d_2 in ( (x,y) for x in near for y in near if x != y ):
            p_dis['NO'][name].append( KMCProcess(
                                          coordinates     = [Origin] + ends[d_1] + ends[d_2],
                                          elements_before = ['NO'] + ['o']*8,
                                          elements_after  = ['o','N','o','o','o','O','o','o','o'],
                                          basis_sites     = [Bp_map[name[0]]],
                                          rate_constant   = pre_sur(Vib_dis['NO'][name], Vib_ad['NO'][name[0]]) ))
            p_dis['NO'][name][-1].name = ('dis', 'NO', name, name[0])
