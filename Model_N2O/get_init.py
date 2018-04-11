#!/usr/bin/env python
from random import choice,shuffle
import numpy as np
from .constant import *
from __main__ import suffix, num_O, num_CO, repetitions, visual
from KMCLib import *


# get initial sites and types
rep_x,rep_y = repetitions
multi = 4 if Surface == '100' else 3
unit_cell = KMCUnitCell(
    cell_vectors = Cell_vectors,
    basis_points = Basis_points)
lattice = KMCLattice(
    unit_cell   = unit_cell,
    repetitions = (rep_x,rep_y,1),
    periodic    = (True, True, False))
sites = lattice.sites()
types = ['o']*len(sites)
remain = range(len(sites))

# define function to detect equal sites
def site_equal(site1, sites):
    for site2 in sites:
        diff = sum(abs(np.array(site1) - np.array(site2)))
        if diff < 1e-3:
            return True
    return False

# define function to remove sites
if Surface == '100':
    block_offset = np.array(N1.values() + N2.values())
elif Surface == '111':
    block_offset = np.array(N1.values())
def remain_remove(site_num):
    remain.remove(site_num)
    site = sites[site_num]
    block = site + block_offset
    for site in block:
        for i,rep in [(0,rep_x),(1,rep_y)]:
            if site[i]+1e-3 > rep:
                 site[i] -= rep
            elif site[i]+1e-3 < 0:
                site[i] += rep
    for i in remain[:]:
        if site_equal(sites[i], block):
            remain.remove(i)
        
# set N and NO
o_offset = (rep_x/2-1)*multi*rep_y + (rep_y/2-1)*multi
if Config == 'Nb-NOb':
    init = ((o_offset + 2, 'N'),(o_offset + 4*rep_y + 2,'NO'))
    blank = (o_offset, o_offset + 4*rep_y)
elif Config == 'Nh-NOt':
    init = ((o_offset,'NO'),(o_offset + 5, 'N'))
    blank = (o_offset + 3, o_offset + 2)
elif Config == 'Nf-NOt':
    init = ((o_offset,'NO'),(o_offset + 3*rep_y + 1, 'N'))
    blank = (o_offset + 3*rep_y + 3, o_offset - 3*rep_y + 2 )
for n,mol in init:
    types[n] = mol
    remain_remove(n)
for n in blank:
    remain.append(n)
    remain_remove(n)

# add surrounding molecules
add_mol = ['O']*num_O + ['CO']*num_CO
shuffle(add_mol)
for mol in add_mol:
    if remain:
        site_num = choice(remain)
        if mol == 'O' and site_num % multi == 0:
            for j in range(100):
                site_num = choice(remain)
                if site_num % multi != 0:
                    break
            else:
                print 'Fail to construnct certain structure, please try again.'
                exit()
        types[site_num] = mol
        remain_remove(site_num)
    else:
        print 'Fail to construnct certain structure, please try again.'
        exit()

# configuration visualization
if visual:
    from .graph import graph
    graph(Surface, repetitions, sites, types, 'Config_'+ Config + suffix)
