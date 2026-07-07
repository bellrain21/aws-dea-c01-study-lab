# AWS DEA-C01 학습 노트
## 03. 핵심 데이터 용어

> 학습 위치: `docs/01_foundation/03_core-data-terms.md`  
> 권장 학습량: 25~35분. 한 번에 끝내지 않아도 됨.  
> 선행 문서: `01_data-pipeline-overview.md`, `02_batch-vs-streaming.md`  
> 다음 문서: `docs/02_storage/01_s3_storage_fundamentals.md`  
> 범위: 이후 S3, Glue, Athena, Redshift 문서를 읽기 위한 최소 데이터 언어임.  
> 제외: S3의 Bucket·Object·Prefix, Parquet 세부, Glue·Athena 구현은 다음 단계에서 다룸.

---

# 1. 읽는 법

이 문서는 용어 사전 전체가 아님.

우선순위는 아래뿐임.

```text
P0: 다음 문서를 읽기 위해 반드시 필요한 단어
P1: 시험 문제에서 자주 보지만 세부 구현은 나중인 단어
```

각 용어는 네 가지로만 봄.

```text
무엇인가
왜 필요한가
예시는 무엇인가
무엇과 헷갈리면 안 되는가
```

---

# 2. 데이터의 가장 작은 단위

## 2.1 표 데이터 읽기

예시:

| order_id | customer_id | amount | order_time |
|---:|---:|---:|---|
| 1001 | 501 | 12000 | 2026-07-06 10:10:00 |
| 1002 | 502 | 8500 | 2026-07-06 10:11:00 |

| 영문 | 발음 | 뜻 | 예시 |
|---|---|---|---|
| Row | 로우 | 한 건의 가로 데이터 | 주문 한 건 |
| Record | 레코드 | 보통 Row와 비슷한 뜻 | 주문 한 건 |
| Column | 컬럼 | 같은 속성의 세로 열 | `amount` |
| Field | 필드 | 컬럼 또는 레코드 안의 속성 | `customer_id` |
| Value | 밸류 | 실제 들어 있는 값 | `12000` |
| Data type | 데이터 타입 | 값의 종류 | integer, string, timestamp |

### 오해 제거

```text
Row와 Record는 대부분 비슷하게 쓰임.
Column과 Field는 문맥에 따라 겹치지만,
시험에서는 둘 다 데이터의 속성 이름으로 이해하면 됨.
```

---

# 3. 데이터 형태

## 3.1 정형·반정형·비정형

| 구분 | 영문 | 발음 | 의미 | 예시 |
|---|---|---|---|---|
| 정형 데이터 | Structured data | 스트럭처드 데이터 | 행·열과 타입 규칙이 명확함 | 관계형 DB 테이블, 일정한 CSV |
| 반정형 데이터 | Semi-structured data | 세미 스트럭처드 데이터 | 구조 단서는 있지만 레코드마다 형태가 달라질 수 있음 | JSON, XML, 애플리케이션 로그 |
| 비정형 데이터 | Unstructured data | 언스트럭처드 데이터 | 고정 표 구조가 없음 | PDF, 이미지, 음성, 자유 텍스트 |

예시 JSON:

```json
{
  "order_id": 1001,
  "customer": {
    "id": 501,
    "name": "Jinu"
  },
  "coupon_code": null
}
```

JSON은 키와 값이 있어 구조를 읽을 수 있으므로 반정형 데이터에 가까움.  
하지만 모든 JSON 레코드가 같은 키를 반드시 갖는 것은 아님.

---

# 4. Schema와 Metadata

## 4.1 Schema

| 영문 | 발음 | 뜻 |
|---|---|---|
| Schema | 스키마 | 데이터에 어떤 컬럼이 있고, 각 값이 어떤 타입이며, 어떤 규칙을 따라야 하는지 정의한 구조 계약 |
| Schema evolution | 스키마 에볼루션 | 시간이 지나면서 스키마 변경을 안전하게 관리하는 일 |
| Data contract | 데이터 컨트랙트 | 데이터를 만드는 쪽과 쓰는 쪽이 합의한 구조·품질·전달 규칙 |

예:

```text
orders 데이터셋은 아래를 만족해야 함.

order_id: bigint, null 불가
customer_id: bigint, null 불가
amount: decimal, 0 이상
order_time: timestamp
```

이런 구조 정의가 Schema임.

## 4.2 Metadata

| 영문 | 발음 | 뜻 | 예시 |
|---|---|---|---|
| Metadata | 메타데이터 | 데이터를 설명하는 데이터 | 파일 위치, 생성 시각, 컬럼명, 타입, 소유자 |
| Data catalog | 데이터 카탈로그 | 데이터셋과 메타데이터를 찾고 관리하는 목록 | 테이블 이름, S3 위치, schema 정보 |

