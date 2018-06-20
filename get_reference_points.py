import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

os.chdir('/home/thaa191/data2')
import kicklib

os.chdir('/home/thaa191/data2/2018')

folder = ['201805081332']
lengths = np.linspace(50,250,9)
all_data = []
for i in range(0,len(folder)):
  num = 0
  for j in os.listdir(folder[i]):
    if(j.endswith('.mat')):
      num = num+1
  print('Found '+ str(num)+' mat files in '+str(folder[i]))
  if(num==0):
    kicklib.getallpics(str(folder[i]),9)
    for j in os.listdir(folder[i]):
      if(j.endswith('.mat')):
        num = num+1
    print('Found '+ str(num)+' mat files in '+str(folder[i]))

  for j in range(0,num):
    #print('Loading /Data_'+str(j)+'.mat')
    data = sio.loadmat(str(folder[i])+'/Data_'+str(j)+'.mat')
    try: 
      all_data[j] += data['a1']/3
    except IndexError:
      all_data.append(data['a1']/3)
  
all_image_points = []
all_channel_points = []
for j in range(0,9):     
  plt.imshow(all_data[j])            
  points = plt.ginput(2,0)
  plt.close()
  points = (np.floor(points)).astype(int)
  x_points = [ points[0][0], points[1][0] ]
  y_points = [ points[0][1], points[1][1] ]
  points_image = [x_points,y_points]
  all_data[j] = all_data[j][y_points[0]:y_points[1],x_points[0]:x_points[1]]
  all_image_points.append(points_image)
    
  print("Select channel boundary points")
  plt.imshow(all_data[j])  
  points_cut = plt.ginput(2,0)
  plt.close()
  points_cut = (np.floor(points_cut)).astype(int)
  points_channel = [ points_cut[0][0], points_cut[1][0]]
  all_channel_points.append(points_channel)
os.chdir('/home/thaa191/Programing/Dumbbells')  
sio.savemat('Disorder_Length_data/ref.mat',{'lengths':lengths,'image_points':all_image_points,'channel_points':all_channel_points})
