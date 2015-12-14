#-*- coding: utf-8 -*-
import json, pymongo, requests, sys
import time, dateutil.parser
import gensim, logging, os, pickle
from pprint import pprint
import numpy as np
# from sklearn.kernel_approximation import RBFSampler
# from sklearn.linear_model import SGDClassifier
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.externals import joblib
from konlpy.tag import Twitter; t = Twitter()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

def over_filter(x):
	if x > 5: return 5.0
	elif x < 0.5: return 0.5
	else: return x

def evaluate(x, y):
	if x > 2.75 and y > 2.75: return 1
	elif x < 2.75 and y < 2.75: return 1
	else: return 0

def evaluatec(x, y):
	if abs(y-x) <= 0.25: return 1
	else: return 0

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['system.indexes']

with open('regression.txt', 'a') as fp:
	for cname in collections.keys():
		model = gensim.models.doc2vec.Doc2Vec.load('D:\watcha_models\\{cname}.model'.format(cname = cname))
		lenX = len(model.docvecs)
		train_len = int(lenX * 0.8)
		train_X = np.asarray([model.docvecs[i] for i in xrange(train_len)])
		train_y = np.asarray([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.75 for i in xrange(train_len)])
		test_X = np.asarray([model.docvecs[i] for i in xrange(train_len+1, lenX)])
		test_y = np.asarray([float(model.docvecs.offset2doctag[i].split('_')[0]) if model.docvecs.offset2doctag[i].split('_')[0] != u'None' else 2.75 for i in xrange(train_len+1 , lenX)])

		fp.write("PROCESSING LINEAR REGRESSION on {cname}\n".format(cname = cname))
		lin = linear_model.LinearRegression(n_jobs = -1)
		lin.fit(train_X, train_y)
		joblib.dump(lin, 'D:\watcha_models\\linear_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in lin.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on LINEAR REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on LINEAR REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write("PROCESSING Ridge REGRESSION on {cname}\n".format(cname = cname))
		rid = linear_model.Ridge()
		rid.fit(train_X, train_y)
		joblib.dump(rid, 'D:\watcha_models\\ridge_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in rid.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on Ridge REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on Ridge REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write("PROCESSING BayesianRidge REGRESSION on {cname}\n".format(cname = cname))
		bridge = linear_model.BayesianRidge()
		bridge.fit(train_X, train_y)
		joblib.dump(bridge, 'D:\watcha_models\\bridge_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in bridge.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on BayesianRidge REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on BayesianRidge REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write("PROCESSING Lasso REGRESSION on {cname}\n".format(cname = cname))
		lasso = linear_model.Lasso()
		lasso.fit(train_X, train_y)
		joblib.dump(lasso, 'D:\watcha_models\\lasso_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in lasso.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on Lasso REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on Lasso REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write("PROCESSING SGDRegressor REGRESSION on {cname}\n".format(cname = cname))
		sgdr = linear_model.SGDRegressor(n_iter=75)
		sgdr.fit(train_X, train_y)
		joblib.dump(sgdr, 'D:\watcha_models\\sgdr_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in sgdr.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on SGDRegressor REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on SGDRegressor REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write("PROCESSING DecisionTreeRegressor REGRESSION on {cname}\n".format(cname = cname))
		dtr = DecisionTreeRegressor()
		dtr.fit(train_X, train_y)
		joblib.dump(dtr, 'D:\watcha_models\\dtr_regression\\{cname}.pkl'.format(cname = cname))
		ftest_X = np.asarray([over_filter(x) for x in dtr.predict(test_X)])
		p = [evaluate(x, y) for x, y in zip(ftest_X, test_y)]
		fp.write("Coarse-grained accuracy on DecisionTreeRegressor REGRESSION is {p}\n".format(p = np.mean(p)))
		fp.write("Fine-grained MSE on DecisionTreeRegressor REGRESSION is {p}\n".format(p = np.mean((ftest_X - test_y)**2)))

		fp.write('\n')