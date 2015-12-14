#-*- coding: utf-8 -*-
import json, pymongo, requests, sys
import time, dateutil.parser
import gensim, logging, os, pickle
from pprint import pprint
import numpy as np
# from sklearn.kernel_approximation import RBFSampler
# from sklearn.linear_model import SGDClassifier
from sklearn import linear_model
from sklearn.externals import joblib
from konlpy.tag import Twitter; t = Twitter()
pos = lambda d: ['/'.join(p) for p in t.pos(d) if p[1] in ['Noun', 'Adjective', 'Determiner', 'Adverb', 'KoreanParticle']]

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['system.indexes']

# for cname in collections.keys():
# 	review_rmodel = joblib.load('D:\watcha_models\\logr\\{cname}.pkl'.format(cname = cname))
# 	model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\{cname}.model'.format(cname = cname))

# 	X = model.docvecs
# 	y = np.asarray([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.5 for i in xrange(len(X))])

# 	print '{cname} model ready'.format(cname = cname)
# 	print 'MSE : ', np.mean((review_rmodel.predict(X) - y)**2)

# 	a = u'한국 호러 장르에서 좀처럼 보기 드문 치밀하고도 영리한 심리적 공포.' # 3.5
# 	a = pos(a)
# 	infered = model.infer_vector(a)
# 	preds = review_rmodel.predict(infered.reshape(1, -1))
# 	print preds

def over_filter(x):
	if x > 5: return 5.0
	elif x < 0: return 0.0
	else: return x

def evaluate(x, y):
	if x > 2.75 and y > 2.75: return 1
	elif x < 2.75 and y < 2.75: return 1
	else: return 0

for cname in collections.keys():
	review_lmodel = joblib.load('D:\watcha_models\\svr\\{cname}.pkl'.format(cname = cname))
	model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\{cname}.model'.format(cname = cname))

	X = model.docvecs
	y = np.asarray([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.5 for i in xrange(len(X))])

	print '{cname} Linear Regression model'.format(cname = cname)
	X = np.asarray([over_filter(x) for x in review_lmodel.predict(X)])
	# print 'MSE : ', np.mean((X - y)**2)
	p = [evaluate(x, y) for x, y in zip(X, y)]
	print 'Accuracy :', np.mean(p)


# a = raw_input()
# a = a.decode('cp949')
# a = pos(a)
# print 'parsed tokens ' + ' '.join(a)

# infered = model.infer_vector(a)
# sims = model.docvecs.most_similar([infered])
# preds = review_lmodel.predict(infered)
# print preds
# for idx, si in sims:
# 	ta = model.docvecs.offset2doctag[idx]
# 	rating, cid, cat = ta.split('_')
# 	r = collections[cat].find({'comment_id': int(cid)})[0]
# 	a = 'rating : {rating}, text : {text}'.format(rating = r['rating'], text = r['text'].encode('utf-8'))
# 	print a.decode('utf-8'), si