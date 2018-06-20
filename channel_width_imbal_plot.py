import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from natsort import natsorted
def match(artist):
  return artist.__module__ == "matplotlib.text"

os.chdir('/home/thaa191/Programing/Dumbbells/Width_data/')
folder = '/home/thaa191/Programing/Dumbbells/Width_data/'
num = 0
files = []
width = [5,10,15,20,25,30,35,40,45,50]
for j in os.listdir(folder):
  if(j.endswith('.mat')):
    num = num+1
    files.append(j)
print('Found '+ str(num)+' mat files in '+str(folder))
files = natsorted(files)
all_imbal = []
all_errors = []
fill_factors = []
for i in files:
  data = sio.loadmat(folder+'/'+i)
  all_imbal.append(data['imbalance'][0])
  all_errors.append(data['error'][0])
time = np.array(data['time'][0])
fig_imbal = plt.figure()
ax = plt.subplot(111)
legend_list = []
for i in range(0,len(all_imbal)):
  #ax = plt.subplot(2,5,i+1)
  ax.errorbar(time, all_imbal[i], yerr=all_errors[i], fmt='o')
  #ax.errorbar(time, all_imbal[3], yerr=all_errors[3], fmt='x')
  #ax.errorbar(time, all_imbal[6], yerr=all_errors[6], fmt='v')
  #ax.errorbar(time, all_imbal[8], yerr=all_errors[8], fmt='s')
  #legend_list=['5 px','20 px','35 px','45 px']
  ax.set_ylim(-0.1,1.05)
  ax.set_xlim(0,255)
  legend_list.append(str(width[i])+' px')
ax.legend(legend_list, fontsize = 5,loc=2,bbox_to_anchor=(1.01,0.9),borderaxespad=0.)
#plot_title = "Imbalances for Length "+str(length)+" (px)"
#plt.title(plot_title)
ax.set_xlabel('Expansion Time (ms)')
ax.set_ylabel('Imbalance')
ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
font_size=24
ax.set_ylim(-0.1,1.05)
ax.set_xlim(0,255)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
for textobj in fig_imbal.findobj(match=match):
  textobj.set_fontsize(font_size)
#plt.tight_layout()

imbal_average = []
error_average = []
for j in range(0,len(all_imbal)):
  imbal_average.append(np.average(all_imbal[j][6:]))
  error = 0
  for i in range(0,len(all_imbal[j])):
    error += (all_errors[j][i]/all_imbal[j][i])**2  
  error_average.append(imbal_average[j]*np.sqrt(error)/21)

width_l = np.array(width)*0.7
avg_fig = plt.figure(figsize=(10, 8), dpi=80)
ax = plt.subplot(111)
ax.errorbar(width_l,imbal_average,yerr=error_average,fmt='o')
ax.set_xlabel('Channel width ($\mu$m)')
ax.set_ylabel('Average Imbalance')
ax.set_xlim(0,36) 
ax.set_ylim(0,1) 
font_size=24
for textobj in avg_fig.findobj(match=match):
  textobj.set_fontsize(font_size)