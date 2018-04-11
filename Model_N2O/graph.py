import numpy as np
import matplotlib.pyplot as plt

def graph(surface, repetitions, sites, types, filename):
    x_rep = repetitions[0]
    y_rep = repetitions[1]
    color_def = {'o':'y', 'N':'b', 'NO':'m', 'O':'r', 'CO':'g'}   # 'y','r','g','b','c','m','k'

    if surface == '100':
        fig = plt.figure(figsize=(x_rep, y_rep))
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim([0,x_rep])
        ax.set_ylim([0,y_rep])
        for s_site,s_type in zip(sites, types):
            st_tmp = (s_site[0]+1e-3) % 1 + (s_site[1]+1e-3) % 1
            if st_tmp < 0.1:
                symbol = plt.Circle((s_site[0]+0.25,s_site[1]+0.25), 0.2, color=color_def[s_type])
            elif 0.4 < st_tmp < 0.6:
                symbol = plt.Polygon([[s_site[0]+0.08,s_site[1]+0.15],[s_site[0]+0.42,s_site[1]+0.15],[s_site[0]+0.25,s_site[1]+0.45]],color=color_def[s_type])
            elif st_tmp > 0.9:
                symbol = plt.Rectangle((s_site[0]+0.05,s_site[1]+0.05),0.4,0.4,color=color_def[s_type])
            else:
                print 'Unsupported site exists.'
                exit()
            ax.add_patch(symbol)
    elif surface == '111':
        fig = plt.figure(figsize=(x_rep+y_rep*0.5, y_rep*(3**0.5/2)))
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim([-y_rep*0.5, x_rep])
        ax.set_ylim([0,y_rep*(3**0.5/2)])
        for s_site,s_type in zip(sites, types):
            s_cor = np.dot(s_site[:2], np.array([[1.0, 0.0], [-0.5, 3**0.5/2]]))
            if (s_site[0]+1e-3) % 1 < 0.1:
                symbol = plt.Circle((s_cor[0]+0.25,s_cor[1]+0.22), 0.2, color=color_def[s_type])
            elif 0.3 < s_site[0] % 1 < 0.4:
                symbol = plt.Polygon([[s_cor[0]+0.08,s_cor[1]+0.12],[s_cor[0]+0.42,s_cor[1]+0.12],[s_cor[0]+0.25,s_cor[1]+0.42]],color=color_def[s_type])
            elif 0.6 < s_site[0] % 1 < 0.7:
                symbol = plt.Polygon([[s_cor[0]+0.08,s_cor[1]+0.32],[s_cor[0]+0.42,s_cor[1]+0.32],[s_cor[0]+0.25,s_cor[1]+0.02]],color=color_def[s_type])
            else:
                print 'Unsupported site exists.'
                exit()
            ax.add_patch(symbol)

    fig.savefig(filename+'.png',bbox_inches='tight')
