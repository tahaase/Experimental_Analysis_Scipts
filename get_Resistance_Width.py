import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from natsort import natsorted
os.chdir('/home/thaa191/Programing/Dumbbells/Width_Disorder_data/')
def match(artist):
  return artist.__module__ == "matplotlib.text"
  
widths = [20,40,60,80,100,120] 
num = 0
files = []
all_imbal = [ [],[] ,[] ,[] ,[] ,[]]
all_errors = [ [],[] ,[] ,[] ,[] ,[]]
fill_factors = [0,0.05,0.1,0.15]
capacitance = [ [],[] ,[] ,[] ,[] ,[]]
hbar = 1.0545718e-34

for zz in range(0,len(widths)):
  folder = 'Width_'+str(widths[zz])
  for j in os.listdir(folder):
    if(j.endswith('.mat')):
      num = num+1
      files.append(j)
  print('Found '+ str(num)+' mat files in '+str(folder))
  files = natsorted(files)

  for i in files:
    data = sio.loadmat(folder+'/'+i)
    all_imbal[zz].append(data['imbalance'][0])
    all_errors[zz].append(data['error'][0])
    capacitance[zz].append(hbar*data['capacitance'][0][0])
  num = 0
  files = []
time = np.array(data['time'][0])*(1e-2)

#plt.figure()
#for i in range(0,len(all_imbal)):
#  ax = plt.subplot(3,5,i+1)
#  ax.plot(time,all_imbal[i])
#  ax.set_title(fill_factors[i])
#  ax.set_ylim(-0.2,1)
#
#plt.figure()
#for i in range(0,len(all_imbal)):
#  log_imbal = np.log(all_imbal[i])
#  ax = plt.subplot(3,5,i+1)
#  ax.plot(log_imbal)
#  ax.set_title(fill_factors[i])

from scipy.optimize import curve_fit
#plt.figure()
#plt.plot(all_imbal[0]) 
#t_point = plt.ginput(1,0)
#t_point = int(np.floor(t_point[0][0]))
#plt.close()

def Exponential_Decay(x,A,B,C,d):
  #return A*(1+((x-d)*B/2))#+(((x-d)*B)**2)/6)
  return A*np.exp(-(x-d)*B)+C

def first_term_exp(x,A,B,C,d):
  return A*(1+((x-d)*B/2))

def second_term_exp(x,A,B,C,d):
  exponent = -(x-d)*B
  return A*(1+(exponent)+(exponent**2/2))+C

def line(x,*p):
    m,c = p
    return x*m+c

Plot_Imbal = False
if Plot_Imbal:
  for zz in range(0,len(widths)):
    fig_imbal = plt.figure(figsize=(10, 8), dpi=80)
    ax = plt.subplot()
    marker_fmt = ['o','x','v','s']
    for i in range(0,len(fill_factors)):
      ax.errorbar(time, all_imbal[zz][i], yerr=all_errors[zz][i], fmt=marker_fmt[i])
    legend_list=['0','0.05','0.1','0.15']
    ax.legend(legend_list, fontsize = 5,loc=2,bbox_to_anchor=(0.9,1),borderaxespad=0.)
    ax.set_xlabel('Expansion Time (s)')
    ax.set_ylabel('Imbalance')
    ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
    font_size=24
    ax.set_ylim(-0.3,1.05)
    for textobj in fig_imbal.findobj(match=match):
      textobj.set_fontsize(font_size)
      
Plot_Stadium = False
if Plot_Stadium:
  fig_stadium = plt.figure(figsize=(10, 8), dpi=80)
  ax = plt.subplot()
  ax.errorbar(time, all_imbal[5][0], yerr=all_errors[5][0], fmt='o')
  ax.set_xlabel('Expansion Time (s)')
  ax.set_ylabel('Imbalance')
  ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
  font_size=24
  ax.set_ylim(-0.3,1.05)
  for textobj in fig_stadium.findobj(match=match):
    textobj.set_fontsize(font_size)


all_res = [ [],[] ,[] ,[] ]
all_res_error = [ [],[] ,[] ,[] ]

