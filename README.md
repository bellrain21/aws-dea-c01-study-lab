# AWS DEA-C01 Study Lab

> **AWS Certified Data Engineer – Associate DEA-C01** 학습·실습 기록 저장소  
> 상태: `IN PROGRESS`  
> 현재 위치: Foundation 정리 완료 후, S3 저장 구조 학습 및 첫 업로드 실습 준비 단계

---

## 1. 목적

이 저장소의 목적은 AWS 서비스를 나열하거나 문제를 외우는 것이 아님.

```text
AWS DEA-C01 취득
→ 데이터 엔지니어링 기본 역량 증명
→ 데이터 흐름과 서비스 선택 이유를 설명 가능한 상태
```

학습 기준은 아래 흐름임.

```text
입력
→ 저장
→ 변환
→ 조회
→ 보안
→ 감시
```

각 서비스는 이름부터 외우지 않음.  
먼저 어떤 데이터가 들어오고, 얼마나 빨리 처리되어야 하며, 어디에 저장하고, 실패하면 어떻게 복구할지를 판단한 뒤 서비스 선택으로 연결함.

---

## 2. 학습 방식

한 번에 전체 AWS 범위를 다루지 않음.

```text
대분류
→ 중분류
→ 소분류
→ 해야 될 것
→ 이해할 점
→ 확인할 사항
→ 완료 기준
```

### 세션 제한

```text
새 서비스: 1개
새 개념: 최대 2개
학습 시간: 20~30분
확인 질문: 최대 3개
다음 단계: 현재 완료 기준을 충족한 뒤 진행
```

### 설명 순서

```text
무엇인가
→ 왜 필요한가
→ 실제 예시
→ 헷갈리는 개념과 차이
→ 한 줄 결론
```

강의 자료는 참고 자료임.  
서비스 동작, 시험 범위, 요금, 제한은 실습 또는 응시 전에 AWS 공식 문서로 다시 확인함.

---

## 3. 현재 학습 순서

```text
01_foundation
→ 02_storage
→ 03_catalog-query
→ 04_etl
→ 05_ingestion-orchestration
→ 06_streaming
→ 07_security-operations
→ 08_exam-practice
```

| 단계 | 학습 목적 | 현재 상태 |
|---|---|---|
| `01_foundation` | 데이터 파이프라인, 배치·스트리밍, 핵심 데이터 용어 | 문서 생성 완료 |
| `02_storage` | S3, 데이터 레이크 계층, Raw 보존, CSV·Parquet | 개념 정리 완료, 첫 S3 실습 준비 |
| `03_catalog-query` | Glue Data Catalog, Crawler, Athena | 디렉터리만 생성 |
| `04_etl` | ETL, Glue Job, 품질 검증, 재처리 | 디렉터리만 생성 |
| `05_ingestion-orchestration` | 수집, 이벤트, 자동화, 오케스트레이션 | 디렉터리만 생성 |
| `06_streaming` | Kinesis, Firehose, MSK | 디렉터리만 생성 |
| `07_security-operations` | IAM, KMS, Lake Formation, CloudWatch, CloudTrail | 디렉터리만 생성 |
| `08_exam-practice` | 서비스 비교, 시나리오 문제, 오답 기록 | 디렉터리만 생성 |

> 현재는 `02_storage`를 넘어서 Glue, Athena, Kinesis를 먼저 학습하지 않음.

---

## 4. 현재 Repository Structure

```text
.
├─ .env                         # 로컬 환경값. Git 커밋 금지
├─ .env.example                 # 환경 파일 작성 원칙만 공개
├─ .gitignore
├─ README.md
├─ requirements.txt
│
├─ data/
│  ├─ README.md                 # 로컬 데이터 작업 공간 규칙
│  ├─ sample/
│  │  └─ orders.csv             # Git에 포함 가능한 작은 샘플 데이터
│  ├─ raw/
│  │  └─ .gitkeep
│  ├─ processed/
│  │  └─ .gitkeep
│  └─ curated/
│     └─ .gitkeep
│
├─ docs/
│  ├─ 00_learning-map/
│  │  └─ dea-c01_learning-roadmap.md
│  ├─ 01_foundation/
│  │  ├─ 01_data-pipeline-overview.md
│  │  ├─ 02_batch-vs-streaming.md
│  │  └─ 03_core-data-terms.md
│  ├─ 02_storage/
│  │  └─ 01_s3_storage_fundamentals.md
│  ├─ 03_catalog-query/         # 다음 단계용 빈 디렉터리
│  ├─ 04_etl/                   # 다음 단계용 빈 디렉터리
│  ├─ 05_ingestion-orchestration/ # 다음 단계용 빈 디렉터리
│  ├─ 06_streaming/             # 다음 단계용 빈 디렉터리
│  ├─ 07_security-operations/   # 다음 단계용 빈 디렉터리
│  ├─ 08_exam-practice/         # 다음 단계용 빈 디렉터리
│  └─ templates/
│     ├─ 001_DEA_C01_2026_기본용어사전_강의선행.md
│     └─ 002_DEA_C01_YouTube_스크립트_문맥번역_최신화주석_2024년_강의_2026년_기준_최신화.md
│
└─ src/
   ├─ __init__.py
   └─ s3_upload_sample.py       # 로컬 CSV 하나를 기존 S3 Bucket에 업로드하는 최소 스크립트
```

