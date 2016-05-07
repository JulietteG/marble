#!/usr/bin/env python
import re, os
import requests
import nltk
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import string, threading
from Queue import Queue
from time import sleep

class Worker(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        while True:
            artist = self.q.get()
            print "q.get", artist
            self.process(artist)
            self.q.task_done()

    def process(self,artist):
        dirname = os.path.join(ROOT,artist + "/")
        artist_url = "http://www.lyrics.com/" + artist
        try:
            r = requests.get(artist_url)
            soup = BeautifulSoup(r.content)
            gdata = soup.find_all('div',{'class':'row'})

            lyrics = []

            for item in gdata:
                title = item.find_all('a',{'itemprop':'name'})[0].text
                title = title.encode('ascii', 'ignore')
                lyricsdotcom = 'http://www.lyrics.com'
                for link in item('a'):
                    lyriclink = lyricsdotcom+link.get('href')
                    lyricdata = None
                    numOfRequests = 0
                    while numOfRequests < 10 and not lyricdata:
                        try:
                            numOfRequests += 1
                            req = requests.get(lyriclink)
                            lyricsoup = BeautifulSoup(req.content)
                            lyricdata = lyricsoup.find_all('div',{'id':re.compile('lyric_space|lyrics')})[0].text.encode('ascii', 'ignore')
                            lyrics.append([title,lyricdata])
                            if not "Submit" in lyricdata[:20]:
                                #print title
                                #print lyricdata
                                if not os.path.isdir(dirname):
                                    os.mkdir(dirname)

                                filename = os.path.join(dirname, title + ".txt")
                                with open(filename,"w") as f:
                                    f.write(lyricdata)
                        except ConnectionError,e:
                            time.sleep(10)
                        except Exception,e:
                            print e
        except ConnectionError, e:
            time.sleep(10)
            self.q.put(artist)
        except Exception,e:
            print e


url = 'http://www.lyrics.com/artists/start/'

artists = []

ROOT = "lyrics/"

if not os.path.isdir(ROOT):
    os.mkdir(ROOT)

q = Queue()

start_letter = 'd'
for letter in string.lowercase[string.lowercase.index(start_letter):]:
#for letter in ['h']:

    index_url = url + letter
    i = 0
    while True:
        request_url = index_url
        
        if i != 0:
            request_url = index_url + "/" + str(i)
        
        r = requests.get(request_url)
        soup = BeautifulSoup(r.content)
        
        selector = "#topsongs > table > tr > td > div > a"
        links = soup.select(selector)

        if not links:
            break
        
        for link in links:
            artist = link["href"][1:]
            q.put(artist)
            print "q.put", artist
        
        i += 90

NUM_THREADS = 64
for k in xrange(NUM_THREADS):
    thrd = Worker(q)
    thrd.start()

    print "Starting:", thrd

q.join()
