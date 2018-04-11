from ..constant import Surface
import numpy as np

route = '/'.join(__file__.split('/')[:-3])
route = route + '/Interaction/figure/'

# Some constats to distinguish two surfaces
if Surface == '100':
    Points = ('t','b1','b2','h')
    Record = range(1,25)
    Modify = range(9,25)
    Extend = range(9,101)
elif Surface == '111':
    Points = ('t','f','h')
    Record = range(1,13) + [17] + range(20,25)
    Modify = range(7,13) + [17] + range(20,25)
    Extend = range(7,81)


# Some functions to judge equality
def site_equal(site1, *sites):
    for site2 in sites:
        diff = sum(abs(np.array(site1) - np.array(site2)))
        if diff < 1e-3:
            return True
    return False

def sign_equal(num1, num2):
    if num1 > 1e-4 and num2 > 1e-4: return True
    elif num1 < -1e-4 and num2 < -1e-4: return True
    elif -1e-4 < num1 < 1e-4 and -1e-4 < num2 < 1e-4: return True
    else: return False

def sign_oppo(num1, num2):
    if num1 > 1e-4 and num2 < -1e-4: return True
    elif num1 < -1e-4 and num2 > 1e-4: return True
    else: return False


# Get coordinate from file for initial site
coord = {0:[]}
with open(route + 'cut_' + Surface) as f:
    for line in f:
        x,y,z = line[1:-2].split()
        coord[0].append((float(x),float(y)))
coord[0] = np.array(coord[0])


# Construct mapping for different center site
site_map = {}
for i in Record:
    coord[i] = coord[0] - coord[0][i]
    site_map[i] = {}
    for j,site in enumerate(coord[i]):
        for k,site_0 in enumerate(coord[0]):
            if site_equal(site, site_0):
                site_map[i][k] = j
                break


# Function to judge site type
def site_type(type_0, num_0):
    origin = coord[0][num_0]
    if Surface == '100':
        if type_0 == 't': o_off = origin
        elif type_0 == 'b1': o_off = origin + np.array([0.5,0])
        elif type_0 == 'b2': o_off = origin + np.array([0,0.5])
        elif type_0 == 'h': o_off = origin + np.array([0.5,0.5])
        if (o_off[0]%1 < 0.1 or o_off[0]%1 > 0.9) and (o_off[1]%1 < 0.1 or o_off[1]%1 > 0.9): o_type = 't'
        elif 0.4 < o_off[0]%1 < 0.6 and (o_off[1]%1 < 0.1 or o_off[1]%1 > 0.9): o_type = 'b1'
        elif (o_off[0]%1 < 0.1 or o_off[0]%1 > 0.9) and 0.4 < o_off[1]%1 < 0.6: o_type = 'b2'
        elif 0.4 < o_off[0]%1 < 0.6 and 0.4 < o_off[1]%1 < 0.6: o_type = 'h'
    elif Surface == '111':
        if type_0 == 't': o_off = origin
        elif type_0 == 'f': o_off = origin + np.array([1./3,2./3])
        elif type_0 == 'h': o_off = origin + np.array([2./3,1./3])
        if o_off[0]%1 < 0.1 or o_off[0]%1 > 0.9: o_type = 't'
        elif 0.3 < o_off[0]%1 < 0.4: o_type = 'f'
        elif 0.6 < o_off[0]%1 < 0.7: o_type = 'h'
    return o_type


# Get pairwise interaction type from file for initial site
Inter_d = { x:{0:{}} for x in Points }        # double
with open(route + 'inter_' + Surface + '_0') as f:
    f.readline()
    for line in f:
        items = line.split()
        l = int(items[0])
        for i,j in enumerate(Points,1):
            Inter_d[j][0][l] = items[i]


# Construct pairwise interaction type for different center site
for i in Record:
    for t in Points:
        o_type = site_type(t,i)
        Inter_d[t][i] = {}
        for k,v in Inter_d[o_type][0].items():
            Inter_d[t][i][site_map[i][k]] = v


