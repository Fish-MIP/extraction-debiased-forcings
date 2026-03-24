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
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/temperature', scenario.lower())
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario}-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    filelist = glob(os.path.join(dirin, '*v2_20[2-9]*1m*grid_T*'))
    filelist += glob(os.path.join(dirin, '*v2_201[5-9]*1m*grid_T*'))
    filelist.sort()
    # print(filelist)

    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data = data.rename({"time_counter": "time"})

        # Conversion from C to K
        temp = (data['thetao'])
        temp.name = 'thetao'
        temp.attrs['units'] = 'C'

        date = temp['time']
        date
        
        years = np.array([d.year for d in date.values])
        months = np.array([d.month for d in date.values])
        days = np.array([d.day for d in date.values])

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_{temp.name}_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        print(foutname)
        temp.to_netcdf(foutname, unlimited_dims=['time'])

# %%
