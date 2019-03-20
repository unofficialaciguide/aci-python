#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get Tenants Example

# This is a simple Python example demonstrating how to list all tenants in a fabric.  
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

tenant_class="node/class/fvTenant.json"
tenant_url = base_url + tenant_class

tenants = s.get(tenant_url, verify=False)
s_out = tenants.json()

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our tenants now.
# Start with an empty list.
tenant_list = []

tn_out_list = s_out['imdata']
for tenant in tn_out_list:
    # print(tenant)
    dn = tenant['fvTenant']['attributes']['dn']
    split_dn = dn.split("/")
    tenant_list.append(split_dn[1])
    
print("Tenants: ")
[print(t) for t in tenant_list]

