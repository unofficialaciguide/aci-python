#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get L3ExtDoms Example

# This is a simple Python example demonstrating how to list all L3ExtDoms in a fabric.  
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

L3ExtDom_class="node/class/l3extDomP.json"
L3ExtDom_url = base_url + L3ExtDom_class

L3ExtDoms = s.get(L3ExtDom_url, verify=False)
s_out = L3ExtDoms.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our L3ExtDoms now.
# Start with an empty list.
L3ExtDom_list = []
count = 0

L3ExtDom_out_list = s_out['imdata']

for L3ExtDom in L3ExtDom_out_list:
   # print(L3ExtDom)
    dn = L3ExtDom['l3extDomP']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    L3ExtDom_list.append(dn)
    count = count + 1

print("\nL3ExtDoms in the Fabric: ")
print('====================')
[print(l3) for l3 in L3ExtDom_list]
print('====================')
print('\nThere are', count, 'L3 External Domains')
