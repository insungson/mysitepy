import MySQLdb
from django.db import models
# Create your models here.
from mysitepy.settings import DATABASES


def connect():
    try:
# 1. db 연결
        conn = MySQLdb.connect(
            host=DATABASES['default']['HOST'],
            port=int(DATABASES['default']['PORT']),
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            db=DATABASES['default']['NAME'],
            charset='utf8')
        return conn

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None

def fetchone (board):
    try:
        conn = connect()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        # 3. SQL문 실행
        sql = '''
            select title, contents,id
            from board
            where id = '%s'
                ''' % board
        cursor.execute(sql)
        # 4. 결과 받아오기(fetch)
        print(cursor.execute(sql), type(cursor.execute(sql)))
        ## 딕셔너리에 값을 추가하여 출력
        results = cursor.fetchone()
        # 5. 자원 정리
        cursor.close()
        conn.close()
        # 결과 출력
        return results
    # 6. 결과 처리
    except MySQLdb.Error as e:
        print('Error {0}: {1}' % (e.args[0], e.args[1]))
    return None


def fetchall ():
    try:
        conn = connect()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
# 3. SQL문 실행
        sql = '''
                select a.id as id, a.title as title, b.name, a.hit as hit, date_format(a.reg_date, '%Y-%m-%d') as reg_date, a.depth as depth, a.group_no as group_no, a.order_no as order_no
                from board a, user_user b
                where a.user_id = b.id
                order by group_no desc, order_no asc
            '''
        cursor.execute(sql)
    # 4. 결과 받아오기(fetch)
        print(cursor.execute(sql),type(cursor.execute(sql)))
        ## 딕셔너리에 값을 추가하여 출력
        results= cursor.fetchall()
        # 5. 자원 정리
        cursor.close()
        conn.close()
        #결과 출력
        return results
    # 6. 결과 처리
    except MySQLdb.Error as e:
        print('Error {0}: {1}' % (e.args[0], e.args[1]))
    return None


def insert(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행


        sql = '''
            insert 
            into board
            values(null,'%s','%s',0,now(),
            ifnull((select max(group_no) from board as board1),0)+1,group_no + depth - 1,0,'%s')
            '''% board

        count = cursor.execute(sql)

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def delete(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
        delete 
        from board
        where id = '%s'
        ''' % board

        count = cursor.execute(sql)

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))


def hitplus(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행


        sql = '''
                update board
                set hit = hit+%d
                where id = '%s'
                '''% board

        count = cursor.execute(sql)

        # 4. 자원 정리
        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def modifyupdate(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
                update board
                set title = '%s', contents='%s'
                where id = '%s'
                 ''' % board

        count = cursor.execute(sql)

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def modifyreply_info(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
                select group_no, order_no
                from board
                where id = '%s'
                 ''' % board

        cursor.execute(sql)

        results = cursor.fetchone()

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return results

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def update_predata(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
            update board
            set order_no = order_no + 1
            where group_no = '%s'
            and order_no > '%s'
                 ''' % board

        count = cursor.execute(sql)

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def findinfo(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
            select group_no, order_no, depth, user_id
            from board
            where id = '%s'
                 ''' % board

        cursor.execute(sql)

        results = cursor.fetchone()

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return results

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))

def insert_modifyreply(board):
    try:
        conn = connect()
        # 2. 커서 생성

        cursor = conn.cursor()
        # 3. SQL문 실행

        sql = '''
                insert 
                into board
                values(null,'%s','%s',0,now(),'%s','%s','%s','%s')
                 ''' % board

        count = cursor.execute(sql)

        # 4. 자원 정리

        cursor.close()

        conn.commit()

        conn.close()

        # 5. 결과 처리

        return count == 1

    except MySQLdb.Error as e:

        print('Error %d: %d' % (e.args[0], e.args[1]))
