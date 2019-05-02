#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get PortChanPGs Example

# This is a simple Python example demonstrating how to list all PortChanPGs in a fabric.  
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

PortChanPG_class="node/class/infraAccBndlGrp.json"
PortChanPG_url = base_url + PortChanPG_class

PortChanPGs = s.get(PortChanPG_url, verify=False)
s_out = PortChanPGs.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our PortChanPGs now.
# Start with an empty list.
PortChanPG_list = []
count = 0

PortChanPG_out_list = s_out['imdata']

for PortChanPG in PortChanPG_out_list:
   # print(PortChanPG)
    dn = PortChanPG['infraAccBndlGrp']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    PortChanPG_list.append(dn)
    count = count + 1

print("\nPortChanPGs in the Fabric: ")
print('====================')
[print(PortChanPG) for PortChanPG in PortChanPG_list]
print('====================')
print('\nThere are', count, 'Port Channel Policy Groups')
