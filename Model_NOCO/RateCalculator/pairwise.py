from KMCLib import *
from ..constant import *
from ..rate import rate_LH
from ..parameter_E import *
from ..routine import processes
from .get_interE import E_inter
from .pairtype import Inter_d, Inter_m, Inter_i
from .dynamic_rate import DA_dif_rate, DA_ads_rate
from .dynamic_count import DA_dif_count, DA_ads_count
import __main__

if __main__.rate_calculator and __main__.dynamic_dif == 'rate':
    dif_ratio = DA_dif_rate(__main__.dif_period, __main__.dif_magnitude, __main__.dif_exclude, __main__.scale_output['dif'])
elif __main__.rate_calculator and __main__.dynamic_dif == 'count':
    dif_ratio = DA_dif_count(__main__.dif_step, __main__.dif_factor, __main__.dif_exclude, __main__.scale_output['dif'])
else:
    dif_ratio = { x:1.0 for x in ('N','O','NO','CO') }

if __main__.rate_calculator and __main__.dynamic_ads == 'rate':
    ads_ratio = DA_ads_rate(__main__.ads_length, __main__.ads_fluc, __main__.ads_period, __main__.ads_magnitude, __main__.scale_output['ads'])
elif __main__.rate_calculator and __main__.dynamic_ads == 'count':
    ads_ratio = DA_ads_count(__main__.ads_length, __main__.ads_fluc, __main__.ads_step, __main__.ads_factor, __main__.scale_output['ads'])
else:
    ads_ratio = { x:1.0 for x in ('NO','CO','O2') }


