import re
from flask import Flask, render_template, request, url_for, redirect, session
import pyrebase
import json


with open(r"auth/firebase.json") as f:  # 파이어베이스 주소
    config = json.load(f)

firebase = pyrebase.initialize_app(config)  # 파이어베이스 초기화 및 연동 완료
db = firebase.database()  # 파이어베이스 사용 준비 끝

# db에 저장하는 방법
# signin = {"id": "abc", "pwd": 12356}
# db.child("user").child("good").set(signin)

# 임시로 저장된 아이디와 비빌먼호 (나중에는 데이터베이스에 저장된 id, 비밀번호로 교체됨)
ID = "hello"  # 임시 아이디
PW = "123"  # 임시 비밀번호


app = Flask(__name__)
app.secret_key = "asfasdfsdagdfhsa"  # 시크릿 키

# 대문 페이지


@app.route("/")
def index():
    return render_template("door.html")  # door.html 열러


# 지역 세부 페이지
@app.route("/regions", methods=['GET'])
def move_regions():
    return render_template("regions.html")  # regions.html 로 열려


# 로그인 페이지
@app.route("/login")
def login():
    if "uid" in session:  # 세션안에 유저 아이디가 있을 경우  (= 로그인 상태 유지 on)
        # 로그인 페이지 눌러도 대문페이지로 보냄
        return render_template("door.html", login=True)
    else:  # 세션안에 유저 아이디가 없는 경우 (로그인이 안되어있는 상태)
        return render_template("login.html")  # 로그인 안되어있으면 로그인 페이지로 가


# 로그인 확인 함수
@app.route("/login_done", methods=['POST'])
def login_done():
    global ID, PW  # 임시 아이디, 비밀번호 등록
    uid = request.form['uid']  # login.html에서 받아온 아이디 값
    pwd = request.form['pwd']  # login.html에서 받아온 비밀번호 값

    if ID == uid and PW == pwd:  # login.html에서 받아온 아이디, 비밀번호가   임시 아이디, 비밀번화가 일치할 경우
        session["uid"] = uid  # 세션에 아이디 정보를 저장함
        return redirect(url_for("index"))  # 대문 페이지로 가

    else:  # 아이디, 비밀번호가 일치하지 않을 경우
        return redirect(url_for("login"))  # 로그인 페이지로 가


# 로그아웃
@app.route("/log_out", methods=['get'])
def login_out():
    session.pop("uid")  # 세션에 아이디 정보를 삭제
    return redirect(url_for("index", login=False))
    # 대문 페이지로 가, login =False 값을 index.html에 전달함


# 회원가입
@app.route("/join", methods=['POST'])
def join():
    receive_uid = request.form['uid']  # join.html에서 id에 입력한 값을 가져옴
    receive_pwd = request.form['pwd']  # join.html에서 pwd에 입력한 값을 가져옴
    pass  # 미완성


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
