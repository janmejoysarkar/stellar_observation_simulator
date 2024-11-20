#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2024-11-20 15:43:17
@author: janmejoyarch
@hostname: suitpoc1

DESCRIPTION
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

ftr_name= "BB03"
bg_rad=100

image= fits.open(f'../products/{ftr_name}.fits')[0].data
bg_data= image[165-bg_rad:165+bg_rad, 166-bg_rad:166+bg_rad]
bg=np.mean(bg_data)

cleaned_image= image-bg
pos= np.where(np.max(cleaned_image)==cleaned_image)
row, col= pos[0][0], pos[1][0]
print(f'Row: {row}, Col: {col}')

radius_ls= np.arange(30)
ee_list= [cleaned_image[row, col]]
for r in radius_ls[1:]:
    ee= np.sum(cleaned_image[row-r:row+r, col-r:col+r])
    ee_list.append(ee)

print(ee_list[0], np.max(cleaned_image))
plt.plot(radius_ls, ee_list, 'o-')
plt.title(ftr_name)
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
