import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

result = {}

for i in range(50):
    key = config('API_KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    # url이 원하는 날짜 형식으로 변환
    targetDt = targetDt.strftime('%Y%m%d')

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={key}&targetDt={targetDt}'
    api_data = requests.get(url).json()
    # pprint(api_data)

    # 주간/주말 박스오피스 데이터 리스트로 가져오기.
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    # pprint(movies)

    # 영화 대표코드 / 영화명 / 누적관객수

    # 영화정보가 담긴 딕셔너리에서 영화 대표 코드를 추출

    for movie in movies:
        code = movie.get('movieCd')
        # pprint(code)
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
        # 그게 가장 마지막 주 자료다. 즉, 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
        if code not in result: 
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
            # pprint(result)
# pprint(movies)


with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        # print(value)
        writer.writerow(value)
