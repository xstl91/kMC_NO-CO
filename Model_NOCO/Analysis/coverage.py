import os
from KMCLib import *
from ..constant import Surface
from __main__ import suffix

class Coverage(KMCAnalysisPlugin):
    '''
    Class for counting coverage.
    '''

    def __init__(self, interval, types, partition=False, part_span=None):
        '''
        :param interval: interval for doing the analysis
        :type  interval: int
        :param types: types of species to do the analysis
        :type  types: list of string
        :param partition: whether to calculate coverage for partition
        :type  partition: bool
        :param part_span: cell number along x and y axes for each part
        :type  part_span: list of int, e.g. [5,5]
        '''
        self.interval = interval
        self.types = list(types) + ['all']
        self.partition = partition
        self.part_span = part_span


    def setup(self, step, time, configuration, interaction):
        if MPICommons.isMaster():
            directory = 'coverage' + suffix
            os.system('mkdir ' + directory)

            if Surface == '100':
                count_types = ('top', 'brg1', 'brg2', 'hol', 'total')
            elif Surface == '111':
                count_types = ('top', 'fcc', 'hcp', 'total')
            self.multi = len(count_types) - 1

            self.sites = configuration.sites()
            self.sites_num = {'whole': len(self.sites)/self.multi}
            if self.partition:
                self.partition = []
                for cor in self.sites:
                    x = int((cor[0]+1e-3)/self.part_span[0])
                    y = int((cor[1]+1e-3)/self.part_span[1])
                    self.partition.append(str(x)+'_'+str(y))
                for part in set(self.partition):
                    self.sites_num[part] = self.partition.count(part)/self.multi

            self.output = {}
            title = '{:>14}{:>18}'.format('step','time')
            for j in count_types:
                title += '{:>8}'.format(j)
            for i in self.types:
                for part in self.sites_num:
                    self.output[(part,i)] = open(directory + '/' + '_'.join((part,i)), 'w', 1)
                    self.output[(part,i)].write(title + '\n')

            self.eachLine(step, time, configuration.types())
        MPICommons.barrier()


    def registerStep(self, step, time, configuration, interaction):
        if MPICommons.isMaster():
            if step % self.interval == 0 or self.breaker:
                self.eachLine(step, time, configuration.types())
        MPICommons.barrier()


    def eachLine(self, step, time, type_list):
        line_pre = '{:>14}{:>18.10e}'.format(step, time)
        count_list = { part:{ mol:[0]*self.multi for mol in self.types } for part in self.sites_num }
        for index,mol in enumerate(type_list):
            site_type = index % self.multi
            if mol != 'o':
                count_list['whole']['all'][site_type] += 1
                if self.partition:
                    count_list[self.partition[index]]['all'][site_type] += 1
            if mol in self.types:
                count_list['whole'][mol][site_type] += 1
                if self.partition:
                    count_list[self.partition[index]][mol][site_type] += 1
        for part in self.sites_num:
            for mol in self.types:
                count_list[part][mol].append(sum(count_list[part][mol]))
                line = ''.join(( '{:>8.4f}'.format(float(x)/self.sites_num[part]) for x in count_list[part][mol] ))
                self.output[(part,mol)].write(line_pre + line + '\n')


    def finalize(self):
        if MPICommons.isMaster():
            for i in self.output.values():
                i.close()
        MPICommons.barrier()
