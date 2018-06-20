import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
def match(artist):
  return artist.__module__ == "matplotlib.text"
os.chdir('/home/thaa191/data2')
import kicklib
#%%
os.chdir('/home/thaa191/data2/2018')
#repeat = 3
#folder_lims = [201803131454,201803132045]
widths = np.arange(5,55,5)
time = np.arange(10,260,10)
width = 10
if width==5:
  folders = ['201803131454','201803131707','201803131901']
if width==10:
  folders = ['201803131506','201803131718','201803131912']
if width==15:
  folders = ['201803131518','201803131730','201803131924']
if width==20:
  folders = ['201803131530','201803131741','201803131935']
if width==25:
  folders = ['201803131543','201803131752','201803131947']
if width==30:
  folders = ['201803131610','201803131804','201803131959']
if width==35:
  folders = ['201803131622','201803131815','201803132010']
if width==40:
  folders = ['201803131633','201803131826','201803132022']
if width==45:
  folders = ['201803131645','201803131838','201803132034']
if width==50:
  folders = ['201803131656','201803131849','201803132045']
if width==60:
  folders = ['201803231302','201803231313','201803231324']
if width==80:
  folders = ['201803261127','201803261139','201803261153']
if width==100:
  folders = ['201803261408','201803261421','201803261434']
if width==120:
  fodlers = ['201803271033','201803271046','201803271101']
#%%

all_data = []

user_select = False
points = [[140,310],[310,400]]

for i in range(0,len(folders)):
    num = 0
    for j in os.listdir(folders[i]):
      if(j.endswith('.mat')):
        num = num+1
    print('Found '+ str(num)+' mat files in '+str(folders[i]))
    for j in range(0,num):
      data = sio.loadmat(str(folders[i])+'/Data_'+str(j)+'.mat')
      if(user_select):
        plt.imshow(data['a1'])            
        points = plt.ginput(2,0)
        plt.close()
        points = (np.floor(points)).astype(int)
        print(points)
        user_select = False
      x_points = [ points[0][0], points[1][0] ]
      y_points = [ points[0][1], points[1][1] ]
        
      try: 
        all_data[j] += data['a1'][y_points[0]:y_points[1],x_points[0]:x_points[1]]/3
      except IndexError:
        all_data.append(data['a1'][y_points[0]:y_points[1],x_points[0]:x_points[1]]/3)
  
    #%%
boundry_select = False
points = [[94,54],[65,39]]
if boundry_select:
    plt.imshow(all_data[len(all_data)-1])
    points = plt.ginput(2,0)
    plt.close()
    points = (np.floor(points)).astype(int)
    print(points)
    boundry_select = False

bounds = [ points[0][0], points[1][0] ]
    
#%%
all_imbal = []
uncert = []
c = (2e-6**2)/(1.938e-13)
for i in range(0,len(all_data)):
    single = np.sum(all_data[i],0)
    N1 = np.sum(single[bounds[0]:],0)
    N2 = np.sum(single[0:bounds[1]],0)
    errComb = np.sqrt(N1+N2)
    imbal = (N1-N2)/(N1+N2)
    relImbal = np.sqrt((errComb/(N1+N2))**2+(errComb/(N1-N2))**2)
    all_imbal.append(imbal)
    uncert.append(imbal*relImbal)
#%%
os.chdir('/home/thaa191/Programing/Dumbbells/Width_data')
save_data = {'imbalance':np.array(all_imbal),'width':width,'time':time}
sio.savemat('width_'+str(width)+'.mat',{'error':uncert,'imbalance':all_imbal,'width':width,'time':time})
plot_images = False
plot_profiles = False
plot_imbal = False
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
  fig_img.savefig("Image_Plot_width_"+str(int(width))+".png")
  plt.close()
if(plot_profiles):
  fig_profiles = plt.figure()
  for i in range(0,len(all_data)):
      ax = plt.subplot(5,pic_row,i+1)
      single = np.sum(all_data[i],0)
      ax.plot(single)
      ax.axvline(bounds[0])
      ax.axvline(bounds[1])
      ax.set_title(time[i])
  plt.tight_layout()
  fig_profiles.savefig("Profile_Plot_width_"+str(int(width))+".png")
  plt.close()
if(plot_imbal):
  fig_imbal = plt.figure()
  ax = plt.subplot()
  ax.errorbar(time, all_imbal, yerr=uncert, fmt='o')
  ax.set_ylim(-0.4,1.05)
  ax.set_xlim(0,255)
  ax.axhline(y=0, xmin=0, xmax=1,color = 'k')
  ax.set_xlabel('Expansion Time (ms)')
  ax.set_ylabel('Imbalance')
  font_size=24
  for textobj in fig_imbal.findobj(match=match):
    textobj.set_fontsize(font_size)
  plt.tight_layout()
  #fig_imbal.savefig("Imbal_Plot_width_"+str(int(width))+".png")
  #plt.close()
  
thesis_plot = True
if thesis_plot:
  fig_img = plt.figure(figsize=(2, 4), dpi=80)
  img_index = [0,14,24]
  plot_titles = ['(a)','(b)','(c)']#,'(d)','(e)','(f)']
  for i in range(0,len(img_index)):
      ax = plt.subplot(3,1,i+1)
      ax.imshow(all_data[img_index[i]])
      ax.set_title(plot_titles[i])
      ax.xaxis.set_visible(False)
      ax.yaxis.set_visible(False)
  plt.tight_layout()
  #fig_img.savefig("Select_Image_Plot_width_"+str(int(width))+".eps")
  #plt.close()
#%%
#check = sio.loadmat('width_5.mat')