class Pairwise(KMCRateCalculatorPlugin):


    def initialize(self):
        self.processes = [ x.name for x in processes ]

        if __main__.static_dif:
            self.dif_ratio = __main__.dif_ratio_s
        else:
            self.dif_ratio = { x:1.0 for x in ('N','O','NO','CO') }

        if Surface == '111':
            #       (sites for high modification),(sites for low modification)
            self.modify_fh = { 1: ((17,20,21,23),( 8,10,12,13,14,18)), 
                               2: ((17,20,22,24),( 7, 9,11,15,16,19)),
                               3: (( 7,10,11,22),(12,20,24,25,39,43)),
                               4: (( 8, 9,12,21),(11,20,23,26,40,45)),
                               5: (( 7, 9,12,24),(10,17,22,27,41,48)),
                               6: (( 8,10,11,23),( 9,17,21,28,42,50))}
            self.fh_map = { 7:1, 8:2, 21:3, 22:4, 23:5, 24:6 }


    @staticmethod
    def find_occupy(types_before, types_after):
        change = [ i for i in range(25) if types_before[i] != types_after[i] ]
        occupy_before = [ x for x in change if types_before[x] != 'o' ]
        occupy_after = [ x for x in change if types_after[x] != 'o' ]
        return (occupy_before, occupy_after)


    @staticmethod
    def calc_interE(types, occupy, o_point):
        inter_energy = 0
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


    def get_Efh(self, direct, mol, types):
        sites = self.modify_fh[direct]
        high = len([ x for x in sites[0] if types[x] != 'o' ])
        low  = len([ x for x in sites[1] if types[x] != 'o' ])
        E_fh = high*E_modify[mol]['h'] + low*E_modify[mol]['l']
        return E_fh


    def rate(self, coords, types_before, types_after, rate_constant,
             process_number, global_coordinate):

        category,mol,react,o_point = self.processes[process_number]

        if category in ('ads','des'):
            if mol in ('NO','CO'):
                if category == 'des':
                    E_bar = -( E_bind[mol][react] + self.calc_interE(types_before, [0], o_point) )
                else:
                    E_bar = E_bind[mol][react] + self.calc_interE(types_after, [0], o_point)
            elif mol == 'O2':
                if category == 'des':
                    E_bar = E_act['des'][mol][react][0] - self.calc_interE(types_before, self.find_occupy(types_before, types_after)[0], o_point)
                else:
                    E_bar = -( E_act['des'][mol][react][0] - self.calc_interE(types_after, self.find_occupy(types_before, types_after)[1], o_point) )
            E_bar = max(0, E_bar)
            return rate_LH(E_bar,rate_constant) * ads_ratio[mol]

        occupy_before,occupy_after = self.find_occupy(types_before, types_after)
        E_act_mod = 0
        E_rxn_mod = 0

        # change IS or FS configuration and calculate modification energy
        if Surface == '100':
            if category == 'dis' and mol == 'NO' and react == 'brg':
                E_act_mod = -self.calc_interE(types_before, occupy_before, o_point)   # modification for NO adsorption energy
                E_rxn_mod = E_act_mod
                occupy_before.pop(0)
            elif category == 'form':
                if (mol == 'NO' and react == 'N-O_bb') or (mol == 'N2' and react == 'N-NO_bb'):
                    E_rxn_mod = self.calc_interE(types_after, occupy_after, o_point)
                    occupy_after.pop(0)
                elif mol == 'N2' and react == 'N-N_hb':
                    for i,j in (((13,14),1), ((15,17),2), ((16,18),3), ((19,20),4)):
                        if occupy_before[1] in i:
                            occupy_after.extend([j,occupy_before[1]])
                            break
                    types_after = list(types_after)
                    for i in occupy_after:
                        types_after[i] = 'N'
        elif Surface == '111':
            if category == 'form':
                if mol == 'N2' and react in ('N-N_ff', 'N-N_hh'):
                    occupy_after.append(0)
                    types_after = list(types_after)
                    types_after[0] = 'N'
                elif mol == 'N2' and react in ('N-NO_ft', 'N-NO_ht'):
                    E_rxn_mod = self.calc_interE(types_after, occupy_after, o_point)
                    occupy_after.pop(0)
            # modification for f-h energy
            if category == 'dif' and react in ('f-h','h-f'):
                E_act_mod = self.get_Efh(occupy_after[0], mol, types_before)
            elif category == 'form' and react in ('N-NO_ft', 'N-NO_ht', 'O-CO_ft', 'O-CO_ht'):
                E_act_mod = self.get_Efh(self.fh_map[occupy_before[-1]], react[0], types_before)
            elif category in ('form','dis') and mol == 'NO':
                types, occupy = (types_before, occupy_before) if category == 'form' else (types_after, occupy_after)
                site_N,site_O = occupy if types[occupy[0]] == 'N' else (occupy[1],occupy[0])
                E_act_mod = self.get_Efh(site_N, 'N', types_before)
                E_act_mod += self.get_Efh(site_O, 'O', types_before)
            elif category == 'form' and mol == 'N2' and react in ('N-N_ff','N-N_hh'):
                E_act_mod1 = self.get_Efh(occupy_before[0], 'N', types_before)
                E_act_mod2 = self.get_Efh(occupy_before[1], 'N', types_before)
 
        # calculate activation energy and reaction energy
        interE_before = self.calc_interE(types_before, occupy_before, o_point)
        interE_after = self.calc_interE(types_after, occupy_after, o_point)
        E_change = interE_after - interE_before
        E_bar0, slope, E_rxn0 = E_act[category][mol][react]
        if category == 'form' and mol == 'N2' and react in ('N-N_hb', 'N-N_ff', 'N-N_hh'):
            E_rxn_mod = -interE_after
        E_rxn = E_rxn0 + E_change + E_rxn_mod
        E_bar = E_bar0 + slope*E_change + E_act_mod
        if category == 'form' and mol == 'N2' and react in ('N-N_ff','N-N_hh'):
            E_bar1 = max(0, E_rxn, E_bar + E_act_mod1)
            E_bar2 = max(0, E_rxn, E_bar + E_act_mod2)
            return rate_LH(E_bar1,rate_constant) + rate_LH(E_bar2,rate_constant)
        E_bar = max(0, E_rxn, E_bar)
        rate = rate_LH(E_bar,rate_constant)
        if category == 'dif':
            rate *= (self.dif_ratio[mol] * dif_ratio[mol])
        return rate


    def cutoff(self):
        if Surface == '100':
            return 3.95
        elif Surface == '111':
            return 4.5


    def cacheRates(self):
        return True


    def excludeFromCaching(self):
        """
        Method for exluding processes from the rate caching.
        Overload for custom behavior. The method only takes effect if caching
        is enabled with the cacheRates function.

        :returns: A tuple of process numbers to exclue from caching.
        :rtype: tuple
        """
        if __main__.dynamic_ads:
            exclude = tuple( index for index,name in enumerate(self.processes) if ( name[0] == 'dif' or (name[0] in ('ads','des') and name[1] in ('NO','CO')) ))
        else:
            exclude = tuple( index for index,name in enumerate(self.processes) if name[0] == 'dif' )
        return exclude
