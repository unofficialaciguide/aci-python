#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Check all BDs for VRF association

# This is a simple Python example demonstrating how to check for BDs with VRF association 
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


## Grab the DNs for all BDs in the Fabric
def GetBD_DN():
  bd_class="node/class/fvBD.json"
  bd_url = base_url + bd_class

  bds = s.get(bd_url, verify=False)
  s_out = bds.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our bds now.
  # Start with an empty list.
  bd_list = []
  count = 0

  bd_out_list = s_out['imdata']

  for bd in bd_out_list:
      dn = bd['fvBD']['attributes']['dn']
      split_dn = dn.split("/")
      bd_list.append(dn)
      count = count + 1

  return bd_list

## Grab the BD Names for all BDs in the Fabric
def GetBD_Name():
  bd_class="node/class/fvBD.json"
  bd_url = base_url + bd_class

  bds = s.get(bd_url, verify=False)
  s_out = bds.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our bds now.
  # Start with an empty list.
  bdname_list = []
  count = 0

  bd_out_list = s_out['imdata']

  for bd in bd_out_list:
      dn = bd['fvBD']['attributes']['name']
      split_dn = dn.split("/")
      bdname_list.append(dn)
      count = count + 1

  return bdname_list

## Grab the VRFs that our BDs are associated with
def GetVRFforBDs():
  BdToVrf_class="node/class/fvRsCtx.json"
  BdToVrf_url = base_url + BdToVrf_class

  BdToVrfs = s.get(BdToVrf_url, verify=False)
  s_out = BdToVrfs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our BdToVrfs now.
  # Start with an empty list.
  ctxname_list = []
  count = 0

  bdstovrf_out_list = s_out['imdata']

  print('========================================================================')

  for bdvrf in bdstovrf_out_list:
      vrf = bdvrf['fvRsCtx']['attributes']['tnFvCtxName']
      ctxname_list.append(vrf)
      count = count + 1

  return ctxname_list

## Grab the various lists from each of the functions
vrfs = GetVRFforBDs()
BDnames = GetBD_Name()
DNs = GetBD_DN()

### Create a tuple of BD names, BD DNs, and VRFs associated with each BD
list_of_bds = zip(BDnames, DNs, vrfs)
df_input = list(list_of_bds)
df = pd.DataFrame(df_input, columns=("BD Name", "DN", "VRF"))

## Use the option.context to override the default suppression of rows and print all rows
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
## Sort the values based on VRFs
    ef = df.sort_values(by=['VRF'], ascending=True)
## Removes the default numbered index column to the left
    print(ef.to_string(index=False))

print('========================================================================')




