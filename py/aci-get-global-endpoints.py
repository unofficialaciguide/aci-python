#!/usr/bin/env python

# # Unofficial ACI Guide
# ## Python 3 Get Global Endpoints Example

# This is a simple Python example demonstrating how to obtain Global Endpoints list.
# In the GUI, this is done through Fabric -> Inventory -> Topology -> Global End-Points.

# This is boilerplate code. Feel free to use in your own scripts/programs.

import requests
import json
import pandas as pd
import os

# We'll read the auth info from config.py in the same directory. 
# Just edit that file to include your controller IP/hostname, username, and password.

from config import controller, username, password

os.system('cls' if os.name == 'nt' else 'clear')

# Set some variables to construct our login URLs

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



# Comment this out to enable certificate warnings.
requests.packages.urllib3.disable_warnings() 

# Change to "verify=True" or just remove verify=False if you use an internal CA or a valid chain cert.
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)


# https://apic-ip-address/api/node/class/fvCEp.json
# What's the endpoints URL?
epo="node/class/fvCEp.json"
ep_url = base_url + epo

s_response = s.get(ep_url, verify=False)
s_ep = s_response.json()

# Set up some empty lists for tenant, endpoint group, endpoint, IP address, MAC address, and encapsulation. 
tenant_list = []
epg_list = []
ep_list = []
ip_list = []
mac_list = []
encap_list = []

object_list = s_ep['imdata']


for object in object_list:
    #print(object)
    dn = object['fvCEp']['attributes']['dn']
    split_dn = dn.split("/")
    tenant_list.append(split_dn[1])
    epg_list.append(split_dn[-2])
    ep_list.append(split_dn[-1])
    ip_list.append(object['fvCEp']['attributes']['ip'])
    mac_list.append(object['fvCEp']['attributes']['mac'])
    encap_list.append(object['fvCEp']['attributes']['encap'])


# Let's take our list and zip them up.
# Convert to list of tuples and stuff it into a Pandas dataframe...
list_of_ep = zip(tenant_list, epg_list, ep_list, ip_list, mac_list, encap_list)
df_input = list(list_of_ep)
df = pd.DataFrame(df_input, columns=("Tenant","EPG or VRF/L3out","Endpoint","IP","MAC Addy","Encap"))

print(" ")

# Use this to print in a standalone script.
print(df)
print(" ")

# Let's extract just the tenants and endpoints, create a groupby object, 
# then count the number of endpoints per tenant.
ep = df[['Tenant','Endpoint']]
grouped_df = ep.groupby(['Tenant']).count()
print(grouped_df)
