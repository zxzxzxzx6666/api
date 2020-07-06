from flask_restful import Resource , reqparse 
import pymysql
from flask import jsonify, make_response

#讀post資料 
parser = reqparse.RequestParser() #設定欄位的白名單（防止sql injection）
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

# 帶入Resource才會啟用api方法
class Users(Resource): #被 flask01 引用的class 
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
        sql = 'select * from user where deleted = False;'
        cursor.execute(sql) #檢查語法
        users = cursor.fetchall() #拿到dict
        db.close()
        return jsonify(users) #拿到json

    def post(self): #使用post 回應567
        # return '567'
        db ,cursor = self.db_init() #拿到資料庫連線
        arg = parser.parse_args() # .parse_args() 將post的資料轉成Dict 
        user = {
            'name' : arg['name'],
            'gender' : arg['gender'],
            'birth' : arg['birth'] or '1900-01-01',
            'note' : arg['note'],
        }
        sql =  '''
        INSERT INTO `test`.`user` (`name`, `gender`, `birth` , `note`) 
        VALUES ('{}', '{}', '{}', '{}');
        '''.format(user['name'] ,user['gender'] ,user['birth'] ,user['note'] )

        result = cursor.execute(sql)#測試語法
        db.commit() #成功後進行insert
        db.close()
        # respose = {'code':200 , 'msg': "sucess"}
        respose = {'msg': "sucess"}
        code = 201 #狀態
        if result == 0:
            respose['msg'] = "error"
            code = 400 #狀態
        return make_response(jsonify(respose),code) #將第一個參數回傳到頁面，第二個回傳狀態

class User(Resource): #被 flask01 引用的class 
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
        sql = 'select * from user where id = {} and deleted = False;'.format(id) #拿到id這個變數
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
        UPDATE `test`.`user`
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
            'name' : arg['name'],
            'gender' : arg['gender'],
            'birth' : arg['birth'] or '1900-01-01',
            'note' : arg['note'],
        }
        
        # update邏輯（有些欄位不一定會post過來）
        query = []
        for key , value in user.items():
            if value != None:
                query.append(key + " = " + " '{}' ".format(value))
        query = " , ".join(query)

        sql = '''
        UPDATE `test`.`user`
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
    #軟刪除實務做法會加上 @時間


    
        

