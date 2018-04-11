import os
from KMCLib import *
from __main__ import suffix

class DynamicAccelerate_dif(KMCAnalysisPlugin):

    def __init__(self, exclude = None, output = False):
        self.output = output
        self.exclude = exclude if exclude else []
        self.ratio = { x:1.0 for x in ('N','O','NO','CO') }

    def setup(self, step, time, configuration, interaction):
        self.step = step
        self.time = time
        self.process_map = {}
        self.process_freeze = []
        for number,process in enumerate(interaction._KMCInteractions__processes):
            category,mol,react,point = process.name
            if category == 'dif':
                self.process_map[number] = mol
            elif category in ('ads','des') and mol in ('NO','CO'):
                self.process_freeze.append(number)
        if self.output:
            if MPICommons.isMaster():
                directory = 'scale' + suffix
                os.system('if ! [ -d ' + directory +' ];then mkdir ' + directory + ';fi')
                self.output = open(directory + '/diffusion', 'w', 1)
                self.output.write(('{:>14}{:>18}'+'{:>12}'*4+'\n').format('step','time','N','O','NO','CO'))
            MPICommons.barrier()

    def eachline(self, step, time):
        if MPICommons.isMaster():
            self.output.write(('{:>14}{:>18.10e}'+'{:>12.4e}'*4+'\n').format(step, time, self['N'], self['O'], self['NO'], self['CO']))
        MPICommons.barrier()

    def finalize(self):
        if MPICommons.isMaster():
            if self.output:
                self.output.close()
        MPICommons.barrier()

    def __getitem__(self, mol):
        if mol in self.exclude:
            return 1.0
        else:
            return self.ratio[mol]


class DynamicAccelerate_ads(KMCAnalysisPlugin):

    def __init__(self, ads_length, ads_fluc, output):
        self.length = ads_length
        self.threshold = ads_length * ads_fluc
        self.output = output
        self.ratio = { x:1.0 for x in ('NO','CO') }
        self.eq_count = { x:[] for x in ('NO','CO') } 
        self.flag = { x:False for x in ('NO','CO') }
        self.type_map = { 'ads':1, 'des':-1 }
        self.another = {'NO': 'CO', 'CO': 'NO'}

    def setup(self, step, time, configuration, interaction):
        self.step = step
        self.time = time
        self.process_map = {}
        self.process_rare = []
        for number,process in enumerate(interaction._KMCInteractions__processes):
            category,mol,react,point = process.name
            if category in ('ads','des') and mol in ('NO','CO'):
                self.process_map[number] = (mol, category)
            elif category != 'dif':
                self.process_rare.append(number)
        if self.output:
            if MPICommons.isMaster():
                directory = 'scale' + suffix
                os.system('if ! [ -d ' + directory +' ];then mkdir ' + directory + ';fi')
                self.output = open(directory + '/adsorption', 'w', 1)
                self.output.write(('{:>14}{:>18}'+'{:>12}'*2+'\n').format('step','time','NO','CO'))
            MPICommons.barrier()

    def eachline(self, step, time):
        if MPICommons.isMaster():
            self.output.write(('{:>14}{:>18.10e}'+'{:>12.4e}'*2+'\n').format(step, time, self['NO'], self['CO']))
        MPICommons.barrier()

    def finalize(self):
        if MPICommons.isMaster():
            if self.output:
                self.output.close()
        MPICommons.barrier()

    def __getitem__(self, mol):
        if mol == 'O2':
            return 1.0
        else:
            return self.ratio[mol]
