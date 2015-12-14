#-*- coding:utf-8 -*-
import requests

url = 'http://localhost:12111/predict'
queries = [u"최고였음",
		u"불량식품과도 같은 영화, 자극적이어서 재밌지만 시간이 지나고 나니 엉성함이 느껴진다. 하지만 이병헌의 카리스마를 보는것 만으로도 충분히 볼만하다.",
		u"말초신경을 간질거리며 우아하고 묵직하게 나아가는 카메라 워킹. 굉장했다",
		u"잘 만들어진 칵테일 처럼 여러 요소를 복합적으로 다루는 칵테일 요법같은 영화",
		u"'프란시스 하'에 그대로 이어지는 듯한 '프란시스트리스 아메리카'.  노아 바움백과 그레타 거윅의 협업을 시리즈처럼 계속 보고 싶다."]
for q in queries:
	query = {'query': q}
	r = requests.post(url, data=query)
	print r.text,