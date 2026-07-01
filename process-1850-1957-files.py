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
from glob import glob
import os
import shutil
import re

# %% [markdown]
# ## Move bad files into a scratch folder

# %% [markdown]
# List all the files

# %%
dirin = '/home1/scratch/nbarrier/fishmip-osp/to_send/salinity/'
variable = 'so'

# %%
filelist = glob(os.path.join(dirin, f'*_{variable}_*nc'))
filelist.sort()
filelist[:5]

# %% [markdown]
# Create a scratch folder

# %%
scratch_folder = os.path.join(dirin, 'scratch')
if not os.path.dir(scratch_folder):
    os.mkdir(scratch_folder)

# %% [markdown]
# Move all the files that match the patterm for the period 1850-1957 to the scratch folder

# %%
# pattern that matches the files with periods from 1850 to 1957. 
# If pattern matches, then move them to scratch
pattern = '.*_18.*|.*195[0-7].*|.*19[0-4].*'
regex = re.compile(pattern)
discards = []
for f in filelist:
    if regex.match(f):
        shutil.move(f, scratch_folder)

# %% [markdown]
# ## Reconstruct now the new files

# %% [markdown]
# Extract the PI files, which are the target files

# %%
filelist = glob(os.path.join(dirin, f'*_pi_{variable}_*nc'))
filelist.sort()
filelist[:5], filelist[-5:]

# %% [markdown]
# Create a dictionnary that matches year (from 1958 to 2087) to the related file

# %%
regex = re.compile('.*_([0-9][0-9][0-9][0-9])_.*')
dict_files = {}
for f in filelist:
    if regex.match(f):
        year = int(regex.match(f).groups()[0])
        dict_files[year] = f
for f in list(dict_files.items())[:2]:
    print(f)
for f in list(dict_files.items())[-2:]:
    print(f)

# %% [markdown]
# Defines the years to be reconstructed (1850 - 1957)

# %%
reconstructed_period = list(range(1850, 1958))

# %% [markdown]
# Reconstuct the matching between the reconstructed years (1850 - 1957) with the ones for which we have data (1958-2087).
#
# We assume that year 1957 corresponds to 2087.

# %%
matching_years = []
matching_years
yearref = 2087
cpt = -1
for i in range(len(reconstructed_period)):
    matching_years.append(yearref)
    yearref -= 1
    cpt -= 1
matching_years.reverse()
matching_years[:5], matching_years[-5:]
matching_years

# %%
for p in range(len(reconstructed_period)):
    year_source = matching_years[p]
    year_dest = reconstructed_period[p]
    if year_source not in dict_files:
        print("Error with PI file for year ", year_source)
    else:
        file_source = dict_files[year_source]
        file_dest = file_source.replace(str(year_source), str(year_dest))
        print(file_dest, file_source)
        if(not os.path.isfile(file_dest)):
            os.symlink(file_source, file_dest)
        hist_file_dest = file_dest.replace('_pi_', '_historical_')
        if(not os.path.isfile(hist_file_dest)):
            os.symlink(file_source, hist_file_dest)

# %%
