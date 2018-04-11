from .dynamic import DynamicAccelerate_dif, DynamicAccelerate_ads

class DA_dif_rate(DynamicAccelerate_dif):

    def __init__(self, dif_period, dif_magnitude, exclude, output):
        DynamicAccelerate_dif.__init__(self, exclude, output)
        self.period = dif_period
        self.magnitude = dif_magnitude
        self.accum = { x:0 for x in ('N','O','NO','CO','rare') }

    def registerStep(self, step, time, configuration, interaction):
        latest_process = configuration.latestEventProcess()
        if latest_process in self.process_map or latest_process in self.process_freeze:
            rates_all = sum( sum(x) for x in interaction.eachRateTable() )
            for process,rates in enumerate(interaction.eachRateTable()):
                if process in self.process_map:
                    mol = self.process_map[process]
                    self.accum[mol] += sum(rates) / rates_all
                else:
                    self.accum['rare'] += sum(rates) / rates_all
            if step - self.step == self.period:
                for mol in self.ratio:
                    self.ratio[mol] = min(1.0, self.ratio[mol]*self.magnitude*self.accum['rare']/self.accum[mol]) if self.accum[mol] else 1.0
                for mol in self.accum:
                    self.accum[mol] = 0
                self.step = step
        else:
            if self.output and sum(self[x] for x in self.ratio) < 4 - 1e-8:
                self.eachline(step, time)
            for mol in self.ratio:
                self.ratio[mol] = 1.0
            for mol in self.accum:
                self.accum[mol] = 0
            self.step = step


class DA_ads_rate(DynamicAccelerate_ads):

    def __init__(self, ads_length, ads_fluc, ads_period, ads_magnitude, output):
        DynamicAccelerate_ads.__init__(self, ads_length, ads_fluc, output)
        self.period = ads_period
        self.magnitude = ads_magnitude
        self.rates = { x:[0]*self.period for x in ('NO','CO','rare') }
        self.next_pos = 0

    def registerStep(self, step, time, configuration, interaction):
        latest_process = configuration.latestEventProcess()
        if latest_process in self.process_rare:
            if self.output and sum(self.ratio.values()) < 2 - 1e-8:
                self.eachline(step, time)
            for mol in self.ratio:
                self.eq_count[mol] = []
                self.flag[mol] = False
                self.ratio[mol] = 1.0
            for mol in self.rates:
                self.rates[mol] = [0]*self.period
            self.next_pos = 0
        else:
            rates_all = sum( sum(x) for x in interaction.eachRateTable() )
            accum = { x:0 for x in ('NO','CO','rare') }
            for process,rates in enumerate(interaction.eachRateTable()):
                if process in self.process_map:
                    mol = self.process_map[process][0]
                    accum[mol] += sum(rates) / rates_all
                elif process in self.process_rare:
                    accum['rare'] += sum(rates) / rates_all
            for mol in accum:
                self.rates[mol][self.next_pos] = accum[mol]
            self.next_pos += 1
            if latest_process in self.process_map:
                mol, category = self.process_map[latest_process]
                if not self.flag[mol]:
                    self.eq_count[mol].append(self.type_map[category])
                    if len(self.eq_count[mol]) == self.length:
                        if abs(sum(self.eq_count[mol])) <= self.threshold:
                            self.flag[mol] = True
                        else:
                            self.eq_count[mol].pop(0)
            if self.next_pos == self.period:
                self.next_pos = 0
                if self.flag['NO'] and self.flag['CO']:
                    for mol in self.ratio:
                        self.ratio[mol] = min(1.0, self.ratio[mol]*self.magnitude*sum(self.rates['rare'])/sum(self.rates[mol])) if sum(self.rates[mol]) else 1.0
                elif self.flag['NO'] or self.flag['CO']:
                    mol = 'NO' if self.flag['NO'] else 'CO'
                    self.ratio[mol] = min(1.0, self.ratio[mol]*self.magnitude*sum(self.rates[self.another[mol]] + self.rates['rare'])/sum(self.rates[mol])) if sum(self.rates[mol]) else 1.0
