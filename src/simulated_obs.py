import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
from astropy.io import fits
import time

def sim_obs(del_c, del_r, peak_intensity, h=320, w=320, BIAS=1500):

    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)

    #Make a blank canvas
    canvas = np.zeros((h, w))
    # Replace a portion of the canvas with the pixel data 
    canvas[int(h/2), int (w/2)] = peak_intensity
    # Introduce convolution

    # Introducing random Poisson noise.
    canvas = np.random.poisson(canvas) 
    # Read noise added separately
    read_noise = np.random.normal(loc=BIAS, scale=10, size=(h, w)) 
    canvas = canvas + read_noise # final image

    return canvas
if __name__=='__main__':
   # Dictionary of photoelectrons per pixel per second
   pe={'NB01': 2083,
       'NB02': 694,
       'NB03': 694,
       'NB04': 833,
       'NB05': 1042,
       'NB06': 1190,
       'NB07': 1389,
       'NB08': 46,
       'BB01': 8333,
       'BB02': 833,
       'BB03': 1389
    }

   image= sim_obs(10, 10, peak_intensity=pe['NB02'])
   plt.imshow(image, origin='lower')
   plt.show()
