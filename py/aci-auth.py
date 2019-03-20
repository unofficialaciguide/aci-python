#!/usr/bin/env python

# # Unofficial ACI Guide
# ## Python 3 Authentication Example
# This is boilerplate code. Feel free to copy/paste.


import requests
import json
import os
import getpass


# Enter your controller hostname/IP and user credentials below.  
# Some examples for reading user info from a config file and prompted are also included.

# Configure username, password, and controller.


# You can use inline variables, a separate config file, or prompted on the command-line.

## Inline:
#controller = "wabac-machine.mr-peabody.com"
#username = "sherman"
#password = "and-away-we-go!"

# Here, we try to read from the config.py file in the same directory.
# Then we test if the variable are set.
# If not (because it couldn't read the config file), then it prompts you for them.


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


# Variables to construct our URLs.

base_url = "https://" + str(controller) + "/api/"
auth_bit = "aaaLogin.json"
auth_url = base_url + auth_bit


# JSON auth data for POST
auth_data = {
  "aaaUser":{
    "attributes":{
      "name":username,
      "pwd":password
    }
  }
}


# ## Construct the Request

# "verify=False" means we will not try to validate the self-signed SSL ccertificate our controller uses
# We also disable the warnings.

print(" ")
print(" ")
print(" ")
print(" ")
print(" ")

print("Iinitiating authentication...")
requests.packages.urllib3.disable_warnings() 
r = requests.post(auth_url, json=auth_data, verify=False)

print(" ")

# This prints the HTTP response, such as 200, 403, 404, 500, etc.
# You could use this for error trapping.
print("Server responsded with " + str(r.status_code))


# We're taking the response, r, and running the json() method to decode JSON 
# into native Python data structures, like list and dictionaries. We'll store
# that into a variable called "r_json" to work with.
r_json = r.json()

# Uncomment if you want to see the JSON dump. 
# print(json.dumps(r_json, indent=4, sort_keys=True))


# ## Tokens and Cookies

print(" ")

# Get session token from response body.
token = r_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
print("Session Token: \n" + token)

print(" ")

# We can also view the HTTP headers from the initial response.
# HTTP headers are captured as a single dictionary with each header key/value
# mapping to a dictionary key/value.
print("HTTP headers: \n" + str(r.headers))

print(" ")

# Show the cookie in the HTTP header
cookie_header = r.headers['Set-Cookie']
print("HTTP cookie header: \n" + cookie_header)

print(" ")

# Accessing the cookie directly
cookie = r.cookies['APIC-cookie']
print("HTTP cookie: \n" + cookie)

print(" ")

print("== Constructing the cookie for request ==")
# cookies = {'Cookie1': some_value, 'Cookie2': some_other_value}
# Construct the cookie in the format 'APIC-cookie: cookie'
cookie_jar = {'APIC-cookie': cookie}

print(" ")

# We could also use that session token above, if we wanted to, since we know the APIC requires the cookie 
# to be in the format "APIC-cookie".
token_cookie_jar = {'APIC-cookie': token}
print("Using cookie header: " + "\n" + str(cookie_jar) + "\n\n" + "Using token: " + "\n" + str(token_cookie_jar))

print(" ")

# Now we can construct an authenticated GET using the token or cookie we've extracted and assembled. 

ep_url = base_url + "node/class/fvCEp.json"
response = requests.get(ep_url, cookies=cookie_jar, verify=False)
out = response.json()
#print(out)

print(" ")
print("Getting endpoints....")

print(" ")



print("== Using response ebject == ")
# Note the "totalCount" object, and how it matches the number fvCEp objects in the imdata list returned...
# Print the value of the totalCount dictionary key.
print("Total Count: " + out["totalCount"] + " objects.")

# The imdata key has a list value, so we'll count the number of list elements using len()
count_of_fvCEp = len(out['imdata'])
print("Total Count: " + str(count_of_fvCEp) + " fvCEp list elements.")



# ## Sessions

# If you don't want to parse and pass token on each request, 
# just use requests session object which will retain persistent data (like cookies) for you.
# http://docs.python-requests.org/en/master/user/advanced/

# Sessions will also keep the TCP connection open for subsequent requests. 

# Create a session object, s, and then POST the auth data just like the earlier example. 
# We don't need to create a new request object since the session will persist that data in the session object.
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)

# Note the lack of cookie headers from the session object, compared to the requests object.
# You can do a whole bunch of s.get() requests if you want to!
# response = requests.get(ep_url, cookies=cookie_jar, verify=False)
session_response = s.get(ep_url, verify=False)

print(" ")

s_out = session_response.json()
print("== Using session object == ")
print("Total Count: " + s_out["totalCount"] + " objects.")

count_of_fvCEp = len(s_out['imdata'])
print("Total Count: " + str(count_of_fvCEp) + " fvCEp list elements.")
print(" ")

