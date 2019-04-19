#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get L2ExtDoms Example

# This is a simple Python example demonstrating how to list all L2ExtDoms in a fabric.  
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

L2ExtDom_class="node/class/l2extDomP.json"
L2ExtDom_url = base_url + L2ExtDom_class

L2ExtDoms = s.get(L2ExtDom_url, verify=False)
s_out = L2ExtDoms.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our L2ExtDoms now.
# Start with an empty list.
L2ExtDom_list = []
count = 0

L2ExtDom_out_list = s_out['imdata']

for L2ExtDom in L2ExtDom_out_list:
   # print(L2ExtDom)
    dn = L2ExtDom['l2extDomP']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    L2ExtDom_list.append(dn)
    count = count + 1

print("\nL2ExtDoms in the Fabric: ")
print('====================')
[print(l2) for l2 in L2ExtDom_list]
print('====================')
print('\nThere are', count, 'L2 External Domains')
