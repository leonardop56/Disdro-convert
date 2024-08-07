# adapted from original script to handle data from different stations
# so that the Ny Alesund data can be processed with the same scripts
# RG 18.8.2017
#
#adapted to SMHI data (from Norunda) in this case

#!/usr/bin/python3
import numpy as np
from parsivel_log_nc_convert_samdconform import writeNC,writeNC_old
import matplotlib.mlab
matplotlib.use('Agg')
import glob
import sys
import os
import datetime


sites = sys.argv[1:]
#sites='nor'

print(sites)

logpath = {
#  'jue':'/data/hatpro/jue/data/parsivel/*/',
#  'nya':'/data/obs/site/nya/parsivel/l1/*/*/*/',
  'nor':'/home/a002304/sshfs/Bi/disdrometer/log/',
}

ncpath = {
#  'jue':'/data/hatpro/jue/data/parsivel/netcdf/',
#  'nya':'/data/obs/site/nya/parsivel/l1/',
  'nor':'/home/a002304/sshfs/Bi/disdrometer/netcdf/',
}


noDaysAgo = {
  'nor':150,
}


for site in sites:

  #find log-files:
  files = sorted(glob.glob(logpath[site]+'parsivel*.log'))

  files = sorted(files)[::-1][:noDaysAgo[site]]   # go back the number of days specified

  for ff,flog in enumerate(files):

    #get date of file:
    datestring = flog.split("/")[-1][-12:-4]
    #print(datestring)
    
    # get string to describe insrument
    descrstring = flog.split("/")[-1][0:8]
    #print(descrstring)

    # make output file directory, if needed
    #if site == 'jue':
    if site == 'nor':
        if not os.path.isdir(ncpath[site]+datestring[2:6]):
            #print(ncpath[site]+datestring[2:6])
            os.mkdir(ncpath[site]+datestring[2:6])
    
    #build outputfilenames
    #if   site == 'jue': 
    if site == 'nor':
        ncout = ncpath[site]+datestring[2:6]+'/'+descrstring+datestring+'.nc'
    #elif site == 'nya': 
    #  ncout = ncpath[site] + datestring[0:4] + '/'+ datestring[4:6] + '/' + datestring[6:8] + '/parsivel_nya_' +  datestring+'.nc'
 
    if site == 'nor':
    ##check if .nc-file already exists, if so: continue with next date.
    ## this note done for nya, since files transfered hourly and should be updated
        if os.path.isfile(ncout):
            print("skipped .log: {}".format(datestring))
            continue
  
    #write parsivel .nc-file
    print('writing .nc: {}'.format(ncout))
  
    if int(datestring) < 20150417:    #measurements earlier than this don't have array on N,v
        writeNC_old(flog,ncout)
    else:
        writeNC(flog,ncout,site)
  

