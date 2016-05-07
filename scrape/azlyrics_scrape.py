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


# class SiteRequest(threading.Thread):
#     """
#     Class for site requests (a Thread). Each SiteRequest object corresponds to requests for MIDI files from one site.
#     """

#     def __init__(self, sitename, base_url, extension):
#         threading.Thread.__init__(self)
#         self.sitename = sitename
#         self.base_url = base_url
#         self.extension = extension

#     def run(self):
#         """
#         Run this thread: request MIDI files from self.base_url
#         """
#         # request the "homepage"
#         req = urllib2.Request(self.base_url)
#         response = urllib2.urlopen(req)
#         page_contents = response.read()

#         # grab all the MIDI links
#         for link in BeautifulSoup(page_contents).findAll('a', href=True):
#             if link['href'].endswith(self.extension):
#                 base_url = urljoin(self.base_url, link['href'])
#                 local_path = self.sitename + "/" + link['href'].split('/')[-1]

#                 if not os.path.exists(local_path):
#                     print "Downloading " + base_url
#                     try:
#                         urllib.URLopener().retrieve(base_url, local_path)

#                         # extract if a .zip file
#                         if extension == ".zip":
#                             with zipfile.ZipFile(local_path, "r") as z:
#                                 z.extractall(self.sitename)
#                     except (IOError, zipfile.BadZipfile) as e:
#                         print e


# if __name__ == '__main__':
#     # open the data file
#     if len(sys.argv) > 1:
#         sites_filename = sys.argv[1]
#     else:
#         sites_filename = "sites.json"

#     with open(sites_filename) as sites_file:
#         sites = json.load(sites_file)['sites']

#     # iterate through all the sites
#     for site in sites:
#         sitename = site['name']
#         extension = site.get('extension', ".mid")

#         # and all the urls for this site
#         for base_url in site['urls']:
#             # make directory as necessary
#             if not os.path.exists(sitename):
#                 os.makedirs(sitename)

#             # and start the requests
#             t = SiteRequest(sitename, base_url, extension)
#             t.start()
