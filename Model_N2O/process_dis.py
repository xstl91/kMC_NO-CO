from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_dis = {}

if Surface == '100':
    p_dis['N2O'] = { x:[] for x in ('flat-u', 'flat-d', 'NOtbt', 'NOtht') }

    for point,d,d_O in (('b1','u','uru'), ('b1','u','ulu'), ('b1','d','drd'), ('b1','d','dld'),
                        ('b2','r','urr'), ('b2','r','drr'), ('b2','l','ull'), ('b2','l','dll')):
        for name in ('flat-u', 'flat-d'):
            p_dis['N2O'][name].append( KMCProcess(
                                           coordinates     = [Origin, N1[d], N3[d], N4[d_O]],
                                           elements_before = ['flat-N', 'flat-mN', 'flat-mO', 'falt-O'],
                                           elements_after  = ['o', 'o', 'O', 'o'],
                                           basis_sites     = [Bp_map[point]],
                                           rate_constant   = pre_sur(Vib_dis['N2O'][name], Vib_ad['N2O']['flat'] )))
            p_dis['N2O'][name][-1].name = ('dis', 'N2O', name, point)

    name = 'NOtbt'
    for d,d_m in (('u','r'), ('u','l'), ('d','r'), ('d','l'),
                  ('r','u'), ('r','d'), ('l','u'), ('l','d')):
        diag = (d + d_m) if d in ('u','d') else (d_m + d)
        p_dis['N2O'][name].append( KMCProcess(
                                       coordinates     = [Origin, N1[d], N3[d], N4[diag+d], N4[diag+d_m], N5[diag], N8[diag+d] ],
                                       elements_before = ['NOtbt-N', 'NOtbt-m', 'NOtbt-O', 'o', 'o', 'o', 'o'],
                                       elements_after  = ['o', 'o', 'o', 'O', 'o','o','o'],
                                       basis_sites     = [Bp_map['t']],
                                       rate_constant   = pre_sur(Vib_dis['N2O'][name], Vib_ad['N2O'][name] )))
        p_dis['N2O'][name][-1].name = ('dis', 'N2O', name, 't')

    name = 'NOtht'
    for d,d_m in (('ur','u'), ('ur','r'), ('dr','d'), ('dr','r'),
                  ('ul','u'), ('ul','l'), ('dl','d'), ('dl','l')):
        p_dis['N2O'][name].append( KMCProcess(
                                       coordinates     = [Origin, N2[d], N5[d], N4[d+d_m], N6[d_m] ],
                                       elements_before = ['NOtht-N', 'NOtht-m', 'NOtht-O', 'o', 'o'],
                                       elements_after  = ['o', 'o', 'o', 'O', 'o'],
                                       basis_sites     = [Bp_map['t']],
                                       rate_constant   = pre_sur(Vib_dis['N2O'][name], Vib_ad['N2O'][name] )))
        p_dis['N2O'][name][-1].name = ('dis', 'N2O', name, 't')


elif Surface == '111':
    p_dis['N2O'] = { x:[] for x in ('NOtbt-f', 'NOtbt-h') }

    for end,d,d_O,b in (('f','ur','ur', 'ru'), ('f', 'r','ur','urr'),
                        ('f','dr', 'd','dld'), ('f','dl', 'd','drd'),
                        ('f', 'l','ul','ull'), ('f','ul','ul', 'lu'),
                        ('h','ur', 'u','ulu'), ('h','ul', 'u','uru'),
                        ('h', 'l','dl','dll'), ('h','dl','dl', 'ld'),
                        ('h','dr','dr', 'rd'), ('h', 'r','dr','drr')):
        name = 'NOtbt-'+end
        p_dis['N2O'][name].append( KMCProcess(
                                       coordinates     = [Origin, N2[d], N3[d_O], N5[d_O], N4[b], N2[b[:-1]]],
                                       elements_before = ['NOtbt-N', 'NOtbt-O', 'o', 'o', 'o', 'o'],
                                       elements_after  = [ 'o', 'o', 'O', 'o', 'o', 'o'],
                                       basis_sites     = [Bp_map['t']],
                                       rate_constant   = pre_sur(Vib_dis['N2O'][name], Vib_ad['N2O']['NOtbt']) ))
        p_dis['N2O'][name][-1].name = ('dis', 'N2O', name, 't')
