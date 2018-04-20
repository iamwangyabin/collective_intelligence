import urllib
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import sqlite3
import re


class crawler:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getEntryId(self, table, field, value, createnew=True):
        cur=self.con.execute("select rowid from %s where %s='%s'" % (table, field, value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute("insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]

    def addToIndex(self, url, soup):
        if self.isIndexed(url):
            return
        print("Indexing " + url)

        #get individual words
        text = self.getTextOnly(soup)
        words=self.separateWords(text)

        #Get url id
        urlId=self.getEntryId('urllist','url',url)

        #Link each word to its url
        for i in range(len(words)):
            word=words[i]
            if word in ignoreWords:
                continue
            wordid=self.getEntryId('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid ,wordid,location) values(%d,%d,%d)" % (urlId,wordid,i))

    def getTextOnly(self,soup):
        #取便签内部的文字内容
        v = soup.string
        if v == None:
            #tag的属性contents将便签子节点以列表形式输出，可以通过遍历获得所有标签
            c = soup.contents
            resultText = ''
            for t in c:
                subtext = self.getTextOnly(t)
                resultText += subtext + '\n'
            return resultText
        else:
            return v.strip()

    def separateWords(self, text):
        #\W表示匹配包括下划线在内的任何单词字符
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def isIndexed(self, url):
        u=self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            v=self.con.execute("select * from wordlocation where urlid=%d " % u[0]).fetchone()
            if v!=None:
                return True
        return False

    def addLinkRef(self, urlFrom, urlTo, linkText):

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
                    print("1")
                    self.addToIndex(page, soup)
                    print("2")
                    links = soup('a')
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urllib.parse.urljoin(page, link['href'])
                            if url.find("'") != -1:
                                continue
                            url = url.split('#')[0]
                            print(url)
                            if url[0:4] == 'http' and not self.isIndexed(url):
                                newpages[url] = 1
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


ignoreWords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
