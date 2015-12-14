import json, pymongo, requests, os, sys
import time, dateutil.parser, codecs
from konlpy.tag import Twitter; t = Twitter()
pos = lambda d: ['/'.join(p) for p in t.pos(d) if p[1] in ['Noun', 'Adjective', 'Determiner', 'Adverb', 'KoreanParticle']]

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['reviews']
del collections['system.indexes']

cursor = collections['comedy'].find()
length = collections['comedy'].count()
cnt = 0

with codecs.open('D:\watcha_reviews\comedy.txt', 'w', encoding='utf-8') as fp:
	for row in cursor:
		cnt += 1
		if cnt % 1000 == 0:
			print str(cnt) + ' / ' + str(length)
		rating = row['rating']
		cid = row['comment_id']
		text = row['text']
		fp.write(' '.join([str(rating), str(cid)] + pos(text)) + '\n')