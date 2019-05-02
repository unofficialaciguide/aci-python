#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get IntProfs Example

# This is a simple Python example demonstrating how to list all IntProfs in a fabric.  
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

IntProf_class="node/class/infraAccPortP.json"
IntProf_url = base_url + IntProf_class

IntProfs = s.get(IntProf_url, verify=False)
s_out = IntProfs.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our IntProfs now.
# Start with an empty list.
IntProf_list = []
count = 0

IntProf_out_list = s_out['imdata']

for IntProf in IntProf_out_list:
   # print(IntProf)
    dn = IntProf['infraAccPortP']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    IntProf_list.append(dn)
    count = count + 1

print("\nIntProfs in the Fabric: ")
print('====================')
[print(Int) for Int in IntProf_list]
print('====================')
print('\nThere are', count, 'IntProfs')
