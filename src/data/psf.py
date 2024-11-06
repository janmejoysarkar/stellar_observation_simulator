#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wed Nov  6 03:07:10 PM IST 2024
@author: janmejoyarch
@hostname: suitpoc1

DESCRIPTION
- Generates PSF cutout from post-disasm mode data.
- 
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os

PLOT, SAVE= True, True # Toggle if plotting/ saving fits files are to be enabled/ disabled.

project_path= '/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/photometry/stellar_photometry_focus/stellar_observation_simulation/'
data_path= os.path.join(project_path, 'data/raw/normal_FF_Dark_Normal_fw1_04_fw2_02_os_254_rd_freq_280k_40sec_024_000002.fits')
sav= os.path.join(project_path, 'data/interim/psf.fits') # Save location

SIZE=6 # Radius of PSF cutout
psf_c, psf_r =1425,1436

data= fits.open(data_path)[0].data
# Calculate median away from the PSF to compute bg counts.
bg= np.median(data[psf_r-10:psf_r+10, psf_c+2*10:psf_c+4*10])
# Crop out the PSF. Subtract the bg.
data_crop=data[psf_r-SIZE : psf_r+SIZE, psf_c-SIZE:psf_c+SIZE]-bg
# Normalize the cropped PSF.
data_crop= data_crop/np.max(data_crop)
if PLOT:
    plt.figure()
    plt.imshow(data_crop, origin='lower')
    plt.show()
if SAVE: fits.writeto(sav, data_crop, overwrite=True)
