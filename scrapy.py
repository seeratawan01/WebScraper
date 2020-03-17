import requests
from bs4 import BeautifulSoup
import tldextract


def getTitle(link):
    """Attempt to get a title."""
    title = ''
    if link.title.string is not None:
        title = link.title.string
    elif link.find("h1") is not None:
        title = link.find("h1")
    return title


def getDescription(link):
    """Attempt to get description."""
    description = ''
    if link.find("meta", property="og:description") is not None:
        description = link.find(
            "meta", property="og:description").get('content')
    elif link.find("p") is not None:
        description = link.find("p").content
    return description


def getImage(link):
    """Attempt to get image."""
    image = ''
    if link.find("meta", property="og:image") is not None:
        image = link.find("meta", property="og:image").get('content')
    elif link.find("img") is not None:
        image = link.find("img").get('href')
    return image


def getSiteName(link, url):
    """Attempt to get the site's base name."""
    sitename = ''
    if link.find("meta", property="og:site_name") is not None:
        sitename = link.find("meta", property="og:site_name").get('content')
    else:
        sitename = url.split('//')[1]
        name = sitename.split('/')[0]
        name = sitename.rsplit('.')[1]
        return name.capitalize()
    return sitename


def scrape(url):
    """Scrape scheduled link previews."""
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    })
    r = requests.get(url, headers=headers)
    raw_html = r.content
    soup = BeautifulSoup(raw_html, 'html.parser')

    links = soup.select('[href^=\.\/], [src^=\.\/]')
    other_links = soup.select(
        '[href]:not([href^=\.]):not([href^=\#]), [src]:not([src^=\.]):not([src^=\#])')

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


# links = soup.select('body p > a')
# previews = []
# for link in links:
#     url = link.get('href')
#     r2 = requests.get(url, headers=headers)
#     link_html = r2.content
#     embedded_link = BeautifulSoup(link_html, 'html.parser')
#     link_preview_dict = {
#         'title': getTitle(embedded_link),
#         'description': getDescription(embedded_link),
#         'image': getImage(embedded_link),
#         'sitename': getSiteName(embedded_link, url),
#         'url': url
#     }
#     previews.append(link_preview_dict)
#     print(link_preview_dict)
scrape("https://github.com/Xuntron/Youtube-Video-Downloader-")
