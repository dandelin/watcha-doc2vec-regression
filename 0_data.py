from requests_futures.sessions import FuturesSession
import json, pymongo, requests, os, sys
import time, dateutil.parser

conn = pymongo.MongoClient("mongodb://localhost")
db = conn.watcha
c_reviews = db.reviews
c_reviews.drop()
c_reviews.create_index('comment_id', unique=True)

def fetchMovieCodes(path, category_idx):
	cookies = {
		'_guinness_session': 'your session here',
		'_guit': 'here too'
	}
	s = requests.Session()
	api_format = 'https://watcha.net/evalmore/category.json?page={page}&per=24&category_idx={category_idx}'
	index = 1
	json_hs = json.loads(s.get(api_format.format(page=str(index), category_idx=category_idx), cookies=cookies).content)
	while json_hs['cards'] != []:
		with open(path, 'a') as fp:
			for card in json_hs['cards']:
				item = card['items'][0]['item']
				fp.write(item['code'] + ',' + item['title_url'] + '\n')
		index += 1
		json_hs = json.loads(s.get(api_format.format(page=str(index), category_idx=category_idx), cookies=cookies).content)


def fetchReviews(unique_id):

	s = FuturesSession()
	
	# Hand shake proc. to figure out how many calls we send to server
	api_format = 'https://watcha.net/comment/list?unique_id={unique_id}&start_index={start_index}&count=10&type=like'
	handshake = api_format.format(unique_id=unique_id, start_index=str(0))
	hs = s.get(handshake).result().content
	json_hs = json.loads(hs)
	total_count = int(json_hs['meta']['total_count'])
	how_many_queries = total_count / 10 + 1

	query_urls = [api_format.format(unique_id=unique_id, start_index=str(i * 10)) for i in xrange(0, how_many_queries, 1)]
	reviews = [
		{
			'movie_title': r['movie_title'],
			'rating': r['rating'],
			'text': r['text'],
			'updated_at': time.mktime(dateutil.parser.parse(r['updated_at']).timetuple()),
			'comment_id': r['comment_id']
		}
		for qu in query_urls
		for r in json.loads(s.get(qu).result().content)['data']
	]
	return reviews

def insertReviews(collection, reviews):
	for review in reviews:
		collection.insert(review)

def processCategory():
	categories = os.listdir('categories')
	for category in categories:
		collection = db[category.split('.')[0]]
		collection.create_index('comment_id', unique=True)
		with open(os.path.abspath('categories/' + category), 'r') as fp:
			code_names = [line.strip().split(',') for line in fp.readlines()]
		for code_name in code_names[24:]:
			with open('log.txt', 'a') as fp:
				try:
					print 'fetching reviews of movie {movie_name} in {category}'.format(movie_name=code_name[1], category=category)
					fp.write('fetching reviews of movie {movie_name} in {category}\n'.format(movie_name=code_name[1], category=category))
					reviews = fetchReviews(code_name[0])
					print 'insert reviews of movie {movie_name} in {category}'.format(movie_name=code_name[1], category=category)
					fp.write('insert reviews of movie {movie_name} in {category}\n'.format(movie_name=code_name[1], category=category))
					insertReviews(collection, reviews)
				except:
					print 'error {error} occured while processing movie {movie_name} in {category}'.format(movie_name=code_name[1], category=category, error=sys.exc_info()[0])
					fp.write('error {error} occured while processing movie {movie_name} in {category}\n'.format(movie_name=code_name[1], category=category, error=sys.exc_info()[0]))


# a = fetchReviews('mmliep')
# fetchMovieCodes('comedy.txt', '38')
processCategory()