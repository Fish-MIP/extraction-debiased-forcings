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

# %%
# Chl in NEMO is stored in mg/m3
# It is converted into kg
mg_to_kg = 1e-6

# %%
for scenario in ['SSP126', 'SSP245',  'SSP370',  'SSP585']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/chl', scenario.lower())
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario}-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    filelist = glob(os.path.join(dirin, '*v2_20[2-9]*1m*ptrc_T*'))
    filelist += glob(os.path.join(dirin, '*v2_201[5-9]*1m*ptrc_T*'))
    filelist.sort()

    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data
        
        # Extract chlorophyle by summing its two components
        
        chl = mg_to_kg * (data['NCHL'] + data['DCHL'])
        chl
        
        # Rename the time_counter variable and the name of the outut variable
        
        chl = chl.rename({'time_counter': 'time'})
        chl.name = 'chl'
        chl
        chl.attrs['units'] = 'kg/m3'
        chl.attrs['long_name'] = 'Mass Concentration of Total Phytoplankton Expressed as Chlorophyll'
        
        date = chl['time']
        date
        
        years = np.array([d.year for d in date.values])
        months = np.array([d.month for d in date.values])
        days = np.array([d.day for d in date.values])
        
        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_chl_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        print(foutname)
        
        chl.to_netcdf(foutname, unlimited_dims=['time'])

# %%
