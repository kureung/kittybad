import re
from flask import Flask, render_template, request, url_for, redirect, session
import pyrebase
import json


with open(r"auth/firebase.json") as f:  # 파이어베이스 주소
    config = json.load(f)

firebase = pyrebase.initialize_app(config)  # 파이어베이스 초기화 및 연동 완료
db = firebase.database()  # 파이어베이스 사용 준비 끝

# db에 저장하는 방법
# information = {"id": "abc", "pwd": 12356}
# db.child("user").child("good").set(signin)


app = Flask(__name__)
app.secret_key = "asfasdfsdagdfhsa"  # 시크릿 키


# 대문 페이지
@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")  # index.html(대문 페이지)을 열어


# 지역 세부 페이지
@app.route("/regions", methods=['GET'])
def move_regions():
    return render_template("regions.html")  # regions.html(지역 세부페이지)을 열어


# 로그인 페이지
@app.route("/login")
def login():
    if "uid" in session:  # 세션안에 유저 아이디가 있을 경우  (= 로그인이 유지가 된 상태)
        return render_template("index.html", login=True)
        # 로그인 페이지로 접속해도 강제적으로 대문페이지로 보냄

    else:  # 세션안에 유저 아이디가 없는 경우 (로그인이 안되어있는 상태)
        return render_template("login.html")  # 로그인 안되어있으면 로그인 페이지로 가


# 로그인 기능
@app.route("/login_done", methods=['POST'])
def login_done():
    uid = request.form['uid']  # login.html(로그인 페이지)에서 받아온 아이디 값
    pwd = request.form['pwd']  # login.html(로그인 페이지)에서 받아온 비밀번호 값
    users = db.child('users').get().val()  # 데이터베이스에서 유저 id 값들을 딕셔너리형태로 반환
    if users == None:   # 데이터베이스에 유저 id 값이 아무것도 없을 경우
        return redirect(url_for('login'))  # 로그인 페이지로 머물러있어

    else:  # 데이터베이스에 유저 id 값이 아무거나 한개라도 있을 경우
        try:  # 예외 처리  (try의 내부 코드들을 실행하고 에러 발생시 except의 내부 코드 실행)

            # 데이터베이스안에 있는 id 값 중에서 로그인 페이지에 받아온 id 값이 있는지 없는지 비교. 없으면 에러가 발생하고 'excetp'로 넘어감. 있으면 userinfo 변수에 id 값아 저장되고 if 문으로 넘어감
            userinfo = users[uid]
            if userinfo['pwd'] == pwd:  # 유저 id 값의 비밀번호가 맞는지 안맞는지 비교
                # 비밀번호가 일치하면 세션에 유저 아이디 정보를 넣어서 로그인 상태로 유지시킴
                session['uid'] = uid

                # 로그인 완료 했으니 index.html(대문페이지)로 보냄
                return redirect(url_for('index'))

            else:  # 비밀번호가 일치하지 않을 경우
                return redirect(url_for('login'))  # 로그인 페이지에 계속 머무르게 함
        except:  # 에러 발생시 작동    # 로그인 페이지에서 입력한 id 값이 데이터베이스에 없을 경우 에러가 남.
            return redirect(url_for('login'))  # 로그인 페이지에 계속 머무르게 함


# 아이디 중복확인
@app.route("/id_duplic", methods=['POST'])
def id_duplic():
    pass

    # 로그아웃


@app.route("/log_out", methods=['get'])
def login_out():
    session.pop("uid")  # 세션에 아이디 정보를 삭제
    return redirect(url_for("index"))
    # 대문 페이지로 가, login =False 값을 index.html에 전달함


# 회원가입 페이지
@app.route("/signup")
def signup():
    return render_template("/signup.html")


# 회원가입 기능
@app.route("/signup_done", methods=['POST'])
def signup_done():
    uid = request.form['uid']  # join.html에서 id에 입력한 값을 가져옴
    pwd = request.form['pwd']  # join.html에서 pwd에 입력한 값을 가져옴
    email = request.form['email']  # join.html에서 email에 입력한 값을 가져옴
    name = request.form['name']  # join.html에서 name에 입력한 값을 가져옴

    information = {
        "pwd": pwd,
        'email': email,
        'name': name
    }

    users = db.child('users').get().val()  # 데이터베이스에서 유저 id 값들을 딕셔너리형태로 반환

    if users == None:  # 데이터 베이스에 아무것도 없을 경우
        db.child("users").child(uid).set(information)  # 데이터 베이스에 아이디 및 개인정보 추가
        return redirect(url_for("index"))  # 회원가입 완료했으면 index 페이지로 가
    else:  # 데이터 베이스에 아무 자료라도 있을 경우
        for i in users:  # 데이터베이스에 있는 모든 유저 id 값을 한개씩 i 값에 대입
            if uid == i:  # 데이터베이스에 있는 모든 유저 id 갑 중에서 회원가입하려는 id 값이 있을 경우
                return redirect(url_for("signup"))  # 회원 가입 페이지에 그대로 유지
            else:  # 데이터 베이스에 있는 모든 유저 id 값 중에서 회원가입하려는 id 값이 없을 경우
                db.child("users").child(uid).set(
                    information)  # 데이터베이스에 아이디 및 개인정보 추가
                return redirect(url_for("index"))  # 회원 가입 완료했으니 index 페이지로 가


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
