#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2024-11-21 15:57:17
@author: janmejoyarch
@hostname: suitpoc1

DESCRIPTION
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
from astropy.io import fits
import time

def sim_obs(del_c, del_r, ftr_name, h=320, w=320, BIAS=1500):
    '''
    This function generates stellar observation simulated images
    based on SUIT PSF and degradation_factor.
 
    Input types:
    del_c, del_r= Position offset of the star from frame center. (integer)
    ftr_name= Filter name 'NB07' (string). After the provided name it looks up the total intensity
    from a predefined dictionary.
    '''
 
    # Dictionary of photoelectrons/pixel/second * degradation_factor
    pe={'NB01': 2083*0.3,
       'NB02': 694*0.68,
       'NB03': 694*0.72,
       'NB04': 833*0.68,
       'NB05': 1042*0.78,
       'NB06': 1190*0.8,
       'NB07': 1389*0.93,
       'NB08': 46*0.9,
       'BB01': 8333*0.3,
       'BB02': 833*0.72,
       'BB03': 1389*0.88
    }
    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)
    psf_path= os.path.join(project_path, "../data/external/psf.fits")
    psf= fits.open(psf_path)[0].data
    #Make a blank canvas
    canvas = np.zeros((h, w))
    # Make the star
    star= psf*pe[ftr_name]/np.sum(psf)
    # Star geometry
    star_row, star_col= int(np.shape(star)[0]/2), int(np.shape(star)[1]/2)
    # Replace a portion of the canvas with the pixel data 
    canvas[int(h/2-star_row+del_r):int(h/2-star_row+del_r+np.shape(star)[0]),
           int(w/2-star_col+del_c):int(w/2-star_col+del_c+np.shape(star)[1])]=star
    # Introducing random Poisson noise.
    canvas = np.random.poisson(canvas) 
    # Read noise added separately (RMS is 10. So mean value is set as BIAS+5)
    read_noise = np.random.normal(loc=BIAS+5, scale=10, size=(h, w)) 
    canvas = canvas + read_noise # final image
    return canvas

if __name__=='__main__':
    PLOT, SAVE=True, True
    ftr_ls= ['NB01','NB02','NB03','NB04','NB05','NB06','NB07','NB08','BB01','BB02','BB03']
    for ftr_name in ftr_ls:
        image= sim_obs(0, 0, ftr_name)
        if SAVE: fits.writeto(f'../products/{ftr_name}.fits', image, overwrite=True)
        print(ftr_name)
        plt.imshow(image, origin='lower')
        plt.title(ftr_name)
        plt.show()
    
