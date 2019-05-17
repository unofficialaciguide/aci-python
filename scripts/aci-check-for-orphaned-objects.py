## aci-check-associations
#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Checks associations of EPGs to BDs and BDs to VRFs for orphaned objects

# This is a simple Python example demonstrating how to check relationship associations
# This is boilerplate. Feel free to use in your own stuff.

import requests
import json
import pandas as pd
import os

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')


# Enter your controller hostname/IP and user credentials below.  
# Put your credentials in the config.py file.

from config import controller, username, password
base_url = "https://" + str(controller) + "/api/"
auth_bit = "aaaLogin.json"
auth_url = base_url + auth_bit
auth_data = {
  "aaaUser":{
    "attributes":{
      "name":username,
      "pwd":password
    }
  }
}

# ## Construct the Request
requests.packages.urllib3.disable_warnings() 
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)


## Grab the VRFs that our BDs are associated with
def GetVRFforBDs():
  BDtoVRF_class="node/class/fvRsCtx.json"
  BDtoVRF_url = base_url + BDtoVRF_class

  BDtoVRFs = s.get(BDtoVRF_url, verify=False)
  s_out = BDtoVRFs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our BDtoVRFs now.
  # Start with an empty list.
  VRFname_list = []
  NoVRF_count = 0

  BDstoVRFs_out_list = s_out['imdata']

  print('========================================================================')
  print("\n+*+*+ Checking BD to VRF association. +*+*+\n")

  for bdvrf in BDstoVRFs_out_list:
      fulldn = bdvrf['fvRsCtx']['attributes']['dn']
      bd = fulldn[4:-6]
      vrf = bdvrf['fvRsCtx']['attributes']['tnFvCtxName']
      VRFname_list.append(vrf)

      ## If there is no VRF association found, alert on it!
      if vrf == "":
        print(bd, "has no VRF associated with it.")
        NoBP_count = NoVRF_count + 1
      else:
        continue
  ## Print all good message if no issues are found    
  if NoVRF_count == 0:
    print("All BDs are associated with VRF.")
    print('========================================================================')
  else:
  	print('========================================================================')


## Grab the VRFs that our BDs are associated with
def GetBDforEPGs():
  EPGtoBD_class="node/class/fvRsBd.json"
  EPGtoBD_url = base_url + EPGtoBD_class

  EPGtoBDs = s.get(EPGtoBD_url, verify=False)
  s_out = EPGtoBDs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our EPGtoBDs now.
  # Start with an empty list.
  bdname_list = []
  epgtobd_count = 0

  epgstobd_out_list = s_out['imdata']

  print('========================================================================')
  print("\n+*+*+ Checking EPG to BD association. +*+*+\n")


  for epgbd in epgstobd_out_list:
      fulldn = epgbd['fvRsBd']['attributes']['dn']
      epg = fulldn[4:-5]
      bd = epgbd['fvRsBd']['attributes']['tnFvBDName']
      bdname_list.append(bd)
      
      ## If there is no BD association found, alert on it!
      if bd == "":
        print(epg, "has no BD associated with it.")
        epgtobd_count = epgtobd_count + 1
      else:
        continue
  ## Print all good message if no issues are found      
  if epgtobd_count == 0:
    print("All EPGs are associated with a BD.")
    print('========================================================================')
  else:
  	print('========================================================================')



GetVRFforBDs()
GetBDforEPGs()