### 핵심 차이

```text
Schema:
데이터 내부 구조의 규칙

Metadata:
데이터를 찾고 이해하고 관리하기 위한 설명 정보
```

Schema는 Metadata의 한 종류가 될 수 있지만, 둘을 같은 말로 쓰면 안 됨.

---

# 5. Schema-on-write와 Schema-on-read

| 용어 | 발음 | 의미 | 친한 저장 방식 |
|---|---|---|---|
| Schema-on-write | 스키마 온 라이트 | 저장하기 전에 구조와 타입을 강하게 확인 | 관계형 DB, 데이터 웨어하우스 |
| Schema-on-read | 스키마 온 리드 | 저장할 때는 원본을 비교적 유연하게 두고, 읽을 때 해석 | 데이터 레이크, 파일 기반 분석 |

예:

```text
Schema-on-write:
데이터를 넣기 전에 amount가 숫자인지 검사
틀리면 적재 거부 또는 오류 처리

Schema-on-read:
원본 JSON을 우선 보관
분석할 때 필요한 구조로 읽고 해석
```

### 오해 제거

```text
Schema-on-read가 규칙이 없다는 뜻은 아님.
규칙을 저장 시점이 아니라 읽기·변환 시점에 적용하는 성격이 강하다는 뜻임.
```

---

# 6. 데이터 품질

## 6.1 Data quality

| 영문 | 발음 | 뜻 |
|---|---|---|
| Data quality | 데이터 퀄리티 | 데이터가 목적에 맞게 정확하고 일관되며 사용할 수 있는 상태 |
| Data validation | 데이터 밸리데이션 | 미리 정한 규칙을 데이터가 통과하는지 검사 |
| Data profiling | 데이터 프로파일링 | 실제 데이터의 분포·범위·누락·고유값 등을 탐색해 모습 파악 |

## 6.2 Validation과 Profiling 차이

| 구분 | 질문 | 예시 |
|---|---|---|
| Validation | 규칙을 통과했는가 | `amount >= 0`인가 |
| Profiling | 실제 데이터는 어떤 모습인가 | `amount`의 최소·최대·평균은 무엇인가 |

## 6.3 최소 품질 규칙

| 규칙 | 예시 |
|---|---|
| Completeness 완전성 | 필수 주문 ID가 비어 있지 않은가 |
| Uniqueness 유일성 | 주문 ID가 중복되지 않는가 |
| Validity 유효성 | 금액이 음수가 아닌가 |
| Consistency 일관성 | 국가 코드가 정해진 형식인가 |
| Timeliness 적시성 | 어제 들어와야 할 파일이 오늘도 누락되지 않았는가 |

---

# 7. 재시도와 재처리 용어

## 7.1 핵심 용어

| 영문 | 발음 | 뜻 | 왜 필요한가 |
|---|---|---|---|
| Retry | 리트라이 | 실패한 작업을 다시 실행 | 일시적 장애 복구 |
| Idempotency | 아이덤포턴시 | 멱등성, 같은 요청을 여러 번 처리해도 결과가 한 번 처리한 것과 같은 성질 | 재시도 중복 방지 |
| Duplicate | 듀플리케이트 | 같은 데이터가 두 번 이상 존재 | 재전송·재시도에서 자주 발생 |
| Deduplication | 디듀플리케이션 | 중복 데이터를 제거하는 처리 | 결과 왜곡 방지 |
| Backfill | 백필 | 과거 기간 데이터를 다시 처리 | 로직 수정·누락 보정 |
| Replay | 리플레이 | 보관된 이벤트를 다시 읽어 처리 | 스트리밍 재처리 |
| Checkpoint | 체크포인트 | 어디까지 정상 처리했는지 남긴 진행 상태 | 재시작 위치 판단 |

## 7.2 Idempotency가 중요한 이유

예시:

```text
2026-07-06 주문 파일을 처리함
처리 도중 실패함
같은 파일을 다시 실행함
```

이때 같은 주문이 두 번 들어가면 잘못된 결과가 나옴.

정상 목표:

```text
한 번 실행한 결과
=
여러 번 재실행한 결과
```

이 성질이 멱등성 Idempotency임.

### 간단한 구현 사고

```text
주문 ID를 고유 기준으로 사용
처리 완료 파일·날짜를 기록
기존 결과와 합칠 때 중복 제거
업데이트 또는 병합 방식 사용
```

서비스별 구현은 나중에 학습함.  
지금은 “재시도에는 중복 위험이 있다”만 확실히 기억하면 됨.

---

# 8. 3V: 데이터 문제를 보는 세 기준

