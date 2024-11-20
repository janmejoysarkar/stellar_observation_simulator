import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from simulated_obs import *
import argparse
from astropy.time import Time
import os

def jit_sim(ftr_name, save, sun_c_path, plot=True, plot_save_path=None, date_str=None):
    # Define paths
    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)
    sav = os.path.join(project_path, '../data/processed')  # Path to save generated FITS files
    
    # Create directory if it doesn't exist
    os.makedirs(sav, exist_ok=True)

    if plot_save_path:
        os.makedirs(plot_save_path, exist_ok=True)  # Create the directory to save plots if not exists

    # Search for a file that matches the provided date string
    if date_str:
        files = sorted(glob(f'{sun_c_path}*.suncentre'))
        matching_files = [f for f in files if date_str in os.path.basename(f)]
        
        if len(matching_files) == 0:
            print(f"No file found for the date: {date_str}")
            return
        elif len(matching_files) > 1:
            print(f"Multiple files found for the date: {date_str}. Using the first one.")
        
        f = matching_files[0]
        print(f"Using file: {f}")
    else:
        print("No date provided. Please provide a valid date.")
        return
    
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
            canvas = sim_obs(x[frame], y[frame], ftr_name)  # Simulate the observation
            
            if plot:
                plt.clf()  # Clear the current figure to update it
                im = plt.imshow(canvas, origin='lower', cmap='inferno', vmin=vmin, vmax=vmax)
                # plt.colorbar(im)
                plt.title(f'NB7 t={date[frame]:.2f} s')
                plt.draw()
                plt.pause(0.05)  # Adjust to control the update speed
            
            if save:
                save_path = os.path.join(sav, f'{ftr_name}_{frame}.fits')
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
    parser.add_argument('--date', type=str, required=True, help='Date of the suncenter file to be used (in format YYYY-MM-DD)')
    parser.add_argument('--ftr_name', type=str, help='Name of the filter to be simulated. Allowed values are: NB01, NB02, NB03, NB04, NB05, NB06, NB07, NB08, BB01, BB02, BB03')
    parser.add_argument('--plot_save_path', type=str, default=None, help='Path to save the individual plots')
    parser.add_argument('--save', action='store_true', help='Flag to save the fits files in ../data/processed (default False)')
    args = parser.parse_args()

    jit_sim(sun_c_path=args.sun_c_path, ftr_name=args.ftr_name, save=args.save, plot_save_path=args.plot_save_path, date_str=args.date)
