# 🐥 구방문방구(9roomdroom9) Project

- 앞뒤가 똑같은 구방문방구를 팀명으로 팀원들의 물건을 재미있게 판매하는 서비스 홈페이지 구현
- [배민문방구](https://brandstore.baemin.com/) 홈페이지를 클론 코딩하며 기본적인 user flow를 구현하는 것이 목표
- 메인 회원가입/로그인 상품리스트 상세페이지 장바구니 + 검색기능 구현
- aws 이용한 배포까지 완료
  - [구방문방구 홈페이지](http://44.202.159.187:8000/)

### 🐥 구방문방구 개발 인원 및 기간

- 프로젝트 기간 : 2022.07.18 ~ 2022.07.29

- 개발 인원 : 프론트 3명, 백엔드 2명<br>
[Front-end](https://github.com/wecode-bootcamp-korea/35-1st-9roomdroom9-frontend) : 엄성훈, 김광희, 정예빈<br>
[Back-end](https://github.com/wecode-bootcamp-korea/35-1st-9roomdroom9-backend) : 이정훈, 음정민

### 🐥 구방문방구 Back-end
- [이정훈](https://github.com/fkelfk)
  - 로그인
  - 회원가입
  - 장바구니
  - 상품검색
- [음정민](https://github.com/J-EUM)
  - 상품리스트(메인, 전체, 카테고리별)
    - 정렬
    - 페이지네이션
  - 상품상세
  - 상품검색

### 🐥 Database Modeling

![image](https://user-images.githubusercontent.com/97498663/182018590-ed9a4a30-9a79-475b-b85e-544d536922dd.png)


  
### 🐥 적용 기술

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white">
<img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=flat-square&logo=Amazon%20AWS&logoColor=white"/>


### 🐥 구현페이지

#### 메인화면

- 메인 슬라이드 이미지와 Nav,Footer로 디자인을 완성했습니다.

`메인화면 gif올리기`

- component를 사용하여 코드의 가독성과 재활용성을 높였다.
- map함수로 메인페이지의 반복적이고 동일한 레이아웃을 데이터를 일일이 적지않도록 하였다.
- useState로 상품 데이터를 props로 불러와 각각 다른 데이터를 가져올 수 있도록 작업하였다.
- fetch를 사용하여 백엔드 서버에서 데이터를 받아와 Best,New, Green(친환경)상품이 나올 수 있도록 구현하였다.

#### 상품 리스트 화면

`상품 리스트 화면 gif올리기`

#### 로그인 화면

`로그인 화면 gif올리기`

#### 회원가입 화면

`회원가입 화면 gif올리기`



### 🐥 협업 툴

<img src="https://img.shields.io/badge/trello-0052CC?style=flat-square&logo=trello&logoColor=white"> <img src="https://img.shields.io/badge/slack-4A154B?style=flat-square&logo=slack&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/notion-000000?style=flat-square&logo=notion&logoColor=white">

- Git & GitHub : 각 페이지마다 branch를 생성하여 관리하였습니다.

- Trello : 각자 맡은 구현부분을 티켓으로 만들어 진행 상황을 공유하였습니다.
  - Backlog: 프로젝트 기간동안 완료해야할 티켓(프로젝트 기간이 짧기 때문에 추가구현사항은 따로 이름을 붙이고 필수사항 위주로 구현)
  - To-Do(This Sprint): 이번 스프린트(1주일 간격)동안 완료해야할 티켓
  - In-Progress: 진행중인 작업들
  - In-Review(PR): 깃허브에 PR을 올리고 리뷰, merge 대기중인 완료작업들
  - Connection(F-B): 백엔드-프론트엔드 통신이 완료된 작업
  - Done(Merge): merge가 완료된 작업들
  
- Notion : 팀 노션 페이지를 만들어 회의록, 진행상황, api명세서 등을 공유하였습니다.

- Slack : 팀원들과 소통에 이용했습니다.
  
![image](https://user-images.githubusercontent.com/97498663/182017835-b0f2ec05-9faf-4415-90b7-d51ad7f8fe59.png)




![image](https://user-images.githubusercontent.com/97498663/182017796-2273d423-49fc-4e8e-ae89-5146b25d27c0.png)

![image](https://user-images.githubusercontent.com/97498663/182018151-531dee6a-a204-4b31-9e50-bf368418fcb2.png)

