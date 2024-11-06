#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wed Nov  6 12:07:43 PM IST 2024
@author: janmejoyarch
@hostname: suitpoc1

DESCRIPTION
- This script generates mock SUIT observations for stellar pointing.
- PSF is used from post-disasm mode data.
- All units are in photoelectrons

NOTE: PRNU should be removed from real observations.
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
from astropy.io import fits
import time

## USER-DEFINED ##
PLOT, SAVE= True, True # Toggle if plotting/ saving fits files are to be enabled/ disabled.
project_path= '/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/photometry/stellar_photometry_focus/stellar_observation_simulation/'
h,w= 320, 320 # Size of canvas (height, width)
frames= 100 # Total frames to be generated
rms_pos= 35 # RMS of fluctuation in position
peak_intensity= 66 # Peak intensity of PSF in photo electrons.
BIAS=1500 # Bias value (photo electron)
##################

sav= os.path.join(project_path, 'data/processed') #Path to save generated files
psf= fits.open(os.path.join(project_path, 'data/interim/psf.fits'))[0].data #PSF file

plt.figure()
for frame in range(frames):
    canvas= np.zeros((h,w))
    star= psf*peak_intensity
    # Generate the offset of PSF positioning from frame center.
    del_c, del_r= np.random.normal(loc=0, scale=rms_pos), np.random.normal(loc=0, scale=rms_pos) 
    # Replace a portion of the canvas with the pixel data 
    canvas[int(h/2+del_r):int(h/2+del_r+np.shape(star)[0]), int(w/2+del_c):int(w/2+del_c+np.shape(star)[1])]=star
    # Introducing random poission noise. 
    canvas= np.random.poisson(canvas) 
    #Poission noise is a property of light coming from the source. Read noise 
    #is not affected by poission noise. So read noise is introduced later.
    read_noise= np.random.normal(loc=BIAS, scale= 10, size= (h,w)) 
    #read noise. Central value of BIAS level. RMS error of 10e given as STDEV.
    canvas= canvas+read_noise #final image
    if PLOT: # Plots the images if PLOT is True
        plt.imshow(canvas, origin='lower')
        plt.show()
        time.sleep(0.05)
        plt.close()
    if SAVE: # Saves the images if SAVE is True.
        fits.writeto(os.path.join(sav, f'{frame}.fits'), canvas)
        print(f'{frame}.fits', overwrite=True)
print("Sequence completed.")
