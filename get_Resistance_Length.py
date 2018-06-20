import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from natsort import natsorted
os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_Length_data/')
def match(artist):
  return artist.__module__ == "matplotlib.text"
  
fillfactor = 16
if(fillfactor == 12):
  folder = 'Fill_12'
elif(fillfactor == 14):
  folder = 'Fill_14'
elif(fillfactor == 16):
  folder = 'Fill_16'
  
num = 0
files = []
for j in os.listdir(folder):
  if(j.endswith('.mat')):
    num = num+1
    files.append(j)
print('Found '+ str(num)+' mat files in '+str(folder))
files = natsorted(files)
all_imbal = []
all_errors = []
lengths = []
for i in files:
  data = sio.loadmat(folder+'/'+i)
  all_imbal.append(data['imbalance'][0])
  all_errors.append(data['error'][0])
  lengths.append(format(data['Length'][0][0],'.2f'))
time = np.array(data['time'][0])*(1e-3)
hbar = 1.0545718e-34
capacitance = hbar*data['capacitance'][0][0]

plt.figure()
for i in range(0,len(all_imbal)):
  log_imbal = np.log(all_imbal[i])
  ax = plt.subplot(3,5,i+1)
  ax.plot(log_imbal)
  ax.set_title(lengths[i])

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

if(fillfactor == 12):
  exp_fits = 0
  t_point_1 = 3
  t_point_2 = 9
  p_guess_exp = [1,0.5,0.45,0]
  sigma_exp = np.ones(len(all_imbal[3][t_point_1:]))
  sigma_exp[t_point_1+5:] = 0.8
  bounds_e = ((0,0,-1.1,-np.inf),(10,10, np.inf,np.inf))

  p_guess_line = [-0.2,1]
  sigma_line = np.ones(len(all_imbal[3][t_point_2:]))
  sigma_line[t_point_2:t_point_2+7] = 0.2

elif(fillfactor == 14):
  exp_fits = 2
  t_point_1 = 9
  t_point_2 = 9
  p_guess_exp = [1,0.01,0.45,0]
  sigma_exp = np.ones(len(all_imbal[3][t_point_1:]))
  sigma_exp[t_point_1+5:] = 0.8
  bounds_e = ((0,0,-1.1,-np.inf),(10,10, np.inf,np.inf))
  
  p_guess_line = [-0.2,1]
  sigma_line = np.ones(len(all_imbal[3][t_point_2:]))
  sigma_line[t_point_2:t_point_2+7] = 0.5    
            
elif(fillfactor == 16):
  exp_fits = 4
  t_point_1 = 4
  t_point_2 = 10
  p_guess_exp = [0.5,0.2,0.4,0]
  sigma_exp = np.ones(len(all_imbal[3][t_point_1:]))
  sigma_exp[t_point_1+5:] = 0.5
  bounds_e = ((0,0,-1.1,-np.inf),(1.2,10, np.inf,np.inf))

  p_guess_line = [-0.1,1]
  
all_res=[]
all_res_error = []
plt.figure()
for i in range(0,len(lengths)):
  ax = plt.subplot(3,5,i+1)
  if(i<exp_fits):
    xdata = time[t_point_1:len(time)]
    ydata= all_imbal[i][t_point_1:len(time)]
    sigma_exp = 2*((np.array(all_errors[i])))[t_point_1:len(time)]
    popt,pcov = curve_fit(second_term_exp, xdata , ydata , p0=p_guess_exp,sigma=sigma_exp,bounds = bounds_e)
    perr = np.sqrt(np.diag(pcov))
    curve = Exponential_Decay(time,*popt)
    all_res.append(1/(popt[1]*capacitance))
    print(popt)
    #error = (perr[1]/popt[1])*(1/(popt[1]*capacitance))
    error = np.average(all_errors[i][t_point_1:len(time)]/np.average(all_imbal[i][t_point_1:len(time)]))
    error = error*(1/(popt[1]*capacitance))
    all_res_error.append(error)
    ax.plot(time,curve)
  else:
    xdata = time[t_point_2:len(time)]
    ydata= np.log(all_imbal[i][t_point_2:len(time)])
    sigma_line = 2*((np.array(all_errors[i])/np.array(all_imbal[i]))*np.log(all_imbal[i]))[t_point_2:]
    popt,pcov = curve_fit(line, xdata , ydata , p0=p_guess_line,sigma=sigma_line,bounds=((-5,-np.inf),(-0,np.inf)))
    perr = np.sqrt(np.diag(pcov))
    curve = np.exp(line(time[t_point_2:],*popt))
    all_res.append(-1/(popt[0]*capacitance))
    print(popt[0])
    #print(perr[0])
    error = (perr[0]/popt[0])*(1/(popt[0]*capacitance))
    all_res_error.append(error)
    ax.plot(time[t_point_2:],curve)
  
  ax.errorbar(time, all_imbal[i], yerr=all_errors[i], fmt='o')
  ax.set_title(lengths[i])
  ax.set_ylim(-0.3,1)
    
#os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/Length_'+str(length)+'/Images')
fig_imbal = plt.figure(figsize=(10, 8), dpi=80)
ax = plt.subplot(111)
ax.errorbar(time, all_imbal[0], yerr=all_errors[0], fmt='o')
ax.errorbar(time, all_imbal[3], yerr=all_errors[3], fmt='x')
ax.errorbar(time, all_imbal[6], yerr=all_errors[6], fmt='v')
ax.errorbar(time, all_imbal[8], yerr=all_errors[8], fmt='s')
legend_list=['50','125','200','250']
ax.legend(legend_list, fontsize = 5,loc=2,bbox_to_anchor=(0.9,1),borderaxespad=0.)
#plot_title = "Imbalances for Length "+str(length)+" (px)"
#plt.title(plot_title)
ax.set_xlabel('Expansion Time (s)')
ax.set_ylabel('Imbalance')
ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
font_size=24
ax.set_ylim(-0.3,1.05)
for textobj in fig_imbal.findobj(match=match):
  textobj.set_fontsize(font_size)
plt.tight_layout()

#fig_imbal.savefig("Imbalance_Plot_Length_"+str(length)+".pdf")

fig_res = plt.figure()
plot_title = "Resistance for fill factor "+str(fillfactor)+" (px)"
plt.title(plot_title)
ax = plt.subplot()
#ax.plot(fill_factors,all_res,'.')
ax.errorbar(lengths[:-1],all_res[:-1],yerr=all_res_error[:-1],fmt='.')
ax.set_ylabel('resistance (AU)')
ax.set_xlabel('Fill Factor') 

font_size=28
for textobj in fig_imbal.findobj(match=match):
  textobj.set_fontsize(font_size)
#fig_res.savefig("Resistance_Plot_Length_"+str(length)+".pdf")

#os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_data/Resistance_Data')
#sio.savemat('Resistance_'+str(length)+'.mat',{'resistance':all_res,'error':all_res_error})