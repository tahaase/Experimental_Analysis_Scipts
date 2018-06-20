import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

os.chdir('/home/thaa191/data2')
import kicklib

os.chdir('/home/thaa191/data2/2018')
repeat = 3
width = 80

if(width == 40):
  folder_lims = [201803231041,201803231251]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
elif(width == 60):
  folder_lims = [201803231302,201803231535]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
elif(width == 80):
  folder_lims = [201803261127,201803261355]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
elif(width == 100):
  folder_lims = [201803261408,20180303261630]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
elif(width == 120):
  folder_lims = [201803271033,20180303271305]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
elif(width == 20):
  folder_lims = [201803271318,20180303271602]
  time = np.arange(10,260,10)
  Fill_Factors = [0,0.05,0.1,0.15]
else: print("No data folders defined for that channel width")

folders = []

Get_Points = True
points_image = []
points_channel = []

Plot_Images = True
Plot_Profiles = True
Plot_Imbal = True

def def_Imabanlce(folder,fill_factor,width,time,points_image, points_channel, Get_Points, plot_images,plot_profiles,plot_imbal):
  all_data = []
  for i in range(0,len(folder)):
    num = 0
    for j in os.listdir(folder[i]):
      if(j.endswith('.mat')):
        num = num+1
    print('Found '+ str(num)+' mat files in '+str(folder[i]))
    if(num==0):
      kicklib.getallpics(str(folder[i]),len(time))
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
  #c = (2e-6**2)/(1.938e-13)
  for i in range(0,len(all_data)):
    single = np.sum(all_data[i],0)
    N1 = np.sum(single[points_channel[0]:],0)
    N2 = np.sum(single[0:points_channel[1]],0)
    imbal = (N1-N2)/(N1+N2)
    errComb = np.sqrt(N1+N2)
    imbal = (N1-N2)/(N1+N2)
    relImbal = np.sqrt((errComb/(N1+N2))**2+(errComb/(N1-N2))**2)
    all_imbal.append(imbal)
    uncert.append(imbal*relImbal)

  #plt.figure()
  #plt.plot(all_imbal)
  print("Saving imbalances")
  hbar = 1.0545718e-34
  g_nonl = 4*np.pi*(hbar**2)*(5.45e-9)/(1.44316060e-25)
  omega_z = 800*2*np.pi
  alpha = ((g_nonl* (0.5*1.44316060e-25*(omega_z**2))**(0.5))/(np.pi*(21e-6**2)*(4/3)))**(2/3)
  capacitance = (0.75/alpha)*((0.5*np.sum(np.sum(all_data[0],1),0))**(1/3))
  print("The capacitance is: "+str(capacitance))
  os.chdir('/home/thaa191/Programing/Dumbbells/Width_Disorder_data/Width_'+str(width))
  #save_data = {'imbalance':np.array(all_imbal),'width':width,'time':time}
  sio.savemat('Fill_'+str(int(fill_factor*100))+'.mat',{'imbalance':all_imbal,'Fill Factor':fill_factor,'error':uncert,'time':time, 'capacitance':capacitance,'all_data':all_data})
  os.chdir('/home/thaa191/Programing/Dumbbells/Width_Disorder_data/Width_'+str(width)+'/Images')
  pic_row = int(np.ceil(len(time)/5))
  if(plot_images):
    fig_img = plt.figure()
    for i in range(0,len(all_data)):
        ax = plt.subplot(5,pic_row,i+1)
        ax.imshow(all_data[i])
        ax.set_title(time[i])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    plt.tight_layout()
    fig_img.savefig("Image_Plot_FillFactor_"+str(int(fill_factor*100))+".png")
    plt.close()
  if(plot_profiles):
    fig_profiles = plt.figure()
    for i in range(0,len(all_data)):
        ax = plt.subplot(5,pic_row,i+1)
        single = np.sum(all_data[i],0)
        ax.plot(single)
        ax.axvline(points_channel[0])
        ax.axvline(points_channel[1])
        ax.set_title(time[i])
    plt.tight_layout()
    fig_profiles.savefig("Profile_Plot_FillFactor_"+str(int(fill_factor*100))+".png")
    plt.close()
  if(plot_imbal):
    fig_imbal = plt.figure()
    plt.plot(time,all_imbal)
    plt.tight_layout()
    fig_imbal.savefig("Imbal_Plot_FillFactor_"+str(int(fill_factor*100))+".png")
    plt.close()
  os.chdir('/home/thaa191/data2/2018')
  return points_image,points_channel

for i in os.listdir(os.getcwd()):
  try:
    date = int(i)
    if (date>=folder_lims[0] and date<=folder_lims[1]):
      folders.append(i)
  except ValueError:
    print(i+' Not a number')
folders = sorted(folders)
for i in range(0,len(Fill_Factors)):
  fill_factor = Fill_Factors[i]
  folder = [folders[i*repeat],folders[i*repeat+1],folders[i*repeat+2]]
  points_image,points_channel = def_Imabanlce(folder,fill_factor,width,time,points_image, points_channel, Get_Points, Plot_Images, Plot_Profiles, Plot_Imbal)
  Get_Points=False