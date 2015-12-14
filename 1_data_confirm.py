import json, pymongo, requests, os, sys
import time, dateutil.parser

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
cnames = db.collection_names()
collections = dict()

for cname in cnames:
	collections[cname] = eval('db.' + cname)

del collections['reviews']
del collections['system.indexes']

for cname in collections.keys():
	print cname, collections[cname].count()