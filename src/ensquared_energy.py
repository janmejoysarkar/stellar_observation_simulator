import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


bg_rad=100

image= fits.open('../products/NB02.fits')[0].data
bg_data= image[165-bg_rad:165+bg_rad, 166-bg_rad:166+bg_rad]
bg=np.mean(bg_data)

cleaned_image= image-bg

radius_ls= np.arange(30)
ee_list= [cleaned_image[165,166]]
for r in radius_ls[1:]:
    ee= np.sum(cleaned_image[165-r:165+r, 166-r:166+r])
    ee_list.append(ee)

plt.plot(radius_ls, ee_list, 'o-')
plt.show()


def SNR(signal, r):
    '''
    signal= 90% ensquared energy
    r= radius for 90% ensquared energy
    '''
    bg_px= cleaned_image[165-bg_rad:165+bg_rad, 166-bg_rad:166+bg_rad]
    dia= r*2
    s= signal-(np.mean(bg_px)*dia**2) #Removing bg counts from signal
    read_noise= np.std(bg_px) #Read noise
    total_noise= np.sqrt(s+read_noise**2) #Adding poission noise and read noise in quadrature
    # Ideally, this should also have sky background, which will be sqrt(bg) added in quadrature. 
    SNR= s/total_noise
    print(SNR)
