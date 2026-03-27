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
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126', 'historical', 'pi']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/', scenario, 'mld')
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario}-fIPSL-cOBSN-v2', 'Output')
    dirin

    # Extract the list of forcing files (one file per month) for the given scenario
    filelist = fe.extract_scenario(scenario, 'grid_T')
    
    cpt = 0
    
    for f in filelist:

        # Conversion of mld from mmol/m3 to mol/m3
        try:
            mld = xr.open_dataset(f)['mldr10_1max']
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        mld = mld.rename({'time_counter': 'time'})
        mld.name = 'mlotstmax'
        mld.attrs['units'] = 'm'

        date, time = fe.compute_time(scenario, cpt) 

        mld = mld.assign_coords({"time": ("time", time)})
        mld['time'].attrs['units'] = fe.units
        mld.attrs['original_file'] = os.path.abspath(f)
        mld.attrs['script'] = 'extract_mldmax.py'

        years = np.array([d.year for d in date])
        months = np.array([d.month for d in date])
        days = np.array([d.day for d in date])
    
        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_{mld.name}_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        print(foutname)
        mld.to_netcdf(foutname, unlimited_dims=['time'])

        cpt += 1

# %%
