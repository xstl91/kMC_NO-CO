import os
from KMCLib import *
from ..constant import K,EV
from __main__ import suffix,T
from numpy import log

kT = K*T

class ProcessRate(KMCAnalysisPlugin):
    '''
    Class to keep track of the rate constants of certain processes when happened.
    '''

    def __init__(self, process_list):
        '''
        :param process_list: list of types of processes to count
        :type  process_list: list of list, e.g.[('ads','NO'),('des','NO'),...]
        '''
        self.process_list = process_list

    def setup(self, step, time, configuration, interaction):
        if MPICommons.isMaster():

            self.processes = interaction._KMCInteractions__processes
            self.process_sites = { tuple(k):[] for k in self.process_list }
            self.process_numbers = []
            for number,process in enumerate(self.processes):
                category,mol,react,point = process.name
                for k in self.process_list:
                    if k[0] == category and k[1] == mol:
                        if react not in self.process_sites[k]:
                            self.process_sites[k].append(react)
                        self.process_numbers.append(number)

            directory = 'process_rate' + suffix
            os.system('mkdir ' + directory)
            title = '{:>14}{:>18}{:>18}{:>12}\n'.format('step','time','rate_constant','E_bar / eV')
            self.output = {}
            for i in self.process_list:
                self.output[i] = {}
                for k in self.process_sites[i]:
                    self.output[i][k] = open(directory + '/' + '_'.join((i[0],i[1],k)), 'w', 1)
                    self.output[i][k].write(title)

        MPICommons.barrier()

    def registerStep(self, step, time, configuration, interaction):
        if MPICommons.isMaster():
            number = configuration.latestEventProcess()
            if number in self.process_numbers:
                rate_constant = configuration.latestEventRate()
                prefactor = self.processes[number].rateConstant()
                E_bar = -log( rate_constant / prefactor ) * kT / EV
                line = '{:>14}{:>18.10e}{:>18.10e}{:>12.3f}\n'.format(step,time,rate_constant,E_bar)
                category,mol,react,point = self.processes[number].name
                self.output[(category,mol)][react].write(line)
        MPICommons.barrier()

    def finalize(self):
        if MPICommons.isMaster():
            for i in self.output.values():
                for j in i.values():
                    j.close()
        MPICommons.barrier()
