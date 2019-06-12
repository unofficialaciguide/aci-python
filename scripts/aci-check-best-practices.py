## aci-check-associations
#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Check all Associations

# This is a simple Python example demonstrating how to check relationship associations
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

## Check to see if BPs are enabled

### Enforce Subnet Check should be set to enforceSubnetCheck:yes
### Disable Remote EP Learn should be set to unicastXrEpLearnDisable:yes
### Domain Validation should be set to domainValidation:yes
### System > System Settings > Fabric Wide Setting
FabWide_class="node/class/infraSetPol.json"
FabWide_url = base_url + FabWide_class

FabWide = s.get(FabWide_url, verify=False)
FabWide_out = FabWide.json()

NoBP_count = 0

### Fabric Wide Variables
FabWideList = FabWide_out['imdata']
IsEnforceActivated = FabWideList[0]['infraSetPol']['attributes']['enforceSubnetCheck']
IsDisXRLearnActivated = FabWideList[0]['infraSetPol']['attributes']['unicastXrEpLearnDisable']
IsDomValActivated = FabWideList[0]['infraSetPol']['attributes']['domainValidation']

### Port Tracking Settings
### Port Tracking should be set to adminSt:on
### System > System Settings > Port Tracking
PortTrack_class="node/class/infraPortTrackPol.json"
PortTrack_url = base_url + PortTrack_class

PortTrack = s.get(PortTrack_url, verify=False)
PortTrack_out = PortTrack.json()

### Port Tracking Variable
PortTrackList = PortTrack_out['imdata']
PortTrackAdminState = PortTrackList[0]['infraPortTrackPol']['attributes']['adminSt']

### EP Loop Protection Settings
### EP Loop Detection should be set to adminSt:enabled
### EP Loop Detection Action settings should be set to action:"" << No actions should be set
### System > System Settings > Endpoint Controls > EP Loop Detection
EPLoop_class="node/class/epLoopProtectP.json"
EPLoop_url = base_url + EPLoop_class

EPLoop = s.get(EPLoop_url, verify=False)
EPLoop_out = EPLoop.json()

### EP Loop Detection Variable
EPLoopList = EPLoop_out['imdata']
EPLoopAdminState = EPLoopList[0]['epLoopProtectP']['attributes']['adminSt']
EPLoopAction = EPLoopList[0]['epLoopProtectP']['attributes']['action']

### Rogue EP Protection Settings
### Rogue EP Status should be adminSt:enabled
### System > System Settings > Endpoint Controls > Rogue EP Control
Rogue_class="node/class/epControlP.json"
Rogue_url = base_url + Rogue_class

Rogue = s.get(Rogue_url, verify=False)
Rogue_out = Rogue.json()

### Rogue EP Variables
RogueList = Rogue_out['imdata']
RogueAdminState = RogueList[0]['epControlP']['attributes']['adminSt']

### IP Aging Settings
### IP Aging should be set to adminSt:enabled
### System > System Settings > Endpoint Controls > IP Aging
IPAging_class="node/class/epIpAgingP.json"
IPAging_url = base_url + IPAging_class

IPAging = s.get(IPAging_url, verify=False)
IPAging_out = IPAging.json()

### IP Aging Variables
IPAgingList = IPAging_out['imdata']
IPAgingAdminState = IPAgingList[0]['epIpAgingP']['attributes']['adminSt']

### MCP Settings
### MCP should be set to adminSt:enabled and ctrl:pdu-per-vlan
### Fabric > Access Policies > Global Policies > MCP Instance Policy default
MCP_class="node/class/mcpInstPol.json"
MCP_url = base_url + MCP_class

MCP = s.get(MCP_url, verify=False)
MCP_out = MCP.json()

### MCP Variables
MCPList = MCP_out['imdata']
MCPAdminState = MCPList[0]['mcpInstPol']['attributes']['adminSt']
MCP_PerEPG = MCPList[0]['mcpInstPol']['attributes']['ctrl']

### BFD Internal fabric Settings
### BFD should be set to bfdIsis:enabled
### Fabric > Fabric Policies > Policies > Interface > L3 Interface > default > BFD ISIS Policy Configuration
BFD_class="node/class/l3IfPol.json"
BFD_url = base_url + BFD_class

BFD = s.get(BFD_url, verify=False)
BFD_out = BFD.json()

### BFD Variables
BFDList = BFD_out['imdata']
BFDAdminState = BFDList[0]['l3IfPol']['attributes']['bfdIsis']


### Coop Strict Settings 
### Coop should be set to type:strict
### System > System Settings > COOP Group
CoopPol_class="node/class/coopPol.json"
CoopPol_url = base_url + CoopPol_class

CoopPol = s.get(CoopPol_url, verify=False)
CoopPol_out = CoopPol.json()

### Coop Variables
CoopPolList = CoopPol_out['imdata']
CoopPolAdminState = CoopPolList[0]['coopPol']['attributes']['type']


### Preserve COS Settings 
### Preserve COS Settings should be set to ctrl:dot1p-preserve
### Fabric > Access Policies > Policies > Global > QOS Class > Preserve COS
PCOS_class="node/class/qosInstPol.json"
PCOS_url = base_url + PCOS_class

PCOS = s.get(PCOS_url, verify=False)
PCOS_out = PCOS.json()

### Preserve COS Variables
PCOSList = PCOS_out['imdata']
PCOSAdminState = PCOSList[0]['qosInstPol']['attributes']['ctrl']

 

