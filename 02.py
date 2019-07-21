import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

# 1. boxoffice.csv 파일에서 영화 코드 읽기
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 테스트를 위한 변수 i
    # i = 0
    
    # 1-1. 영화코드(movieCd) 담을 빈 리스트 생성
    movieCd_lists = []

    # 1-2. 한줄씩 읽어 리스트에 담기
    for row in reader:
        # i += 1
        # 리스트에 하나씩 담음
        movieCd_lists.append(row['movieCd'])
        
        """
        # 요청 수 적약을 위한 구문
        if i == 1:
            break
        """
# movieCd_list에 잘 담겼나 확인.
# pprint(movieCd_lists)

#############

# 정보 넣을 딕셔너리
result = {}

# 2. 담은 movieCd로 영화 상세정보 요청하기
for movieCd_list in movieCd_lists:
    
    # 2-1. url에 들어갈 키와 요청 parameter -> 영화코드
    key = config('API_KEY')
    movieCd = movieCd_list

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'
    
    # 2-2. 요청한 데이터 저장
    detail_data = requests.get(url).json()
    
    # json 요청 잘 되나 확인
    # pprint(detail_data)

    # 2-3. 필요한 정보(영화코드, 영화명 국문, 영문, 원문, 등급, 개봉연도, 상영시간, 장르, 감독)
    #      접근 후 저장
    movie_infos = detail_data.get('movieInfoResult').get('movieInfo')

    # 잘 접근했나 확인
    # pprint(movie_infos)

    # 2-4. 딕셔너리에 넣기
    for movie_info in movie_infos:
        # 영화 코드명을 key로 가지는 딕셔너리 내부에, 필요정보들을 가지는 딕셔너리를 생성
        result[movieCd_list] = {
            'movieCd': movie_infos.get('movieCd'),
            'movieNm': movie_infos.get('movieNm'),
            'movieNmEn': movie_infos.get('movieNmEn'),
            'movieNmOg': movie_infos.get('movieNmOg'),
            # 리스트가 비어있는 경우를 처리하기 위한 조건표현식.
            'watchGradeNm': movie_infos.get('audits')[0].get('watchGradeNm') if movie_infos.get('audits') else None, 
            'openDt': movie_infos.get('openDt'),
            'showTm': movie_infos.get('showTm'),
            'genres': movie_infos.get('genres')[0].get('genreNm'),
            'peopleNm': movie_infos.get('directors')[0].get('peopleNm') if movie_infos.get('directors') else None,
        }
        
# result 딕셔너리 잘 들어갔나 확인
# pprint(result)

# 3. result 딕셔너리를 movie.csv을 생성하여 저장
with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genres', 'peopleNm')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        writer.writerow(value)
