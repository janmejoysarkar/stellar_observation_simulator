import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
from astropy.io import fits
import time

def sim_obs(del_c, del_r, total_intensity, h=320, w=320, BIAS=1500):

    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)
    psf_path= os.path.join(project_path, "../data/interim/psf.fits")
    psf= fits.open(psf_path)[0].data
    #Make a blank canvas
    canvas = np.zeros((h, w))
    # Make the star
    star= psf*total_intensity/np.sum(psf)
    # Replace a portion of the canvas with the pixel data 
    canvas[int(h/2+del_r):int(h/2+del_r+np.shape(star)[0]), int(w/2+del_c):int(w/2+del_c+np.shape(star)[1])]=star
    # Introducing random Poisson noise.
    canvas = np.random.poisson(canvas) 
    # Read noise added separately
    read_noise = np.random.normal(loc=BIAS, scale=10, size=(h, w)) 
    canvas = canvas + read_noise # final image

    return canvas
if __name__=='__main__':
   # Dictionary of photoelectrons/pixel/second * degradation_factor
   pe={'NB01': 2083*0.5,
       'NB02': 694*0.5,
       'NB03': 694*0.5,
       'NB04': 833*0.5,
       'NB05': 1042*0.5,
       'NB06': 1190*1,
       'NB07': 1389*1,
       'NB08': 46*1,
       'BB01': 8333*1,
       'BB02': 833*1,
       'BB03': 1389*1
    }

   image= sim_obs(10, 10, total_intensity=pe['NB07'])
   plt.imshow(image, origin='lower')
   plt.show()
