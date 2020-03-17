from bs4 import BeautifulSoup
import requests
import tldextract

import sys

url = sys.argv[1]

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
})
r = requests.get(url, headers=headers)
raw_html = r.content
soup = BeautifulSoup(raw_html, 'html.parser')

links = soup.select(r'[href^=\.\/], [src^=\.\/]')
other_links = soup.select(
    r'[href]:not([href^=\.]):not([href^=\#]), [src]:not([src^=\.]):not([src^=\#])')

for link in links:

    if link.get('href'):
        link['href'] = link['href'].replace("./", url)
    else:
        link['src'] = link['src'].replace("./", url)

for link in other_links:

    if link.get('href'):
        urlcheck = tldextract.extract(link['href'])
        if(urlcheck.suffix == ''):
            link['href'] = url+'/'+link['href']

    elif link.get('src'):
        urlcheck = tldextract.extract(link['src'])
        if(urlcheck.suffix == ''):
            link['src'] = url+'/'+link['src']

name = tldextract.extract(url)
f = open(name.domain+".html", "w", encoding="utf-8")
f.write(soup.prettify())
f.close()

print(name.domain+".html")
