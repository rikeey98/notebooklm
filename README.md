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

### GET 파라미터
| 이름      | 타입   | 필수/옵션 | 설명                       |
|---------|-------|---------|--------------------------|
| user_id | int   | 옵션    | 해당 사용자의 프로젝트만 조회 |

### POST(생성) 파라미터
| 이름        | 타입   | 필수/옵션 | 설명           |
|-----------|-------|---------|----------------|
| name      | str   | 필수    | 프로젝트명      |
| description | str | 옵션    | 설명(빈 값 가능) |
| user      | int   | 필수    | 사용자 id      |

#### 예시
```
POST /api/projects/
{
  "name": "프로젝트명",
  "description": "설명",
  "user": 1
}
```

---

## 2. Jira 설정(JiraConfig)
### 엔드포인트
```
/api/jira-configs/
```
### GET 파라미터
| 이름      | 타입   | 필수/옵션 | 설명                       |
|---------|-------|---------|--------------------------|
| project | int   | 옵션    | 해당 프로젝트의 Jira만 조회 |

### POST(생성) 파라미터
| 이름   | 타입 | 필수/옵션 | 설명         |
|------|-----|---------|------------|
| url  | str | 필수    | Jira URL   |
| project | int | 필수 | 프로젝트 id |

#### 예시
```
POST /api/jira-configs/
{
  "url": "https://jira.example.com",
  "project": 1
}
```

---

## 3. 메일 설정(MailConfig)
### 엔드포인트
```
/api/mail-configs/
```
### GET 파라미터
| 이름      | 타입   | 필수/옵션 | 설명                       |
|---------|-------|---------|--------------------------|
| project | int   | 옵션    | 해당 프로젝트의 메일만 조회 |

### POST(생성) 파라미터
| 이름        | 타입 | 필수/옵션 | 설명         |
|-----------|-----|---------|------------|
| recipients | str | 필수    | 이메일 리스트(콤마 구분) |
| project    | int | 필수    | 프로젝트 id |

#### 예시
```
POST /api/mail-configs/
{
  "recipients": "a@a.com,b@b.com",
  "project": 1
}
```

---

## 4. 노트북(Notebook)
### 엔드포인트
```
/api/notebooks/
```
### GET 파라미터
| 이름        | 타입   | 필수/옵션 | 설명                       |
|-----------|-------|---------|--------------------------|
| user_id   | int   | 옵션    | 해당 사용자의 노트북만 조회 |
| project_id| int   | 옵션    | 해당 프로젝트의 노트북만 조회 |

### POST(생성) 파라미터
| 이름        | 타입   | 필수/옵션 | 설명           |
|-----------|-------|---------|----------------|
| name      | str   | 옵션    | 노트북명(기본값: 'unnamed-notebook') |
| project   | int   | 필수    | 프로젝트 id    |
| create_user | int | 필수    | 사용자 id      |

#### 예시
```
POST /api/notebooks/
{
  "name": "노트북1",
  "project": 1,
  "create_user": 1
}
```

---

## 5. 소스(Source)
### 엔드포인트
```
/api/sources/
```
### GET 파라미터
| 이름      | 타입   | 필수/옵션 | 설명                       |
|---------|-------|---------|--------------------------|
| user_id | int   | 옵션    | 해당 사용자가 생성한 소스만 조회 |
| project | int   | 옵션    | 해당 프로젝트의 소스만 조회 |
| notebook| int   | 옵션    | 해당 노트북에 연결된 소스만 조회 |
| title   | str   | 옵션    | 제목에 특정 단어가 포함된 소스만 조회 |

### POST(생성) 파라미터
| 이름        | 타입     | 필수/옵션 | 설명           |
|-----------|---------|---------|----------------|
| title     | str     | 필수    | 소스 제목(고유) |
| project   | int     | 필수    | 프로젝트 id    |
| create_user | int   | 필수    | 사용자 id      |
| notebook  | int     | 필수    | 연결할 노트북 id|
| content   | str     | 필수    | 소스 내용      |
| tag       | list(str)| 옵션   | 태그 목록(기본값: 빈 리스트) |
| link      | str(URL) | 옵션   | 관련 URL 링크(없으면 null/빈 값) |

