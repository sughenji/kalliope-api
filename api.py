#!/usr/bin/python3

import requests
from urllib3.exceptions import InsecureRequestWarning
import hashlib
import random
import string
import base64
from datetime import datetime
import pytz
import logging

user="privacyadminuser"
password="privacyadminpassword"
salt="{xxxxxxxxxxxxxxxx}" # curl -k https://your.pbxdomain.net/rest/salt/default

# nonce

nonce = hashlib.md5(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)).encode()).hexdigest()
print("Printing nonce ...")
print(nonce+"\n")

# digestPassword

digestPassword = hashlib.sha256()
digestPassword.update(password.encode())
digestPassword.update(salt.encode())
digestPassword.digest
print("Printing digestPassword ...")
dp = digestPassword.hexdigest()
print(dp+"\n")

# created

# Get the current date and time in UTC
now_utc = datetime.now(pytz.utc)
# Format the date and time as a string
formatted_date_time = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
print("Printing created ...")
print(formatted_date_time+"\n")

# digest

digest = hashlib.sha256()
digest.update(nonce.encode())
digest.update(dp.encode())
digest.update(user.encode())
digest.update("default".encode())
digest.update(formatted_date_time.encode())
dig = digest.digest()
encoded = base64.b64encode(dig)
print("Printing digest ...")
print(encoded.decode('ascii'))
print("\n")

# our request

proxies = { 'http': 'http://localhost:8080',
            'https': 'http://localhost:8080'
          }
"""
# debug stuff
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
"""

s = requests.session()
headers = { "X-authenticate": 'RestApiUsernameToken Username="'+user+'", Domain="default", Digest="'+encoded.decode('ascii')+'", Nonce="'+nonce+'", Created="'+formatted_date_time+'"', "Accept": 'json' }
print(headers.items())

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

r = s.get('https://your.pbxdomain.net/rest/cdr/v3_compat/2023/9/11', headers=headers, verify=False)
print(r.status_code)
print(r.json())