from KMCLib import *
from .constant import *
from .rate import *

# rate_constant set here refers to prefactor

p_dif = { x:{} for x in ('N', 'O', 'NO', 'CO') }

if Surface == '100':
    ends = { x : ([N1['r'], N3['r'], N4['urr'], N4['drr']],
                  [N1['l'], N3['l'], N4['ull'], N4['dll']]) for x in ('t-b1','b1-t','b2-h','h-b2') }
    ends.update( { x : ([N1['u'], N3['u'], N4['uru'], N4['ulu']],
                        [N1['d'], N3['d'], N4['drd'], N4['dld']]) for x in ('t-b2','b2-t','b1-h','h-b1') } )
    types = { x : ('t-b1','b1-t','b2-h','h-b2','t-b2','b2-t','b1-h','h-b1') for x in ('NO','CO') }
    types.update( { x : ('b2-h','h-b2','b1-h','h-b1') for x in ('N','O') } )
elif Surface == '111':
    ends = { x : ([N1['u'], N2['ur'], N2['ul'], N3['u']],
                  [N1['dr'], N2['r'], N2['dr'], N3['dr']],
                  [N1['dl'], N2['l'], N2['dl'], N3['dl']]) for x in ('t-f','f-h','h-t') }
    ends.update( { x : ([N1['ur'], N2['r'], N2['ur'], N3['ur']],
                        [N1['d'], N2['dr'], N2['dl'], N3['d']],
                        [N1['ul'], N2['l'], N2['ul'], N3['ul']]) for x in ('t-h','h-f','f-t') } )
    types = { x : ('t-f','f-h','h-t','t-h','h-f','f-t') for x in ('NO','CO') }
    types.update( { x : ('f-h','h-f') for x in ('N','O') } )

for mol in ('N','O','NO','CO'):
    for t in types[mol]:
        p_dif[mol][t] = []
        point = t[0] if t[0] != 'b' else t[:2]
        title = '-'.join([ x for x in t if x.isalpha() ])
        TS = ''.join( sorted( x for x in t if x.isalpha() ))
        for end in ends[t]:
            p_dif[mol][t].append( KMCProcess(
                                      coordinates     = [Origin] + end,
                                      elements_before = [mol, 'o', 'o', 'o', 'o'],
                                      elements_after  = ['o', mol, 'o', 'o', 'o'],
                                      basis_sites     = [Bp_map[point]],
                                      rate_constant   = pre_sur(Vib_dif[mol][TS], Vib_ad[mol][t[0]])))
            p_dif[mol][t][-1].name = ('dif', mol, title, point)
