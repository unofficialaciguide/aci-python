#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Check all EPGss for their BD association

# This is a simple Python example demonstrating how to check for EPGss for their BD association 
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


## Grab the DNs for all EPGs in the Fabric
def GetEPG_DN():
  epg_class = "node/class/fvAEPg.json"
  epg_url = base_url + epg_class

  epgs = s.get(epg_url, verify=False)
  s_out = epgs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our EPGs now.
  # Start with an empty list.
  epg_list = []
  count = 0

  epg_out_list = s_out['imdata']

  for epg in epg_out_list:
      dn = epg['fvAEPg']['attributes']['dn']
      split_dn = dn.split("/")
      epg_list.append(dn)
      count = count + 1

  return epg_list

## Grab the EPG Names for all EPGs in the Fabric
def GetEPG_Name():
  epg_class="node/class/fvAEPg.json"
  epg_url = base_url + epg_class

  epgs = s.get(epg_url, verify=False)
  s_out = epgs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our bds now.
  # Start with an empty list.
  epgname_list = []
  count = 0

  epg_out_list = s_out['imdata']

  for epg in epg_out_list:
      dn = epg['fvAEPg']['attributes']['name']
      split_dn = dn.split("/")
      epgname_list.append(dn)
      count = count + 1

  return epgname_list

## Grab the BDs that our EPGs are associated with
def GetBDforEPG():
  BDforEPG_class="node/class/fvRsBd.json"
  BDforEPG_url = base_url + BDforEPG_class

  BDforEPGs = s.get(BDforEPG_url, verify=False)
  s_out = BDforEPGs.json()

  # Uncomment to print full output.
  #print(json.dumps(s_out, indent=4, sort_keys=True))

  # Let's get all our BDforEPGs now.
  # Start with an empty list.
  bdname_list = []
  count = 0

  bdsforepgs_out_list = s_out['imdata']

  print('========================================================================')

  for epgbd in bdsforepgs_out_list:
      bd = epgbd['fvRsBd']['attributes']['tnFvBDName']
      bdname_list.append(bd)
      count = count + 1

  return bdname_list

## Grab the various lists from each of the functions
BDforEPGnames = GetBDforEPG()
EPGnames = GetEPG_Name()
DNs = GetEPG_DN()

### Create a tuple of BD names, BD DNs, and BDforEPGnames associated with each BD
list_of_bds = zip(EPGnames, DNs, BDforEPGnames)
df_input = list(list_of_bds)
df = pd.DataFrame(df_input, columns=("BDs", "DNs", "BD for EPG"))

## Use the option.context to override the default suppression of rows and print all rows
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
## Sort the values based on BDforEPGnames
    ef = df.sort_values(by=['BD for EPG'], ascending=True)
## Removes the default numbered index column to the left
    print(ef.to_string(index=False))

print('========================================================================')




