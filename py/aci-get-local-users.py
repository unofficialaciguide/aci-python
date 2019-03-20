#!/usr/bin/env python
# coding: utf-8

# # Unofficial ACI Guide
# 
# ## Python 3 - Get APIC Users Example

# List local users on the APIC controller.  
# No Cisco ACI-related toolkits, SDKs, or bindings were harmed in the creation of this example.

# In[ ]:


import requests
import json
import pandas as pd
import os
import getpass

os.system('cls' if os.name == 'nt' else 'clear')

# Enter your controller hostname/IP and user credentials in config.py.  
# If there is no config.py, we prompt for entries.  
# The getpass() function allows for shadow entries.  

if os.path.isfile('./config.py'):
    from config import controller, username, password

try:
    controller
except NameError:
    controller = input("Controller Hostname/IP: ")

try:
    username
except NameError:
    username = input("APIC Username: ")
    
try: 
    password 
except NameError:
    password = getpass.getpass("APIC Password: ")


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


# We use verify=False to allow self-signed certs. 
# The disable_warnings() line prevents warning messages.
requests.packages.urllib3.disable_warnings() 
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)


# Set up the URLs to query.
qstring = "?rsp-subtree=children"
# Construct the user post URL
user_class="node/mo/uni/userext.json"
user_url = base_url + user_class + qstring

# Initiate the request and get JSON.
users = s.get(user_url, verify=False)
users = users.json()

# Print JSON output as pretty as a dandelion
#print(json.dumps(users, indent=4, sort_keys=True))


#Grab the DN
dn = users['imdata'][0]['aaaUserEp']['attributes']['dn']

# Set up empty lists
name_list = []
firstname_list = []
lastname_list = []
status_list = []
phone_list = []
rn_list = []


# Grab the user objects.
users_list = users['imdata'][0]['aaaUserEp']['children']

# Iterate over each object and extract the values we want.
for user in users_list:
    if "aaaUser" in user: 
        #print(user)
        rn = user['aaaUser']['attributes']['rn']
        name = user['aaaUser']['attributes']['name']  
        firstname = user['aaaUser']['attributes']['firstName']
        lastname = user['aaaUser']['attributes']['lastName']
        status = user['aaaUser']['attributes']['accountStatus']
        phone = user['aaaUser']['attributes']['phone']
        name_list.append(name)
        rn_list.append(rn)
        firstname_list.append(firstname)
        lastname_list.append(lastname)
        phone_list.append(phone)
        status_list.append(status)

# Zip it up, buttercup!
zlist = zip(status_list, name_list, firstname_list, lastname_list, phone_list, rn_list)

# Convert to pandas dataframe
df_input = list(zlist)
df = pd.DataFrame(df_input, columns=("Status","User Name","First Name","Last Name","Phone","RN"))

print(df)


