import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

os.chdir('/home/thaa191/Programing/Dumbbells') 
data = sio.loadmat('Disorder_Length_data/ref.mat')
lengths = data['lengths'][0]
image_points = data['image_points']
channel_points = data['channel_points']

#%%
os.chdir('/home/thaa191/data2')
import kicklib

os.chdir('/home/thaa191/data2/2018')
repeat = 3
fillfactor = 16
if(fillfactor == 12):
  folder_lims = [201805081340,201805082050]
  time = np.arange(10,310,10)
elif(fillfactor == 14):
  folder_lims = [201805091044,201805091725]
  time = np.arange(10,310,10)
elif(fillfactor == 16):
  folder_lims = [201805101044,201805101725]
  time = np.arange(10,310,10)

folders = []

Plot_Images = True
Plot_Profiles = True
Plot_Imbal = True

def def_Imabanlce(folder,length,fillfactor,time,image_point,channel_point, plot_images,plot_profiles,plot_imbal):
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
   
    for j in range(0,num):
      y_points = [image_point[0][1],image_point[1][1]]
      x_points = [image_point[0][0],image_point[1][0]]
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
    points_channel = [channel_point[0],channel_point[1]]
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
  os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_Length_data/Fill_'+str(fillfactor))
  #save_data = {'imbalance':np.array(all_imbal),'width':width,'time':time}
  sio.savemat('Length_'+str(int(length))+'.mat',{'imbalance':all_imbal,'Length':length,'error':uncert,'time':time, 'capacitance':capacitance,'all_data':all_data})
  os.chdir('/home/thaa191/Programing/Dumbbells/Disorder_Length_data/Fill_'+str(fillfactor)+'/Images')
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
    fig_img.savefig("Image_Plot_Length_"+str(int(length))+".png")
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
    fig_profiles.savefig("Profile_Plot_Length_"+str(int(length))+".png")
    plt.close()
  if(plot_imbal):
    fig_imbal = plt.figure()
    plt.plot(time,all_imbal)
    plt.tight_layout()
    fig_imbal.savefig("Imbal_Plot_Length_"+str(int(length))+".png")
    plt.close()
  os.chdir('/home/thaa191/data2/2018')


for i in os.listdir(os.getcwd()):
  try:
    date = int(i)
    if (date>=folder_lims[0] and date<=folder_lims[1]):
      folders.append(i)
  except ValueError:
    print(i+' Not a number')
folders = sorted(folders)
for i in range(0,len(lengths)):
  length = lengths[i]
  image_point = image_points[i]
  channel_point = channel_points[i]
  folder = [folders[i*repeat],folders[i*repeat+1],folders[i*repeat+2]]
  def_Imabanlce(folder,length,fillfactor,time,image_point,channel_point,Plot_Images,Plot_Profiles,Plot_Imbal)
  