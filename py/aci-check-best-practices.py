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


print("========")
print("+  MCP +")
print("========")
if MCPAdminState == "disabled" or MCP_PerEPG == "":
  print("**** Warning: MCP is either Disabled Globally or the MCP Per Vlan option is not enabled. ****")
  print("Go to Fabric > Access Policies > Global Policies > MCP Instance Policy default to enable.\n")
else:
  print("Good job!")
  print("MCP state is", MCPAdminState, "and Per-EPG-Config is", MCP_PerEPG, "\n")  

print("=========================")
print("+  Enforce Subnet Check +")
print("=========================")

if IsEnforceActivated != "yes":
	print("**** Warning: EnforceSubnetCheck not enabled. ****")
	print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Good job!")
  print("Enforce Subnet Check is enabled.\n") 

print("===========================")
print("+  Disable Remote EP Learn +")
print("===========================")

if IsDisXRLearnActivated != "yes":
  print("**** Warning: Disable Remote EP Learn is not enabled. ****")
  print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Good job!")
  print("Disable Remote EP Learn is enabled.\n")

print("=======================")
print("+  Domain Validation +")
print("=======================")

if IsDomValActivated != "yes":
  print("**** Warning: Domain Validation is not enabled.")
  print("Go to System > System Settings > Fabric Wide Setting to enable.\n")
else:
  print("Good job!")
  print("Domain Validation is enabled.\n")

print("===========================")
print("+  Uplink Port Tracking   +")
print("===========================")

if PortTrackAdminState !="on":
  print("**** Warning: Uplink Port Tracking is not enabled.")
  print("Go to System > System Settings > Port Tracking to enable.\n")
else:
  print("Good job!")
  print("Uplink Port Tracking is", PortTrackAdminState, "\n")

#print("===========================")
#print("+  Rogue EP Control       +")
#print("===========================")

#if RogueAdminState != "enabled":
#	print("**** Warning: Rogue EP Control is not enabled.")
#	print("Go to System > System Settings > Endpoint Controls > Rogue EP Control to enable.\n")
#else:
#  print("Good job!")
	#print("Rogue EP Control is", RogueAdminState, "\n")

print("===========================")
print("+  Internal Fabric BFD    +")
print("===========================")

if BFDAdminState !="enabled":
  print("**** Warning: Internal Fabric BFD is not enabled.")
  print("Go to Fabric > Fabric Policies > Policies > Interface > L3 Interface > default > BFD ISIS Policy Configuration to enable.\n")
else:
  print("Good job!")
  print("Internal Fabric BFD is", BFDAdminState, "\n")

print("===========================")
print("+  Coop Policy            +")
print("===========================")

if CoopPolAdminState != "strict":
  print("**** Warning: Your COOP policy is not set to strict.")
  print("Go to System > System Settings > COOP Group to enable.\n")
else:
  print("Good job!")
  print("Coop Policy is", CoopPolAdminState, "\n")

print("===========================")
print("+  Preserve COS Values    +")
print("===========================")

if PCOSAdminState != "dot1p-preserve":
  print("**** Warning: Your fabric is not configured to preserve COS values.")
  print("Go to Fabric > Access Policies > Policies > Global > QOS Class > Preserve COS to enable.\n")
else:
  print("Good job!")
  print("Preserve COS policy is", PCOSAdminState, "\n")

print('\n========================================================================')