# Construct modification interaction type for initial site
Inter_m = { x:{0:{}} for x in Points }    # modification
Inter_i = { x:{0:{}} for x in Points }    # influenced
for t in Points:
    for i in Modify:
        Inter_m[t][0][i] = {}
        for j in Extend:
            type0 = Inter_d[t][0][i] if i in Inter_d[t][0] else None
            type1 = Inter_d[t][i][j] if j in Inter_d[t][i] else None
            type2 = Inter_d[t][0][j] if j in Inter_d[t][0] else None
            key_i = tuple(sorted([i,j]))
            if Surface == '100':
                offset0 = coord[0][i]
                offset1 = coord[i][j]
                offset2 = coord[0][j]
                if type0 in ('bb2h','bb2t','hh1','tt1'):
                    d = 0 if -1e-4 < offset0[1] < 1e-4 else 1
                    if type1 in ('bb2h','bb2t','hh1','tt1') and sign_equal(offset0[d], offset1[d]) :
                        Inter_m[t][0][i][j] = type0+'f'
                        Inter_i[t][0][key_i] = type1+'f'
                    elif type1 in ('bh2','bt2','hb2','tb2','hh2') and sign_equal(offset0[d], offset1[d]) :
                        Inter_i[t][0][key_i] = type1+'f' if i < j else type1[1] + type1[0] + type1[2] + 'f'
                    elif type2 in ('bb2h','bb2t','hh1','tt1') and sign_oppo(offset0[d], offset2[d]) :
                        Inter_m[t][0][i][j] = type0+'f'
                elif type0 in ('bh2','bt2','hb2','tb2'):
                    if ((type1 in ('bb2h','bb2t','hh1','tt1') and ( sign_equal(offset0[0], offset1[0]) or sign_equal(offset0[1], offset1[1]) )) or
                        (type2 in ('bb2h','bb2t','hh1','tt1') and ( sign_oppo(offset0[0], offset2[0]) or sign_oppo(offset0[1], offset2[1]) )) or
                        (type2 in ('bh2','bt2','hb2','tb2') and sign_oppo(offset0[0], offset2[0]) and sign_oppo(offset0[1], offset2[1]))):
                        Inter_m[t][0][i][j] = type0+'f'
                    elif type1 in ('bh2','bt2','hb2','tb2') and sign_equal(offset0[0], offset1[0]) and sign_equal(offset0[1], offset1[1]):
                        Inter_m[t][0][i][j] = type0+'f'
                        Inter_i[t][0][key_i] = type1+'f' if i < j else type1[1] + type1[0] + type1[2] + 'f'
                    elif type1 == 'hh2' and sign_equal(offset0[0], offset1[0]) and sign_equal(offset0[1], offset1[1]):
                        Inter_i[t][0][key_i] = type1+'f'
                elif type0 == 'hh2':
                    if ((type1 in ('bb2h','bb2t','hh1','tt1') and ( sign_equal(offset0[0], offset1[0]) or sign_equal(offset0[1], offset1[1]) )) or
                        (type1 in ('bh2','bt2','hb2','tb2') and sign_equal(offset0[0], offset1[0]) and sign_equal(offset0[1], offset1[1])) or
                        (type2 in ('bb2h','bb2t','hh1','tt1') and ( sign_oppo(offset0[0], offset2[0]) or sign_oppo(offset0[1], offset2[1]) )) or
                        (type2 in ('bh2','bt2','hb2','tb2', 'hh2') and sign_oppo(offset0[0], offset2[0]) and sign_oppo(offset0[1], offset2[1]))):
                        Inter_m[t][0][i][j] = type0+'f'
                    elif type1 == 'hh2' and sign_equal(offset0[0], offset1[0]) and sign_equal(offset0[1], offset1[1]):
                        Inter_m[t][0][i][j] = type0+'f'
                        Inter_i[t][0][key_i] = type1+'f'
            elif Surface == '111':
                if type0 == 'tt1':
                    if type1 == 'tt1' and type2 == 'tt3':
                        Inter_m[t][0][i][j] = type0+'r'
                        Inter_i[t][0][key_i] = type1+'r'
                    elif ((type1 == 'tt3' and type2 == 'tt1') or
                          (type1 in ('tf2','th2') and type2 in ('tf4','th4')) or
                          (type1 in ('tf4','th4') and type2 in ('tf2','th2'))):
                        Inter_m[t][0][i][j] = type0+'r'
                elif type0 in ('ff1','hh1'):
                    for k in range(1,7):
                        if Inter_d[t][0][k] in ('ft1','ht1') and Inter_d[t][i][k] in ('ft1','ht1'):
                            break
                    if type1 in ('ff1','hh1') and type2 in ('ff3','hh3'):
                        Inter_m[t][0][i][j] = type0+'r'
                        Inter_i[t][0][key_i] = type1+'r'
                    elif ((type1 in ('ff3','hh3') and type2 in ('ff1','hh1')) or
                          (type1 in ('ft2','ht2') and type2 in ('ft4','ht4')) or
                          (type1 in ('ft4','ht4') and type2 in ('ft2','ht2')) or
                          (type1 in ('ff1','hh1') and type2 in ('ff2h','hh2f')) or
                          (type1 in ('ff2h','hh2f') and type2 in ('ff1','hh1'))):
                        Inter_m[t][0][i][j] = type0+'r'
                    elif type1 in ('ff1','hh1') and type2 in ('ff1','hh1') and Inter_d[t][k][j] in ('tf1','th1'):
                        Inter_m[t][0][i][j] = type0+'p'
                        Inter_i[t][0][key_i] = type1+'p'
                    elif type1 in ('ff1','hh1') and type2 in ('ff2t','hh2t'):
                        Inter_i[t][0][key_i] = type1+'r'
                elif type0 in ('ft2','ht2'):
                    if type1 == 'tt1' and type2 in ('ft4','ht4'):
                        Inter_i[t][0][key_i] = type1+'r'
                elif type0 in ('tf2','th2'):
                    if type1 in ('ff1','hh1') and type2 in ('tf4','th4'):
                        Inter_i[t][0][key_i] = type1+'r'
    Inter_m[t][0] = { k:v for k,v in Inter_m[t][0].items() if v }


# Construct modification interaction type for different center site
for i in Record:
    for t in Points:
        o_type = site_type(t,i)
        Inter_m[t][i] = { site_map[i][j]:{ site_map[i][k]:v for k,v in Inter_m[o_type][0][j].items() } for j in Inter_m[o_type][0] }
        Inter_i[t][i] = {}
        for k,v in Inter_i[o_type][0].items():
            key = (site_map[i][k[0]], site_map[i][k[1]])
            if key[0] < key[1]:
                Inter_i[t][i][key] = v
            else:
                Inter_i[t][i][(key[1],key[0])] = v[1] + v[0] + v[2:]


# Delete unsupported pairwise interaction type
for t in Points:
    for i in Inter_d[t]:
        for k,v in Inter_d[t][i].items():
            if v in ('t','b1','b2','h','f','tb1','th1','bt1','bh1','bb1','ht1','hb1','tf1','ft1','fh1','hf1'):
                Inter_d[t][i].pop(k)
