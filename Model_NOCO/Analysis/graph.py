from KMCLib import *
import numpy as np
import os
try:
    import matplotlib.pyplot as plt
    support = True
except:
    support = False
from ..constant import Surface
from __main__ import suffix

if support:
    class Graph(KMCAnalysisPlugin):
        '''
        Class for printing image.
        '''

        def __init__(self, interval, section = None):
            '''
            :param interval: interval for doing the analysis
            :type  interval: int
            :param section: step section to do the analysis
            :type  section: list of list of two int, e.g. [[1000,2000],[5000,6000]]
            '''
            self.interval = interval
            self.section = section if section else [[0,-1]]
            self.color_def = {'o':'y', 'N':'b', 'NO':'m', 'O':'r', 'CO':'g'}   # 'y','r','g','b','c','m','k'
            self.alpha_def = {'o':0.3, 'N':  1, 'NO':  1, 'O':  1, 'CO':  1}

        def draw(self, step, sites, types):
            if Surface == '100':
                fig = plt.figure(figsize=(self.x_rep, self.y_rep))
                ax = fig.add_subplot(1,1,1)
                ax.set_xlim([0,self.x_rep])
                ax.set_ylim([0,self.y_rep])
                for s_site,s_type in zip(sites, types):
                    st_tmp = (s_site[0]+1e-3) % 1 + (s_site[1]+1e-3) % 1
                    if st_tmp < 0.1:
                        symbol = plt.Circle((s_site[0]+0.25,s_site[1]+0.25), 0.2, color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    elif 0.4 < st_tmp < 0.6:
                        symbol = plt.Polygon([[s_site[0]+0.08,s_site[1]+0.15],[s_site[0]+0.42,s_site[1]+0.15],[s_site[0]+0.25,s_site[1]+0.45]],color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    elif st_tmp > 0.9:
                        symbol = plt.Rectangle((s_site[0]+0.05,s_site[1]+0.05),0.4,0.4,color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    else:
                        raise Exception('Unsupported site.')
                    ax.add_patch(symbol)
            elif Surface == '111':
                fig = plt.figure(figsize=(self.x_rep+self.y_rep*0.5, self.y_rep*(3**0.5/2)))
                ax = fig.add_subplot(1,1,1)
                ax.set_xlim([-self.y_rep*0.5, self.x_rep])
                ax.set_ylim([0,self.y_rep*(3**0.5/2)])
                for s_site,s_type in zip(sites, types):
                    s_cor = np.dot(s_site[:2], np.array([[1.0, 0.0], [-0.5, 3**0.5/2]]))
                    if (s_site[0]+1e-3) % 1 < 0.1:
                        symbol = plt.Circle((s_cor[0]+0.25,s_cor[1]+0.22), 0.2, color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    elif 0.3 < s_site[0] % 1 < 0.4:
                        symbol = plt.Polygon([[s_cor[0]+0.08,s_cor[1]+0.12],[s_cor[0]+0.42,s_cor[1]+0.12],[s_cor[0]+0.25,s_cor[1]+0.42]],color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    elif 0.6 < s_site[0] % 1 < 0.7:
                        symbol = plt.Polygon([[s_cor[0]+0.08,s_cor[1]+0.32],[s_cor[0]+0.42,s_cor[1]+0.32],[s_cor[0]+0.25,s_cor[1]+0.02]],color=self.color_def[s_type], alpha=self.alpha_def[s_type])
                    else:
                        raise Exception('Unsupported site.')            
                    ax.add_patch(symbol)
            filename = 'step%s.png'%step
            fig.savefig('graph' + suffix + '/' +filename,bbox_inches='tight')
		
        def setup(self, step, time, configuration, interactions):
            if MPICommons.isMaster():
                directory = 'graph' + suffix
                os.system('mkdir ' + directory)
                self.x_rep = configuration.cellRepetitions()[0]
                self.y_rep = configuration.cellRepetitions()[1]
                for i in self.section:
                    if i[0] <= step <= (i[1] if i[1] != -1 else step):
                        self.draw(step=step, sites = configuration.sites(), types = configuration.types())
                        break
            MPICommons.barrier()
	
        def registerStep(self, step, time, configuration, interactions):
            if MPICommons.isMaster():
                if step % self.interval == 0 or self.breaker:
                    for i in self.section:
                        if i[0] <= step <= (i[1] if i[1] != -1 else step):
                            self.draw(step=step, sites = configuration.sites(), types = configuration.types())
                            break
            MPICommons.barrier()

else:
    class Graph(KMCAnalysisPlugin):
        def __init__(self, interval, section = None):
            pass
