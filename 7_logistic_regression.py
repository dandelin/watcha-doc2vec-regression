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
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['system.indexes']

for cname in collections.keys():
	model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\{cname}.model'.format(cname = cname))
	X = model.docvecs
	y = np.array([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.5 for i in xrange(len(X))])
	lin = linear_model.SGDRegressor(eta0=0.001, verbose=True, n_iter=100)
	lin.fit(X, y)

	joblib.dump(lin, 'D:\watcha_models\\logr\\{cname}.pkl'.format(cname = cname))