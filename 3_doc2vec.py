import json, pymongo, requests, sys
import time, dateutil.parser
import gensim, logging, os
from konlpy.tag import Twitter; t = Twitter()
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='review' + '.log')
pos = lambda d: ['/'.join(p) for p in t.pos(d)]

# class LSGenerator(object):
# 	def __init__(self, collname):
# 		self.conn = pymongo.MongoClient("mongodb://localhost")
# 		self.db = self.conn.watcha
# 		self.cnames = self.db.collection_names()
# 		self.collections = dict()
# 		self.collname = collname

# 		for cname in self.cnames:
# 			self.collections[cname] = eval('self.db.' + cname)

# 		del self.collections['reviews']
# 		del self.collections['system.indexes']

# 	def __iter__(self):
# 		for row in self.collections[self.collname].find():
# 			rating = row['rating']
# 			cid = row['comment_id']
# 			text = row['text']
# 			pos_text = pos(text)
# 			tags = [str(rating) + '_' + str(cid) + '_' + self.collname]
# 			yield gensim.models.doc2vec.TaggedDocument(words = pos_text, tags = tags)

class LSGenerator(object):
	def __init__(self, collname):
		self.conn = pymongo.MongoClient("mongodb://localhost")
		self.db = self.conn.watcha
		self.cnames = self.db.collection_names()
		self.collections = dict()
		self.collname = collname

		for cname in self.cnames:
			self.collections[cname] = eval('self.db.' + cname)

		del self.collections['reviews']
		del self.collections['system.indexes']

	def __iter__(self):
		for cname in self.collections.keys():
			for row in self.collections[cname].find():
				rating = row['rating']
				cid = row['comment_id']
				text = row['text']
				pos_text = pos(text)
				tags = [str(rating) + '_' + str(cid) + '_' + cname]
				yield gensim.models.doc2vec.TaggedDocument(words = pos_text, tags = tags)

documents = LSGenerator('comedy')
cnames = documents.collections.keys()

# for cname in cnames:
# 	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename=cname + '.log')
# 	documents = LSGenerator(cname)
# 	model = gensim.models.doc2vec.Doc2Vec(size=300, workers=8, alpha=0.025, min_alpha=0.025)
# 	model.build_vocab(documents)

# 	for epoch in range(31):
# 		documents = LSGenerator(cname)
# 		model.train(documents)
# 		model.alpha = model.alpha * 0.8
# 		model.min_alpha = model.alpha
# 		model.save('D:\watcha_models\{cname}_epoch_'.format(cname = cname) + str(epoch) + '.model')
# 	model.init_sims(replace=True)
# 	model.save('D:\watcha_models\{cname}.model'.format(cname = cname))

# for cname in cnames:
# 	documents = LSGenerator(cname)
# 	model = gensim.models.doc2vec.Doc2Vec(size=300, workers=8)
# 	model.build_vocab(documents)
# 	model.train(documents)
# 	model.save('D:\watcha_models\{cname}.model'.format(cname = cname))

model = gensim.models.doc2vec.Doc2Vec(size=300, workers=8)
model.build_vocab(documents)
model.train(documents)
model.save('D:\watcha_models\{cname}.model'.format(cname = 'reviews'))