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

# %%
weight = mesh['e3t_0'] * mesh['tmask']
weight = weight.fillna(0)

# %%
mmol_to_mol = 1e-3

# %%
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/phyto', scenario.lower())
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
        data = data.rename({"time_counter": "time", "olevel": 'z'})

        #-------- processing diatoms
        diat = mmol_to_mol * data['PHY2']
        diat.name = 'phydiat'
        diat.attrs['units'] = 'mol/m3'

        diat_vint = diat.weighted(weight).sum(dim='z')
        diat_vint.name = 'phydiat-vint'
        diat_vint.attrs['units'] = 'mol/m2'

        #--------- processing misc
        misc = mmol_to_mol * data['PHY']
        misc.name = 'phymisc'
        misc.attrs['units'] = 'mol/m3'

        misc_vint = misc.weighted(weight).sum(dim='z')
        misc_vint.name = 'phymisc-vint'
        misc_vint.attrs['units'] = 'mol/m2'

        #------- Sum of diat + misc
        phyc = diat + misc
        phyc.name = 'phyc'
        phyc.attrs['units'] = 'mol/m3'

        phyc_vint = phyc.weighted(weight).sum(dim='z')
        phyc_vint.name = 'phyc-vint'
        phyc_vint.attrs['units'] = 'mol/m2'
        
        date = phyc['time']
        date
        
        years = np.array([d.year for d in date.values])
        months = np.array([d.month for d in date.values])
        days = np.array([d.day for d in date.values])

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_phydiat_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['phydiat'] = phydiat
        dsout['phydiat-vint'] = phydiat_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_phymisc_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['phymisc'] = phymisc
        dsout['phymisc-vint'] = phymisc_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_phyc_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['phyc'] = phyc
        dsout['phyc-vint'] = phyc_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

# %%
