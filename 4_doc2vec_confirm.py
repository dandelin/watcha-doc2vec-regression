#-*- coding: utf-8 -*-
import json, pymongo, requests, sys
import time, dateutil.parser
import gensim, logging, os
from pprint import pprint
from konlpy.tag import Twitter; t = Twitter()
pos = lambda d: ['/'.join(p) for p in t.pos(d)]

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['reviews']
del collections['system.indexes']

model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\family.model')

print model.random.get_state()
model.random.set_state(model.random.get_state())

# print dir(model.docvecs)

# a = model.docvecs.doctags['3.5_2542564_comedy']
# b = model.docvecs
# print dir(b)
# print a
# print b.offset2doctag[89507]

# ============================================

# testword = pos('재밌다'.decode('utf-8'))[0]

# for i in model.most_similar(testword):
# 	print i[0].encode('utf-8'), i[1]

# ============================================

# a = raw_input()
# a = a.decode('cp949')
# a = pos(a)
# print 'parsed tokens ' + ' '.join(a)

# infered = model.infer_vector(a)
# sims = model.docvecs.most_similar([infered])
# for idx, si in sims:
# 	ta = model.docvecs.offset2doctag[idx]
# 	rating, cid, cat = ta.split('_')
# 	r = collections[cat].find({'comment_id': int(cid)})[0]
# 	a = 'rating : {rating}, text : {text}'.format(rating = r['rating'], text = r['text'].encode('utf-8'))
# 	print a.decode('utf-8'), si

# ============================================