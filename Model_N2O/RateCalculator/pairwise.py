from KMCLib import *
from ..constant import *
from ..rate import rate_LH
from ..parameter_E import *
from ..routine import processes
from .get_interE import E_inter
from .pairtype import Inter_d, Inter_m, Inter_i


class Pairwise(KMCRateCalculatorPlugin):


    def initialize(self):
        self.processes = [ x.name for x in processes ]
        self.replace = { 'o':'o', 'N':'N', 'O':'O', 'NO':'NO', 'CO':'CO', 'top':'NO' }
        if Surface == '100':
            self.replace.update({ 'flat-N':'NO', 'flat-mN':'o', 'flat-mO':'o', 'falt-O':'NO',
                                  'NNbhb-N':'NO', 'NNbhb-m':'NO', 'NNbhb-O':'o',
                                  'NNtbt-N':'NO', 'NNtbt-m':'NO', 'NNtbt-O':'o',
                                  'NOtbt-N':'NO', 'NOtbt-m':'NO', 'NOtbt-O':'o',
                                  'NOtht-N':'NO', 'NOtht-m':'o', 'NOtht-O':'NO'})
        elif Surface == '111':
            self.replace.update({ 'NNbftt-N':'o', 'NNbftt-m':'NO', 'NNbftt-O':'o',
                                  'NNbhtt-N':'o', 'NNbhtt-m':'NO', 'NNbhtt-O':'o',
                                  'NNtbt-N':'NO', 'NNtbt-O':'o',
                                  'NOtbt-N':'NO', 'NOtbt-O':'o',
                                  'NObft-N':'NO', 'NObft-m':'o', 'NObft-O':'o',
                                  'NObht-N':'NO', 'NObht-m':'o', 'NObht-O':'o'})
        self.modify = { 23: (( 7, 9,12,24),(10,17,22)),
                         8: ((17,20,22,24),( 7, 9,11)),
                        21: (( 7,10,11,22),(12,20,24)),
                        24: (( 8,10,11,23),( 9,17,21)),
                        22: (( 8, 9,12,21),(11,20,23)),
                         7: ((17,20,21,23),( 8,10,12))}
        self.output = True


    @staticmethod
    def find_change(types_before, types_after):
        return [ i for i in range(25) if types_before[i] != types_after[i] ]


    @staticmethod
    def calc_interE(types, change, o_point):
        inter_energy = 0
        occupy = [ x for x in change if types[x] != 'o' ]
        if occupy:
            sur = [ x for x,y in enumerate(types) if y != 'o' and x not in occupy ]
            sur_n = len(sur)
            pairs = [ (sur[i],sur[j]) for i in range(sur_n) for j in range(i+1,sur_n) ]
            if len(occupy) == 2:
                mol1,mol2 = occupy
                if mol2 in Inter_m[o_point][mol1]:
                    for i in sur:
                        if i in Inter_m[o_point][mol1][mol2]:
                            inter_energy += E_inter[ types[mol1] + '-' + types[mol2] ][ Inter_m[o_point][mol1][mol2][i] ]
            for mol in occupy:
                for i in sur:
                    if i in Inter_d[o_point][mol]:
                        inter_energy += E_inter[ types[mol] + '-' + types[i] ][ Inter_d[o_point][mol][i] ]
                        for j in sur + occupy:
                            if i in Inter_m[o_point][mol] and j in Inter_m[o_point][mol][i]:
                                inter_energy += E_inter[ types[mol] + '-' + types[i] ][ Inter_m[o_point][mol][i][j] ]
                for pair in pairs:
                    if pair in Inter_i[o_point][mol]:
                        inter_energy += E_inter[ types[pair[0]] + '-' + types[pair[1]] ][ Inter_i[o_point][mol][pair] ]
        return inter_energy


    def rate(self, coords, types_before, types_after, rate_constant,
             process_number, global_coordinate):
        category,mol,react,o_type = self.processes[process_number]

        change = self.find_change(types_before, types_after)

        replace = self.replace.copy()
        if category in ('form','back'):
            if Surface == '100':
                replace.update({'NNbhb-N':'o', 'NNbhb-m':'o'})
            elif Surface == '111':
                replace.update({'NNbftt-m':'o', 'NNbhtt-m':'o'})
        elif react in ('flat-NOtht','NOtht-flat'):
            replace.update({'NOtht-N':'o', 'NOtht-m':'NO', 'NOtht-O':'o'})
        elif Surface == '111' and react in ('NNtbt-top', 'top-NNtbt', 'top-NOtbt', 'NOtbt-top'):
            replace.update({'NNtbt-O':'NO', 'NOtbt-O':'NO'})

        types_before = [ replace[x] for x in types_before ]
        types_after = [ replace[x] for x in types_after ]
        E_change = self.calc_interE(types_after, change, o_type)- self.calc_interE(types_before, change, o_type)
        E_bar0, slope, E_rx0, slope_rx = E_act[category][mol][react]
        E_bar = E_bar0 + slope*E_change
        E_rx = E_rx0 + slope_rx*E_change
        if Surface == '111' and category in ('form','back'):
            h_sites, l_sites = self.modify[change[-1]]
            high = len([ x for x in h_sites if types_before[x] != 'o' ])
            low  = len([ x for x in l_sites if types_before[x] != 'o' ])
            E_mod = (high*0.128-low*0.047)*EV
            if category == 'form':
                E_bar += E_mod
                E_rx += E_mod
            elif category == 'back':
                E_rx -= E_mod
        E_bar = max(0, E_rx, E_bar)
        rate = rate_LH(E_bar,rate_constant)
        if self.output:
            self.E_diff = E_change/EV
            self.E_bar = E_bar/EV
            self.prefactor = rate_constant
            self.rate_constant = rate
            self.output = False
        return rate


    def cutoff(self):
        if Surface == '100':
            return 3.95
        elif Surface == '111':
            return 4.5


    def cacheRates(self):
        return True
