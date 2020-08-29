import subprocess
import sys
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
import requests


def _downloadFile(url:str):
    filename = urlsplit(url).path.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as f:
        soup = BeautifulSoup(f.read(), 'lxml')

        links = soup.find_all('a', href=True)
        for link in links:
            if 'OpenDataFiles' in link['href'] and link['href'].endswith('en-GB.xml'):
                url = link['href']
                _downloadFile(url)
