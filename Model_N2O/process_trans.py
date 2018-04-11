from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_trans = { 'N2O':{} }


if Surface == '100':

    name = 'NNbhb-flat'
    p_trans['N2O'][name] = []
    for point,d,d_O in (('b1','u','uru'), ('b1','u','ulu'), ('b1','d','drd'), ('b1','d','dld'),
                        ('b2','r','urr'), ('b2','r','drr'), ('b2','l','ull'), ('b2','l','dll')):
        b = d_O[:-1] + d_O[ 1 if point == 'b1' else 0 ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[d_O], N4[b], N5[d_O[:-1]], N8[d_O]],
                                         elements_before = ['NNbhb-N', 'NNbhb-m', 'NNbhb-O', 'o', 'o', 'o', 'o'],
                                         elements_after  = ['flat-N', 'flat-mN', 'flat-mO', 'falt-O', 'o', 'o', 'o'],
                                         basis_sites     = [Bp_map[point]],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['NNbhb'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    name = 'flat-NNbhb'
    p_trans['N2O'][name] = []
    for point,d,d_O in (('b1','u','uru'), ('b1','u','ulu'), ('b1','d','drd'), ('b1','d','dld'),
                        ('b2','r','urr'), ('b2','r','drr'), ('b2','l','ull'), ('b2','l','dll')):
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[d_O]],
                                         elements_before = ['flat-N', 'flat-mN', 'flat-mO', 'falt-O'],
                                         elements_after  = ['NNbhb-N', 'NNbhb-m', 'NNbhb-O', 'o'],
                                         basis_sites     = [Bp_map[point]],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['NNbhb-flat'], Vib_ad['N2O']['flat'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    name = 'flat-NOtbt'
    p_trans['N2O'][name] = []
    for point,d,d_O,b in (('b1','u','uru','drr'), ('b1','u','ulu','dll'), ('b1','d','drd','urr'), ('b1','d','dld','ull'),
                          ('b2','r','urr','ulu'), ('b2','r','drr','dld'), ('b2','l','ull','uru'), ('b2','l','dll','drd')):
        d_N = d_O[ 1 if point == 'b1' else 0 ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[d_O], N1[d_N], N2[d_O[:-1]], N3[d_N], N4[b]],
                                         elements_before = ['flat-N', 'flat-mN', 'flat-mO', 'falt-O', 'o', 'o', 'o','o'],
                                         elements_after  = ['o', 'o', 'o', 'NOtbt-O', 'NOtbt-N', 'NOtbt-m', 'o', 'o'],
                                         basis_sites     = [Bp_map[point]],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['flat'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    name = 'NOtbt-flat'
    p_trans['N2O'][name] = []
    for d,d_m,b1 in (('u','r','drr'), ('u','l','dll'), ('d','r','urr'), ('d','l','ull'),
                     ('r','u','ulu'), ('r','d','dld'), ('l','u','uru'), ('l','d','drd')):
        h = (d + d_m) if d in ('u','d') else (d_m + d)
        d_N = h + d
        b2 = h + d_m
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N1[d_m], N2[h], N4[d_N], N3[d_m], N4[b1], N4[b2], N5[h], N8[d_N]],
                                         elements_before = ['NOtbt-O', 'NOtbt-m', 'NOtbt-N', 'o', 'o', 'o', 'o', 'o', 'o','o', 'o'],
                                         elements_after  = ['falt-O','o','o','flat-mO', 'flat-mN', 'flat-N', 'o', 'o', 'o', 'o','o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['flat-NOtbt'], Vib_ad['N2O']['NOtbt'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'flat-NOtht'
    p_trans['N2O'][name] = []
    for point,d,d_O,d_N in (('b1','u','uru','l'), ('b1','u','ulu','r'), ('b1','d','drd','l'), ('b1','d','dld','r'),
                            ('b2','r','urr','d'), ('b2','r','drr','u'), ('b2','l','ull','d'), ('b2','l','dll','u')):
        b1,b2 = [ x+d_N*2 for x in ('u','d') ] if point == 'b1' else [ d_N+x+d_N for x in ('l','r') ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[d_O], N1[d_N], N3[d_N], N4[b1], N4[b2]],
                                         elements_before = ['flat-N', 'flat-mN', 'flat-mO', 'falt-O', 'o', 'o', 'o','o'],
                                         elements_after  = ['o', 'NOtht-m', 'o', 'NOtht-O', 'NOtht-N', 'o', 'o', 'o'],
                                         basis_sites     = [Bp_map[point]],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['flat'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    name = 'NOtht-flat'
    p_trans['N2O'][name] = []
    for d,d_N,b in (('ur','u','drr'), ('ur','r','ulu'), ('dr','d','urr'), ('dr','r','dld'),
                    ('ul','u','dll'), ('ul','l','uru'), ('dl','d','ull'), ('dl','l','drd')):
        d_m = [ x for x in d if x != d_N ][0]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N2[d], N5[d], N1[d_m], N4[d+d_N], N4[b], N6[d_N]],
                                         elements_before = ['NOtht-O', 'NOtht-m', 'NOtht-N', 'o', 'o', 'o', 'o'],
                                         elements_after  = ['falt-O','flat-mN','o','flat-mO', 'flat-N', 'o', 'o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['flat-NOtht'], Vib_ad['N2O']['NOtht'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'NNbhb-NNtbt'
    p_trans['N2O'][name] = []
    for point,d,d_m in (('b1','u','r'), ('b1','u','l'), ('b1','d','r'), ('b1','d','l'),
                        ('b2','r','u'), ('b2','r','d'), ('b2','l','u'), ('b2','l','d')):
        diag = (d + d_m) if d in ('u','d') else (d_m + d)
        b1,b2 = [ x+d_m*2 for x in ('u','d') ] if point == 'b1' else [ d_m+x+d_m for x in ('l','r') ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N1[d_m], N2[diag], N4[diag+d], N3[d_m], N4[b1], N4[b2], N5[diag], N8[diag+d]],
                                         elements_before = ['NNbhb-N', 'NNbhb-m', 'NNbhb-O', 'o', 'o', 'o', 'o','o','o','o','o'],
                                         elements_after  = ['o', 'o', 'o', 'NNtbt-N', 'NNtbt-m', 'NNtbt-O', 'o','o','o','o','o'],
                                         basis_sites     = [Bp_map[point]],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['NNbhb'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    name = 'NNtbt-NNbhb'
    p_trans['N2O'][name] = []
    for d,d_m in (('u','r'), ('u','l'), ('d','r'), ('d','l'),
                  ('r','u'), ('r','d'), ('l','u'), ('l','d')):
        diag = (d + d_m) if d in ('u','d') else (d_m + d)
        b1,b2 = [ x+d_m*2 for x in ('u','d') ] if d in ('u','d') else [ d_m+x+d_m for x in ('l','r') ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N1[d_m], N2[diag], N4[diag+d], N3[d_m], N4[b1], N4[b2], N5[diag], N8[diag+d]],
                                         elements_before = ['NNtbt-N', 'NNtbt-m', 'NNtbt-O', 'o', 'o', 'o', 'o','o','o','o','o'],
                                         elements_after  = ['o', 'o', 'o', 'NNbhb-N', 'NNbhb-m', 'NNbhb-O', 'o','o','o','o','o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['NNbhb-NNtbt'], Vib_ad['N2O']['NNtbt'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'NNtbt-top'
    p_trans['N2O'][name] = []
    for d in ('u', 'd', 'r', 'l'):
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d]],
                                         elements_before = ['NNtbt-N', 'NNtbt-m', 'NNtbt-O'],
                                         elements_after  = ['top', 'o', 'o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['NNtbt'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'top-NNtbt'
    p_trans['N2O'][name] = []
    for d in ('u', 'd', 'r', 'l'):
        b1,b2 = [ d+x+d for x in ('r','l') ] if d in ('u','d') else [ x+d*2 for x in ('u','d') ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[b1], N4[b2], N6[d], N7[b1], N7[b2]],
                                         elements_before = ['top', 'o', 'o', 'o','o','o','o','o'],
                                         elements_after  = ['NNtbt-N', 'NNtbt-m', 'NNtbt-O', 'o','o','o','o','o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['NNtbt-top'], Vib_ad['N2O']['top'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'top-NOtbt'
    p_trans['N2O'][name] = []
    for d in ('u', 'd', 'r', 'l'):
        b1,b2 = [ d+x+d for x in ('r','l') ] if d in ('u','d') else [ x+d*2 for x in ('u','d') ]
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d], N4[b1], N4[b2], N6[d], N7[b1], N7[b2]],
                                         elements_before = ['top', 'o', 'o', 'o','o','o','o','o'],
                                         elements_after  = ['NOtbt-N', 'NOtbt-m', 'NOtbt-O', 'o','o','o','o','o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['top'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'NOtbt-top'
    p_trans['N2O'][name] = []
    for d in ('u', 'd', 'r', 'l'):
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N1[d], N3[d]],
                                         elements_before = ['NOtbt-N', 'NOtbt-m', 'NOtbt-O'],
                                         elements_after  = ['top', 'o', 'o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['top-NOtbt'], Vib_ad['N2O']['NOtbt'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'top-NOtht'
    p_trans['N2O'][name] = []
    for d in ('ur', 'ul', 'dr', 'dl'):
        b1,b2 = d
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N2[d], N5[d], N3[b1], N3[b2], N4[d+b1], N4[d+b2], N7[d+b1], N7[d+b2], N8[d+b1], N8[d+b2], N11[d]],
                                         elements_before = ['top', 'o', 'o', 'o','o','o','o','o','o','o','o','o'],
                                         elements_after  = ['NOtht-N', 'NOtht-m', 'NOtht-O', 'o','o','o','o','o','o','o','o','o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O']['top'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    name = 'NOtht-top'
    p_trans['N2O'][name] = []
    for d in ('ur', 'ul', 'dr', 'dl'):
        p_trans['N2O'][name].append( KMCProcess(
                                         coordinates     = [Origin, N2[d], N5[d]],
                                         elements_before = ['NOtht-N', 'NOtht-m', 'NOtht-O'],
                                         elements_after  = ['top', 'o', 'o'],
                                         basis_sites     = [Bp_map['t']],
                                         rate_constant   = pre_sur(Vib_trans['N2O']['top-NOtht'], Vib_ad['N2O']['NOtht'] )))
        p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')


elif Surface == '111':

    for is_c, fs_c in (('NNbftt','NNtbt'), ('NNbhtt','NNtbt'), ('NObft','NOtbt'), ('NObht','NOtbt')):
        name = is_c +'-'+ fs_c
        p_trans['N2O'][name] = []
        if is_c[3] == 'f':
            config = (('h', 'd','dl', 'l'), ('h', 'd','dr', 'r'),
                      ('h','ur','dr','dr'), ('h','ur', 'u','ul'),
                      ('h','ul','dl','dl'), ('h','ul', 'u','ur'))
        elif is_c[3] == 'h':
            config = (('f', 'u','ul', 'l'), ('f', 'u','ur', 'r'),
                      ('f','dr','ur','ur'), ('f','dr', 'd','dl'),
                      ('f','dl','ul','ul'), ('f','dl', 'd','dr'))
        for point,d,d_N,b in config:
            p_trans['N2O'][name].append( KMCProcess(
                                             coordinates     = [Origin, N1[d], N3[d], N1[d_N], N2[b], N3[d_N]],
                                             elements_before = [is_c+'-N', is_c+'-m', is_c+'-O', 'o', 'o', 'o'],
                                             elements_after  = ['o', 'o', fs_c+'-O', fs_c+'-N', 'o', 'o'],
                                             basis_sites     = [Bp_map[point]],
                                             rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O'][is_c]) ))
            p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, point)

    for is_c, fs_c in (('NNtbt','NNbftt'), ('NNtbt','NNbhtt'), ('NOtbt','NObft'), ('NOtbt','NObht')):
        name = is_c +'-'+ fs_c
        p_trans['N2O'][name] = []
        if fs_c[3] == 'f':
            config = (('ur', 'u','ulu'), ('ul', 'u','uru'),
                      ( 'l','dl','dll'), ('dl','dl', 'ld'),
                      ('dr','dr', 'rd'), ( 'r','dr','drr'))
        elif fs_c[3] == 'h':
            config = (('ur','ur', 'ru'), ( 'r','ur','urr'),
                      ('dr', 'd','dld'), ('dl', 'd','drd'),
                      ( 'l','ul','ull'), ('ul','ul', 'lu'))
        for d,d_N,b in config:
            p_trans['N2O'][name].append( KMCProcess(
                                             coordinates     = [Origin, N2[d], N1[d_N], N3[d_N], N5[d_N], N4[b], N2[b[:-1]]],
                                             elements_before = [is_c+'-O', is_c+'-N', 'o', 'o', 'o', 'o', 'o'],
                                             elements_after  = [fs_c+'-O', 'o', fs_c+'-m', fs_c+'-N', 'o', 'o', 'o'],
                                             basis_sites     = [Bp_map['t']],
                                             rate_constant   = pre_sur(Vib_trans['N2O'][fs_c+'-'+is_c], Vib_ad['N2O'][is_c]) ))
            p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't') 

    for is_c in ('NNtbt','NOtbt'):
        name = is_c +'-top'
        p_trans['N2O'][name] = []
        for d in ('ur','r','dr','dl','l','ul'):
            p_trans['N2O'][name].append( KMCProcess(
                                             coordinates     = [Origin, N2[d]],
                                             elements_before = [is_c+'-N', is_c+'-O'],
                                             elements_after  = ['top', 'o'],
                                             basis_sites     = [Bp_map['t']],
                                             rate_constant   = pre_sur(Vib_trans['N2O'][name], Vib_ad['N2O'][is_c]) ))
            p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')

    for fs_c in ('NNtbt','NOtbt'):
        name = 'top-' + fs_c
        p_trans['N2O'][name] = []
        for d in ('ur','r','dr','dl','l','ul'):
            b1,b2 = ('u'+d,'d'+d) if d in ('r','l') else (d,d[0])
            b3,b4 = (d+'u',d+'d') if d in ('r','l') else (d+d[0],d+d[1])
            p_trans['N2O'][name].append( KMCProcess(
                                             coordinates     = [Origin, N2[d], N3[b1], N3[b2], N4[b3], N4[b4]],
                                             elements_before = ['top', 'o','o','o','o','o'],
                                             elements_after  = [is_c+'-N', is_c+'-O','o','o','o','o'],
                                             basis_sites     = [Bp_map['t']],
                                             rate_constant   = pre_sur(Vib_trans['N2O'][fs_c+'-top'], Vib_ad['N2O']['top']) ))
            p_trans['N2O'][name][-1].name = ('trans', 'N2O', name, 't')
