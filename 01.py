import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

# 필요한 상세정보를 담을 빈 딕셔너리 생성
result = {}

# 1. url을 호출하여 상세정보 요청하기
# 기간: 50주
for i in range(50):

    # 1-1. url에 들어갈 키와 요청 parameter -> 주간박스오피스 및 날짜 처리
    key = config('API_KEY')
    # 2019년 7월 13일을 기준으로 1주일씩 과거의 데이터를 확인
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    # url이 원하는 날짜 형식으로 변환
    targetDt = targetDt.strftime('%Y%m%d')

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={key}&targetDt={targetDt}'
    
    # 1-2. 받은 상세정보를 저장
    api_data = requests.get(url).json()

    # pprint(api_data)

    # 1-3. 필요한 정보(영화코드, 영화명, 누적관객수)까지 접근 후 재저장
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    
    # pprint(movies)

    # 1-4. 딕셔너리에 넣기
    for movie in movies:
        code = movie.get('movieCd')
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
        # 그게 가장 마지막 주 자료다. 즉, 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
        if code not in result: 
            # 영화 코드명을 key로 가지는 딕셔너리 내부에, 필요정보들을 가지는 딕셔너리를 생성
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }

# pprint(result)

# 2. result 딕셔너리를 boxoffice.csv을 생성하여 저장
with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        # print(value)
        writer.writerow(value)
