import urllib
from bs4 import BeautifulSoup

class crawler:
    def __init__(self,dbname):
        pass

    def __del__(self):
        pass
    def dbcommit(self):
        pass

    def getEntryId(self,table,field,value,createnew=True):
        return None

    def addToIndex(self,url,soup):
        print('Indexing %s' % url)

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
            newpages = set()
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print('Could not open %s' % page)
                    continue
                soup = BeautifulSoup(c.read())
                self.addToIndex(page, soup)
                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urllib.parse.urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'https' and not self.isIndexed(url):
                            newpages.add(url)
                        linkText = self.getTextOnly(link)
                        self.addLinkRef(page, url, linkText)
                self.dbcommit()
            pages = newpages

    def createIndexTables(self):
        pass

ignoreWords=set(['the','of','to','and','a','in','is','it'])

