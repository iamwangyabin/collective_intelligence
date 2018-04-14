import jieba

fr=open('/home/wang/PycharmProjects/collective_intelligence/Groups/ch.txt')
fr2=open('/home/wang/PycharmProjects/collective_intelligence/Groups/out.txt','w')
words={}
wordlist=[]
wordcount=[]
for line in fr.readlines():
    seg_list = jieba.cut(line, cut_all=True)
    for word in seg_list:
        keyl="".join(word).strip()
        if len(keyl) <= 1 :
            continue
        else:
            if keyl not in words:
                 words.setdefault(keyl,0)
            words[keyl]+=1
            wordlist.append(keyl)

for i in words:
    wordcount.append(words[i])
print(words)
fr2.write(str(words)+'\n')

fr2.write(str(wordcount)+'\n')
for word in wordlist: fr2.write(' %s' % word)
fr2.write('\n')
