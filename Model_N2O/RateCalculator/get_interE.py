from ..constant import Surface, EV

# load interaction energy, J
E_inter = {}
route = '/'.join(__file__.split('/')[:-3]) + '/Interaction/' + Surface + '/'
if Surface == '100':
    asymmetry = {'bb4h':'bb4t', 'bb4t':'bb4h'}
elif Surface == '111':
    asymmetry = {'ff2t':'ff2h', 'ff2h':'ff2t',
                 'hh2f':'hh2t', 'hh2t':'hh2f',
                 'tt2f':'tt2h', 'tt2h':'tt2f'}
for pair in ('N-N','O-O','NO-NO','CO-CO','N-O','N-NO','N-CO','O-NO','O-CO','NO-CO'):
    E_inter[pair] = {}
    with open(route + pair) as f:
        for line in f:
            k,v = line.split()
            E_inter[pair][k] = float(v)*EV
    if pair in ('N-N','O-O','NO-NO','CO-CO'):
        for k in E_inter[pair].keys():
            if k[0] != k[1]:
                E_inter[pair][k[1]+k[0]+k[2:]] = E_inter[pair][k]
            elif k in asymmetry:
                E_inter[pair][asymmetry[k]] = E_inter[pair][k]
    else:
        mols = pair.split('-')
        pair_ex = mols[1] + '-' + mols[0]
        E_inter[pair_ex] = {}
        for k in E_inter[pair].keys():
            if k in asymmetry:
                E_inter[pair_ex][asymmetry[k]] = E_inter[pair][k]
                continue
            E_inter[pair_ex][k[1]+k[0]+k[2:]] = E_inter[pair][k]
