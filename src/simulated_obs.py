import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
from astropy.io import fits
import time

def sim_obs(del_c, del_r, h=320, w=320, peak_intensity=66, BIAS=1500,):

    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)

    # h,w=Size of canvas (height, width)
    # frames=Total frames to be generated
    # peak_intensity=Peak intensity of PSF in photo electrons.
    # BIAS=Bias value (photo electron)

    psf = fits.open(os.path.join(project_path, '../data/interim/psf.fits'))[0].data # PSF file

    
    canvas = np.zeros((h, w))
    star = psf * peak_intensity
    # Replace a portion of the canvas with the pixel data 
    canvas[int(h/2 + del_r):int(h/2 + del_r + np.shape(star)[0]), 
            int(w/2 + del_c):int(w/2 + del_c + np.shape(star)[1])] = star
    # Introducing random Poisson noise.
    canvas = np.random.poisson(canvas) 
    # Read noise added separately
    read_noise = np.random.normal(loc=BIAS, scale=10, size=(h, w)) 
    canvas = canvas + read_noise # final image

    return canvas