for fi in range(0,len(fill_factors)):
  fig_fit = plt.figure()
  print("Next Width")
  for i in range(0,len(widths)):
    width = widths[i]
    if(width==20):
      
      t_point_1 = 4
      t_point_2 = 9
      p_guess_exp = [1,0.5,0.45,0]
      sigma_exp = np.ones(len(all_imbal[3][t_point_1:]))
      sigma_exp[t_point_1+5:] = 0.8
      bounds_e = ((0,0,-1.1,-np.inf),(10,10, np.inf,np.inf))
    
      p_guess_line = [-0.2,1]
      sigma_line = np.ones(len(all_imbal[3][t_point_2:]))
      sigma_line[t_point_2:t_point_2+7] = 0.2
    if fi ==2:
      bounds_line = ((-6,-np.inf),(-0.06,np.inf))
    else:
      bounds_line = ((-6,-np.inf),(-0,np.inf))
  
  
  
    ax = plt.subplot(2,3,i+1)
    if(fi<1):
      xdata = time[t_point_1:len(time)]
      ydata= all_imbal[i][fi][t_point_1:len(time)]
      sigma_exp = 2*((np.array(all_errors[i][fi])))[t_point_1:len(time)]
      popt,pcov = curve_fit(second_term_exp, xdata , ydata , p0=p_guess_exp,sigma=sigma_exp,bounds = bounds_e)
      perr = np.sqrt(np.diag(pcov))
      curve = Exponential_Decay(time,*popt)
      all_res[fi].append(1/(popt[1]*capacitance[i][fi]))
      print(popt)
      #error = (perr[1]/popt[1])*(1/(popt[1]*capacitance))
      error = np.average(all_errors[i][fi][t_point_1:len(time)]/np.average(all_imbal[i][fi][t_point_1:len(time)]))
      error = error*(1/(popt[1]*capacitance[i][fi]))
      all_res_error[fi].append(error)
      ax.plot(time,curve)
    else:
      xdata = time[t_point_2:len(time)]
      ydata= np.log(all_imbal[i][fi][t_point_2:len(time)])
      sigma_line = 2*((np.array(all_errors[i][fi])/np.array(all_imbal[i][fi]))*np.log(all_imbal[i][fi]))[t_point_2:]
      popt,pcov = curve_fit(line, xdata , ydata , p0=p_guess_line,sigma=sigma_line,bounds=bounds_line)
      perr = np.sqrt(np.diag(pcov))
      curve = np.exp(line(time[t_point_2:],*popt))
      all_res[fi].append(-1/(popt[0]*capacitance[i][fi]))
      print(popt[0])
      #print(perr[0])
      error = (perr[0]/popt[0])*(1/(popt[0]*capacitance[i][fi]))
      all_res_error[fi].append(error)
      ax.plot(time[t_point_2:],curve)
    
    ax.errorbar(time, all_imbal[i][fi], yerr=all_errors[i][fi], fmt='o')
    #ax.set_title(fill_factors[i])
    ax.set_ylim(-0.3,1)

plot_resistance = True
if plot_resistance== True:
  fig_res = plt.figure(figsize=(10, 8), dpi=80)
  titles = ['(a)','(b)','(c)','(d)']
  marker_fmt = ['o','x','v','s']
  for i in range(0,4): 
    ax = plt.subplot(2,2,i+1)
    ax.errorbar(widths, all_res[i], yerr=all_res_error[i], fmt='o',ms=10)
    ax.set_xlim(0,121)
    ax.set_title(titles[i])
    ax.set_ylabel(r'Resistance ($h\times{}10^{-3}$)')
    ax.set_xlabel('Width (px)')
  #legend_list=['0','0.05','0.1','0.15']
  #ax.legend(legend_list, fontsize = 5,loc=2,bbox_to_anchor=(0.9,1),borderaxespad=0.)
  #ax.set_ylim(0,15)
  
  font_size=24
  for textobj in fig_res.findobj(match=match):
    textobj.set_fontsize(font_size)