import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

os.chdir('/home/thaa191/data2')
import kicklib

os.chdir('/home/thaa191/data2/2018')

def match(artist):
  return artist.__module__ == "matplotlib.text"

Get_Points= True
barrier_pos = np.linspace(0,150,16)
#folder = ['201805181551','201805181638','201805181647'] 
folder = ['201805181700','201805181709','201805181717']

all_data = []
for i in range(0,len(folder)):
  num = 0
  for j in os.listdir(folder[i]):
    if(j.endswith('.mat')):
      num = num+1
  print('Found '+ str(num)+' mat files in '+str(folder[i]))
  if(num==0):
    kicklib.getallpics(str(folder[i]),len(barrier_pos))
    for j in os.listdir(folder[i]):
      if(j.endswith('.mat')):
        num = num+1
    print('Found '+ str(num)+' mat files in '+str(folder[i]))
  
  if(Get_Points):
    for j in range(0,num):
      #print('Loading /Data_'+str(j)+'.mat')
      data = sio.loadmat(str(folder[i])+'/Data_'+str(j)+'.mat')
      try: 
        all_data[j] += data['a1']/3
      except IndexError:
        all_data.append(data['a1']/3)
    print("Select image boundry points")
    plt.imshow(data['a1'])            
    points = plt.ginput(2,0)
    plt.close()
    points = (np.floor(points)).astype(int)
    x_points = [ points[0][0], points[1][0] ]
    y_points = [ points[0][1], points[1][1] ]
    points_image = [x_points,y_points]
    for j in range(0,num):
      all_data[j] = all_data[j][y_points[0]:y_points[1],x_points[0]:x_points[1]]
   
    print("Select channel boundary points")
    plt.imshow(all_data[len(all_data)-1])  
    points_cut = plt.ginput(2,0)
    plt.close()
    points_cut = (np.floor(points_cut)).astype(int)
    points_channel = [ points_cut[0][0], points_cut[1][0]]
    Get_Points = False
    print(np.shape(all_data[0]),points_channel)
      
  else:
    x_points = points_image[0]
    y_points = points_image[1]
    for j in range(0,num):
      #print('Loading /Data_'+str(j)+'.mat')
      data = sio.loadmat(str(folder[i])+'/Data_'+str(j)+'.mat')
      try: 
        all_data[j] += data['a1'][y_points[0]:y_points[1],x_points[0]:x_points[1]]/3
      except IndexError:
        all_data.append(data['a1'][y_points[0]:y_points[1],x_points[0]:x_points[1]]/3)
          
print("Calculating imbalances")
all_imbal = []
uncert = []
c = (2e-6**2)/(1.938e-13)
for i in range(0,len(all_data)):
  single = np.sum(all_data[i],0)
  N1 = np.sum(single[points_channel[0]:],0)
  N2 = np.sum(single[0:points_channel[1]],0)
  errComb = np.sqrt(N1+N2)
  imbal = (N1-N2)/(N1+N2)
  relImbal = np.sqrt((errComb/(N1+N2))**2+(errComb/(N1-N2))**2)
  all_imbal.append(imbal)
  uncert.append(abs(imbal*relImbal))
  
Plot_Imbal = True
if Plot_Imbal:
  fig_imbal = plt.figure(figsize=(10, 8), dpi=80)
  ax = plt.subplot()
  #marker_fmt = ['o']
  ax.errorbar(barrier_pos, all_imbal, yerr=uncert)
  ax.set_xlabel('Barrier Position (px)')
  ax.set_ylabel('Imbalance')
  #ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
  font_size=24
  ax.set_ylim(0,0.6)
  for textobj in fig_imbal.findobj(match=match):
    textobj.set_fontsize(font_size)