from shibboleth_login import ShibbolethClient
from bs4 import BeautifulSoup

username = 'username'
password = 'password'
url = 'url'

client = ShibbolethClient(username, password)

try:
    res = client.get(url)
    print(type(res))

    soup = BeautifulSoup(res.text, "lxml")
    information_html = soup.select("html > body > form > section > div > dl > dd")

    for information in information_html:
        print(information.get_text())

except Exception:
    print("Error")
finally:
    client.close()