# AWS DEA-C01 학습 로드맵

> 목적: AWS Certified Data Engineer - Associate DEA-C01 취득을 위해, 서비스 목록 암기가 아니라 **데이터 파이프라인 한 개를 끝까지 설명할 수 있는 수준**까지 단계적으로 학습함.  
> 문서 위치: `docs/00_learning-map/dea-c01_learning-roadmap.md`  
> 기준 확인일: 2026-07-06  
> 공식 시험 가이드 기준: DEA-C01 v1.1, 2025-12-12 공개

---

## 1. 최종 목표

시험 직전 아래 흐름을 서비스 이름과 선택 근거까지 설명할 수 있으면 됨.

```text
배치 또는 실시간 원천 데이터
→ S3 Raw 원본 보관
→ Glue Data Catalog로 구조 등록
→ Glue로 정제·변환
→ S3 Processed에 Parquet 저장
→ Athena 또는 Redshift로 분석
→ IAM·Lake Formation·KMS로 권한과 암호화 통제
→ CloudWatch·CloudTrail로 감시와 감사
```

이 로드맵은 AWS의 전체 서비스 목록을 외우는 계획이 아님.  
문제에서 요구하는 **비용, 성능, 운영 부담, 보안, 재처리 가능성**을 보고 가장 적합한 서비스를 선택하는 학습 계획임.

---

## 2. 시험 범위 최소 지도

| 도메인 | 비중 | 이 로드맵의 학습 위치 |
|---|---:|---|
| 데이터 수집 및 변환 | 34% | 04~06 단계 |
| 데이터 저장소 관리 | 26% | 02~03, 07 단계 |
| 데이터 운영 및 지원 | 22% | 06, 09 단계 |
| 데이터 보안 및 거버넌스 | 18% | 09 단계 |

> 문제 수와 점수만 쫓지 말 것. 초반에는 데이터 흐름을 이해하고, 중반부터 서비스 비교 문제를 풀며, 마지막에 시간 제한 모의고사로 넘어감.

---

## 3. 학습 운영 규칙

### 한 세션의 상한

```text
새 서비스: 1개
새 개념: 최대 2개
학습 시간: 20~30분
기록: 5~10줄
확인 문제: 최대 3문제
종료 기준: 내 말로 1분 설명 가능
```

### 서비스 노트 고정 양식

각 서비스 문서에 아래 다섯 줄을 먼저 작성함.

```text
무엇인가
왜 필요한가
입력은 무엇인가
출력은 어디로 가는가
비슷한 서비스와 무엇이 다른가
```

### 한 단계의 완료 기준

다음 셋 중 하나라도 막히면 다음 단계로 넘어가지 않음.

```text
정의: 서비스가 무엇인지 한 문장으로 설명
흐름: 입력 → 처리 → 출력 설명
선택: 비슷한 서비스와 차이를 한 문장으로 설명
```

---

## 4. 전체 학습 순서

```text
0. 데이터 파이프라인 기초
1. S3와 데이터 레이크
2. Glue Data Catalog와 Athena
3. Glue ETL
4. 배치 수집과 자동 실행
5. 분석 저장소 선택
6. 스트리밍
7. 보안·운영·거버넌스
8. 최신 범위 보강
9. 시험형 문제와 오답 관리
```

### 단계 간 의존성

```text
S3
→ Catalog
→ Athena
→ Glue ETL
→ EventBridge / Lambda / SQS
→ Redshift
→ Kinesis
→ IAM / Lake Formation / KMS / CloudWatch
→ 문제 풀이
```

Kinesis, EMR, MSK부터 시작하지 않음.  
S3 기반 배치 파이프라인을 먼저 이해하지 못하면 실시간 처리 서비스는 이름만 남고 선택 기준은 남지 않음.

---

# 0. 데이터 파이프라인 기초

- 디렉터리: `docs/01_foundation/`
- 목표: AWS 서비스 이름 없이도 데이터 파이프라인의 목적과 흐름 설명

