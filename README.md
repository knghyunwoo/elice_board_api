# My Flask Project

## 서버 실행 방법

```bash
# python 프로젝트 가상 환경 폴더 생성
python -m venv python-env
# 프로젝트 가상 환경 접속
source python-env/bin/activate
# 가상환경이랑 같은 requirements 설치
pip install -r requirements.txt
# 서버를 그냥 실행
python launcher.py
# 서버를 gunicorn으로 뒤에서 실행
gunicorn launcher:app -Db 0.0.0.0:5000
# gunicorn이 몇번째 pid로 실행중인지 확인
ps -ef | grep gunicorn
# 서버를 다시 실행시 gunicorn이 실행되고 있는 pid를 죽임
kill -9 gunicorn_pid
```

## Installation

```bash
git clone https://kdt-gitlab.elice.io/knghyunwoo/my-flask-project.git
```



## 과제 설명 (구현한 API)

### 완전 기본루트

```
@app.route('/')
```
를 서버가 잘연결되었는지를 확인하기 위해 만들었습니다.<br>


## 과제1

User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.<br>
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.<br>
Logout API : 현재 로그인 된 유저를 로그아웃합니다.<br>

### SignUp
```
@app.route('/auth/register', methods=['POST'])
```
### LOGIN
```
@app.route('/auth/login', methods=['POST'])
```
### LOGOUT
```
@app.route('/auth/logout')
```
<br>

## 과제2

Board APIs - 게시판 CRUD

Create API : name 을 입력받아 새로운 게시판을 만듭니다.<br>
Read API : 현재 등록된 게시판 목록을 가져옵니다.<br>
Update API : 기존 게시판의 name 을 변경합니다.<br>
Delete API : 특정 게시판을 제거합니다. <br>

### READ
```
def get(self)
```
### CREATE
```
def post(self)
```
### UPDATE
```
def put(self)
```
### DELETE
```
def delete(self)
```

## 과제3

BoardArticle APIs - 게시판 글 CRUD

Create API : title, content 를 입력받아 특정 게시판(board)에 새로운 글을 작성합니다.<br>
Read API : 게시판의 글 목록을 가져오거나, 특정 게시판(board)에 글의 내용을 가져옵니다.<br>
Update API : 게시판 글의 title, content를 변경합니다.<br>
Delete API : 특정 게시판 글을 제거합니다.<br>

### READ
```
def get(self, board_id=None, board_article_id=None)
```
### CREATE
```
def post(self, board_id)
```
### UPDATE
```
def put(self, board_id=None, board_article_id=None)
```
### DELETE
```
def delete(self, board_id=None, board_article_id=None)
```

## 과제4
Dashboard APIs

RecentBoardArticle API : 모든 게시판에 대해 각각의 게시판의 가장 최근 n 개의 게시판 글의 title 을 가져옵니다. <br>
(k 개의 게시판이 있다면 최대 k * n 개의 게시판 글의 title 을 반환합니다.)

```
@app.route('/recentarticle', methods=['POST'])
```
