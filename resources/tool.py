import pymysql

def query(user): 
    query = []
    for key , value in user.items():
        if value != None:
            query.append(key + " = " + " '{}' ".format(value))
    query = " , ".join(query)
    return query

def sqlselectone_Number(table,key,value):
    db = pymysql.connect( #資料庫連線
        '10.147.17.41',
        'adminer',
        'Pn123456',
        'test'
    ) 
    cursor = db.cursor(pymysql.cursors.DictCursor) #DictCursor 回應dict而不是tuple
    sql  = """
    select * from {} where {} = {};
    """.format(table,key,value)
    cursor.execute(sql)
    onedict = cursor.fetchone()
    db.close()
    return onedict

def sqlupdate(table,postdict):
    db = pymysql.connect( #資料庫連線
        '10.147.17.41',
        'adminer',
        'Pn123456',
        'test'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    # update邏輯（有些欄位不一定會post過來）
    query = []
    for key , value in postdict.items():
        if value != None:
            query.append(key + " = " + " '{}' ".format(value))
    query = " , ".join(query)

    sql = '''
    UPDATE {}
    SET {}
    WHERE id = {};
    '''.format(table,query,id)
    
    result = cursor.execute(sql)#測試語法
    db.commit() #成功後進行insert
    db.close()

def sqldelete():
    pass

def sqlinsert():
    pass

def response200():
    pass
