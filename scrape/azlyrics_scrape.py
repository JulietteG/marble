#!/usr/bin/env python

import string, urllib2, httplib
from bs4 import BeautifulSoup
from urlparse import urljoin


ROOT_URL = "http://www.azlyrics.com/"

index_urls = []
for letter in string.lowercase:
    index_urls.append(urljoin(ROOT_URL, letter + ".html"))

index_urls.append(urljoin(ROOT_URL, "19.html"))

for index_url in index_urls:
    req = urllib2.Request(index_url)
    response = None
    try:
        response = urllib2.urlopen(req)
        page_contents = response.read()
        soup = BeautifulSoup(page_contents,"html.parser")
        container = soup.select("body > div.container.main-page")
        container_soup = BeautifulSoup(container)

        for link in container_soup.findAll('a'):
            print link

    except httplib.BadStatusLine:
        import pdb; pdb.set_trace()
