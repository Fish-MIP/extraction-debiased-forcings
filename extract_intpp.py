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
for scenario in ['SSP126', 'SSP245',  'SSP370',  'SSP585', 'historical', 'pi']:

    print("-------------------------- Processing scenario ", scenario)

    # Output folder
    dirout = os.path.join('/home1/scratch/nbarrier/fishmip-osp/', scenario, 'intpp')
    dirout
    
    # Create output folder if not exists
    if not os.path.exists(dirout):
        os.makedirs(dirout)
    
    # Extract the list of forcing files (one file per month) for the given scenario
    filelist = fe.extract_scenario(scenario, 'diad_T')
        
    cpt = 0
    
    for f in filelist:

        variable = []
        print("+++++ Processing file ", f)

        try:
            data = xr.open_dataset(f)
        except:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ error with ", f)
            continue
        
        data = data.rename({"time_counter": "time"})

        if 'INTPPPHY' in data.variables:
            intppmisc = data['INTPPPHY']
            intppmisc.name = 'intppmisc'
            variable.append(intppmisc)

        if 'INTPPPHY2' in data.variables:
            intppdiat = data['INTPPPHY2']
            intppdiat.name = 'intppdiat'
            variable.append(intppdiat)

        if 'INTPP' in data.variables:
            intpp = data['INTPP']
            intpp.name = 'intpp'    
            variable.append(intpp)
      
        date, time = fe.compute_time(scenario, cpt) 
                
        years = np.array([d.year for d in date])
        months = np.array([d.month for d in date])
        days = np.array([d.day for d in date])

        for var in variable:

            print(var.name)

            var = var.assign_coords({"time": ("time", time)})
            var['time'].attrs['units'] = fe.units
            var.attrs['original_file'] = os.path.abspath(f)
            var.attrs['script'] = 'extract_intpp.py'
            
            foutname = os.path.join(dirout, f'ipsl_{scenario.lower()}_{var.name}_1deg_global_monthly_{years.min()}_{years.max()}.nc')
            foutname
            print(foutname)
            var.to_netcdf(foutname, unlimited_dims=['time'])

        cpt += 1

# %%
