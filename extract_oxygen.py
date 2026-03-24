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
depth = mesh['gdept_0'].squeeze()
depth.isel(z=mbathy).plot()

# %%
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/oxygen', scenario.lower())
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
    filelist[:5]
    
    for f in filelist:

        # Conversion of oxy from mmol/m3 to mol/m3
        oxy = 1e-3 * xr.open_dataset(f)['O2']
        oxy = oxy.rename({'time_counter': 'time'})
        oxy.name = 'o2'
        oxy.attrs['units'] = 'mol/m3'
        
        date = oxy['time']

        years = np.array([d.year for d in date.values])
        months = np.array([d.month for d in date.values])
        days = np.array([d.day for d in date.values])
    
        # creation of oxy_surf variable by taking the 
        # first ocean level
        oxy_surf = oxy.isel(olevel=0)
        oxy_surf.name = 'o2-surf'
        oxy_surf.attrs['units'] = oxy.attrs['units']
    
        # creation of oxy_bot variable by taking the 
        # last ocean level
        oxy_bot = oxy.isel(olevel=mbathy)
        oxy_bot.name = 'o2-bot'
        oxy_bot.attrs['units'] = oxy.attrs['units']
        
        dsout = xr.Dataset()
        dsout['o2'] = oxy
        dsout['o2-bot'] = oxy_bot
        dsout['o2-surf'] = oxy_surf
        
        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_o2_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        print(foutname)
        dsout.to_netcdf(foutname, unlimited_dims=['time'])

# %%
