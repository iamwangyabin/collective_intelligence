import feedparser
import re

def getWordCounts(url):
    d=feedparser.parse(url)
    wc={}

    for e in d.entries:
        if 'summary' in e:
            summary=e.summary
        else:
            summary=e.description

    words=getwords(e.title+''+summary)
    for word in words:
        wc.setdefault(word,0)
        wc[word]+=1
    return d.feed.title,wc