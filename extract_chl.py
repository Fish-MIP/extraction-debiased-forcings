# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python [conda env:nbarrier2]
#     language: python
#     name: conda-env-nbarrier2-py
# ---

# %%
import xarray as xr
from glob import glob
import os
import numpy as np
import filelist_extraction as fe

# %%
# Chl in NEMO is stored in mg/m3
# It is converted into kg
mg_to_kg = 1e-6

# %%
for scenario in ['SSP126', 'SSP245',  'SSP370',  'SSP585', 'historical', 'pi']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/', scenario, 'chl')
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    filelist = fe.extract_scenario(scenario, 'ptrc_T')

    # counter for the date extraction
    cpt = 0

    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data
        
        # Extract chlorophyle by summing its two components

        try:
            chl = mg_to_kg * (data['NCHL'] + data['DCHL'])
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
                    
        # Rename the time_counter variable and the name of the outut variable
        
        chl = chl.rename({'time_counter': 'time'})
        chl.name = 'chl'
        chl
        chl.attrs['units'] = 'kg/m3'
        chl.attrs['long_name'] = 'Mass Concentration of Total Phytoplankton Expressed as Chlorophyll'

        date, time = fe.compute_time(scenario, cpt) 
        
        chl = chl.assign_coords({"time": ("time", time)})
        chl['time'].attrs['units'] = fe.units
        chl.attrs['original_file'] = os.path.abspath(f)
        chl.attrs['script'] = 'extract_chl.py'
        
        years = np.array([d.year for d in date])
        months = np.array([d.month for d in date])
        days = np.array([d.day for d in date])
        
        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_chl_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        print(foutname)
        
        chl.to_netcdf(foutname, unlimited_dims=['time'])

        cpt += 1
