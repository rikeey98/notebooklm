# 📒 notebooklm 전체 API 개발 문서

## 프로젝트 개요

notebooklm은 프로젝트, 노트북, 소스(Source) 등 다양한 정보를 관리할 수 있는 Django 기반 백엔드 시스템입니다. 사용자별로 프로젝트와 노트북을 생성하고, 각 노트북에 다양한 소스 데이터를 연결하여 관리할 수 있습니다. 또한, 대량의 소스 데이터를 효율적으로 삭제할 수 있는 bulk delete API 등 다양한 기능을 제공합니다.

---

## 공통 사항
- 모든 API는 기본적으로 `/api/` prefix를 가집니다.
- 대부분의 엔드포인트는 RESTful하게 동작합니다.
- 인증/권한 처리는 프로젝트 설정에 따라 다를 수 있습니다(기본은 인증 필요).
- 모든 예시는 기본적으로 `localhost:8000` 기준입니다.

---

## 1. 프로젝트(Project)
### 엔드포인트
```
/api/projects/
```
### 지원 메서드
- GET: 전체/단일 프로젝트 조회
- POST: 프로젝트 생성
- PUT/PATCH: 프로젝트 수정
- DELETE: 프로젝트 삭제

### 파라미터 및 예시
#### 1) 전체 프로젝트 조회
```
GET /api/projects/
```
- 쿼리 파라미터: `user_id` (해당 사용자의 프로젝트만 조회)
- 예시: `/api/projects/?user_id=1`

#### 2) 단일 프로젝트 조회
```
GET /api/projects/{id}/
```

#### 3) 프로젝트 생성
```
POST /api/projects/
{
  "name": "프로젝트명",
  "description": "설명",
  "user": 1
}
```

#### 4) 프로젝트 수정
```
PUT /api/projects/{id}/
{
  "name": "수정된 프로젝트명",
  ...
}
```

#### 5) 프로젝트 삭제
```
DELETE /api/projects/{id}/
```

---

## 2. Jira 설정(JiraConfig)
### 엔드포인트
```
/api/jira-configs/
```
### 지원 메서드
- GET: 전체/단일 Jira 설정 조회 (project로 필터 가능)
- POST: 생성
- PUT/PATCH: 수정
- DELETE: 삭제

### 예시
- `/api/jira-configs/?project=1` (특정 프로젝트의 Jira 설정만 조회)

---

## 3. 메일 설정(MailConfig)
### 엔드포인트
```
/api/mail-configs/
```
### 지원 메서드 및 예시
- GET: 전체/단일 조회 (`project`로 필터 가능)
- POST: 생성
- PUT/PATCH: 수정
- DELETE: 삭제

---

## 4. 노트북(Notebook)
### 엔드포인트
```
/api/notebooks/
```
### 지원 메서드 및 예시
- GET: 전체/단일 조회 (`user_id`, `project_id`로 필터 가능)
- POST: 생성
- PUT/PATCH: 수정
- DELETE: 삭제

#### 예시
- `/api/notebooks/?user_id=1&project_id=2`

---

## 5. 소스(Source)
### 엔드포인트
```
/api/sources/
```
### 지원 메서드
- GET: 전체/단일 소스 조회 (여러 필터 지원)
- POST: 소스 생성
- PUT/PATCH: 소스 수정
- DELETE: 소스 삭제

### GET 파라미터
- `user_id`: 해당 사용자가 생성한 소스만 조회
- `project`: 해당 프로젝트의 소스만 조회
- `notebook`: 해당 노트북에 연결된 소스만 조회
- `title`: 소스 제목에 특정 단어가 포함된 소스만 조회

#### 예시
- `/api/sources/?user_id=1`
- `/api/sources/?project=2`
- `/api/sources/?notebook=3`
- `/api/sources/?title=검색어`

### POST 예시
```
POST /api/sources/
{
  "title": "소스 제목",
  "project": 1,
  "create_user": 1,
  "notebook": 2,  // 연결할 노트북 id
  "tag": ["태그1", "태그2"],
  "content": "소스 내용"
}
```

### 상세 조회
```
GET /api/sources/{id}/
```
- metadata, summary 등 상세 정보 포함

---

