import flask
from flask_restful import Api , Resource
from resources.user import Users ,User
from resources.account import Accounts ,Account
import pymysql
from flask import request , jsonify  #不是取得api而是取得使用者傳給我們的資料
app = flask.Flask(__name__) # 將api server 存進一個變數
app.config['DEBUG'] = True # debug 參數
api = Api(app) # 引入api 並將 api server 帶入
api.add_resource(Users , "/users") # 帶入自定義的Class(帶有Resource) 並定義網址 
api.add_resource(User , "/user/<id>") # 將id這個變數傳到自定義的class User中，直接定義在def get(self ,id): 中
# 練習account
api.add_resource(Accounts , "/accounts") 
api.add_resource(Account , "/account/<id>")

#錯誤訊息回應在網頁上（上線時一定要加） 在開發的時候可以拿掉
# @app.errorhandler(Exception)#若Exception有東西產生（有錯誤）就會執行
# def handle(error):
#     code = 500
#     if type(error).__name__ == 'NotFound':
#         code = 404
#     return{
#         'msg':type(error).__name__
#     },401

@app.before_request#接觸api前會跑一次
def auth():
    # 開發常用密碼套件 json web token (pip install jwt) 密碼產生驗證套件 產出字串
    token = request.headers.get('auth')#找到header裡面的值來驗證
    if token == '567':
        pass
    else:
        return {
            'msg': 'invalid token',
            # 'code': 401 # 可以設定在外面 會直接回應狀態
        },401



@app.route('/', methods = ['GET']) # 直接執行下面的函式
def home():
    return "hello world"

@app.route('/cool', methods = ['GET']) # 直接執行下面的函式
def cool():
    return "so cool"

#重構
def get_account(account_number):
    db = pymysql.connect( #資料庫連線
            '10.147.17.41',
            'adminer',
            'Pn123456',
            'test'
        ) 
    cursor = db.cursor(pymysql.cursors.DictCursor) #DictCursor 回應dict而不是tuple
    #查詢原本多少錢並修正
    sql  = """
    select * from account where account_number = {};
    """.format(account_number)
    cursor.execute(sql)
    account = cursor.fetchone()
    return db , cursor ,account

#存錢
@app.route('/account/<account_number>/deposit', methods = ['post']) # 直接執行下面的函式
def deposit(account_number):
        db , cursor ,account = get_account(account_number)
        money = request.values["money"]
        balance = account["balance"] + int(money)

        sql  = """
        UPDATE `test`.`account`
        SET balance = {}
        WHERE account_number = {};
        """.format(balance,account_number)
        result = cursor.execute(sql) #檢查語法
        db.commit() #成功後進行insert
        db.close()

        respose = {'code':200 , 'msg': "sucess"}
        if result == 0:
            respose['msg'] = "error"
        return jsonify(respose) #拿到json
#領錢
@app.route('/account/<account_number>/withdraw', methods = ['post']) # 直接執行下面的函式
def withdraw(account_number):
        db , cursor ,account = get_account(account_number)
        money = request.values["money"]
        balance = account["balance"] - int(money)

        if balance < 0 :
            respose = {'code':400 , 'msg': "not enough"}
            return jsonify(respose) #拿到json

        sql  = """
        UPDATE `test`.`account`
        SET balance = {}
        WHERE account_number = {};
        """.format(balance,account_number)
        result = cursor.execute(sql) #檢查語法
        db.commit() #成功後進行insert
        db.close()

        respose = {'code':200 , 'msg': "sucess"}
        if result == 0:
            respose['msg'] = "error"
        return jsonify(respose) #拿到json

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 80)