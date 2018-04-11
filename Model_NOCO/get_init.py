#!/usr/bin/env python
from KMCLib import *
from random import choice,shuffle
import numpy as np
from .constant import *
from .routine import unit_cell,lattice
from __main__ import num_mol, suffix
import os

if MPICommons.isMaster():
    fail_error = Exception('Fail to construnct certain structure.')

    # get initial sites and types
    multi = len(Basis_points)
    sites = lattice.sites()
    repetitions = lattice.repetitions()
    def site_map(site):
        site=site.copy()
        for i in [0,1]:
            site[i] += 1e-3
            if site[i] > repetitions[i]:
                site[i] -= repetitions[i]
            elif site[i] < 0:
                site[i] += repetitions[i]
        return ( int(site[0]), int(site[1]), int(site[0]%1//0.4), int(site[1]%1//0.4) )
    sites_map = { site_map(site):num for num,site in enumerate(sites) }
    types = ['o']*len(sites)
    block_counts = np.zeros(len(sites),dtype=int)

    # offsets for block sites
    if Surface == '100':
        block_offset = np.array(N1.values() + N2.values())
    elif Surface == '111':
        block_offset = np.array(N1.values())

    # add molecule
    def add_mol(mol, site_num):
        types[site_num] = mol
        block_counts[site_num] = 9
        for site in sites[site_num] + block_offset:
            block_counts[sites_map[site_map(site)]] += 1

    # delete molecule
    def del_mol(site_num):
        types[site_num] = 'o'
        block_counts[site_num] = 0
        for site in sites[site_num] + block_offset:
            block_counts[sites_map[site_map(site)]] -= 1

    # choose site
    def choose_add(mol):
        avail = (block_counts == 0).nonzero()[0]
        if mol in ['N','O']:
            avail = np.extract(avail % multi != 0, avail)
        if not avail.size:
            return None
        return choice(avail)

    # move molecule
    def move_mol():
        avail = (block_counts == 1).nonzero()[0]
        if not avail.size:
            raise fail_error
        while avail.size:
            site_num_a = choice(avail)
            surround = [ sites_map[site_map(site)] for site in sites[site_num_a] + block_offset ]
            mol,site_num_b = [ (types[x],x) for x in surround if types[x] != 'o' ][0]
            if mol in ['N','O'] and site_num_a % multi == 0:
                avail = np.extract(avail != site_num_a, avail)
            else:
                break
        else:
            raise fail_error
        del_mol(site_num_b)
        add_mol(mol,site_num_a)

    # construct configuration
    try_loop = int(np.sqrt(len(sites)/multi))
    for mol in num_mol:
        for i in range(num_mol[mol]):
            for j in range(try_loop):
                site_num = choose_add(mol)
                if site_num:
                    add_mol(mol, site_num)
                    break
                else:
                    move_mol()
            else:
                raise fail_error

    # write a file
    with open('_tmp_types'+suffix,'w') as f:
        f.write('types = ')
        f.write(str(types))

MPICommons.barrier()

exec(open('_tmp_types'+suffix).read())

if MPICommons.isMaster():
    os.system('rm _tmp_types'+suffix)
MPICommons.barrier()
