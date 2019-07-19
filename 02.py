import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

# 1. boxoffice.csv 파일에서 영화들 코드 읽기
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    i = 0
    
    # movieCd 담을 빈 리스트 하나 생성
    movieCd_lists = []

    # 한줄씩 읽는다.
    for row in reader:
        i += 1
        # 리스트에 하나씩 담음
        movieCd_lists.append(row['movieCd'])
        
        
        # 요청 수 아끼려고 임시로 넣은 break 구문.
        """
        if i == 13:
            break
        """
# movieCd_list에 잘 담겼나 확인.
# pprint(movieCd_list)

#############

# 정보 넣을 딕셔너리
result = {}

# 2. 담은 movieCd로 영화 상세정보 요청하기
for movieCd_list in movieCd_lists:
    key = config('API_KEY')
    movieCd = movieCd_list
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'
    # 요청한 데이터 저장
    detail_data = requests.get(url).json()
    
    # json 요청 잘 되나 확인
    # pprint(detail_data)

    # 상세정보까지 접근 후 저장
    movie_infos = detail_data.get('movieInfoResult').get('movieInfo')
    # 잘 접근했나 확인
    pprint(movie_infos)

    # 딕셔너리에 넣기
    for movie_info in movie_infos:

        result[movieCd_list] = {
            'movieCd': movie_infos.get('movieCd'),
            'movieNm': movie_infos.get('movieNm'),
            'movieNmEn': movie_infos.get('movieNmEn'),
            'movieNmOg': movie_infos.get('movieNmOg'),
            'watchGradeNm': movie_infos.get('audits')[0].get('watchGradeNm') if movie_infos.get('audits') else None, 
            'openDt': movie_infos.get('openDt'),
            'showTm': movie_infos.get('showTm'),
            'genres': movie_infos.get('genres')[0].get('genreNm'),
            'peopleNm': movie_infos.get('directors')[0].get('peopleNm') if movie_infos.get('directors') else None,
        }
        
# result 딕셔너리 잘 들어갔나 확인
# pprint(result)


with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genres', 'peopleNm')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        # print(value)
        writer.writerow(value)

