# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python [conda env:nbarrier2]
#     language: python
#     name: conda-env-nbarrier2-py
# ---

from glob import glob
import os
import numpy as np
import cftime
from datetime import datetime

yearref = {}
yearref['pi'] = 1850
yearref['historical'] = 1850
for scen in ['ssp126', 'ssp370', 'ssp585', 'ssp245']:
    yearref[scen] = 2015

units = 'seconds since 1850-01-01 00:00:00'


def extract_scenario(scenario, suffix):
    if scenario == 'historical':
        return extract_historical(suffix)
    elif scenario == 'pi':
        return extract_pi(suffix)
    else:
        return extract_cc_scenario(scenario, suffix)


def extract_cc_scenario(scenario, suffix):
        
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', f'{scenario.upper()}-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    filelist = glob(os.path.join(dirin, f'*v2_20[2-9]*1m*{suffix}*nc'))
    filelist += glob(os.path.join(dirin, f'*v2_201[5-9]*1m*{suffix}*nc'))
    filelist.sort()

    return filelist


def extract_historical(suffix):

    dirin = os.path.join('/home/datawork-marbec-pmod/Matt/ORCA1_PISCES_BLK', 'PI-bJRA-v2-c5/', 'Output')
    dirin
    
    filelist1 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist1.sort()
    filelist1 = filelist1[-43:]
    len(filelist1)
    
    dirin = os.path.join('/home/datawork-marbec-pmod/Matt/ORCA1_PISCES_BLK', 'PD-JRA-v2-c6', 'Output')

    filelist2 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist2.sort()
    filelist2
    
    dirin = os.path.join('/home/datawork-marbec-scenlab/NEMO/FORCING-FISHMIP/', 'SSP245-fIPSL-cOBSN-v2', 'Output')
    dirin
    
    filelist3 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist3.sort()
    
    years = np.arange(1958, 2015)
    years
    filelist3 = filelist3[:len(years)]
    filelist3
    
    filelist = filelist1 + filelist2 + filelist3
    filelist

    return filelist


def extract_pi(suffix):
    suffix = 'ptrc_T'

    dirin = os.path.join('/home/datawork-marbec-pmod/Matt/ORCA1_PISCES_BLK', 'PI-bJRA-v2-c5/', 'Output')
    dirin
    
    filelist1 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist1.sort()
    filelist1 = filelist1[-43:]
    len(filelist1)
    
    dirin = os.path.join('/home/datawork-marbec-pmod/Matt/ORCA1_PISCES_BLK', 'PD-JRA-v2-c6', 'Output')

    filelist2 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist2.sort()
    filelist2
    
    dirin = os.path.join('/home/datawork-marbec-pmod/Matt/ORCA1_PISCES_FLX/PI-JRA-v2/Output')
    dirin
    
    filelist3 = glob(os.path.join(dirin, f'*1m*{suffix}*nc'))
    filelist3.sort()
    
    years = np.arange(1958, 2015)
    years
    filelist3
    
    filelist = filelist1 + filelist2 + filelist3
    filelist

    return filelist


def compute_time(scenario, index):
    scenario = scenario.lower()
    year = yearref[scenario] + index
    dates = [datetime(year, m, 15) for m in range(1, 13)]
    dates
    time = cftime.date2num(dates, units)
    time
    return dates, time


if __name__ == '__main__':

    yearstot = np.arange(1850, 2088)
    yearstot, len(yearstot)
    
    file_pi = extract_pi('grid_T')
    file_pi, len(file_pi)
    
    file_hist = extract_scenario('historical', 'grid_T')
    file_hist, len(file_hist)
    
    file_ssp = extract_scenario('ssp126', 'grid_T')
    file_ssp, len(file_ssp)
    
    len(file_ssp) + len(file_hist)

    for i in range(len(file_ssp)):
        dates, time = compute_time('ssp126', i)
        print(file_ssp[i], dates[0], dates[-1])


