import urllib
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import sqlite3

class crawler:
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getEntryId(self,table,field,value,createnew=True):
        return None

    def addToIndex(self,url,soup):
        if self.isIndexed(url):
            return

    def getTextOnly(self,soup):
        return None
    def separateWords(self,text):
        return None
    def isIndexed(self,url):
        return False

    def addLinkRef(self,urlFrom,urlTo,linkText):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = {}
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print('Could not open %s' % page)
                    continue
                try:
                    soup = BeautifulSoup(c.read())
                    self.addToIndex(page, soup)

                    links = soup('a')
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urllib.parse.urljoin(page, link['href'])
                            if url.find("'") != -1:
                                continue
                            url = url.split('#')[0]
                            print(url)
                            if url[0:4] == 'http' and not self.isIndexed(url):
                                newpages[url]=1
                            linkText = self.getTextOnly(link)
                            self.addLinkRef(page, url, linkText)
                    self.dbcommit()
                except:
                    print('Coule not parse page %s' % page)
            pages = newpages
            print(newpages)

    def createIndexTables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()

ignoreWords=set(['the','of','to','and','a','in','is','it'])

