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
import file_extraction as fe

# %%
mesh = xr.open_dataset("/home1/datawork/nbarrier/apecosm/apecosm-private/test/resources/mesh_mask_orca1.nc4")
mesh = mesh.squeeze()
mesh

# %%
# mbathy returns the number of ocean cells.
# if 74, to have the bottom cell we must extract at k=73
# so we remove 1 to mbathy. When it is land, mbathy is then -1 and we 
# reset negative values to 0
mbathy = mesh['mbathy'] - 1
mbathy = mbathy.where(mbathy >= 0).fillna(0)
mbathy = mbathy.astype(int)
mbathy

# %%
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126', 'historical', 'pi']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/velocities', scenario.lower())
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    
    # Extract the list of forcing files (one file per month) for the given scenario
    filelist = fe.extract_scenario(scenario, 'grid_W')
    cpt = 0
    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data = data.rename({"time_counter": "time"})

        # Conversion from C to K
        temp = (data['wo'])
        temp.name = 'wo'
        temp.attrs['units'] = 'm/s'

        date, time = fe.compute_time(scenario, cpt) 

        years = np.array([d.year for d in date])
        months = np.array([d.month for d in date])
        days = np.array([d.day for d in date])
            
        temp.assign_coords({"time": ("time", time)}, inplace=True)
        temp['time'].attrs['units'] = fe.units
        temp.attrs['original_file'] = os.path.abspath(f)
        temp.attrs['script'] = 'extract_wo.py'

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_{temp.name}_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        temp.to_netcdf(foutname, unlimited_dims=['time'])
        cpt += 1

# %%
