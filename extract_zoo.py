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
mesh

# %%
mmol_to_mol = 1e-3

# %%
for scenario in ['SSP245',  'SSP370',  'SSP585', 'SSP126', 'historical', 'pi']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/', scenario, 'zoo')
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario}-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    # Extract the list of forcing files (one file per month) for the given scenario
    filelist = fe.extract_scenario(scenario, 'ptrc_T')
    cpt = 0

    for f in filelist:

        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        data = data.rename({"time_counter": "time", "olevel": 'z'})
        date, time = fe.compute_time(scenario, cpt) 

        data.assign_coords({"time": ("time", time)})
        data['time'].attrs['units'] = fe.units
        data.attrs['original_file'] = os.path.abspath(f)
        data.attrs['script'] = 'extract_zoo.py'

        #-------- processing diatoms
        zmicro = mmol_to_mol * data['ZOO']
        zmicro.name = 'zmicro'
        zmicro.attrs['units'] = 'mol/m3'

        zmicro_vint = zmicro.weighted(weight).sum(dim='z')
        zmicro_vint.name = 'zmicro-vint'
        zmicro_vint.attrs['units'] = 'mol/m2'

        #--------- processing misc
        zmeso = mmol_to_mol * data['ZOO2']
        zmeso.name = 'zmeso'
        zmeso.attrs['units'] = 'mol/m3'

        zmeso_vint = zmeso.weighted(weight).sum(dim='z')
        zmeso_vint.name = 'zmeso-vint'
        zmeso_vint.attrs['units'] = 'mol/m2'

        #------- Sum of diat + misc
        zooc = zmicro + zmeso
        zooc.name = 'zooc'
        zooc.attrs['units'] = 'mol/m3'

        zooc_vint = zooc.weighted(weight).sum(dim='z')
        zooc_vint.name = 'zooc-vint'
        zooc_vint.attrs['units'] = 'mol/m2'
        
        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_zmicro_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['zmicro'] = zmicro
        dsout['zmicro-vint'] = zmicro_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_zmeso_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['zmeso'] = zmeso
        dsout['zmeso-vint'] = zmeso_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

        foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_zooc_1deg_global_monthly_{years.min()}_{years.max()}.nc')
        foutname
        dsout = xr.Dataset()
        dsout['zooc'] = zooc
        dsout['zooc-vint'] = zooc_vint
        dsout.to_netcdf(foutname, unlimited_dims=['time'])   

        cpt += 1
