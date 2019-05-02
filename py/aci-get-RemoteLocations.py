#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get RemoteLocations Example

# This is a simple Python example demonstrating how to list all RemoteLocations in a fabric.  
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

RemoteLocation_class="node/class/fileRemotePath.json"
RemoteLocation_url = base_url + RemoteLocation_class

RemoteLocations = s.get(RemoteLocation_url, verify=False)
s_out = RemoteLocations.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our RemoteLocations now.
# Start with an empty list.
RemoteLocation_list = []
count = 0

RemoteLocation_out_list = s_out['imdata']

for RemoteLocation in RemoteLocation_out_list:
   # print(RemoteLocation)
    dn = RemoteLocation['fileRemotePath']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    RemoteLocation_list.append(dn)
    count = count + 1

print("\nRemoteLocations in the Fabric: ")
print('====================')
[print(RemoteLocation) for RemoteLocation in RemoteLocation_list]
print('====================')
print('\nThere are', count, 'Remote Location Backup Policies')
