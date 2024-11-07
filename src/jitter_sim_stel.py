import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from simulated_obs import *
import argparse
from astropy.time import Time
import os

def jit_sim(idx=200, sun_c_path='/Users/soumyaroy/Desktop/masterlimbfit/', plot=True, save=True, plot_save_path=None):
    # Define paths
    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)
    sav = os.path.join(project_path, '../data/processed')  # Path to save generated FITS files
    
    # Create directory if it doesn't exist
    os.makedirs(sav, exist_ok=True)

    if plot_save_path:
        os.makedirs(plot_save_path, exist_ok=True)  # Create the directory to save plots if not exists

    # Load Sun center fit data
    files = sorted(glob(f'{sun_c_path}*.suncentre'))
    if idx >= len(files):
        print(f"Index {idx} is out of range. Found {len(files)} files.")
        return
    f = files[idx]
    print(f"Using file: {f}")
    
    # Define the dtype: str for the first column (date), float for the remaining columns
    dtype = [('date', 'U25'), ('x', 'f8'), ('dx', 'f8'), ('y', 'f8'), ('dy', 'f8'), ('r', 'f8'), ('dr', 'f8')]
    try:
        data = np.loadtxt(f, dtype=dtype)
    except Exception as e:
        print(f"Error loading data from {f}: {e}")
        return
    
    # Convert the 'date' field to Time
    date = Time(data['date'])
    x = data['x'] - data['x'][0]  # Adjust x coordinates to start from 0
    y = data['y'] - data['y'][0]  # Adjust y coordinates to start from 0
    
    frames = len(x)
    date = (date.jd - date[0].jd) * 86400.  # Convert to seconds relative to the first date

    # Set up plotting
    if plot:
        plt.figure()
    
    # Define color limits
    vmin, vmax = 1460, 1560  # Adjust these values based on your data range

    # Loop through frames and simulate observations
    for frame in range(frames):
        try:
            canvas = sim_obs(x[frame], y[frame])  # Simulate the observation
            
            if plot:
                plt.clf()  # Clear the current figure to update it
                im = plt.imshow(canvas, origin='lower', cmap='inferno', vmin=vmin, vmax=vmax)
                # plt.colorbar(im)
                plt.title(f'NB7 t={date[frame]:.2f} s')
                plt.draw()
                plt.pause(0.05)  # Adjust to control the update speed
            
            if save:
                save_path = os.path.join(sav, f'{frame}.fits')
                fits.writeto(save_path, canvas, overwrite=True)
                print(f"Frame {frame}: Saved {save_path}")
            
            if plot_save_path:
                # Save the plot to the specified folder
                plot_filename = os.path.join(plot_save_path, f"plot_{frame:04d}.png")  # Use frame number as filename
                plt.savefig(plot_filename, dpi=300)  # Save the plot as a PNG file with high resolution
                print(f"Frame {frame}: Saved plot as {plot_filename}")
            
            # Check if the plot window has been closed
            if not plt.get_fignums():
                print("Plot closed by the user.")
                break
        
        except ValueError as ve:
            print(f"ValueError at frame {frame}: {ve}")
        except Exception as e:
            print(f"Unexpected error at frame {frame}: {e}")

    if plot:
        plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sun_c_path', type=str, default='/Users/soumyaroy/Desktop/masterlimbfit/', help='Path to the project directory')
    parser.add_argument('--idx', type=int, default=200, help='Index of suncenter file to be used')
    parser.add_argument('--plot_save_path', type=str, default=None, help='Path to save the individual plots')
    args = parser.parse_args()

    jit_sim(sun_c_path=args.sun_c_path, idx=args.idx, save=False, plot_save_path=args.plot_save_path)
