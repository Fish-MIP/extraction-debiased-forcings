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
mesh

# %%
mmol_to_mol = 1e-3

# %%
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/', scenario.lower())
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario}-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    filelist = glob(os.path.join(dirin, '*1m*ptrc_T*'))
    filelist.sort()
    filelist[:5]

    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data = data.rename({"time_counter": "time"})

        szoo = mmol_to_mol * data['ZOO']
        szoo.name = 'szoo'
        szoo.attrs['units'] = 'mol/m3'
        
        lzoo = mmol_to_mol * data['ZOO2']
        lzoo.name = 'lzoo'
        lzoo.attrs['units'] = 'mol/m3'
        
        zoo = szoo + lzoo
        zoo.name = 'zoo'
        zoo.attrs['units'] = 'mol/m3'
        
        date = zoo['time']
        date
        
        years = np.array([d.year for d in date.values])
        months = np.array([d.month for d in date.values])
        days = np.array([d.day for d in date.values])

        for var in [szoo, lzoo, zoo]: 
            print(var.name)
            foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_{var.name}_1deg_global_monthly_{years.min()}_{years.max()}.nc')
            foutname
            print(foutname)
            var.to_netcdf(foutname, unlimited_dims=['time'])

# %%
