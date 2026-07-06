# AWS DEA-C01 학습 노트
## 01. S3 저장 구조와 데이터 레이크 기초

> 학습 단계: `docs/02_storage/`  
> 범위: Bucket, Object, Object Key, Prefix, Raw·Processed·Curated, Raw 보존 정책, CSV·Parquet  
> 목적: AWS S3를 단순 파일 저장소가 아니라 **데이터 파이프라인의 원본·가공 데이터 저장 기반**으로 이해함.

---

# 1. 이 단계에서 답할 수 있어야 하는 질문

- S3는 왜 DB가 아닌가
- Bucket, Object, Object Key, Prefix는 각각 무엇인가
- S3에서 `/`는 실제 폴더 구분자인가
- Raw 데이터는 왜 수정하면 위험한가
- Raw 데이터는 언제 삭제할 수 있는가
- CSV, pandas DataFrame, Excel, Parquet는 무엇이 다른가
- Parquet는 왜 대용량 분석에 유리한가
- Raw, Processed, Curated 계층은 왜 나누는가

---

# 2. S3의 본질

## 2.1 한 줄 정의

```text
Amazon S3는 파일 단위의 객체 Object를 저장하는 객체 스토리지임.
```

S3는 일반 파일시스템도 아니고, 관계형 DB도 아님.

```text
S3:
키 Key와 객체 Object를 연결해 저장함.

DB:
테이블의 행 Row과 컬럼 Column을 구조적으로 관리하고 질의·수정함.
```

---

## 2.2 S3는 왜 DB가 아닌가

원천 데이터가 들어가서 S3가 DB가 아닌 것은 아님.  
DB도 원천 데이터, JSON, 로그 등을 저장할 수 있음.

S3가 DB가 아닌 이유는 **저장·수정·조회 모델이 DB와 다르기 때문**임.

| 구분 | S3 | 관계형 DB |
|---|---|---|
| 본질 | 객체 저장소 | 데이터 관리·질의 시스템 |
| 저장 단위 | 파일 전체 Object | 행 Row, 레코드 Record |
| 수정 방식 | 객체 전체 교체 | 특정 행·컬럼 수정 |
| 관계 관리 | 기본적으로 없음 | PK, FK, JOIN |
| 제약조건 | DB 제약조건 목적 아님 | UNIQUE, NOT NULL 등 |
| 트랜잭션 | 다중 객체 단위 DB식 ACID 트랜잭션 목적 아님 | 트랜잭션 핵심 기능 |
| 주 용도 | 대용량 파일·로그·분석 데이터 저장 | 서비스 운영 데이터 관리 |

예시:

```text
S3:
orders_2026_07_06.csv 파일 전체 저장

RDS:
orders 테이블에서 order_id = 1004 행만 UPDATE
```

### 시험용 답안

```text
S3는 파일 단위 객체 저장소이며,
DB처럼 행 단위 수정, 관계형 제약조건, SQL 트랜잭션을 중심으로 동작하지 않으므로 DB가 아님.
```

---

# 3. Bucket, Object, Object Key, Prefix

## 3.1 용어 정의

| 용어 | 정의 | 비유 |
|---|---|---|
| Bucket | Object를 담는 S3 최상위 저장 공간 | 창고 건물 |
| Object | S3에 저장되는 실제 데이터 단위 | 창고 안 상자 하나 |
| Object Key | Object를 식별하는 전체 문자열 이름 | 상자의 전체 주소 |
| Prefix | Object Key 앞부분을 이용한 논리적 분류 기준 | 창고 구역 표지판 |

예시:

```text
Bucket:
my-data-lake

Object Key:
raw/2026/07/06/orders.csv
```

위 Object Key의 Prefix 예시:

```text
raw/
raw/2026/
raw/2026/07/
raw/2026/07/06/
```

---

## 3.2 Object의 구성

개념적으로 Object는 아래와 같이 봄.

```text
Object
= Object Key
+ 실제 데이터 본문
+ 메타데이터
```

예시:

```text
Object Key:
raw/2026/07/06/orders.csv

본문:
CSV 파일의 실제 데이터

메타데이터:
Content-Type, 생성 시각, 암호화 정보 등
```

