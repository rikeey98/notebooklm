import os
from django.conf import settings

# 환경변수 세팅 (프로젝트 루트에 instantclient, oracle_config 폴더가 있다고 가정)
INSTANT_CLIENT_PATH = os.path.join(settings.BASE_DIR, 'instantclient')
TNS_ADMIN_PATH = os.path.join(settings.BASE_DIR, 'oracle_config')
os.environ['PATH'] = INSTANT_CLIENT_PATH + os.pathsep + os.environ.get('PATH', '')
os.environ['TNS_ADMIN'] = TNS_ADMIN_PATH

import cx_Oracle

def insert_data_to_oracle(param1, param2):
    conn = cx_Oracle.connect(settings.ORACLE_DSN, settings.ORACLE_USER, settings.ORACLE_PASSWORD)
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO my_table (col1, col2) VALUES (:1, :2)", (param1, param2))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def select_data_from_oracle(query, dsn, user, password, params=None):
    conn = cx_Oracle.connect(user, password, dsn)
    try:
        cur = conn.cursor()
        cur.execute(query, params or {})
        columns = [col[0] for col in cur.description]
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        return results
    finally:
        cur.close()
        conn.close() 