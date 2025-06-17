import cx_Oracle
from django.conf import settings

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