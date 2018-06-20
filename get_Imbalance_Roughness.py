import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

os.chdir('/home/thaa191/data2')
import kicklib

os.chdir('/home/thaa191/data2/2018')

roughness = 10
length = 100

if(roughness == 1):
  folders = ['201803281027','201803281206','201803281342']
  time = np.arange(10,260,10)

if(roughness == 5):
  folders = ['201803281041','201803281220','201803281355']
  time = np.arange(10,260,10)

if(roughness == 10):
  folders = ['201803281055','201803281234','201803281407']
  time = np.arange(10,260,10)
  
  
Get_Points = True
points_image = []
points_channel = []

Plot_Images = True
Plot_Imbal = True

def def_Imabanlce(folder,roughness,length,time,points_image, points_channel, Get_Points, plot_images,plot_imbal):
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
     
      print("Select 1st reservoir boundary points")
      plt.imshow(all_data[len(all_data)-1])  
      points = plt.ginput(2,0)
      plt.close()
      points = (np.floor(points)).astype(int)
      x_points_1 = [ points[0][0], points[1][0] ]
      y_points_1 = [ points[0][1], points[1][1] ]
      print("Select 2nd reservoir boundary points")
      plt.imshow(all_data[len(all_data)-1])  
      points = plt.ginput(2,0)
      plt.close()
      points = (np.floor(points)).astype(int)
      x_points_2 = [ points[0][0], points[1][0] ]
      y_points_2 = [ points[0][1], points[1][1] ]
      Get_Points = False
        
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
    single = all_data[i][y_points_1[0]:y_points_1[1],x_points_1[0]:x_points_1[1]]
    N1 = np.sum(np.sum(single,1),0)
    single = all_data[i][y_points_2[0]:y_points_2[1],x_points_2[0]:x_points_2[1]]
    N2 = np.sum(np.sum(single,1),0)
    errComb = np.sqrt(N1+N2)
    imbal = (N1-N2)/(N1+N2)
    relImbal = np.sqrt((errComb/(N1+N2))**2+(errComb/(N1-N2))**2)
    all_imbal.append(imbal)
    uncert.append(imbal*relImbal)
  
  #plt.figure()
  #plt.plot(all_imbal)
  print("Saving imbalances")
  os.chdir('/home/thaa191/Programing/Dumbbells/Rough_Reservoir/')
  #save_data = {'imbalance':np.array(all_imbal),'length':length,'time':time}
  sio.savemat('Roughness_'+str(roughness)+'.mat',{'imbalance':all_imbal,'error':uncert,'Roughness':roughness,'time':time, 'length':length})
  os.chdir('/home/thaa191/Programing/Dumbbells/Rough_Reservoir/Images')
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
    fig_img.savefig("Image_Plot_Roughness_"+str(roughness)+".png")
    plt.close()
  if(plot_imbal):
    fig_imbal = plt.figure()
    ax = plt.subplot()
    ax.errorbar(time, all_imbal, yerr=uncert, fmt='o')
    ax.set_ylim(-0.4,1.05)
    plt.tight_layout()
    fig_imbal.savefig("Imbal_Plot_Roughness_"+str(roughness)+".png")
    plt.close()
  thesis_plot = True
  if thesis_plot:
    fig_img = plt.figure(figsize=(2, 4), dpi=80)
    img_index = [0,14,24]
    plot_titles = ['(a)','(b)','(c)','(d)','(e)','(f)']
    for i in range(0,len(img_index)):
        ax = plt.subplot(3,1,i+1)
        ax.imshow(all_data[img_index[i]])
        ax.set_title(plot_titles[i])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    plt.tight_layout()
    #fig_img.savefig("Select_Image_Plot_width_"+length+".eps")
    #plt.close()
      
  os.chdir('/home/thaa191/data2/2018')
  return points_image,points_channel


points_image,points_channel = def_Imabanlce(folders,roughness,length,time,points_image, points_channel, Get_Points, Plot_Images, Plot_Imbal)
Get_Points=False