---

## 3.3 S3에 `/`가 들어갈 수 있는 이유

일반 OS 파일시스템에서는 `/`를 파일명 문자로 쓸 수 없음.

```text
Windows, Linux, macOS:
`/`는 경로 구분자이므로 파일명에 사용 불가
```

하지만 S3에서는 Object Key가 문자열이므로 `/`를 포함할 수 있음.

```text
raw/2026/07/06/orders.csv
```

이것은 S3 내부에서 실제 폴더 5개와 파일 1개가 있는 구조가 아님.

```text
S3 내부 관점:
"raw/2026/07/06/orders.csv"라는 Key 문자열 하나
```

콘솔과 SDK가 `/`를 기준으로 폴더처럼 보이게 표현하는 것임.

```text
콘솔 화면 관점:
raw/
└─ 2026/
   └─ 07/
      └─ 06/
         └─ orders.csv
```

### 핵심

```text
S3의 `/`는 실제 디렉터리 구분자가 아니라,
평면 Key 공간을 사람이 폴더처럼 보기 쉽게 관리하기 위한 관례임.
```

---

## 3.4 Prefix를 쓰는 이유

Prefix는 편의성만을 위한 것은 아님.

| 목적 | 설명 |
|---|---|
| 논리적 분류 | 환경, 날짜, 도메인, 데이터 상태를 나눔 |
| 조회 범위 축소 | 특정 Prefix만 대상으로 객체 목록을 조회 가능 |
| 권한 제어 | Prefix별 S3 접근 권한을 줄 수 있음 |
| Lifecycle 적용 | Raw Prefix에만 장기 보관·삭제 정책 적용 가능 |
| 비용·성능 관리 | 날짜 Partition과 함께 필요한 범위만 읽게 설계 가능 |

예시:

```text
raw/commerce/orders/year=2026/month=07/day=06/
processed/commerce/orders/year=2026/month=07/day=06/
curated/commerce/daily_sales/year=2026/month=07/day=06/
```

---

# 4. 데이터 레이크 계층

## 4.1 기본 구조

```text
외부 API, DB, 로그, 파일
→ Raw
→ Processed
→ Curated
→ 분석·대시보드·머신러닝
```

S3 Bucket 하나 안에서 Prefix로 논리 계층을 나누는 방식이 흔함.

```text
s3://my-data-lake/
├─ raw/
├─ processed/
└─ curated/
```

---

## 4.2 Raw, Processed, Curated 정의

| 계층 | 목적 | 예시 |
|---|---|---|
| Raw | 외부에서 처음 수집한 원본 보관 | API JSON, DB 덤프 CSV, 웹 로그 |
| Processed | 타입 정리, 오류 처리, 포맷 변환 | CSV → Parquet, 문자열 날짜 → date |
| Curated | 분석·리포트·모델용으로 목적별 정리 | 일별 매출 집계, 고객별 구매 요약 |

---

## 4.3 왜 계층을 나누는가

| 분리하지 않으면 생기는 문제 | 계층 분리로 얻는 효과 |
|---|---|
| 원본과 가공본이 섞임 | 원본성과 처리 결과를 분리 |
| 변환 로직 오류를 찾기 어려움 | Raw부터 다시 검증 가능 |
| 분석 데이터가 재사용하기 어려움 | Curated 결과를 여러 분석자가 공유 |
| 재처리 시 기존 결과를 덮어씀 | 버전별 Processed 결과 관리 가능 |
| 권한과 보존 정책을 한꺼번에 적용 | 계층별 보안·Lifecycle 정책 분리 |

### 한 줄 정리

```text
Raw는 증거,
Processed는 재사용 가능한 정제 결과,
Curated는 목적별 최종 제공 데이터임.
```

---

# 5. Raw 데이터는 왜 수정하면 위험한가

## 5.1 핵심: 원본성 상실

Raw는 외부에서 처음 들어온 **사실 기록이자 원본 증거**임.

