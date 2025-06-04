# 2025년 백엔드 파트 챌린지 세션

## 요구사항

이 프로젝트는 Django와 Django REST framework를 사용하여 간단한 게시판 API 서버를 구현하는 챌린지입니다.

### 필수 구현 사항

1. 사용자 관리
   - 회원가입 (POST /api/users/, name='user-registration')
   - 로그인 (POST /api/users/login/, name='user-login')
   - 로그아웃 (POST /api/users/logout/, name='user-logout')
   - 세션 기반 인증 사용

2. 게시글 관리
   - 게시글 목록 조회 (GET /api/articles/, name='article-list')
   - 게시글 상세 조회 (GET /api/articles/{id}/, name='article-detail')
   - 게시글 작성 (POST /api/articles/, name='article-list')
   - 게시글 수정 (PUT /api/articles/{id}/, name='article-detail')
   - 게시글 삭제 (DELETE /api/articles/{id}/, name='article-detail')
   - 게시글 작성/수정 시 썸네일 이미지 첨부 가능

3. 댓글 관리
   - 댓글 목록 조회 (GET /api/articles/{article_id}/comments/, name='article-comments-list')
   - 댓글 작성 (POST /api/articles/{article_id}/comments/, name='article-comments-list')
   - 댓글 수정 (PUT /api/articles/{article_id}/comments/{id}/, name='article-comments-detail')
   - 댓글 삭제 (DELETE /api/articles/{article_id}/comments/{id}/, name='article-comments-detail')

4. drf-yasg를 사용한 API 문서화
    - https://drf-yasg.readthedocs.io/en/stable/
    - Swagger UI: /swagger/ (name='schema-swagger-ui')
    - ReDoc: /redoc/ (name='schema-redoc')
    - OpenAPI Schema: /swagger.json/ (name='schema-json')

## 개발 시 참고 사항

1. Django REST framework의 기본적인 기능들을 활용하여 구현합니다.
   - Serializers
   - ViewSets
   - Permissions
   - Authentication
   - File Upload

2. 코드 작성 시 다음 사항들을 고려합니다.
   - REST API 설계 원칙 준수
   - 적절한 HTTP 메서드 사용
   - 상태 코드의 올바른 사용
   - 에러 처리
   - 파일 업로드 처리

3. 테스트 코드 작성 시 고려사항
   - 각 API 엔드포인트에 대한 단위 테스트 작성
   - 인증이 필요한 API에 대한 테스트
   - 권한 검사에 대한 테스트
   - 예외 상황에 대한 테스트
   - 파일 업로드 테스트

## 프로젝트 구조

```
challenge_backend_2025/
├── config/                 # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user/                   # 사용자 관련 앱
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── article/               # 게시글 관련 앱
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── comment/               # 댓글 관련 앱
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── media/                # 업로드된 파일 저장
│   └── thumbnails/
├── manage.py
└── README.md
```

## 모델 / 테이블 명세

1. User 모델
   - username: 문자열, 고유값
   - password: 문자열
   - email: 문자열, 고유값
   - created_at: DateTimeField
   - updated_at: DateTimeField

2. Article 모델
   - title: 문자열
   - content: TextField
   - thumbnail: ImageField (선택적)
   - author: User 모델과 ForeignKey 관계
   - created_at: DateTimeField
   - updated_at: DateTimeField

3. Comment 모델
   - content: TextField
   - article: Article 모델과 ForeignKey 관계
   - author: User 모델과 ForeignKey 관계
   - created_at: DateTimeField
   - updated_at: DateTimeField

## API 명세

### 사용자 API
- POST /api/users/ (name='user-registration')
  - 회원가입
  - Request Body: {username, password, email}
  - Response: 201 Created

- POST /api/users/login/ (name='user-login')
  - 로그인
  - Request Body: {username, password}
  - Response: 200 OK

- POST /api/users/logout/ (name='user-logout')
  - 로그아웃
  - Response: 204 No Content

### 게시글 API
- GET /api/articles/ (name='article-list')
  - 게시글 목록 조회
  - Response: 200 OK
  - 응답 데이터: 게시글 목록 (제목, 작성자, 작성일, 댓글 수, 썸네일 URL)

- GET /api/articles/{id}/ (name='article-detail')
  - 게시글 상세 조회
  - Response: 200 OK
  - 응답 데이터: 게시글 상세 정보 (제목, 내용, 작성자, 작성일, 수정일, 썸네일 URL)

- POST /api/articles/ (name='article-list')
  - 게시글 작성
  - Request Body: multipart/form-data
    - title: 문자열 (필수)
    - content: 문자열 (필수)
    - thumbnail: 이미지 파일 (선택)
  - Response: 201 Created

- PUT /api/articles/{id}/ (name='article-detail')
  - 게시글 수정
  - Request Body: multipart/form-data
    - title: 문자열 (필수)
    - content: 문자열 (필수)
    - thumbnail: 이미지 파일 (선택)
  - Response: 200 OK

- DELETE /api/articles/{id}/ (name='article-detail')
  - 게시글 삭제
  - Response: 204 No Content

### 댓글 API
- GET /api/articles/{article_id}/comments/ (name='article-comments-list')
  - 댓글 목록 조회
  - Response: 200 OK

- POST /api/articles/{article_id}/comments/ (name='article-comments-list')
  - 댓글 작성
  - Request Body: {content}
  - Response: 201 Created

- PUT /api/articles/{article_id}/comments/{id}/ (name='article-comments-detail')
  - 댓글 수정
  - Request Body: {content}
  - Response: 200 OK

- DELETE /api/articles/{article_id}/comments/{id}/ (name='article-comments-detail')
  - 댓글 삭제
  - Response: 204 No Content

## test를 통한 검증 방법

1. 테스트 실행
```bash
python manage.py test
```

2. 특정 앱의 테스트만 실행
```bash
python manage.py test user
python manage.py test article
python manage.py test comment
```

각 API 엔드포인트에 대한 테스트는 다음 사항들을 검증합니다:
- 정상적인 요청에 대한 응답
- 잘못된 요청에 대한 에러 처리
- 인증이 필요한 API에 대한 접근 제어
- 권한 검사 (작성자만 수정/삭제 가능)
- 데이터 유효성 검사
- 파일 업로드 처리
