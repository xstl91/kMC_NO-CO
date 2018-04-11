import numpy as np
import matplotlib.pyplot as plt

for surface in ('100', '111'):
    if surface == '100':
        points = (([0,0,0],'t'),([0.5,0,0],'b1'),([0,0.5,0],'b2'),([0.5,0.5,0],'h'))
        cell_vectors = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        color = {'t':'y', 'b1':'g', 'b2':'b', 'h':'r'}
        def site_type(site):
            if site[0]%1 < 0.1 and site[1]%1 < 0.1: site_type = 't'
            elif 0.4 < site[0]%1 < 0.6 and site[1]%1 < 0.1: site_type = 'b1'
            elif site[0]%1 < 0.1 and 0.4 < site[1]%1 < 0.6: site_type = 'b2'
            elif 0.4 < site[0]%1 < 0.6 and 0.4 < site[1]%1 < 0.6: site_type = 'h'
            return site_type
    elif surface == '111':
        points = (([0,0,0],'t'),([1./3,2./3,0],'f'),([2./3,1./3,0],'h'))
        cell_vectors = np.array([[1.0, 0.0, 0.0], [-0.5, 3**0.5/2, 0.0], [0.0, 0.0, 1.0]])
        color = {'t':'y', 'f':'b', 'h':'r'}
        def site_type(site):
            if site[0]%1 < 0.1 or site[0]%1 > 0.9: site_type = 't'
            elif 0.3 < site[0]%1 < 0.4: site_type = 'f'
            elif 0.6 < site[0]%1 < 0.7: site_type = 'h'
            return site_type
    for offset,suffix in points:
        coor=[]
        with open('cut_' + surface + '_7') as f:
            for line in f:
                coor.append([ float(x) for x in line[1:-2].split() ])
            coor_f=np.array(coor)+offset
        coor_c = np.dot(coor_f, cell_vectors)
        fig = plt.figure(figsize=(17,17))
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim([-8.5,8.5])
        ax.set_ylim([-8.5,8.5])
        types = []
        for i in range(len(coor_f)):
            types.append(site_type(coor_f[i]))
            ax.add_patch(plt.Circle((coor_c[i][0],coor_c[i][1]), 0.2, color=color[types[-1]], alpha=0.5))
            ax.text(coor_c[i][0],coor_c[i][1], str(i), fontsize=12,horizontalalignment='center')
            ax.text(coor_c[i][0],coor_c[i][1]-0.15, types[-1], fontsize=8,horizontalalignment='center')
        ax.add_patch(plt.Circle((coor_c[0][0],coor_c[0][1]), 0.1, color='k', alpha=0.7))
        fig.savefig(surface+'_'+suffix+'.png',bbox_inches='tight')