## 소분류

| 문서 | 해야 될 것 | 이해할 점 | 완료 기준 |
|---|---|---|---|
| `data-pipeline-overview.md` | 수집 → 저장 → 변환 → 조회 → 감시 그리기 | 데이터 파이프라인은 데이터를 분석 가능 상태로 이동·정리·보호하는 구조임 | 다섯 단계를 각 한 문장으로 설명 |
| `batch-vs-streaming.md` | 배치와 스트리밍 비교 | 배치는 모아서 처리, 스트리밍은 도착에 가깝게 처리 | 하루 1회 CSV 처리와 실시간 클릭 로그를 구분 |
| `core-data-terms.md` | schema, metadata, ETL, data lake 정의 | 서비스보다 데이터 구조 용어가 먼저임 | 용어를 한 줄씩 설명 |

## 완료 체크

- [ ] 데이터 파이프라인이 왜 필요한지 설명 가능
- [ ] 원천 데이터를 바로 분석하지 않는 이유 설명 가능
- [ ] 배치와 스트리밍을 구분 가능

---

# 1. S3와 데이터 레이크

- 디렉터리: `docs/02_storage/`
- 목표: 파일 저장, 원본 보존, 분석 파일 형식의 차이 이해
- 현재 시작점: 여기부터 진행

## 소분류

| 문서 | 해야 될 것 | 이해할 점 | 완료 기준 |
|---|---|---|---|
| `s3_bucket-object-prefix.md` | Bucket, Object, Key, Prefix 기록 | S3는 평면 객체 저장소이며 `/`는 Prefix를 폴더처럼 보이게 하는 관례임 | Object Key와 Prefix의 차이 설명 |
| `s3_data-lake-layers.md` | Raw, Processed, Curated 그림 | 원본·정제·분석용 결과를 섞지 않는 구조임 | 각 계층의 입력·출력 설명 |
| `raw-data-retention-policy.md` | 수정 금지와 삭제 정책 구분 | Raw는 영구 보관이 아니라, 보존 기간 동안 원본성을 유지하는 증거 데이터임 | 수정 대신 재처리·새 버전 생성 이유 설명 |
| `csv-json-parquet.md` | CSV, JSON, Parquet 비교 | Parquet는 컬럼 기반이라 필요한 컬럼만 읽고 압축 효율이 좋음 | DataFrame, Excel, Parquet의 층위 차이 설명 |
| `partition-prefix-design.md` | 날짜 Prefix 설계 | Partition은 필요한 데이터만 읽게 해 분석 비용과 시간을 줄임 | `year=2026/month=07/day=06`의 목적 설명 |

## 완료 체크

- [x] S3가 DB가 아닌 이유 설명 가능
- [x] Raw 데이터를 수정하면 위험한 이유 설명 가능
- [x] Parquet가 분석에 유리한 이유 설명 가능
- [x] Prefix와 실제 폴더의 차이 설명 가능
- [ ] Raw 보존 기간과 Lifecycle 저장 등급을 구분 가능

---

# 2. Glue Data Catalog와 Athena

- 디렉터리: `docs/03_catalog-query/`
- 목표: S3 파일을 SQL 테이블처럼 찾고 읽는 구조 이해

| 문서 | 해야 될 것 | 이해할 점 | 완료 기준 |
|---|---|---|---|
| `glue-data-catalog.md` | Catalog, table, schema 정의 | Catalog는 S3 파일 자체가 아니라 파일 구조를 기록하는 메타데이터 저장소임 | S3와 Catalog의 역할 차이 설명 |
| `glue-crawler.md` | Crawler 역할 기록 | Crawler는 S3 등을 스캔하여 schema를 추정하고 Catalog를 채움 | Crawler와 Glue Job 차이 설명 |
| `athena.md` | Athena 쿼리 흐름 기록 | Athena는 S3 데이터를 SQL로 읽는 서버리스 분석 서비스임 | Athena가 데이터를 직접 저장하는 DB인지 판단 |
| `athena-vs-redshift.md` | 비교 표 작성 시작 | Athena는 S3 애드혹 분석, Redshift는 반복·대규모 분석용 DW에 가까움 | 요구사항에 따라 하나 선택 |

