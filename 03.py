import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

# 1. movie.csv 파일에서 감독이름 빈 리스트에 담기
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 테스트를 위한 변수 i
    # i = 0

    # 1-1. 감독이름(peopleNm) 담을 빈 리스트 생성
    peopleNm_lists = []

    # 1-2. 한줄씩 읽어 리스트에 담기
    for row in reader:
        # i += 1
        peopleNm_lists.append(row['peopleNm'])
        """
        # 요청 수 절약을 위한 구문
        if i == 5:
            break
        """
# peopleNm_lists에 잘 담기나 확인
# pprint(peopleNm_lists)

######

# 상세정보를 담을 딕셔너리
result = {}

# 2. url을 호출하여 상세정보 요청하기
for peopleNm_list in peopleNm_lists:
    
    # 2-1. url에 들어갈 키와 요청 parameter -> 영화인명
    key = config('API_KEY')
    peopleNm = peopleNm_list

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={peopleNm}'

    # 2-2. 받은 상세정보를 저장
    detail_data = requests.get(url).json()

    # 잘 받았는지 확인
    # pprint(detail_data)

    # 2-3. 필요한 정보(영화인 코드, 영화인명, 분야, 필모리스트)까지 접근 후 재저장
    people_lists = detail_data.get('peopleListResult').get('peopleList')

    # 잘 접근했는지 확인
    # pprint(people_lists)

    # 2-3.
    # people_lists는 리스트 내부에 딕셔너리가 포함되어 있는 형태
    # 빈딕셔너리에 값을 할당하기 위해 0번째 인덱스만 가져와 완전한 딕셔너리 형태로 변환
    people_dicts = people_lists[0]

    # pprint(people_dicts)

    # 2-4. 딕셔너리에 넣기
    for people_dict in people_dicts:
        # 감독의 이름을 key로 가지는 딕셔너리 내부에, 필요정보들을 가지는 딕셔너리를 생성
        result[peopleNm_list] = {
            'peopleCd': people_dicts.get('peopleCd'),
            'peopleNm': people_dicts.get('peopleNm'),
            'repRoleNm': people_dicts.get('repRoleNm'),
            'filmoNames': people_dicts.get('filmoNames')
        }

# result 딕셔너리 확인
# pprint(result)

# 3. result 딕셔너리를 director.csv을 생성하여 저장
with open('director.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        writer.writerow(value)
