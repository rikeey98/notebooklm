# 📒 notebooklm 개발 문서

## 프로젝트 개요

notebooklm은 프로젝트, 노트북, 소스(Source) 등 다양한 정보를 관리할 수 있는 Django 기반 백엔드 시스템입니다. 사용자별로 프로젝트와 노트북을 생성하고, 각 노트북에 다양한 소스 데이터를 연결하여 관리할 수 있습니다. 또한, 대량의 소스 데이터를 효율적으로 삭제할 수 있는 bulk delete API를 제공합니다.

---

## 주요 모델 구조

- **User**: Django 기본 사용자 모델
- **Project**: 사용자가 생성하는 프로젝트 단위
- **Notebook**: 프로젝트 내에서 생성되는 노트북 단위
- **Source**: 노트북에 연결되는 데이터 소스(문서, 파일 등)
- **NotebookMap**: 노트북과 소스의 매핑 테이블
- **SourceMetadata**: 소스의 메타데이터(태그, 내용 등)
- **SourceSummary**: 소스의 요약 정보
- **Output**: 프로젝트/노트북별 결과 데이터

---

## API 엔드포인트 요약

### 1. 기본 엔드포인트

- `/api/projects/` : 프로젝트 CRUD
- `/api/notebooks/` : 노트북 CRUD
- `/api/sources/` : 소스 CRUD
- `/api/source-metadata/` : 소스 메타데이터 조회
- `/api/source-summary/` : 소스 요약 CRUD
- `/api/outputs/` : 결과 데이터 CRUD

### 2. Bulk Delete API (주요 기능)

#### 엔드포인트
```
DELETE /api/sources/bulk_delete/
```

#### 지원 파라미터 (한 번에 하나만!)
- `project_id` : 해당 프로젝트의 모든 소스 삭제
- `notebook_id` : 해당 노트북의 모든 소스 삭제
- `user_id` : 해당 사용자가 생성한 모든 소스 삭제

#### 사용 예시
- 프로젝트 기준 삭제:
  ```
  DELETE /api/sources/bulk_delete/?project_id=1
  ```
- 노트북 기준 삭제:
  ```
  DELETE /api/sources/bulk_delete/?notebook_id=2
  ```
- 사용자 기준 삭제:
  ```
  DELETE /api/sources/bulk_delete/?user_id=3
  ```

#### 응답 예시
```json
{
  "deleted": 5
}
```

#### 에러 예시
- 파라미터가 없거나 2개 이상일 때:
```json
{
  "error": "project_id, notebook_id, user_id 중 하나는 필수입니다."
}
```
또는
```json
{
  "error": "한 번에 하나의 파라미터만 허용됩니다."
}
```

#### 주의사항
- 반드시 **DELETE** 메서드로 호출해야 합니다.
- `/api/sources/bulk_delete/` (끝에 `/` 포함)로 요청해야 합니다.
- 한 번에 하나의 파라미터만 허용되며, 여러 개 입력 시 400 에러가 반환됩니다.
- 서버 코드 수정 후에는 반드시 서버를 재시작해야 새로운 엔드포인트가 반영됩니다.

#### 확장성 및 안전장치
- title로 삭제 등 추가 기능 확장 가능(실수 방지 로직 필요)
- 대량 삭제 시 삭제 전 개수/목록 확인, 로그 기록 등 안전장치 도입 권장

---

## 개발 환경 및 실행 방법

### 1. 개발 환경
- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite (기본)

### 2. 프로젝트 실행 방법

1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 마이그레이션 적용
   ```bash
   python manage.py migrate
   ```
3. 개발 서버 실행
   ```bash
   python manage.py runserver
   ```

### 3. 관리자 계정 생성(선택)
```bash
python manage.py createsuperuser
```

---

## API 테스트 방법

### 1. curl 예시
```bash
# 프로젝트 id=1의 모든 소스 삭제
curl -X DELETE "http://localhost:8000/api/sources/bulk_delete/?project_id=1"

# notebook id=2의 모든 소스 삭제
curl -X DELETE "http://localhost:8000/api/sources/bulk_delete/?notebook_id=2"

# user id=3의 모든 소스 삭제
curl -X DELETE "http://localhost:8000/api/sources/bulk_delete/?user_id=3"
```

### 2. Postman 예시
- Method: DELETE
- URL: `http://localhost:8000/api/sources/bulk_delete/?project_id=1` (또는 notebook_id, user_id)
- Body: 없음

---

## 모델 관계 다이어그램 (텍스트)

- User 1 --- N Project
- Project 1 --- N Notebook
- Project 1 --- N Source
- Notebook 1 --- N NotebookMap N --- 1 Source
- Source 1 --- 1 SourceMetadata
- Source 1 --- 1 SourceSummary
- Output: Project, Notebook, User와 연결

---

## 주요 코드 설명

### 1. BulkDeleteSourceView (core/views.py)
```python
class BulkDeleteSourceView(APIView):
    def delete(self, request):
        project_id = request.query_params.get('project_id')
        notebook_id = request.query_params.get('notebook_id')
        user_id = request.query_params.get('user_id')
        params = [p for p in [project_id, notebook_id, user_id] if p is not None]
        if len(params) == 0:
            return Response({'error': 'project_id, notebook_id, user_id 중 하나는 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(params) > 1:
            return Response({'error': '한 번에 하나의 파라미터만 허용됩니다.'}, status=status.HTTP_400_BAD_REQUEST)
        count = 0
        with transaction.atomic():
            if project_id is not None:
                count, _ = Source.objects.filter(project_id=project_id).delete()
            elif notebook_id is not None:
                from .models import NotebookMap
                source_ids = NotebookMap.objects.filter(notebook_id=notebook_id).values_list('source_id', flat=True)
                count, _ = Source.objects.filter(id__in=source_ids).delete()
            elif user_id is not None:
                count, _ = Source.objects.filter(create_user_id=user_id).delete()
        return Response({'deleted': count}, status=status.HTTP_200_OK)
```

### 2. URL 등록 (core/urls.py)
```python
urlpatterns = router.urls + [
    path('oracle-insert/', OracleInsertView.as_view(), name='oracle-insert'),
    path('sources/bulk_delete/', BulkDeleteSourceView.as_view(), name='bulk-delete-source'),
]
```

---

## 향후 개발/확장 제안
- title로 소스 삭제 기능 추가 시, 삭제 전 미리 삭제될 목록/개수 확인 기능 도입
- 대량 삭제 시 관리자 승인, 로그 기록 등 안전장치 강화
- 프론트엔드에서 삭제 전 사용자 재확인(confirmation) UI 구현
- 삭제된 데이터 복구 기능(soft delete 등) 고려

---

## 문의 및 기여
- 추가 문의, 버그 제보, 기여는 프로젝트 관리자 또는 이슈 트래커를 이용해 주세요. 