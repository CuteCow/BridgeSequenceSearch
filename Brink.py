import requests
from lxml import html
from bs4 import BeautifulSoup
import re
import time
import os

#pattern = re.match(r'(/d+)')

USERNAME = "Username"
PASSWORD = "Password"

LOGIN_URL = "https://www.bridgebase.com/myhands/myhands_login.php?t=%2Fmyhands%2Findex.php%3F"
URL = "https://www.bridgebase.com/vugraph_archives/vugraph_archives.php?v3b="

# Create payload
payload = {
    "username": USERNAME, 
    "password": PASSWORD
}

payload1 = {
    "searchstring": "",
    "command": "search"
}

session_requests = requests.session()

# Get login csrf token
result = session_requests.get(LOGIN_URL)
tree = html.fromstring(result.text)

# Perform login
result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

year = 2018
total = list()
while year > 2010 :
    
    payload1["searchstring"] = "brink drijver " + str(year)
    
    # Scrape url
    result = requests.post(URL, data = payload1)
    
    soup = BeautifulSoup(result.content, 'lxml')
    
    z = re.findall(r'(\d\d\d\d\d)', str(soup.table))
    zz = sorted((list(set(z))))
    
    total = total + zz
    year = year - 1
    print(len(zz))
    time.sleep(1)

os.chdir('c:\\Users\\james\\Dropbox\\Python Scripts\\Brink')
for link in total:
    url = "https://www.bridgebase.com/tools/vugraph_linfetch.php?id="
    r = requests.get(url + link, allow_redirects=True)
    open(link + '.lin', 'wb').write(r.content)