## 6. 노트북-소스 매핑(NotebookMap)
### 엔드포인트
```
/api/notebook-maps/
```
### 지원 메서드 및 예시
- GET: 전체/단일 조회
- POST: 생성 (노트북과 소스 연결)
- PUT/PATCH: 수정
- DELETE: 삭제

---

## 7. 소스 메타데이터(SourceMetadata)
### 엔드포인트
```
/api/source-metadata/
```
### 지원 메서드
- GET: 전체/단일 소스 메타데이터 조회 (읽기 전용)

---

## 8. 소스 요약(SourceSummary)
### 엔드포인트
```
/api/source-summary/
```
### 지원 메서드
- GET: 전체/단일 소스 요약 조회
- POST: 생성
- PUT/PATCH: 수정
- DELETE: 삭제

---

## 9. 결과 데이터(Output)
### 엔드포인트
```
/api/outputs/
```
### 지원 메서드
- GET: 전체/단일 결과 조회 (`user`, `project`, `notebook`으로 필터 가능)
- POST: 생성
- PUT/PATCH: 수정
- DELETE: 삭제

#### 예시
- `/api/outputs/?user=1&project=2&notebook=3`

---

## 10. 유저(User)
### 엔드포인트
```
/api/users/
```
### 지원 메서드
- GET: 전체/단일 유저 조회 (읽기 전용)

---

## 11. 오라클 데이터 삽입
### 엔드포인트
```
/api/oracle-insert/
```
### 지원 메서드
- POST: 오라클 DB에 데이터 삽입

#### 요청 예시
```
POST /api/oracle-insert/
{
  "param1": "값1",
  "param2": "값2"
}
```
- param1, param2는 필수

#### 응답 예시
- 성공: `{ "result": "success" }`
- 실패: `{ "error": "에러 메시지" }`

---

## 12. 소스 Bulk Delete (대량 삭제)
### 엔드포인트
```
DELETE /api/sources/bulk_delete/
```
### 지원 파라미터 (한 번에 하나만!)
- `project_id` : 해당 프로젝트의 모든 소스 삭제
- `notebook_id` : 해당 노트북의 모든 소스 삭제
- `user_id` : 해당 사용자가 생성한 모든 소스 삭제

#### 사용 예시
- `/api/sources/bulk_delete/?project_id=1`
- `/api/sources/bulk_delete/?notebook_id=2`
- `/api/sources/bulk_delete/?user_id=3`

#### 응답 예시
```
{
  "deleted": 5
}
```

#### 에러 예시
```
{
  "error": "project_id, notebook_id, user_id 중 하나는 필수입니다."
}
```
또는
```
{
  "error": "한 번에 하나의 파라미터만 허용됩니다."
}
```

---

## 13. 기타 참고 사항
- 모든 엔드포인트는 Django REST Framework의 표준 규칙을 따릅니다.
- GET: 목록/상세 조회, POST: 생성, PUT/PATCH: 수정, DELETE: 삭제
- 필터링 파라미터는 쿼리스트링으로 전달
- 상세한 필드 정보는 `/api/{엔드포인트}/schema/` 또는 Swagger 등 API 문서화 도구로 확인 가능

---

## 14. 예시: 전체 API 흐름
1. 사용자 생성(관리자)
2. 프로젝트 생성
3. 노트북 생성 (프로젝트에 연결)
4. 소스 생성 (노트북, 프로젝트, 사용자 연결)
5. 소스 메타데이터/요약 자동 생성
6. 결과 데이터 생성 및 조회
7. 필요시 소스 대량 삭제

---

## 15. 모델 관계 다이어그램 (텍스트)
- User 1 --- N Project
- Project 1 --- N Notebook
- Project 1 --- N Source
- Notebook 1 --- N NotebookMap N --- 1 Source
- Source 1 --- 1 SourceMetadata
- Source 1 --- 1 SourceSummary
- Output: Project, Notebook, User와 연결

---

## 16. 개발 환경 및 실행 방법
- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite (기본)

### 실행 방법
1. 의존성 설치: `pip install -r requirements.txt`
2. 마이그레이션: `python manage.py migrate`
3. 서버 실행: `python manage.py runserver`
4. 관리자 계정 생성(선택): `python manage.py createsuperuser`

---

## 17. 문의 및 기여
- 추가 문의, 버그 제보, 기여는 프로젝트 관리자 또는 이슈 트래커를 이용해 주세요. 