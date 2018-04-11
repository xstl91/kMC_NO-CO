from .dynamic import DynamicAccelerate_dif, DynamicAccelerate_ads

class DA_dif_count(DynamicAccelerate_dif):

    def __init__(self, dif_step, dif_factor, exclude, output):
        DynamicAccelerate_dif.__init__(self, exclude, output)
        self.dif_step = dif_step
        self.dif_factor = dif_factor
        self.count = { x:0 for x in ('N','O','NO','CO') }

    def registerStep(self, step, time, configuration, interaction):
        latest_process = configuration.latestEventProcess()
        if latest_process in self.process_map:
            mol = self.process_map[latest_process]
            self.count[mol] += 1
            if self.count[mol] == self.dif_step:
                self.ratio[mol] *= self.dif_factor
                self.count[mol] = 0
        elif latest_process in self.process_freeze:
            for mol in self.ratio:
                 self.count[mol] = 0
                 self.ratio[mol] = min(1.0, self.ratio[mol] / self.dif_factor)
        else:
            if self.output and sum(self[x] for x in self.ratio) < 4 - 1e-8:
                self.eachline(step, time)
            for mol in self.ratio:
                self.count[mol] = 0
                self.ratio[mol] = 1.0


class DA_ads_count(DynamicAccelerate_ads):

    def __init__(self, ads_length, ads_fluc, ads_step, ads_factor, output):
        DynamicAccelerate_ads.__init__(self, ads_length, ads_fluc, output)
        self.ads_step = ads_step
        self.ads_factor = ads_factor
        self.multicount = { x:0 for x in ('NO','CO') }

    def registerStep(self, step, time, configuration, interaction):
        latest_process = configuration.latestEventProcess()
        if latest_process in self.process_rare:
            if self.output and sum(self.ratio.values()) < 2 - 1e-8:
                self.eachline(step, time)
            for mol in self.ratio:
                self.eq_count[mol] = []
                self.flag[mol] = False
                self.multicount[mol] = 0
                self.ratio[mol] = 1.0
        elif latest_process in self.process_map:
            mol, category = self.process_map[latest_process]
            if not self.flag[mol]:
                self.eq_count[mol].append(self.type_map[category])
                if len(self.eq_count[mol]) == self.length:
                    if abs(sum(self.eq_count[mol])) <= self.threshold:
                        self.flag[mol] = True
                        self.multicount[mol] = self.length - 1
                    else:
                        self.eq_count[mol].pop(0)
            if self.flag[mol]:
                self.multicount[mol] += 1
                if self.multicount[mol] >= self.ads_step:
                    self.ratio[mol] *= self.ads_factor
                    self.multicount[mol] = 0
            elif self.flag[self.another[mol]]:
                self.multicount[self.another[mol]] = 0
                self.ratio[self.another[mol]] = min(1.0, self.ratio[self.another[mol]] / self.ads_factor)
