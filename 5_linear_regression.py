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
	y = np.asarray([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.5 for i in xrange(len(X))])
	lin = linear_model.LinearRegression(n_jobs = -1)
	lin.fit(X, y)
	# rbf_feature = RBFSampler(gamma=1, random_state=1)
	# X_features = rbf_feature.fit_transform(X)
	# clf = SGDClassifier(verbose = True)
	# clf.fit(X_features, y)
	# clf = svm.SVR(kernel='linear', cache_size=8000, verbose=True)
	# clf.fit(X, y)
	joblib.dump(lin, 'D:\watcha_models\\svr\\{cname}.pkl'.format(cname = cname))


# model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\comedy.model')

# f=0
# for i, docvec in enumerate(model.docvecs):
# 	print docvec[:10], model.docvecs.offset2doctag[i]
# 	f+=1
# 	if f>10:
# 		break

# X = model.docvecs
# y = [float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.5 for i in xrange(len(X))]
# clf = svm.SVR(kernel='linear', cache_size=8000)
# clf.fit(X, y)
# joblib.dump(clf, 'D:\watcha_models\\svr\\comedy.pkl')

# X = [[0, 0, 1, 2, 3, 5, 2], [5, 2, 3, 4, 5, 7, 1]]
# y = [0.5, 2.5]
# clf = svm.SVR()
# clf.fit(X, y)
# joblib.dump(clf, 'test.pkl')
# a = joblib.load('test.pkl')
# print a.predict([[0, 1, 2, 3, 4, 5, 6]])