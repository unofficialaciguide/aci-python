#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get All Tenant Endpoint Groups and their Endpoints Example

# This is a simple Python example demonstrating how to get tenants, endpoint groups, and endpoints.  
# This is boiler plate code. Share and enjoy!


import requests
import json
import pandas as pd
import numpy as np
import os

os.system('cls' if os.name == 'nt' else 'clear')

# Use config.py to store your credentials.
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


# Construct the Request

requests.packages.urllib3.disable_warnings() 
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)


# Get all EPGs

c_string = "?rsp-subtree=children"
epg_path="node/class/fvAEPg.json"
epg_url = base_url + epg_path + c_string

epg_response = s.get(epg_url, verify=False)
epg_json = epg_response.json()

# Uncomment if you want to see the raw output.
#print(json.dumps(epg_json, indent=4, sort_keys=True))

# Read the imdata key, and assign the value (a list of objects) to epg_objects_list.
epg_objects_list = epg_json['imdata']

#Set up some empty lists to capture the data we need. 
tenant_list = []
ap_list = []
epg_list = []
endpoint_list = []
ip_list = []
mac_list = []
encap_list = []


# Now we have a list of objects, let's iterate over each object and do the following:
#  - Grab the Distriguished name (DN)
#  - Split the DN string into a list using the forward slash as a separator
#  - Ignore uni, which is element 0.
#  - Then, grab the tenant from element 1
#  - the Application profile (AP) is element 2
#  - Skip to the last element (-1) to grab the endpoint group.
#  - In the aci-get-global-endpoints example, we describe why we read from the end.
#  - But basically, the last element is always endpoint, but the fourth (3) element is not always
#    the last element.

for epg_object in epg_objects_list:
    #print(object)
    dn = epg_object['fvAEPg']['attributes']['dn']
    split_dn = dn.split("/")
    tenant = split_dn[1]
    ap = split_dn[2]
    epg = split_dn[-1]
    
    # Get the child objects, which are values under the key "children".
    # We also set null value for endpoint, ip address, mac, and encapsulation.
    # Not every EPG will have and endpoint, so we want to keep a placeholder for later.
    
    children_list = epg_object['fvAEPg']['children']
    endpoint = None
    ip = None
    mac = None
    encap = None
    for child in children_list:
        #print(child.items())
        
        # For each child object, we look for anything in the class "fvCEp", which is an endpoint.
        # If it is, we overwrite the null values for endpoint name, ip, mac, and encapsulation.
        # If it isn't fvCEp, we skip it and just keep the placeholders above.
        # Uncomment the print statements if you want to see the data.

        if "fvCEp" in child:
            endpoint = child['fvCEp']['attributes']['name']
            ip = child['fvCEp']['attributes']['ip']
            mac = child['fvCEp']['attributes']['mac']
            encap = child['fvCEp']['attributes']['encap']
    #print(tenant, ap, epg, endpoint, ip, mac, encap)
    # Append our extracted values into each of the lists we created above.
    tenant_list.append(tenant)
    ap_list.append(ap)
    epg_list.append(epg)
    endpoint_list.append(endpoint)
    ip_list.append(ip)
    mac_list.append(mac)
    encap_list.append(encap)

# Zip the lists into a zip object. This effectively turns then into tuples of 
# tenant, application profile, EPG, endpoint, etc.
tn_ep_list = zip(tenant_list, ap_list, epg_list, endpoint_list, ip_list, mac_list, encap_list)

# Take the zip of tuples, convert to list, and stuff them into a Pandas dataframe.
# Also, convert "None" to numpy NaN, though Pandas deals with "None" just fine for groupby objects. 
df_input = list(tn_ep_list)
df = pd.DataFrame(df_input, columns=("Tenant","AP","EPG","Endpoint","IP","MAC Addy","Encap"))
df.fillna(value=pd.np.nan, inplace=True)

# Sort dataframe by Endpoints and then print the first 20 rows
#df.sort_values(by=['Endpoint'], ascending=False).head(20)

# Or sort dataframe by Endpoints and then print it all.
print(df.sort_values(by=['Endpoint'], ascending=False))

# Or you can just print the unsorted dataframe:
# print(df)


# Report total number of EPGs and EPs per Tenant using groupby object.
grouped_df = df.groupby(['Tenant']).agg({'EPG':'count','Endpoint':'count'})
print(grouped_df)

# We can drop all rows with any empty fields.
#df = df.dropna()
#print(df)