### 디렉터리 역할

| 경로 | 역할 |
|---|---|
| `docs/00_learning-map/` | 전체 학습 순서, 단계별 완료 기준 |
| `docs/01_foundation/` | AWS 서비스 이전에 필요한 데이터 파이프라인 기초 |
| `docs/02_storage/` | S3, Raw·Processed·Curated, 보존 정책, 파일 형식 |
| `docs/03~08_*` | 이후 학습 단계에서 문서를 추가할 공간 |
| `docs/templates/` | 기존 강의 정리·번역 자료. 현재 학습 단계의 정답 문서가 아니라 참고용 원본 |
| `src/` | 현재 학습 단계에서 직접 실행하는 최소 코드 |
| `data/sample/` | 작고 비민감한 Git 포함용 예제 데이터 |
| `data/raw/` | 로컬 실습용 원본 복사본 또는 임시 원본 |
| `data/processed/` | 로컬 변환 중간 결과 |
| `data/curated/` | 로컬 분석·확인용 결과 |

`data/`는 운영 데이터 레이크가 아님.  
AWS 실습에서 원본·가공 데이터의 기준 저장소는 이후 S3임.

---

## 5. 현재 실습: S3 Object Storage

### 목적

S3의 Bucket, Object, Object Key, Prefix를 콘솔과 코드 양쪽에서 확인함.

```text
data/sample/orders.csv
→ 기존 S3 Bucket
→ raw/2026/07/06/orders.csv
→ S3 콘솔에서 Object Key와 Prefix 확인
```

### 현재 범위

- Bucket, Object, Object Key, Prefix
- S3가 관계형 DB가 아닌 이유
- Raw, Processed, Curated 계층
- Raw 수정 금지와 보존 기간 종료 후 삭제의 차이
- CSV, pandas DataFrame, Excel, Parquet의 차이
- Prefix와 Partition의 목적

### 이번 실습에서 하지 않는 것

```text
Glue
Athena
Parquet 변환
S3 Lifecycle 세부 설정
Versioning 세부 설정
IAM Policy JSON
KMS 암호화 설정 세부
```

한 실습에서 여러 서비스를 붙이면 구조 이해보다 콘솔 조작만 남음.  
현재 실습의 성공 기준은 “S3에 Object 하나를 올리고, Key와 Prefix를 직접 확인하는 것”임.

---

## 6. Local Setup

### 6.1 Python 의존성

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

현재 의존성은 S3 SDK인 `boto3` 하나뿐임.

### 6.2 Dry Run

AWS 호출 없이 입력값과 대상 Object Key만 확인함.

Windows PowerShell 예시:

```powershell
python src/s3_upload_sample.py `
  --bucket <your-bucket-name> `
  --source-file data/sample/orders.csv `
  --object-key raw/2026/07/06/orders.csv `
  --dry-run
```

확인할 출력:

```text
Source file : data/sample/orders.csv
Object key  : raw/2026/07/06/orders.csv
Target      : s3://<your-bucket-name>/raw/2026/07/06/orders.csv
Dry run complete. No AWS API call was made.
```

### 6.3 Actual Upload

실제 업로드 전 조건:

```text
1. 대상 S3 Bucket이 이미 존재함
2. boto3가 사용할 AWS 자격증명이 로컬에 준비됨
3. 해당 Bucket에 PutObject 권한이 있음
```

실행:

```powershell
python src/s3_upload_sample.py `
  --bucket <your-bucket-name> `
  --source-file data/sample/orders.csv `
  --object-key raw/2026/07/06/orders.csv
```

업로드 후 S3 콘솔에서 확인:

```text
Object Key:
raw/2026/07/06/orders.csv