| 영문 | 발음 | 뜻 | 문제 예시 |
|---|---|---|---|
| Volume | 볼륨 | 데이터 양 | TB·PB 단위 데이터를 어디에 저장·처리할 것인가 |
| Velocity | 벨로시티 | 생성·유입·처리 속도 | 초당 수천 건 이벤트를 어떻게 처리할 것인가 |
| Variety | 버라이어티 | 형식·출처 다양성 | CSV, JSON, DB, 로그를 어떻게 통합할 것인가 |

문제를 읽을 때 서비스보다 먼저 봄.

```text
문제의 핵심이 데이터 양인가
문제의 핵심이 지연 시간인가
문제의 핵심이 데이터 형식 다양성인가
```

---

# 9. Data Lake, Data Warehouse, Lakehouse

## 9.1 한 번에 외울 최소 차이

| 구조 | 핵심 목적 | 데이터 특성 | 대표 사용 상황 |
|---|---|---|---|
| Data lake | 다양한 원본 데이터를 대규모·저비용으로 보관 | 정형·반정형·비정형 | 탐색, 원본 보관, 유연한 분석 |
| Data warehouse | 정제된 데이터를 빠르게 반복 분석 | 주로 정형·분석용 테이블 | BI, 정기 리포트, 대규모 집계 |
| Data lakehouse | 레이크의 유연성과 웨어하우스식 테이블 관리 결합 | 다양한 데이터 + 관리·분석 특성 | 레이크 위에서 강한 테이블·거버넌스 필요 |

### 비유

```text
Data lake:
원재료와 중간 재료를 많이 보관하는 큰 창고

Data warehouse:
검수·정리된 완제품 분석 창고

Lakehouse:
큰 창고 위에 완제품 관리 규칙과 분석 기능을 함께 올린 구조
```

비유는 방향을 잡는 용도임. 실제 제품 구조는 더 복잡함.

---

# 10. SQL은 어느 수준까지 필요한가

DEA-C01에서 SQL 전문가가 될 필요는 없음.  
다만 분석이 무엇을 하는지 이해하려면 아래는 알아야 함.

| 키워드 | 최소 의미 |
|---|---|
| SELECT | 어떤 컬럼을 읽을지 선택 |
| FROM | 어느 테이블·데이터셋에서 읽을지 지정 |
| WHERE | 조건에 맞는 데이터만 필터 |
| GROUP BY | 같은 기준끼리 묶어 집계 |
| SUM, COUNT, AVG | 합계, 개수, 평균 |
| JOIN | 서로 다른 데이터셋을 공통 키로 연결 |

예:

```sql
SELECT country, SUM(amount)
FROM orders
WHERE order_date = DATE '2026-07-06'
GROUP BY country;
```

뜻:

```text
2026-07-06 주문 중에서
국가별로 묶어
금액 합계를 계산
```

---

# 11. 이번 단계에서 외우지 않을 것

아래는 다음 단계 이후에 다룸.

```text
Bucket, Object, Prefix
Parquet 내부 구조
S3 Lifecycle 설정
Glue Crawler·Job
Athena 비용 계산
Redshift Distribution Key
Kinesis 샤드
IAM Policy JSON
```

기초 문서에서 서비스 구현까지 밀어 넣으면 다시 구조가 무너짐.

---

# 12. 완료 확인

- [x] Row, Column, Record, Field, Value, Data type을 구분 가능
- [x] 정형·반정형·비정형 데이터의 차이를 설명 가능
- [x] Schema와 Metadata의 차이를 설명 가능
- [x] Schema-on-write와 Schema-on-read를 구분 가능
- [x] Validation과 Profiling을 구분 가능
- [x] Retry와 Idempotency가 왜 함께 나오는지 설명 가능
- [x] Volume, Velocity, Variety가 각각 무엇인지 설명 가능
- [x] Data lake와 Data warehouse의 목적 차이를 설명 가능
- [x] 기본 SQL의 SELECT, WHERE, GROUP BY, JOIN의 역할을 설명 가능

---

# 13. 최종 1분 답안

```text
Schema는 데이터 구조의 계약이고,
Metadata는 데이터를 찾고 이해하고 관리하기 위한 설명 정보임.

Data validation은 규칙 통과 여부를 검사하고,
Data profiling은 실제 데이터의 분포와 특성을 파악함.

재시도 Retry는 장애 복구에 필요하지만 중복 적재를 만들 수 있으므로,
같은 데이터를 여러 번 처리해도 결과가 같은 멱등성 Idempotency가 중요함.

Data lake는 다양한 원본 데이터를 유연하게 보관하는 구조이고,
Data warehouse는 정제된 데이터를 반복 분석하기 위한 구조임.
```

---

# 14. 다음 단계

```text
docs/02_storage/01_s3_storage_fundamentals.md
```

다음 단계부터 AWS의 첫 저장 서비스인 S3를 학습함.
