from shibboleth_login import ShibbolethClient
from bs4 import BeautifulSoup

username = 'username'
password = 'password'
url = 'url'

client = ShibbolethClient(username, password)

try:
    res = client.get('url')
    print(type(res))

    soup = BeautifulSoup(res.text, "lxml")

    data_html = soup.select("html")

    print(data_html)

except Exception:
    print("Error")
finally:
    client.close()