논리적 Prefix:
raw/
raw/2026/
raw/2026/07/
raw/2026/07/06/
```

> S3의 `/`는 실제 폴더가 아니라, 평면적인 Object Key를 폴더처럼 분류·표시하는 Prefix 관례임.

---

## 7. Documentation Standard

각 학습 문서는 아래 항목을 우선함.

```text
문서 목적
학습 범위
핵심 정의
왜 필요한가
예시
헷갈리기 쉬운 개념 비교
확인 질문
완료 기준
다음 학습 문서
```

실습을 진행한 뒤에는 아래도 기록함.

```text
문제 정의
성공 기준
입력 → 처리 → 출력
실행 결과
실패·제한사항
비용·정리 절차
출처와 확인일
```

### Evidence Labels

| Label | Meaning |
|---|---|
| `VERIFIED` | 실행 결과, 테스트, 로그 또는 AWS 공식 문서로 확인함 |
| `ASSUMPTION` | 아직 검증하지 않은 전제 |
| `TODO` | 미구현 또는 미검증 항목 |
| `RISK` | 보안, 비용, 데이터 품질, 운영 리스크 |
| `ANTI-PATTERN` | 학습 편의상 보일 수 있으나 운영 환경에는 부적절한 구성 |
| `CURRENT NOTE` | 강의 시점과 현재 AWS 동작·시험 범위의 차이 |

---

## 8. Security and Cost Guardrails

### Never Commit

아래 값은 README, 코드, SQL, 로그, 스크린샷, Git history에 포함하지 않음.

- AWS Access Key ID, Secret Access Key, Session Token
- root 계정 정보, MFA 복구 정보, 비밀번호
- `.env`, `~/.aws/credentials`, `.pem`, `.key`, 인증서
- 실제 AWS Account ID, 운영 ARN, 조직 ID, 운영 엔드포인트
- 개인정보, 운영 데이터, 원본 감사 로그

실제 값 대신 환경 변수 또는 예시 값을 사용함.

```text
${AWS_ACCOUNT_ID}
${AWS_REGION}
${S3_BUCKET_NAME}
${DB_PASSWORD}
```

### Access and Storage

- 기본은 거부이며 필요한 작업만 명시적으로 허용함.
- `Action: "*"`, `Resource: "*"`, `AdministratorAccess`를 기본 예제로 사용하지 않음.
- 장기 Access Key보다 IAM Role과 임시 자격증명을 우선 검토함.
- S3는 Block Public Access를 기본으로 유지함.
- `data/sample/` 외 경로에 개인정보·대용량·운영 데이터를 넣지 않음.
- Raw 데이터는 보관 기간 동안 원본성을 유지하고, 변환 결과는 새 경로 또는 새 버전으로 생성함.

### Cost Control

- 실습마다 과금 가능 리소스와 삭제 절차를 기록함.
- 사용하지 않는 S3 객체, 이전 버전, 쿼리 결과, 로그를 방치하지 않음.
- Redshift, EMR, OpenSearch, NAT Gateway, Elastic IP 등 비용 영향이 큰 서비스는 생성 전에 삭제 경로를 먼저 확인함.
- 생성 리소스에는 가능한 경우 아래 태그를 사용함.

```text
Project=aws-dea-c01-study-lab
Environment=learning
Owner=<github-id>
AutoDeleteAfter=<YYYY-MM-DD>
```

---

## 9. Git Convention

```text
커밋 메시지: 영어
문서 본문: 한국어 중심
코드·변수·파일명·브랜치: 영어
```

기본 형식:

```text
<type>: <summary>
```

| Type | Use |
|---|---|
| `docs` | 문서 추가·수정 |
| `feat` | 기능 또는 실습 코드 추가 |
| `fix` | 오류 수정 |
| `refactor` | 동작 변경 없는 구조 개선 |
| `test` | 테스트 추가·수정 |
| `chore` | 설정, 의존성, 정리 작업 |

예시:

```text
docs: update project README
docs: add S3 storage study notes
feat: add S3 upload sample script
chore: add Python dependencies
```

---

## 10. Progress

- [x] 학습 로드맵 생성
- [x] Foundation 문서 생성
- [x] S3 저장 구조 및 데이터 레이크 기초 정리
- [x] 로컬 `src/`, `data/` 최소 템플릿 생성
- [ ] S3 Bucket 생성
- [ ] 샘플 CSV 업로드 및 Prefix 확인
- [ ] S3 실습 결과 기록
- [ ] Glue Data Catalog 학습 시작
- [ ] 공식 문제 세트 기반 오답 기록 시작

---

## 11. Reference Policy

- AWS 공식 문서를 최우선 근거로 사용함.
- 외부 강의, 블로그, 샘플 코드는 출처와 참고 범위를 표시함.
- 강의 자료가 오래됐을 수 있으면 `CURRENT NOTE`로 현재 상태와 차이를 기록함.
- 타인의 스크립트, 슬라이드, 코드 전체를 재배포하지 않음.
- 이 저장소에는 직접 이해하고 재구성한 설명, 직접 작성한 코드, 익명화된 검증 결과만 포함함.

---

## 12. Disclaimer

이 저장소는 개인 학습 및 포트폴리오 목적의 기록임.  
운영 환경에 적용하기 전에는 최신 AWS 공식 문서, 조직 보안 정책, 비용 정책, 데이터 보존 정책을 별도로 검토해야 함.
