# FILE: check_maos_psfs.py

# Import packages
import os
import fnmatch
import numpy as np
from astropy.io import fits

def check_maos_psfs_filepath(directory, silent=True):

    if not silent:
        print("Checking if path to PSFs exist...")

    if os.path.exists(directory):
        if not silent:
            print(f"Found psf directory: {directory}\n")
    else:
        raise FileNotFoundError(f"PSF directory does not exist: {directory}\n")
                    
    return

def load_maos_psfs(directory, seed=1, silent=True):
    
    filelist = os.listdir(directory)
    fits_files = fnmatch.filter(filelist, f'evlpsfcl_{seed}_x*_y*.fits')
    fits_files.sort()

    all_psfs = []
    all_pos = []
    all_wavelengths = []

    for fname in fits_files:
        with fits.open(os.path.join(directory, fname)) as hdul:
            for hdu in hdul:
                data = hdu.data
                header = hdu.header
                all_psfs.append(data)
                all_wavelengths.append(header['wvl'] * 1e9)
                theta = header['theta']
                all_pos.append([theta.real, theta.imag])

    psfs = np.array(all_psfs)
    pos = np.array(all_pos)
    wavelengths = np.array(all_wavelengths)
    pixel_scale = hdul[0].header['dp']

    if not silent:
        print(all_pos)
        print(f"Found {len(all_pos)} psfs.")
        print(f"Found {len(wavelengths)} wavelengths from {wavelengths[0]} nm to {wavelengths[-1]} nm.")

    return psfs, pos, wavelengths, pixel_scale
                
    
    return