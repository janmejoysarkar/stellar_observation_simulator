import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from simulated_obs import *
import argparse
from astropy.time import Time
import os
from scipy.interpolate import interp1d

def jit_sim(ftr_name, save, save_dith, sun_c_path, dt, plot=True, plot_save_path=None, date_str=None, ):

    """Function to dither the simulated star observations. 
    
    Mandatory input:
    
    --date: str. In the format 'YYYY-MM-DD'. Will find the appropriate sun_c file and take the appropriate
            sun center values from the corresponding date.
    
    --ftr_name: str. The name of the filter for which the observation needs to be generated.
    
    Optional input:

    --sun_c_path: str. The path where the "*.suncenter" files are saved. By default assumes 
                  /Users/soumyaroy/Desktop/masterlimbfit/
    
    Optional flags:

    --save: provide the flag if the individual fits files need to be saved. Files will be saved in 
            {project_dir}/data/processed/fits_files/{ftr_name}_{frame_no}.fits
    
    --save_dith: provide the flag if the individual x and y dither values are to be saved. The values will
                 be saved in a .txt file in {project_dir}/data/processed/dith_{date}_{ftr_name}.txt
    
    Example usage:

    python jitter_sim_stel.py --date='2024-09-19' --ftr_name='NB07' --save --save_dith

    """


    # Define paths
    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(current_file_path)
    sav = os.path.join(project_path, '../data/processed/')  # Path to save generated FITS files
    
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
    date1 = Time(data['date'])
    x1 = data['x'] - data['x'][0]  # Adjust x coordinates to start from 0
    y1 = data['y'] - data['y'][0]  # Adjust y coordinates to start from 0

    x_func = interp1d((date1.jd-date1[0].jd)*86400., 2.*x1); y_func = interp1d((date1.jd-date1[0].jd)*86400., 2.*y1)
    
    frames = 600; 
    #date = (date.jd - date[0].jd) * 86400.  # Convert to seconds relative to the first date

    # Set up plotting
    if plot:
        plt.figure()
    
    # Define color limits
    vmin, vmax = 1460, 1560  # Adjust these values based on your data range

    x_app = []; y_app= []
    # Loop through frames and simulate observations
    for frame in range(frames):
        try:
            t = 0. + frame* dt; x = x_func(t); y = y_func(t)
            canvas = sim_obs(x, y, ftr_name)  # Simulate the observation
            x_app.append(x); y_app.append(y)
            
            if plot:
                plt.clf()  # Clear the current figure to update it
                im = plt.imshow(canvas, origin='lower', cmap='inferno', vmin=vmin, vmax=vmax)
                # plt.colorbar(im)
                plt.title(f'{ftr_name} t={t:.2f} s')
                plt.draw()
                plt.pause(0.05)  # Adjust to control the update speed
            
            if save:
                if(frame<10):
                    save_path = os.path.join(sav, f'fits_files/{ftr_name}_00{frame}.fits')
                elif(frame<100):
                    save_path = os.path.join(sav, f'fits_files/{ftr_name}_0{frame}.fits')
                else:
                    save_path = os.path.join(sav, f'fits_files/{ftr_name}_{frame}.fits')
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

    if save_dith:
        x_app = np.array(x_app); y_app = np.array(y_app)
        np.savetxt(f'{sav}dith_{date_str}_{ftr_name}.txt', np.c_[x_app, y_app],)

    if plot:
        plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sun_c_path', type=str, default='/Users/soumyaroy/Desktop/masterlimbfit/', help='Path to the limbfit directory')
    parser.add_argument('--date', type=str, required=True, help='Date of the suncenter file to be used (in format YYYY-MM-DD)')
    parser.add_argument('--dt', type=float, default=8., help='The total amount of time spent to expose and read one frame')
    parser.add_argument('--ftr_name', type=str, help='Name of the filter to be simulated. Allowed values are: NB01, NB02, NB03, NB04, NB05, NB06, NB07, NB08, BB01, BB02, BB03')
    parser.add_argument('--plot_save_path', type=str, default=None, help='Path to save the individual plots')
    parser.add_argument('--save', action='store_true', help='Flag to save the fits files in ../data/processed (default False)')
    parser.add_argument('--save_dith', action='store_true', help='Flag to save the dither values used in ../data/processed (default False)')
    args = parser.parse_args()

    jit_sim(sun_c_path=args.sun_c_path, ftr_name=args.ftr_name, dt=args.dt, save=args.save, save_dith=args.save_dith, plot_save_path=args.plot_save_path, date_str=args.date)