```text
외부 API 응답
→ Raw 원본 보관
→ 변환 로직 적용
→ Processed 생성
→ 분석용 Curated 생성
```

Raw 본문을 수정하면 “처음 받은 데이터가 무엇이었는가”를 증명하기 어려워짐.

---

## 5.2 수정하면 깨지는 것

| 문제 | 이유 |
|---|---|
| 재처리 | 변환 로직 변경 후 원본부터 다시 계산하기 어려움 |
| 오류 추적 | 원본 오류인지 변환 코드 오류인지 구분 불가 |
| 결과 재현 | 과거 분석 결과를 같은 입력으로 검증하기 어려움 |
| 감사 | 최초 수집 데이터의 증거력이 약해짐 |
| 품질 검증 | Raw와 Processed를 비교해 변환 결과를 검증하기 어려움 |

예시:

```text
Raw:
"2026-07-06", "1000", "KRW"

변환:
"1000" 문자열 → 숫자 1000
"KRW" → 통화 코드 기반 처리
```

여기서 Raw의 `"1000"`을 사람이 `"10000"`으로 덮어쓰면,  
나중에 금액이 왜 달라졌는지 원인을 검증하기 어려워짐.

---

## 5.3 수정이 필요해 보일 때의 정상 처리

| 상황 | 정상 처리 |
|---|---|
| 변환 코드 오류 | Raw 유지, Processed를 새 버전으로 재생성 |
| 원천 API 오류 | Raw 유지, 보정 데이터 또는 보정 규칙을 별도 관리 |
| 중복 수집 | Raw를 고치지 않고 중복 판정 메타데이터를 별도 기록 |
| 형식 오류 | Raw 유지, 실패 상태와 오류 사유 기록 |
| 개인정보 삭제 요구 | 법적 요구가 우선이면 Raw도 삭제·익명화·격리 검토 |

예시:

```text
raw/orders_001.json
processed/v1/orders_001.parquet
processed/v2/orders_001.parquet
```

### 한 줄 정리

```text
Raw는 수정 대신 새 처리 결과나 새 버전을 만든다.
```

---

# 6. Raw는 언제 삭제할 수 있는가

## 6.1 수정 금지와 영구 보관은 다름

```text
Raw는 보관 기간 동안 원본성을 유지한다.
Raw는 영구 보관 대상이 아니다.
```

삭제 여부는 기술 문제가 아니라 **보존 정책 Retention Policy** 문제임.

---

## 6.2 보존 기간을 정하는 기준

| 기준 | 보존 기간이 길어질 수 있는 조건 |
|---|---|
| 재처리 가치 | 과거 데이터를 다시 계산할 가능성이 큼 |
| 감사·분쟁 대응 | 거래·계약·보안 사고 증거가 필요함 |
| 법·규정 | 세무, 금융, 개인정보, 의료 등 보존 의무 |
| 데이터 계약 | 외부 제공자의 데이터 보관 조건 |
| 데이터 특성 | 드문 장애, 보안 사고, 희귀 사건 기록 |

중요도만으로 기간을 정하는 것이 아님.  
법적 의무, 운영 필요, 계약 조건, 재처리 가치가 같이 결정함.

---

## 6.3 90일은 무엇인가

90일은 표준값이 아니라 **자주 쓰이는 예시값**임.

```text
보존 기간 Retention:
데이터를 총 언제까지 남길 것인가

저장 등급 Lifecycle:
그 보존 기간 동안 어느 스토리지 등급에 둘 것인가
```

예시:

```text
0~90일:
S3 Standard
재처리·장애 분석·품질 검증에 즉시 사용

90일~1년:
S3 Standard-IA 또는 Glacier Instant Retrieval
가끔 재처리·감사에 사용

1~3년:
Glacier Deep Archive
감사·분쟁·규정 대응 중심

3년 이후:
법·계약·감사 의무가 끝난 경우 삭제
```

### 핵심

```text
90일은 흔한 운영 보관 예시일 뿐,
Raw 전체 보존 기간은 데이터 성격과 정책에 따라 달라짐.
```

---

## 6.4 삭제하면 안 되는 예외