## 완료 체크

- [ ] `S3 → Glue Data Catalog → Athena` 흐름 설명 가능
- [ ] Crawler와 Job을 구분 가능
- [ ] Athena 비용이 스캔 데이터와 연결되는 이유 설명 가능

---

# 3. Glue ETL

- 디렉터리: `docs/04_etl/`
- 목표: 원천 데이터를 분석 가능한 형태로 바꾸는 이유와 재처리 구조 이해

| 문서 | 해야 될 것 | 이해할 점 | 완료 기준 |
|---|---|---|---|
| `etl-overview.md` | Extract, Transform, Load 정리 | ETL은 데이터를 꺼내고, 정제·변환하고, 목적지에 적재하는 흐름임 | CSV → Parquet 변환이 Transform인 이유 설명 |
| `glue-job.md` | Glue Job의 입출력 그리기 | Glue Job은 실제 데이터 변환 작업을 수행함 | Crawler가 변환을 하지 않는 이유 설명 |
| `schema-data-quality.md` | schema, null, type 오류 기록 | 데이터 타입과 품질 오류는 분석 결과를 왜곡함 | 문자열 금액과 숫자 금액의 차이 설명 |
| `job-bookmark.md` | Bookmark 목적 기록 | 이미 처리한 입력을 다시 처리하지 않게 돕는 상태 기록임 | 중복 적재 방지와 연결 |

## 최소 실습 목표

```text
CSV 원천 데이터
→ Glue Job
→ Parquet 변환
→ processed S3 경로 저장
→ Athena SQL 조회
```

---

# 4. 배치 수집과 자동 실행

- 디렉터리: `docs/05_ingestion-orchestration/`
- 목표: 데이터가 들어온 뒤 후속 작업이 자동 실행되는 구조 이해

| 문서 | 우선 서비스 | 이해할 점 | 완료 기준 |
|---|---|---|---|
| `batch-ingestion.md` | S3, DMS, AppFlow | 파일·DB·SaaS 데이터가 들어오는 경로 | 원천별 수집 방식을 구분 |
| `eventbridge.md` | EventBridge | 이벤트 또는 일정에 따라 후속 작업 연결 | EventBridge가 데이터 저장소가 아닌 이유 설명 |
| `lambda.md` | Lambda | 짧은 이벤트 기반 코드 실행 | Lambda와 Glue Job의 처리 규모 차이 설명 |
| `sqs-sns.md` | SQS, SNS | SQS는 버퍼·비동기 처리, SNS는 알림·pub/sub 전달 | SQS와 SNS 구분 |
| `step-functions-mwaa.md` | Step Functions, MWAA | 여러 작업의 순서·재시도·실패 처리를 관리 | DAG·상태 머신이 필요한 상황 판단 |

> 이 단계에서는 EventBridge, Lambda, SQS만 먼저 깊게 학습함. Step Functions와 MWAA는 역할 구분부터 시작함.

---

# 5. 분석 저장소 선택

- 디렉터리: `docs/03_catalog-query/` 및 `docs/02_storage/`
- 목표: 문제에서 저장·조회 요구사항을 보고 Athena, Redshift, S3 등을 구분

| 상황 | 우선 후보 | 선택 근거 |
|---|---|---|
| S3 파일을 가끔 SQL로 탐색 | Athena | 서버리스 애드혹 분석 |
| BI 대시보드가 반복적으로 대규모 집계 | Redshift | 분석용 데이터 웨어하우스 |
| 파일 기반 저비용 데이터 레이크 | S3 | 대규모 객체 저장 |
| 키-값 초고속 접근 | DynamoDB 또는 MemoryDB | 목적과 접근 패턴이 다름 |

