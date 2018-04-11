import os
from KMCLib import *
from __main__ import suffix

class ProcessCount(KMCAnalysisPlugin):
    '''
    Class for counting happened processes.
    '''

    def __init__(self, interval, process_list):
        '''
        :param interval: interval for doing the analysis
        :type  interval: int
        :param process_list: list of types of processes to count
        :type  process_list: list of list, e.g.[('ads','NO'),('des','NO'),...]
        '''
        self.interval = interval
        self.process_list = process_list

    def setup(self, step, time, configuration, interaction):
        if MPICommons.isMaster():
            # map the process_list to process number
            self.process_map = { tuple(k):{} for k in self.process_list }
            self.process_numbers = []
            for number,process in enumerate(interaction._KMCInteractions__processes):
                category,mol,react,point = process.name
                for k in self.process_list:
                    if k[0] == category and k[1] == mol:
                        if self.process_map[k].has_key(react):
                            self.process_map[k][react].append(number)
                        else:
                            self.process_map[k][react] = [number]
                        self.process_numbers.append(number)

            directory = 'process_count' + suffix
            os.system('mkdir ' + directory)
            self.process_count = [0] * interaction.processesNumber()
            title_pre = '{:>14}{:>18}'.format('step','time')
            self.output = {}
            for i in self.process_list:
                title = ''
                for k in sorted(self.process_map[i].keys()):
                    title += '{:>14}'.format(k)
                self.output[i] = open(directory + '/' + '_'.join((i[0],i[1])), 'w', 1)
                self.output[i].write(title_pre + title + '\n')
            self.eachLine(step,time)
        MPICommons.barrier()

    def registerStep(self, step, time, configuration, interaction):
        if MPICommons.isMaster():
            number = configuration.latestEventProcess()
            if number in self.process_numbers:
                self.process_count[number] += 1
            if step % self.interval == 0 or self.breaker:
                self.eachLine(step, time)
        MPICommons.barrier()

    def eachLine(self,step,time):
        line_pre = '{:>14}{:>18.10e}'.format(step,time)
        for i in self.process_list:
            line = ''
            for k in sorted(self.process_map[i].keys()):
                number = sum( self.process_count[x] for x in self.process_map[i][k] )
                line += '{:>14}'.format(number)
            self.output[i].write(line_pre + line + '\n')

    def finalize(self):
        if MPICommons.isMaster():
            for i in self.output.values():
                i.close()
        MPICommons.barrier()