아래 상황에서는 보존 기간이 지나도 삭제하면 안 될 수 있음.

```text
법적 분쟁 진행 중
감사 진행 중
보안 사고 조사 중
금융·계약 증빙 필요
규제상 보존 의무 존재
Legal Hold 적용 상태
```

---

# 7. CSV, Excel, pandas DataFrame, Parquet

## 7.1 같은 층위가 아님

| 대상 | 정체 | 존재 위치 |
|---|---|---|
| CSV | 텍스트 기반 파일 형식 | 디스크, S3 |
| Excel | 사람이 보고 수정하는 스프레드시트 도구·파일 | 디스크, 로컬 작업 환경 |
| pandas DataFrame | Python 실행 중 메모리에 존재하는 표 자료구조 | RAM |
| Parquet | 컬럼 기반 분석용 파일 형식 | 디스크, S3 |

비유:

```text
pandas DataFrame = 작업대 위에 펼친 데이터
CSV·Parquet = 창고에 보관하는 데이터 파일
Excel = 사람이 직접 보고 수정하는 표 문서
```

---

## 7.2 CSV의 특징

CSV는 행 Row 중심 텍스트 파일로 이해하면 됨.

```text
user_id,country,amount,created_at
1,KR,10000,2026-07-06
2,KR,20000,2026-07-06
3,US,5000,2026-07-06
```

장점:

```text
사람이 읽기 쉬움
도구 호환성이 좋음
초기 데이터 전달에 간단함
```

단점:

```text
타입 정보가 약함
압축·분석 효율이 낮을 수 있음
대용량 컬럼 분석에서 불필요한 데이터를 많이 읽을 수 있음
```

---

## 7.3 Parquet의 특징

Parquet는 컬럼 Column 중심 파일 형식임.

위 데이터는 개념적으로 아래처럼 컬럼별로 묶여 저장됨.

```text
user_id:
1, 2, 3

country:
KR, KR, US

amount:
10000, 20000, 5000

created_at:
2026-07-06, 2026-07-06, 2026-07-06
```

실제 내부 구조를 이렇게 단순 문자열로 저장한다는 뜻은 아님.  
핵심은 **컬럼별 데이터 묶음에 최적화된 저장 구조**라는 것임.

---

## 7.4 Parquet가 분석에 유리한 이유

예시 SQL:

```sql
SELECT country, SUM(amount)
FROM sales
WHERE created_at = DATE '2026-07-06'
GROUP BY country;
```

필요한 컬럼:

```text
country
amount
created_at
```

필요 없는 컬럼:

```text
user_id
```

CSV 같은 행 중심 구조는 데이터가 매우 크면 필요한 컬럼만 읽기 어려울 수 있음.  
Parquet는 필요한 컬럼 중심으로 읽을 수 있어, 분석 엔진이 읽는 데이터량을 줄이는 데 유리함.

| 장점 | 이유 |
|---|---|
| 필요한 컬럼만 읽기 쉬움 | 불필요한 컬럼 스캔 감소 |
| 압축 효율 향상 | 같은 컬럼에는 비슷한 값이 반복되기 쉬움 |
| 분석 비용 절감 | Athena는 스캔 데이터량이 비용과 연결될 수 있음 |
| 분석 속도 향상 | 읽어야 할 데이터 양이 줄어듦 |
| 스키마 관리에 유리 | 컬럼별 분석 작업에 적합 |

### 압축이 잘 되는 직관

```text
country:
KR, KR, KR, KR, KR, US, US, US
```

같은 종류의 값이 연속되므로 반복값 압축, 사전 인코딩 같은 방식이 잘 맞음.

```text
KR = 0
US = 1

0, 0, 0, 0, 0, 1, 1, 1
```

### 시험용 답안

```text
Parquet는 컬럼 단위 저장 구조라 필요한 컬럼만 읽을 수 있고,
같은 종류의 값이 모여 있어 압축 효율이 높으므로
Athena·Glue·Spark 기반 대용량 분석에 유리함.
```

---

# 8. pandas DataFrame과 Parquet의 관계

둘은 경쟁 관계가 아님.

