from flask_restful import Resource , reqparse
import pymysql
from flask import jsonify

#讀post資料 
parser = reqparse.RequestParser() #設定欄位的白名單（防止sql injection）
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

# 帶入Resource才會啟用api方法
class Accounts(Resource): #被 flask01 引用的class 
    def db_init(self):
        db = pymysql.connect( #資料庫連線
            '10.147.17.41',
            'adminer',
            'Pn123456',
            'test'
        ) 
        cursor = db.cursor(pymysql.cursors.DictCursor) #DictCursor 回應dict而不是tuple
        return db,cursor

    def get(self): #使用get 回應123
        # return '123'
        db ,cursor = self.db_init() #拿到資料庫連線
        sql = 'select * from account where deleted = False;'
        cursor.execute(sql) #檢查語法
        users = cursor.fetchall() #拿到dict
        db.close()
        return jsonify(users) #拿到json

    def post(self): #使用post 回應567
        # return '567'
        db ,cursor = self.db_init() #拿到資料庫連線
        arg = parser.parse_args() # .parse_args() 將post的資料轉成Dict 
        user = {
            'balance' : arg['balance'] or 0,
            'account_number' : arg['account_number'] or 0,
            'user_id' : arg['user_id'] or 0
        }
        sql =  '''
        INSERT INTO `test`.`account` (`balance`, `account_number`, `user_id` ) 
        VALUES ('{}', '{}', '{}');
        '''.format(user['balance'] ,user['account_number'] ,user['user_id'] )

        result = cursor.execute(sql)#測試語法
        db.commit() #成功後進行insert
        db.close()
        respose = {'code':200 , 'msg': "sucess"}
        if result == 0:
            respose['msg'] = "error"
        return jsonify(respose)

class Account(Resource): #被 flask01 引用的class 
    def db_init(self):
        db = pymysql.connect( #資料庫連線
            '10.147.17.41',
            'adminer',
            'Pn123456',
            'test'
        ) 
        cursor = db.cursor(pymysql.cursors.DictCursor) #DictCursor 回應dict而不是tuple
        return db,cursor

    def get(self, id): #使用get 回應123
        # return '123'
        db ,cursor = self.db_init() #拿到資料庫連線
        sql = 'select * from account where id = {} and deleted = False;'.format(id) #拿到id這個變數
        cursor.execute(sql)#測試語法
        users = cursor.fetchone() #拿到dict
        db.close()
        return jsonify(users) #拿到json

    # def delete(self, id): #使用get 回應123
    #     # return '123'
    #     db ,cursor = self.db_init() #拿到資料庫連線
    #     sql = 'delete from user where id = {}'.format(id) #拿到id這個變數
    #     result = cursor.execute(sql) #檢查語法
    #     db.commit() #成功後進行insert
    #     db.close()

    #     respose = {'code':200 , 'msg': "sucess"}
    #     if result == 0:
    #         respose['msg'] = "error"
    #     return jsonify(respose) #拿到json

    #軟刪除使用update，同時修改 get
    #   實務做法會加上 @時間 deleted預設是 0
    def delete(self, id): #使用delete
        db ,cursor = self.db_init() #拿到資料庫連線
        sql = """
        UPDATE `test`.`account`
        SET deleted = True
        WHERE id = {};
        """.format(id) #拿到id這個變數
        result = cursor.execute(sql) #檢查語法
        db.commit() #成功後進行insert
        db.close()

        respose = {'code':200 , 'msg': "sucess"}
        if result == 0:
            respose['msg'] = "error"
        return jsonify(respose) #拿到json
    
    def patch(self,id): #使用patch (update)
        # return '567'
        db ,cursor = self.db_init() #拿到資料庫連線
        arg = parser.parse_args() # .parse_args() 將post的資料轉成Dict 
        user = {
            'balance' : arg['balance'],
            'account_number' : arg['account_number'],
            'user_id' : arg['user_id'] 
        }
        
        # update邏輯（有些欄位不一定會post過來）
        query = []
        for key , value in user.items():
            if value != None:
                query.append(key + " = " + " '{}' ".format(value))
        query = " , ".join(query)

        sql = '''
        UPDATE `test`.`account`
        SET {}
        WHERE id = {};
        '''.format(query,id)
        
        result = cursor.execute(sql)#測試語法
        db.commit() #成功後進行insert
        db.close()
        respose = {'code':200 , 'msg': "sucess"}
        if result == 0:
            respose['msg'] = "error"
        return jsonify(respose)
    


    
        

