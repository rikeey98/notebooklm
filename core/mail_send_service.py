import os
from pymongo import MongoClient
from django.conf import settings

# MongoDB 연결 정보는 환경변수 또는 settings.py에서 가져오세요.
# 예시: settings.MONGODB_URI, settings.MONGODB_DB_NAME
# 반드시 settings.py에 아래와 같이 추가:
# MONGODB_URI = 'mongodb://localhost:27017/'
# MONGODB_DB_NAME = 'notebooklm'

def save_mail_to_mongodb(title, content, recipients):
    """
    메일 정보를 MongoDB에 저장합니다.
    :param title: 메일 제목 (str)
    :param content: 메일 본문 (str)
    :param recipients: 수신자 리스트 또는 콤마로 구분된 문자열
    :return: 저장된 document의 id
    """
    mongodb_uri = getattr(settings, 'MONGODB_URI', 'mongodb://localhost:27017/')
    db_name = getattr(settings, 'MONGODB_DB_NAME', 'notebooklm')
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db['mails']

    # recipients가 문자열이면 리스트로 변환
    if isinstance(recipients, str):
        recipients = [r.strip() for r in recipients.split(',') if r.strip()]

    doc = {
        'title': title,
        'content': content,
        'recipients': recipients
    }
    result = collection.insert_one(doc)
    client.close()
    return str(result.inserted_id) 