## 완료 체크

- [ ] Athena와 Redshift의 차이 설명 가능
- [ ] S3와 RDS의 차이 설명 가능
- [ ] 저장소 선택 기준으로 비용·성능·접근 패턴을 제시 가능

---

# 6. 스트리밍

- 디렉터리: `docs/06_streaming/`
- 목표: 실시간 데이터에서 직접 처리와 자동 적재를 구분

| 문서 | 서비스 | 최소 이해 |
|---|---|---|
| `kinesis-data-streams.md` | Kinesis Data Streams | 소비자가 직접 읽고 재처리 가능한 스트림 |
| `firehose.md` | Amazon Data Firehose | S3·Redshift·OpenSearch 등으로 관리형 전달 |
| `msk.md` | Amazon MSK | Kafka 호환 생태계가 필요한 경우 |
| `streaming-service-comparison.md` | 비교 | Streams, Firehose, MSK, Flink의 역할 차이 |

## 핵심 비교

```text
직접 소비자 애플리케이션이 스트림을 읽고 제어해야 함
→ Kinesis Data Streams

가공을 최소화하고 S3 또는 Redshift로 자동 전달하면 됨
→ Amazon Data Firehose

Kafka 호환성 또는 기존 Kafka 생태계가 필요함
→ Amazon MSK
```

---

# 7. 보안·운영·거버넌스

- 디렉터리: `docs/07_security-operations/`
- 목표: 데이터 접근, 암호화, 감시, 감사, 개인정보 보호를 한 흐름으로 연결

| 문서 | 서비스 | 핵심 질문 |
|---|---|---|
| `iam.md` | IAM | 누가 어떤 리소스에 무엇을 할 수 있는가 |
| `kms-secrets-manager.md` | KMS, Secrets Manager | 데이터를 어떻게 암호화하고 비밀값을 어디에 보관하는가 |
| `lake-formation.md` | Lake Formation | 데이터 레이크의 테이블·컬럼·행 접근을 어떻게 통제하는가 |
| `cloudwatch-cloudtrail.md` | CloudWatch, CloudTrail | 장애 감시와 API 감사 기록의 차이는 무엇인가 |
| `data-governance.md` | Macie, AWS Config 등 | PII, 데이터 주권, 정책 준수, 변경 추적을 어떻게 다루는가 |

## 완료 체크

- [ ] IAM과 Lake Formation의 역할 차이 설명 가능
- [ ] KMS와 Secrets Manager의 역할 차이 설명 가능
- [ ] CloudWatch와 CloudTrail의 역할 차이 설명 가능
- [ ] 최소 권한 원칙을 데이터 파이프라인 예시로 설명 가능

---

# 8. 최신 범위 보강

- 위치: 각 서비스 문서 하단의 `최신 범위` 섹션 또는 별도 요약 문서
- 시작 시점: 0~7 단계의 기본 흐름 완료 후
- 목적: 기존 강의에 없는 2025-12-12 v1.1 변경점 때문에 문제에서 용어를 봐도 멈추지 않기

## 우선 보강 항목

| 항목 | 지금 필요한 수준 |
|---|---|
| IaC: CloudFormation, CDK | 반복 가능한 리소스 배포를 코드로 관리한다는 이해 |
| S3 Tables | 분석용 테이블 데이터 저장 관련 S3 기능이라는 이해 |
| Aurora PostgreSQL HNSW | 벡터 유사도 검색용 인덱스 사용 사례라는 이해 |
| MemoryDB | 빠른 키-값 접근 사용 사례라는 이해 |
| SageMaker Catalog, ML Lineage | 데이터 자산·계보를 추적하고 관리하는 맥락 이해 |
| Glue DataBrew, SageMaker Unified Studio | 데이터 준비·변환을 돕는 도구라는 역할 구분 |
| Bedrock, Kendra, Amazon Q, Data Exchange | 서비스 이름과 데이터 엔지니어링 접점만 우선 파악 |

