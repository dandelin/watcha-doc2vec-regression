#-*- coding:utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask.ext.restful import reqparse, abort, Api, Resource
from sklearn import linear_model
from sklearn.externals import joblib
import gensim, re
import numpy as np
from konlpy.tag import Twitter; t = Twitter()
pos = lambda d: ['/'.join(p) for p in t.pos(d)]

app = Flask(__name__)
api = Api(app)
model = gensim.models.doc2vec.Doc2Vec.load('{cname}.model'.format(cname = 'reviews'))
rs = model.random.get_state()
review_rmodel = joblib.load('{cname}.pkl'.format(cname = 'reviews'))
parser = reqparse.RequestParser()
parser.add_argument('query', type=unicode)

def over_filter(x):
    if x > 5: return 5.0
    elif x < 0.5: return 0.5
    else: return x

class Predict(Resource):
    global rs
    def post(self):
        args = parser.parse_args()
        print args
        s = args['query']
        p = pos(s)
        print p
        model.random.set_state(rs)
        infered = model.infer_vector(p)
        print np.sum(infered)
        preds = review_rmodel.predict(infered.reshape(1, -1))
        return over_filter(preds[0])

api.add_resource(Predict, '/predict')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7333)