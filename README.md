pjt_01

## 1. 프로젝트 목표

- #### '영화진흥위원회'의 Open API를 활용하여 테이터를 수집 및 가공

- #### Python 코드를 이용하여 .csv 파일 생성



## 2. 코드 설명

### 2.1 `01.py`

#### 2.1.1 목표

- ##### 50주간의 박스오피스 데이터(영화코드, 영화명, 누적관객수)를 저장하여 boxoffice.csv파일에 저장

  

#### 2.1.2 준비 사항

- ##### API 사이트: 영화진흥위원회 오픈 API

- ##### `http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do`

- ##### 주간 상영영화를 조회하기 위한 기본 요청 URL

  `http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json`



#### 2.1.3  코딩 절차

- ##### 주간/주말 박스오피스 `url`을 `requests`와 `json`으로 불러와 변수에 저장

  ```python
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
  ```

- ##### 영화의 코드, 영화명, 누적관객수를 추출

  ```python
  # 1-3. 필요한 정보(영화코드, 영화명, 누적관객수)까지 접근 후 재저장
  movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
  ```

- ##### 빈 딕셔너리에 코드, 영화명, 관객수를 넣어준다.

  - ### &#128680; 시행착오

    - ##### 반복문을 돌릴 때 영화코드와 조건식을 이용하여 중복되지 않게 처리하는 방법

      ```python
      # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어간다면,
      # 그게 마지막 주 자료이다. 즉, 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
      if code not in result:
      # result 라는 딕셔너리에 code에 해당하는 키가 없을 경우에만 if문을 들어간다.
      ```

  ```python
  # 2. result 딕셔너리를 boxoffice.csv을 생성하여 저장
  with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
      fieldnames = ('movieCd', 'movieNm', 'audiAcc')
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for value in result.values():
          # print(value)
          writer.writerow(value)
  ```

  - #### `boxoffice.csv` Image

  ![boxoffice](https://user-images.githubusercontent.com/52814897/61593002-06ce8800-ac15-11e9-842a-1518edc6f96e.PNG)








### 2.2 `02.py`

#### 2.1.1 목표

- ##### `01.py` 에서 저장한 `boxoffice.csv`을 읽는 방법을 코딩

- ##### `boxoffice.csv`에서 읽은 `영화 코드`와 오픈 api를 이용하여 상세정보를 호출

- ##### 호출된 정보에서 필요한 데이터를 뽑아  `movie.csv`에 생성/저장

  

#### 2.1.2 준비 사항

- ##### `영화 코드`로 상세정보를 조회하기 위한 기본 요청 URL

  ` http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json`



#### 2.1.3  코딩 절차

- ##### `01.py`에서 생성한 `boxoffice.csv`파일 열고 읽기

  ```python
  # 1. boxoffice.csv 파일에서 영화 코드 읽기
  with open('boxoffice.csv', newline='', encoding='utf-8') as f:
      reader = csv.DictReader(f)
  ```

- ##### `영화코드` 를 리스트에 저장

  ```python
  # 1-1. 영화코드(movieCd) 담을 빈 리스트 생성
  movieCd_lists = []
  
  # 1-2. 한줄씩 읽어 리스트에 담기
  for row in reader:
      # 리스트에 하나씩 담음
      movieCd_lists.append(row['movieCd'])
  ```

- ##### 리스트에 담긴 `영화코드` 개수 만큼 반복하면서 상세 정보 요청하기

  ```python
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
  
  ```

- ##### 딕셔너리에 필요한 정보를 담아준다.(영화코드, 영화면 국문, 영문, 등급, 개봉연도, 상영시간, 장르, 감독)

  - ### &#128680; 시행착오

    - ##### 딕셔너리 내부에 조건표현식 처리하기

      ```python
      # 리스트가 비어있는 경우를 처리하기 위한 조건표현식.
      <참일 경우의 결과> if <조건식> else <거짓일 경우의 결과>
      
      'watchGradeNm': movie_infos.get('audits')[0].get('watchGradeNm') if movie_infos.get('audits') else None, 
      ```

      

  ```python
  # 2-3. 필요한 정보(영화코드, 영화명 국문, 영문, 원문, 등급, 개봉연도, 상영시간, 장르, 감독)
  #      접근 후 저장
  movie_infos = detail_data.get('movieInfoResult').get('movieInfo')
  
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
  ```

- ##### csv 파일 생성/저장

  ```python
  # 3. result 딕셔너리를 movie.csv을 생성하여 저장
  with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
      fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genres', 'peopleNm')
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for value in result.values():
          writer.writerow(value)
  ```

  - #### `movie.csv` Image

![movie](https://user-images.githubusercontent.com/52814897/61593019-37aebd00-ac15-11e9-824d-2aaac37cdc54.PNG)





### 2.3 `03.py`

#### 2.3.1 목표

- ##### `02.py`에서 저장한 `movie.csv`에서 감독의 이름을 읽어 상세 정보 호출

- ##### 호출된 정보를 이용하여 감독에 대한 정보를 담은 `director.csv`파일 생성



#### 2.3.2 준비 사항

- ##### `영화인명`으로 조회하기 위한 기본 요청 URL

  ` http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json `



#### 2.3.2 코딩 절차

- ##### `02.py` 에서 만든 `movie.csv` 파일에서 `감독이름` 빈 리스트에 담기

  ```python
  # 1. movie.csv 파일에서 감독이름 빈 리스트에 담기
  with open('movie.csv', newline='', encoding='utf-8') as f:
       reader = csv.DictReader(f)
       # 1-1. 감독이름(peopleNm) 담을 빈 리스트 생성
       peopleNm_lists = []
          
       # 1-2. 한줄씩 읽어 리스트에 담기
       for row in reader:
           peopleNm_lists.append(row['peopleNm'])
  ```

- ##### `감독이름` 개수 만큼 반복하며 상세 정보 요청

  ```python
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
  
      # 2-3. 필요한 정보(영화인 코드, 영화인명, 분야, 필모리스트)까지 접근 후 재저장
      people_lists = detail_data.get('peopleListResult').get('peopleList')
  ```

- ### &#128680; 시행착오

  - ##### 리스트 안에 딕셔너리가 들어가 있을 경우 key:value 값 사용방법

    ```python
    # 2-3.
    # people_lists는 리스트 내부에 딕셔너리가 포함되어 있는 형태
    # 빈딕셔너리에 값을 할당하기 위해 0번째 인덱스만 가져와 완전한 딕셔너리 형태로 변환
    people_dicts = people_lists[0]
    ```

- ##### 딕셔너리에 정보 담기

  ```python
  # 2-4. 딕셔너리에 넣기
  for people_dict in people_dicts
      # 감독의 이름을 key로 가지는 딕셔너리 내부에, 필요정보들을 가지는 딕셔너리를 생성
      result[peopleNm_list] = {
          'peopleCd': people_dicts.get('peopleCd'),
          'peopleNm': people_dicts.get('peopleNm'),
          'repRoleNm': people_dicts.get('repRoleNm'),
          'filmoNames': people_dicts.get('filmoNames')
      }
  ```

- ##### csv 파일 생성/저장

  ```python
  # 3. result 딕셔너리를 director.csv을 생성하여 저장
  with open('director.csv', 'w', encoding='utf-8', newline='') as f:
      fieldnames = ('peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames')
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for value in result.values():
          writer.writerow(value)
  ```

  - #### `director.csv ` Image

![director](https://user-images.githubusercontent.com/52814897/61593032-56ad4f00-ac15-11e9-9332-1a5b0ad67011.PNG)

