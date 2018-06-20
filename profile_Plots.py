import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.optimize import curve_fit
os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/')
def match(artist):
  return artist.__module__ == "matplotlib.text"
  
def Exp(x,A,B,C,D):
  return A*np.exp((x-C)*B)+D

length = [50,100,150,200,225,250]
all_pics = []
for i in range (0,len(length)):
  folder = 'Length_'+str(length[i])
  os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/'+folder)
  data = sio.loadmat('Fill_16.mat')
  all_pics.append(data['all_data'][24])

channel_points = [[68, 53], [79, 51], [94, 51], [113, 54], [117, 53], [121, 52]]
#for i in range(0,len(all_pics)):
#  plt.imshow(all_pics[i])  
#  points_cut = plt.ginput(2,0)
#  plt.close()
#  points_cut = (np.floor(points_cut)).astype(int)
#  points = [ points_cut[0][0], points_cut[1][0]]
#  channel_points.append(points)
  
onepix = 2.3*1e-6
c = (2e-6**2)/(1.938e-13)

curve = []
loc_length = []
loc_error = []
y_ticks = [0,100,200,300]
x_ticks = [0,100,200,300,400]
for i in range (3,len(all_pics)):
  single = np.sum(all_pics[i],0)
  single = single[channel_points[i][1]:channel_points[i][0]]
  x_array = np.arange(0,len(single),1)
  x_array = x_array*onepix
  p_guess_exp = [0,0,0,0]
  sigma = np.ones(len(x_array))
  popt,pcov = curve_fit(Exp, x_array , single , p0=p_guess_exp,sigma = sigma)
  pcov = np.diag(pcov)
  pcov = np.sqrt(pcov)
  loc_length.append(1/popt[1])
  loc_error.append((pcov[1]/popt[1])*(1/popt[1]))
  curve.append(Exp(x_array,*popt))
j=0
fig_profiles = plt.figure(figsize=(12, 10), dpi=80)
title = ['(a)','(b)','(c)','(d)','(e)','(f)']  
for i in range(0,len(all_pics)):
  ax = plt.subplot(3,2,i+1)
  single = np.sum(all_pics[i],0)
  x_array = np.arange(0,len(single),1)
  x_array = x_array*onepix*1e6
  ax.plot(x_array,single*c)
  if i>2:
    ax.plot(x_array[channel_points[i][1]:channel_points[i][0]],curve[j]*c,'k', linewidth=2.5)
    j += 1
  ax.axvline(channel_points[i][0]*onepix*1e6)
  ax.axvline(channel_points[i][1]*onepix*1e6)
  ax.set_title(title[i])
  ax.set_xlabel('Position ($\mu$m)')
  ax.set_ylabel('Atom number')
  ax.xaxis.set_ticks(x_ticks)
  ax.yaxis.set_ticks(y_ticks)
  ax.set_xlim(0,max(x_array))
  
font_size=28
for textobj in fig_profiles.findobj(match=match):
  textobj.set_fontsize(font_size)
