import pymysql
from flask import Flask, request, jsonify, session
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api(app)

#데이터베이스 연결, azure mysql로 데이터베이스를 설정하였습니다.
db = pymysql.connect( 
        user = 'knghyunwoo@elice-api',
        passwd = 'iAMJENIUS1',
        host = 'elice-api.mysql.database.azure.com',
        db = 'elice_db',
        charset = 'utf8'
    )
cursor = db.cursor()

parser = reqparse.RequestParser()

#완전 기본루트
@app.route('/')
def abc():
    return """
        If you want to 
        1. Signup, please add /auth/register
        2. Login, please add /auth/login
        3. Logout, please add /auth/logout    
    """

"""
과제 1
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.
"""

# session을 위한 secret_key 설정
app.config.from_mapping(SECRET_KEY='dev')
#SIGNUP
@app.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']        
        error = None

        # 아이디가 없다면?
        if not fullname:
            error = 'fullname이 유효하지 않습니다.'
        # 비밀번호가 없다면?
        elif not password:
            error = 'Password가 유효하지 않습니다.'
        # 이메일이 없다면?
        elif not email:
            error = 'email이 유효하지 않습니다.'

        # 에러가 발생하지 않았다면 회원가입 실행
        if error is None:
            cursor.execute(
                'INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)',
                (fullname, email, generate_password_hash(password))
            )
            db.commit()

        return "Success You are now registered"

#LOGIN
@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        sql = "SELECT * FROM user WHERE email = (%s)"
        cursor.execute(sql, (email))
        user = cursor.fetchone()

        # print(user)

        # 입력한 유저의 정보가 없을 때
        if user is None:
            error = '등록되지 않은 계정입니다.'
        elif not check_password_hash(user[3], password): #3번째 인덱스가 비밀번호입니다.
            error = 'password가 틀렸습니다.'

        # 정상적인 정보를 요청받았다면?
        if error is None:
            # 로그인을 위해 기존 session을 비웁니다.
            session.clear()
            # 지금 로그인한 유저의 정보로 session을 등록합니다.
            session['user_id'] = user[0] #0번째 인덱스가 user_id 값입니다.
            
            return "Success You are now logged in"
        
        return error

#LOGOUT
@app.route('/auth/logout')
def logout():
    try:
        session.clear()
        return "logout success"
    except:
        return "logout failed"


"""
과제 2
Board APIs - 게시판 CRUD

Create API : name 을 입력받아 새로운 게시판을 만듭니다.
Read API : 현재 등록된 게시판 목록을 가져옵니다.
Update API : 기존 게시판의 name 을 변경합니다.
Delete API : 특정 게시판을 제거합니다.
"""

parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('writerid')

class Board(Resource):
    #READ
    def get(self): # board 테이블과 user 테이블을 조인해서 user에 있는 fullname 즉 작성자도 같이 출력했습니다.
        sql = """SELECT board.id, board.name, user.fullname, board.create_date  
                FROM elice_db.board
                inner join user
                where board.writerid = user.id;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)
        
    #CREATE
    def post(self):
        args = parser.parse_args()
        sql = "INSERT INTO `board` (name, writerid) VALUES (%s, %s)"
        cursor.execute(sql, (args['name'], args["writerid"]))
        db.commit()
        
        return jsonify(status = "success", result = {"name": args["name"], "writerid" : args["writerid"]})
        
    #UPDATE
    def put(self):
        args = parser.parse_args()
        sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
        cursor.execute(sql, (args['name'], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"], "name": args["name"]})
    
    #DELETE
    def delete(self):
        args = parser.parse_args()
        sql = "DELETE FROM `board` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

# API Resource 라우팅을 등록!
api.add_resource(Board, '/board')

"""
과제 3
BoardArticle APIs - 게시판 글 CRUD

Create API : title, content 를 입력받아 특정 게시판(board)에 새로운 글을 작성합니다.
Read API : 게시판의 글 목록을 가져오거나, 특정 게시판(board)에 글의 내용을 가져옵니다.
Update API : 게시판 글의 title, content를 변경합니다.
Delete API : 특정 게시판 글을 제거합니다.
"""
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('content')
parser.add_argument('board_id')


class BoardArticle(Resource):
    #READ
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            sql = "SELECT * FROM `boardArticle` WHERE `id`=%s"
            cursor.execute(sql, (board_article_id,))
            result = cursor.fetchone()
        else:
            sql = "SELECT * FROM `boardArticle` WHERE `board_id`=%s"
            cursor.execute(sql, (board_id,))
            result = cursor.fetchall()
            
        return jsonify(status = "success", result = result)

    #CREATE
    def post(self, board_id):
        args = parser.parse_args()
        sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['title'], args['content'], args['board_id']))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"]})
        
    #UPDATE    
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "UPDATE `boardArticle` SET title = %s, content = %s WHERE `id` = %s"
        cursor.execute(sql, (args['title'], args["content"], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"], "content": args["content"]})
        
    #DELETE
    def delete(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

# API Resource 라우팅을 등록!
api.add_resource(BoardArticle, '/board', '/board/<board_id>', '/board/<board_id>/<board_article_id>')


"""
과제 4
Dashboard APIs
RecentBoardArticle API : 모든 게시판에 대해 각각의 게시판의 가장 최근 n 개의 게시판 글의 title 을 가져옵니다. 
(k 개의 게시판이 있다면 최대 k * n 개의 게시판 글의 title 을 반환합니다.)
"""

@app.route('/recentarticle', methods=['POST'])
def recentarticle():
    if request.method == 'POST':
        amount = request.form['amount']
        amount = amount[0] 

        sql = "select id from board"
        cursor.execute(sql)
        result = cursor.fetchall()

        boardids = []
        for i in range(len(result)):
            boardids.append(result[i][0])  #현재 갖고있는 boardid를 다 받아서 리스트로 변환시킵니다.

        ans = []
        # print(boardids)
        for i in range(len(result)):
            sql = f"SELECT title FROM boardarticle where board_id = {boardids[i]} limit {amount};"
            cursor.execute(sql)
            result = cursor.fetchall()
            ans.append(result)

        print(ans)

        return jsonify(status = "success", result = ans)
    
    return "Error try again please"

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)