print('========================================================================')
print("\n+*+*+ Checking Best Practice Configuration Settings. +*+*+\n")
#print("MCP state is", MCPAdminState, "and Per-EPG-Config is", MCP_PerEPG)  
#print("Disable Remote EP learn is", IsDisXRLearnActivated)
#print("Domain Validation is", IsDomValActivated)
#print("Uplink Port Tracking is", PortTrackAdminState)
#print("Rogue EP Detection is", RogueAdminState)
#print("Internal Fabric BFD is", BFDAdminState)
#print("Coop Policy is", CoopPolAdminState)
#print("Preserve COS policy is", PCOSAdminState)



if MCPAdminState == "disabled" or MCP_PerEPG == "":
  print("MisCabling Protocol (MCP):")
  print("**** Warning: MCP is either Disabled Globally or the MCP Per Vlan option is not enabled. ****")
  print("Go to Fabric > Access Policies > Global Policies > MCP Instance Policy default to enable.\n")
else:
  print("MisCabling Protocol (MCP):")
  print("MisCabling Protocol (MCP) is following Best Practices.")
  print("MCP state is", MCPAdminState, "and Per-EPG-Config is", MCP_PerEPG, "\n")  

if IsEnforceActivated != "yes":
  print("Enforced Subnet Check:")
  print("**** Warning: EnforceSubnetCheck not enabled. ****")
  print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Enforced Subnet Check:")  
  print("Enforced Subnet Check is following Best Practices.")
  print("Enforce Subnet Check is enabled.\n") 

if IsDisXRLearnActivated != "yes":
  print("Disable Remote EP Learn:")
  print("**** Warning: Disable Remote EP Learn is not enabled. ****")
  print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Disable Remote EP Learn:")  
  print("Disable Remote EP Learn is following Best Practices.")
  print("Disable Remote EP Learn is enabled.\n")

if IsDomValActivated != "yes":
  print("Domain Validation:")
  print("**** Warning: Domain Validation is not enabled.")
  print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Domain Validation:")  
  print("Domain Validation is following Best Practices.")
  print("Domain Validation is enabled.\n")

if PortTrackAdminState !="on":
  print("Uplink Port Tracking:")
  print("**** Warning: Uplink Port Tracking is not enabled.")
  print("Go to System > System Settings > Port Tracking to enable.\n")
else:
  print("Uplink Port Tracking:") 
  print("Uplink Port Tracking is following Best Practices.")
  print("Uplink Port Tracking is", PortTrackAdminState, "\n")

if EPLoopAdminState !="enabled":
  print("Endpoint Loop Detection:")
  print("**** Warning: EP Loop Detection is not enabled.")
  print("Go to System > System Settings > Endpoint Controls to enable.\n")
elif EPLoopAdminState == "enabled" and EPLoopAction != "":
  print("Endpoint Loop Detection:")
  print("**** Warning: EP Loop Detection is enabled, but we recommend you disable the Actions which are currently set to", EPLoopAction)
  print("Go to System > System Settings > Endpoint Controls to disable Actions.\n")
else:
  print("Endpoint Loop Detection:") 
  print("Endpoint Loop Detection is following Best Practices.")
  print("Endpoint Loop Detection is", PortTrackAdminState, "and Endpoint Actions are not configured.\n")

#if RogueAdminState != "enabled":
#  print("Rogue Endpoint Control:")
#  print("**** Warning: Rogue EP Control is not enabled.")
#  print("Go to System > System Settings > Endpoint Controls > Rogue EP Control to enable.\n")
#else:
#  print("Rogue Endpoint Control:")
#  print("Rogue Endpoint Control is following Best Practices.")
#  print("Rogue EP Control is", RogueAdminState, "\n")

if IPAgingAdminState != "enabled":
  print("IP Aging:")
  print("**** Warning: IP Aging is not enabled.")
  print("Go to System > System Settings > Endpoint Controls > IP Aging to enable.\n")
else:
  print("IP Aging:")
  print("IP Aging is following Best Practices.")
  print("IP Aging is", IPAgingAdminState, "\n")

if BFDAdminState !="enabled":
  print("Internal Fabric BFD:")
  print("**** Warning: Internal Fabric BFD is not enabled.")
  print("Go to Fabric > Fabric Policies > Policies > Interface > L3 Interface > default > BFD ISIS Policy Configuration to enable.\n")
else:
  print("Internal Fabric BFD:")  
  print("Internal Fabric BFD is following Best Practices.")
  print("Internal Fabric BFD is", BFDAdminState, "\n")

if CoopPolAdminState != "strict":
  print("Coop Policy mode:")
  print("**** Warning: Your COOP policy is not set to strict.")
  print("Go to System > System Settings > COOP Group to enable.\n")
else:
  print("Coop Policy mode:")  
  print("Coop Policy mode is following Best Practices.")
  print("Coop Policy is", CoopPolAdminState, "\n")

#if PCOSAdminState != "dot1p-preserve":
#  print("Preserve COS:")
#  print("**** Warning: Your fabric is not configured to preserve COS values.")
#  print("Go to Fabric > Access Policies > Policies > Global > QOS Class > Preserve COS to enable.\n")
#else:
#  print("Preserve COS:")  
#  print("Preserve COS setting is following Best Practices.")
#  print("Preserve COS policy is", PCOSAdminState, "\n")

print('\n========================================================================')
