#!/usr/bin/env python
# coding: utf-8

# # Ops Check
# ## A Python script to gather data on the ACI fabric's operational state.

# Overview:
# The script will carry out API calls necessary to gather important info-at-a-glance, then print to console/display.
# 
# Flow: 
# 1. Authenticate with config.py or interactively.
# 2. Gather:
#    - Fabric Health Score
#    - Global Endpoints
#    - Tenant Endpoints by EPG
# 3. Print report from the above information.

# In[62]:


# Import needed modules
import requests
import json
import pandas as pd
import os
import sys



# In[25]:


# Grab credentials from config.py file in same directory.
# TO DO: Test variables, and prompt for interactive entry if empty.
from config import controller, username, password


# In[26]:


# Set some variables to construct our login URLs
base_url = "https://" + str(controller) + "/api/"
auth_bit = "aaaLogin.json"

auth_url = base_url + auth_bit
#auth_url


# In[27]:


# JSON data constructed from user/pass above.
auth_data = {
  "aaaUser":{
    "attributes":{
      "name":username,
      "pwd":password
    }
  }
}


# In[28]:


# Comment or delete this line if you want to see SSL certificate warnings (eg, self-signed, untrusted, etc)
requests.packages.urllib3.disable_warnings() 


# In[29]:


# Initiate a session with the APIC
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)


# In[30]:


# Set up our class/object URI variables
# Global Endpoints Class
global_ep="node/class/fvCEp.json"

# Tenant Endpoints by EPG
tenant_endpoints = "node/class/fvAEPg.json"
c_string = "?rsp-subtree=children"
tenant_endpoints_url = base_url + tenant_endpoints + c_string


# Health Score / Summary Classes
health = "node/mo/topology/HDfabricOverallHealth5min-0.json"
info = "node/mo/info.json"
fault = "node/class/faultSummary.json"

global_ep_url = base_url + global_ep
health_url = base_url + health
info_url = base_url + info
fault_url = base_url + fault


# In[31]:


def get_endpoints(url):
    s_response = s.get(url, verify=False)
    s_global_ep = s_response.json()
    tenant_list = []
    epg_list = []
    ep_list = []
    ip_list = []
    mac_list = []
    encap_list = []

    object_list = s_global_ep['imdata']
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
    list_of_global_ep = zip(tenant_list, epg_list, ep_list, ip_list, mac_list, encap_list)
    df_input = list(list_of_global_ep)
    df = pd.DataFrame(df_input, columns=("Tenant","EPG or VRF/L3out","Endpoint","IP","MAC Addy","Encap"))
    ep = df[['Tenant','Endpoint']]
    grouped_df = ep.groupby(['Tenant']).count()
    return grouped_df, df


# In[57]:


# Get Global Endpoints 
global_endpoints_summary, global_endpoints = get_endpoints(global_ep_url)


# In[33]:


def get_tenant_endpoints(url):
    epg_response = s.get(tenant_endpoints_url, verify=False)
    epg_json = epg_response.json()
    epg_objects_list = epg_json['imdata']
    tenant_list = []
    ap_list = []
    epg_list = []
    endpoint_list = []
    ip_list = []
    mac_list = []
    encap_list = []
    for epg_object in epg_objects_list:
        dn = epg_object['fvAEPg']['attributes']['dn']
        split_dn = dn.split("/")
        tenant = split_dn[1]
        ap = split_dn[2]
        epg = split_dn[-1]
        children_list = epg_object['fvAEPg']['children']
        endpoint = None
        ip = None
        mac = None
        encap = None
        for child in children_list:
            if "fvCEp" in child:
                endpoint = child['fvCEp']['attributes']['name']
                ip = child['fvCEp']['attributes']['ip']
                mac = child['fvCEp']['attributes']['mac']
                encap = child['fvCEp']['attributes']['encap']
        tenant_list.append(tenant)
        ap_list.append(ap)
        epg_list.append(epg)
        endpoint_list.append(endpoint)
        ip_list.append(ip)
        mac_list.append(mac)
        encap_list.append(encap)
    tn_ep_list = zip(tenant_list, ap_list, epg_list, endpoint_list, ip_list, mac_list, encap_list)
    df_input = list(tn_ep_list)
    df = pd.DataFrame(df_input, columns=("Tenant","AP","EPG","Endpoint","IP","MAC Addy","Encap"))
    df.fillna(value=pd.np.nan, inplace=True)
    sorted_df = df.sort_values(by=['Endpoint'], ascending=False)
    grouped_df = df.groupby(['Tenant']).agg({'EPG':'count','Endpoint':'count'})
    return grouped_df, sorted_df


# In[34]:


# Get Endpoints summary by tenant, thenget list of all tenant endpoints, 
# including EPGs with no endpoints. 
tenant_endpoints_summary, tenant_endpoints = get_tenant_endpoints(tenant_endpoints_url)


# In[39]:


# Returns Five Minute Health Score, Summary of Faults, and Table of Faults
def get_healthcheck(health_url, fault_url):
    # get ACI Fabric Health Score, Five Minute Average
    s_response = s.get(health_url, verify=False)
    s_health_data = s_response.json()
    health_score = s_health_data['imdata'][0]
    five_min_avg = health_score['fabricOverallHealthHist5min']['attributes']['healthAvg']
    # Get ACI faults
    s_response = s.get(fault_url, verify=False)
    s_fault = s_response.json()
    descr_list = []
    severity_list = []
    code_list = []
    type_list = []
    dn_list = []
    cause_list = []
    object_list = s_fault['imdata']
    for object in object_list:
        #print(object)
        dn_list.append(object['faultSummary']['attributes']['dn'])
        descr_list.append(object['faultSummary']['attributes']['descr'])
        severity_list.append(object['faultSummary']['attributes']['severity'])
        code_list.append(object['faultSummary']['attributes']['code'])
        type_list.append(object['faultSummary']['attributes']['type'])
        cause_list.append(object['faultSummary']['attributes']['cause'])
    list_of_objects = zip(code_list,severity_list,descr_list,cause_list,type_list,dn_list)
    df_input = list(list_of_objects)
    df = pd.DataFrame(df_input, columns=("Code","Severity","Description","Cause","Type","DN"))
    summary_df = df.groupby(['Severity', 'Type']).agg({'Cause':'count'})
    return five_min_avg, summary_df, df


# In[40]:


score, fault_summary, fault_list = get_healthcheck(health_url, fault_url)


# In[59]:


# Summary Output
print("ACI Operations Summary")
print("==================================================")
print(" ")
print("Health Score: " + str(score))
print(" ")
print("===== Faults =====")
print(fault_summary)
print(" ")
print("===== Global Endpoints =====")
print(global_endpoints_summary)
print(" ")
print("===== Tenant Endpoints =====")
print(tenant_endpoints_summary)


# In[53]:


i = input("[C]ontinue with Full Report, or [Q]uit?")
if i == "q" or i == "Q":
    sys.exit()


# In[60]:


# Full Output
print("ACI Operations Report")
print("==================================================")
print(" ")
print("Health Score: " + str(score))
print(" ")
print("===== Faults =====")
print(fault_list)
print(" ")
print("===== Global Endpoints =====")
print(global_endpoints)
print(" ")
print("===== Tenant Endpoints =====")
print(tenant_endpoints)


# 
