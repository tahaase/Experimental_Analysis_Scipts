import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.optimize import curve_fit
os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/')
def match(artist):
  return artist.__module__ == "matplotlib.text"
from matplotlib_scalebar.scalebar import ScaleBar
length = 100
fill_factors = [0,8,16]
all_pics = []
for i in range (0,len(fill_factors)):
  folder = 'Length_'+str(length)
  os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/'+folder)
  data = sio.loadmat('Fill_'+str(fill_factors[i])+'.mat')
  all_pics.append(data['all_data'][24])
  
img_fig= plt.figure()
title = ['(a)','(b)','(c)']
for i in range(0,len(all_pics)):
  ax = plt.subplot(3,1,i+1)
  scalebar = ScaleBar(3*1e-6) # 1 pixel = 0.2 meter
  plt.gca().add_artist(scalebar)
  ax.imshow(all_pics[i])
  ax.set_title(title[i])
  ax.xaxis.set_visible(False)
  ax.yaxis.set_visible(False) 