> 여기서는 구현 깊이를 요구하지 않음. 시험 문제에서 용어를 봤을 때 역할·선택 근거를 최소 한 문장으로 판단하는 수준이 목표임.

---

# 9. 시험형 문제와 오답 관리

- 디렉터리: `docs/08_exam-practice/`
- 시작 조건: 0~7 단계 완료 후

## 문제 풀이 단위

```text
문제 5개
→ 오답 서비스·선택 기준 기록
→ 해당 서비스 문서 20분 복습
→ 유사 문제 5개
→ 종료
```

## 오답 기록 양식

```text
문제 상황:
정답 서비스:
내가 고른 서비스:
정답이 되는 조건:
내 답이 틀리는 조건:
다음에 확인할 키워드:
```

## 종료 기준

- [ ] 공식 문제 세트에서 서비스 선택 근거를 설명 가능
- [ ] 오답을 서비스 이름이 아니라 요구사항 조건으로 기록함
- [ ] 65문항, 130분 모의고사는 마지막 단계에서만 실시함

---

# 10. 현재 해야 할 일

현재는 **1단계 S3와 데이터 레이크**만 진행함.

```text
문서:
docs/02_storage/s3_bucket-object-prefix.md
docs/02_storage/s3_data-lake-layers.md
docs/02_storage/raw-data-retention-policy.md
docs/02_storage/csv-json-parquet.md
```

오늘의 종료 기준:

- [ ] Bucket, Object, Key, Prefix 정의를 내 말로 설명
- [ ] Raw, Processed, Curated 구조를 그림
- [ ] S3가 DB가 아닌 이유를 한 문장으로 설명
- [ ] Raw가 수정 금지지만 영구 보관 대상은 아닌 이유 설명
- [ ] Parquet와 pandas DataFrame이 같은 층위가 아니라는 점 설명

다음 서비스인 Glue는 위 다섯 항목을 막힘 없이 설명한 뒤에 시작함.

---

# 11. 공식 자료 사용 순서

1. **AWS Exam Guide**  
   시험 도메인, 서비스 범위, 변경 사항을 확인하는 기준 문서임.

2. **AWS Skill Builder Exam Prep Plan**  
   전체 준비 순서와 도메인별 Review·Practice를 확인함.

3. **Official Practice Question Set**  
   기본 흐름을 이해한 뒤 서비스 선택 기준을 점검하는 용도로 사용함.

4. **Official Practice Exam**  
   마지막 단계에서 시간 제한과 실전 감각 확인 용도로 사용함.

---

# 12. 공식 참고 자료

- [AWS Certified Data Engineer - Associate Exam Guide DEA-C01](https://docs.aws.amazon.com/pdfs/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.pdf)
- [DEA-C01 Exam Guide Revisions](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/dea-01-revisions.html)
- [DEA-C01 In-Scope AWS Services](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/dea-01-in-scope-services.html)
- [AWS Skill Builder Exam Prep Plan: DEA-C01](https://skillbuilder.aws/learning-plan/QYZWVSMX4B/exam-prep-plan-aws-certified-data-engineer--associate-deac01--english/YTMBK7R698)
- [AWS Skill Builder Official Practice Question Set: DEA-C01](https://skillbuilder.aws/learn/2JS5H1Z9KP/official-practice-question-set-aws-certified-data-engineer--associate-deac01--english/VX268Y5VBA)

---

## 최종 원칙

```text
한 번에 AWS 전체를 이해하려고 하지 않음.
한 단계에서 필요한 개념만 이해함.
서비스 이름보다 데이터의 입력·처리·출력·실패·권한 흐름을 먼저 설명함.
문제를 많이 푸는 것보다, 틀린 선택 이유를 남김.
```