#### 예시
```
POST /api/sources/
{
  "title": "소스 제목",
  "project": 1,
  "create_user": 1,
  "notebook": 2,
  "content": "소스 내용",
  "tag": ["태그1", "태그2"],
  "link": "https://example.com"
}
```

- link는 입력하지 않으면 null 또는 빈 값으로 저장됩니다.
- metadata 반환 시 link 필드도 함께 반환됩니다.

---

## 6. 노트북-소스 매핑(NotebookMap)
### 엔드포인트
```
/api/notebook-maps/
```
### POST(생성) 파라미터
| 이름      | 타입 | 필수/옵션 | 설명         |
|---------|-----|---------|------------|
| notebook| int | 필수    | 노트북 id   |
| source  | int | 필수    | 소스 id     |

#### 예시
```
POST /api/notebook-maps/
{
  "notebook": 1,
  "source": 2
}
```

---

## 7. 소스 메타데이터(SourceMetadata)
### 엔드포인트
```
/api/source-metadata/
```
### GET 파라미터
- 없음 (전체/단일 조회만 지원)

---

## 8. 소스 요약(SourceSummary)
### 엔드포인트
```
/api/source-summary/
```
### POST(생성) 파라미터
| 이름    | 타입 | 필수/옵션 | 설명     |
|-------|-----|---------|--------|
| source| int | 필수    | 소스 id |
| summary| str| 필수    | 요약 내용|

#### 예시
```
POST /api/source-summary/
{
  "source": 1,
  "summary": "요약 내용"
}
```

---

## 9. 결과 데이터(Output)
### 엔드포인트
```
/api/outputs/
```
### GET 파라미터
| 이름      | 타입   | 필수/옵션 | 설명                       |
|---------|-------|---------|--------------------------|
| user    | int   | 옵션    | 해당 사용자의 결과만 조회 |
| project | int   | 옵션    | 해당 프로젝트의 결과만 조회 |
| notebook| int   | 옵션    | 해당 노트북의 결과만 조회 |

### POST(생성) 파라미터
| 이름        | 타입 | 필수/옵션 | 설명         |
|-----------|-----|---------|------------|
| project   | int | 필수    | 프로젝트 id |
| create_user | int | 필수  | 사용자 id   |
| notebook  | int | 필수    | 노트북 id   |
| content   | str | 필수    | 결과 내용   |

#### 예시
```
POST /api/outputs/
{
  "project": 1,
  "create_user": 1,
  "notebook": 2,
  "content": "결과 내용"
}
```

---

## 10. 유저(User)
### 엔드포인트
```
/api/users/
```
### GET 파라미터
- 없음 (전체/단일 조회만 지원)

---

## 11. 오라클 데이터 삽입
### 엔드포인트
```
/api/oracle-insert/
```
### POST(생성) 파라미터
| 이름   | 타입 | 필수/옵션 | 설명     |
|------|-----|---------|--------|
| param1| str | 필수    | 값1     |
| param2| str | 필수    | 값2     |

#### 예시
```
POST /api/oracle-insert/
{
  "param1": "값1",
  "param2": "값2"
}
```

---

## 12. 소스 Bulk Delete (대량 삭제)
### 엔드포인트
```
DELETE /api/sources/bulk_delete/
```
### 쿼리 파라미터(한 번에 하나만!)
| 이름        | 타입 | 필수/옵션 | 설명         |
|-----------|-----|---------|------------|
| project_id| int | 옵션    | 해당 프로젝트의 소스 전체 삭제 |
| notebook_id| int| 옵션    | 해당 노트북의 소스 전체 삭제   |
| user_id   | int | 옵션    | 해당 사용자의 소스 전체 삭제   |

- 세 파라미터 중 반드시 하나만 입력해야 하며, 여러 개 입력 시 400 에러 반환

#### 예시
```
DELETE /api/sources/bulk_delete/?project_id=1
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