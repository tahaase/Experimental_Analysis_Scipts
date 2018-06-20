import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
#from natsort import natsorted
def match(artist):
  return artist.__module__ == "matplotlib.text"

os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/')

imbal1 = []
error1 = []
data = sio.loadmat('Length_150/Fill_0.mat')
imbal1.append(data['imbalance'][0])
error1.append(data['error'][0])
time = np.array(data['time'][0])

os.chdir('/home/thaa191/Programing/Dumbbells/Bent_Channel/')

imbal2 = []
error2 = []
data = sio.loadmat('Length_50-50.mat')
imbal2.append(data['imbalance'][0])
error2.append(data['error'][0])

imbal3 = []
error3 = []
data = sio.loadmat('Length_100-50.mat')
imbal3.append(data['imbalance'][0])
error3.append(data['error'][0])

fig_imbal = plt.figure(figsize=(10, 8), dpi=80)
ax = plt.subplot(111)
ax.errorbar(time, imbal1[0], yerr=error1[0], fmt='o',ms=8)
ax.errorbar(time, imbal2[0], yerr=error2[0], fmt='x',ms=8)
ax.errorbar(time, imbal3[0], yerr=error3[0], fmt='v',ms=8)
legend_list=['Straight','50-50','100-50']
ax.legend(legend_list, fontsize = 5,loc=2,bbox_to_anchor=(0.85,1),borderaxespad=0.)
#plot_title = "Imbalances for Length "+str(length)+" (px)"
#plt.title(plot_title)
ax.set_xlabel('Expansion Time (ms)')
ax.set_ylabel('Imbalance')
ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
font_size=24
ax.set_ylim(-0.3,1.05)
ax.set_xlim(0,255)
for textobj in fig_imbal.findobj(match=match):
  textobj.set_fontsize(font_size)
plt.tight_layout()

#fig_imbal.savefig("Imbalance_Plot_Length_"+str(length)+".pdf")