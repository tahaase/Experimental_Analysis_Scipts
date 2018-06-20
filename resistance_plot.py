import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.optimize import curve_fit
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/Resistance_Data')
def match(artist):
  return artist.__module__ == "matplotlib.text"
  
def Exp(x,A,B,C,D):
  return A*np.exp((x-C)*B)+D

length = [50,75,100,125,150,175,200,225,250]
fill_factor = [0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16]
all_res = []
res_error = []
for i in range(0,len(length)):
  data = sio.loadmat('Resistance_'+str(length[i])+'.mat')
  all_res.append(data['resistance'][0])
  res_error.append(data['error'][0])

titles = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)']
m_s = 6
x_ticks = [0,0.04,0.08,0.12,0.16]
x_ticks2 = [0,0.16]
res_fig = plt.figure()
for i in range (0,len(length)):
  ax = plt.subplot(3,3,i+1)
  if i==1:
    fill_temp = np.delete(fill_factor,7)
    res_temp = np.delete(all_res[i],[7,9,10])
    err_temp = np.delete(res_error[i],[7,9,10])
    ax.errorbar(fill_temp, res_temp, yerr=err_temp, fmt='o', ms = m_s)
    ax2 = inset_axes(ax, width="30%", height=1, loc=2)
    ip = InsetPosition(ax,[0.18,0.62,0.4,0.3])
    ax2.errorbar(fill_factor, all_res[i][:len(fill_factor)], yerr=res_error[i][:len(fill_factor)], fmt='o')
    ax2.set_axes_locator(ip)
    ax2.xaxis.set_ticks(x_ticks2)
    ax2.yaxis.set_ticks([0,15,30])
    ax2.set_xlim(-0.01,0.17)
  elif i==8:
    fill_temp = np.delete(fill_factor,4)
    res_temp = np.delete(all_res[i],4)
    err_temp = np.delete(res_error[i],4)
    ax.errorbar(fill_temp, res_temp, yerr=err_temp, fmt='o', ms = m_s)
    ax2 = inset_axes(ax, width="30%", height=1, loc=2)
    ip = InsetPosition(ax,[0.18,0.62,0.4,0.3])
    ax2.errorbar(fill_factor, all_res[i][:len(fill_factor)], yerr=res_error[i][:len(fill_factor)], fmt='o')
    ax2.set_axes_locator(ip)
    ax2.xaxis.set_ticks(x_ticks2)
    ax2.set_xlim(-0.01,0.17)
    ax2.yaxis.set_ticks([0,15,30])
    ax2.set_ylim(0,35)
  else:
    ax.errorbar(fill_factor, all_res[i][:len(fill_factor)], yerr=res_error[i][:len(fill_factor)], fmt='o', ms = m_s)
  ax.set_title(titles[i])
  ax.set_ylim(0,all_res[i][8]+5)  
  ax.xaxis.set_ticks(x_ticks)
  ax.set_xlim(-0.01,0.17)
  if i==3: ax.set_ylabel(r'Resistance($h\times{}10^{-3}$)')
  if i==7:ax.set_xlabel('Fill factor')

font_size=28
for textobj in res_fig.findobj(match=match):
  textobj.set_fontsize(font_size)


res_fig2 = plt.figure()
res_length = []
res_length_error = []
curve = []
loc_length = []
loc_error = []




j=0
x_ticks = [0,50,100,150,200,250] 
for i in range(0, len(fill_factor)):
  for j in range(0,len(length)):
    res_length.append(all_res[j][i]) 
    res_length_error.append(res_error[j][i])
   
  ax = plt.subplot(3,3,i+1)
  ax.errorbar(length,res_length,yerr=res_length_error,fmt='o', ms = m_s)
  ax.xaxis.set_ticks(x_ticks)
  ax.set_title(titles[i])
  ax.set_xlim(0,255)
  if i==3: ax.set_ylabel(r'Resistance($h\times{}10^{-3}$)')
  if i==7:ax.set_xlabel('Length (px)')

  if i==0: 
    ax.yaxis.set_ticks([0,1,2,3,4])
    ax.set_ylim(0,5)
  if i==1:
    ax.yaxis.set_ticks([0,1,2,3,4])
    ax.set_ylim(0,5)
  if i==2:
    #ax.yaxis.set_ticks([0,2,4])
    ax.set_ylim(0,10)
  if i==3:
    ax.yaxis.set_ticks([0,4,8,12,16,20])
    ax.set_ylim(0,18)
  if i==4:
    ax.yaxis.set_ticks([0,10,20,30,40])
    ax.set_ylim(0,35)
  if i==5:
    #ax.yaxis.set_ticks([0,10,20,30,40])
    ax.set_ylim(0,15)
  if i==8:
    ax.yaxis.set_ticks([0,10,20,30,40,50])
    #ax.set_ylim(0,15)

  if(i>6):
    print(i)
    p_guess_exp = [0,0,0,0]
    sigma = np.ones(len(length))
    popt,pcov = curve_fit(Exp, length[:-1] , res_length[:-1] , p0=p_guess_exp)
    pcov = np.diag(pcov)
    #pcov = np.sqrt(pcov)
    loc_length.append(2/popt[1])
    loc_error.append((pcov[1]/popt[1])*(1/popt[1]))
    curve.append(Exp(length,*popt))
    ax.plot(length,Exp(length,*popt),'k',linewidth=2.5)
    #test = np.array([12.484,1/120,9.26,-12.4])
    #single = Exp(length,*test)
    #ax.plot(length,single)
  res_length = []
  res_length_error = []
font_size=28
for textobj in res_fig2.findobj(match=match):
  textobj.set_fontsize(font_size)