```python
import pandas as pd

df = pd.read_csv("raw_sales.csv")
df.to_parquet("processed_sales.parquet")
```

흐름:

```text
CSV 또는 Parquet 파일
→ pandas가 읽음
→ DataFrame으로 RAM에 올림
→ 정제·변환
→ Parquet 파일로 저장
→ S3에 적재
→ Athena 또는 Glue가 분석
```

### 핵심

```text
DataFrame은 실행 중 메모리 구조.
Parquet는 저장용 파일 형식.
```

---

# 9. 파티션과 Prefix

## 9.1 파티션 예시

```text
s3://my-data-lake/processed/orders/
year=2026/month=07/day=06/part-0001.parquet
```

여기서:

```text
year=2026/month=07/day=06/
```

은 날짜 기준으로 데이터를 나눈 Partition 경로임.

---

## 9.2 왜 필요한가

일별 매출을 분석할 때 전체 5년치 데이터가 아니라 오늘 또는 특정 하루만 읽도록 만들기 위함임.

```text
전체 데이터 스캔
→ 느림, 비용 증가 가능

필요 날짜 Partition만 스캔
→ 읽는 양 감소, 비용·시간 감소
```

### 한 줄 정리

```text
Partition은 데이터 저장 경로를 날짜·국가·서비스 등 기준으로 나누어
분석 시 필요한 범위만 읽게 만드는 설계임.
```

---

# 10. 데이터 흐름으로 연결하기

현재까지 이해한 AWS 데이터 파이프라인의 최소 흐름:

```text
외부 API·DB·로그
→ S3 Raw에 원본 저장
→ 변환 작업
→ S3 Processed에 Parquet 저장
→ 데이터 카탈로그 등록
→ Athena SQL 분석
→ Curated 결과 생성
```

이후 학습할 서비스 연결:

```text
S3
→ Glue Data Catalog
→ Athena
→ Glue Job
→ EventBridge / Lambda / SQS
→ Redshift
→ Kinesis
→ IAM / Lake Formation / KMS / CloudWatch
```

---

# 11. 최종 확인 답안

## S3는 왜 DB가 아닌가

```text
S3는 파일 단위 객체 저장소이며,
DB처럼 행 단위 수정, 관계형 제약조건, SQL 트랜잭션을 중심으로 동작하지 않기 때문임.
```

## Raw 데이터는 왜 수정하면 위험한가

```text
Raw는 외부에서 처음 들어온 원본 증거 데이터이므로,
수정하면 재처리, 오류 추적, 감사, 결과 재현, 품질 검증이 어려워지기 때문임.
```

## Raw 데이터는 언제 삭제할 수 있는가

```text
Raw는 영구 보관 대상이 아니라,
법적·계약상 의무와 재처리·감사 필요가 끝난 뒤
Retention Policy와 Lifecycle Rule에 따라 아카이브하거나 삭제할 수 있음.
```

## Parquet는 왜 분석에 유리한가

```text
Parquet는 컬럼 단위 저장 구조이므로,
분석에 필요한 컬럼만 읽을 수 있고 압축 효율이 높아
대용량 분석 비용과 시간을 줄이는 데 유리함.
```

## Prefix는 실제 폴더인가

```text
아님.
S3는 평면적인 Object Key 공간이며,
Prefix와 `/`는 객체를 폴더처럼 분류·표시하기 위한 논리적 규칙임.
```

---

# 12. 다음 학습 진입 기준

아래를 막힘 없이 설명하면 다음 단계로 이동함.

- [ ] Bucket, Object, Object Key, Prefix를 설명 가능
- [ ] `/`가 S3에서 실제 폴더 구분자가 아닌 이유 설명 가능
- [ ] Raw, Processed, Curated 계층 역할 설명 가능
- [ ] Raw 수정 금지와 보존 기간 종료 후 삭제를 구분 가능
- [ ] CSV, Excel, DataFrame, Parquet의 차이 설명 가능
- [ ] Parquet와 Partition이 Athena 분석 비용과 연결되는 이유 설명 가능

다음 문서:

```text
docs/03_catalog-query/glue-data-catalog.md
```
