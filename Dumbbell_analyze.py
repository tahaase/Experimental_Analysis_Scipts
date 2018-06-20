import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from tkinter import Tk
from tkinter import filedialog

os.chdir('/home/thaa191/data2')
import kicklib

#%%
Tk().withdraw()
#folderpath = filedialog.askdirectory() 
folders = []
#folders.append(folderpath)

#folders = ['201608161822']
folders = ['201608161607']

all_data = []

user_select = True
y_points = [258,280]
x_points = [252,294]

for i in range(0,len(folders)):
    num = 0
    for j in os.listdir(folders[i]):
        if(j.endswith('.mat')):
            num = num+1
    print('Found '+ str(num)+' mat files in '+str(folders[i]))
    for j in range(0,num):
        data = loadmat(str(folders[i])+'/Data_'+str(j)+'.mat')
        all_data.append(data['a1'])
        
if(user_select):
    plt.imshow(all_data[len(all_data)-1])            
    points = plt.ginput(2,0)
    plt.close()
    points = (np.floor(points)).astype(int)
    print(points)
    x_points = [ points[0][0], points[1][0] ]
    y_points = [ points[0][1], points[1][1] ]
    user_select = False
    
for i in range(0,len(all_data)):
    data = all_data[i]
    all_data[i] = data[y_points[0]:y_points[1],x_points[0]:x_points[1]]

#%%
boundry_select = True
if boundry_select:
    plt.imshow(all_data[len(all_data)-1])
    points = plt.ginput(2,0)
    plt.close()
    points = (np.floor(points)).astype(int)
    print(points)
    bounds = [ points[0][0], points[1][0] ]
    boundry_select = False

#%%
all_imbal = []
c = (2e-6**2)/(1.938e-13)
for i in range(0,len(all_data)):
    data = np.sum(all_data[i],0)
    N1 = np.sum(data[0:bounds[0]],0)*c
    N2 = np.sum(data[bounds[1]:],0)*c
    imbal = (N1-N2)/(N1+N2)
    all_imbal.append(imbal)
    
#%%
    
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as plticker

fig = plt.figure()
gs = gridspec.GridSpec(3,2)
ax1 = plt.subplot(gs[0,:-1])
ax2 = plt.subplot(gs[1,:-1])
ax3 = plt.subplot(gs[2,:-1])
ax4 = plt.subplot(gs[:,1:])

data_ax1 = kicklib.filter2(all_data[0])
ax1.imshow(data_ax1)
ax1.set_title(r'(a)',x=0.1)
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)

data_ax2 = kicklib.filter2(all_data[15])
ax2.imshow(data_ax2)
ax2.set_title(r'(b)',x=0.1)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

data_ax3 = kicklib.filter2(all_data[40])
ax3.imshow(data_ax3)
ax3.set_title(r'(c)',x=0.1)
ax3.xaxis.set_visible(False)
ax3.yaxis.set_visible(False)

ax4_time = np.linspace(0,150,len(all_data))
ax4.plot(ax4_time, all_imbal,'o')
ax4.set_title(r'(d)',x=0.1)
ax4.set_xlabel('Time(ms)', fontsize = 22)
ax4.set_ylabel('Imbalance', fontsize = 22)
ax4.set_xlim(0,150)

plt.rc('font', size = 18)
plt.tight_layout
#%%
os.chdir('/home/thaa191/Documents/SLM_paper')
fig.savefig("Dumbbells.pdf")