# AWS DEA-C01 Study Lab

> **AWS Certified Data Engineer – Associate (DEA-C01)** 학습·실습·검증 기록 저장소
> 상태: `IN PROGRESS`
> 목표: AWS 서비스를 나열하는 수준이 아니라, 데이터 요구사항을 서비스 선택, 최소 권한, 비용 통제, 운영 검증으로 연결하는 능력을 축적한다.

## Overview

이 저장소는 AWS를 처음 학습하는 관점에서 DEA-C01 범위의 핵심 개념과 실습을 단계적으로 정리한다.

```text
요구사항 → 서비스 선택 → 권한 설계 → 구현 → 검증 → 실패 분석 → 비용 정리
```

## Scope

* AWS foundation: Account, Region, IAM, S3, VPC 기본 개념
* Data lake and governance: S3, Glue Data Catalog, Lake Formation, encryption
* Batch processing: Glue, Athena, Redshift, EMR, Spark
* Streaming and orchestration: Kinesis, MSK, EventBridge, Step Functions, MWAA
* Operations: data quality, monitoring, logging, recovery, cost control
* Current DEA-C01 topics: Iceberg, S3 Tables, vector data concepts, data lineage and governance

> 강의 자료는 보조 자료로만 사용한다. 서비스 동작, 요금, 시험 범위는 실습 또는 응시 전 AWS 공식 문서로 다시 확인한다.

## Repository Structure

```text
.
├─ docs/                 # 개념, 서비스 선택 기준, 용어 정리
├─ labs/                 # 재현 가능한 실습 단위
├─ infra/                # CloudFormation 등 IaC 예제
├─ scripts/              # Python, SQL, 보조 스크립트
├─ evidence/             # 익명화된 검증 결과와 실행 증적
├─ .env.example          # 환경 변수 이름만 공개
├─ .gitignore
└─ README.md
```

## Study Standard

각 문서와 실습은 아래 질문에 답한다.

* 무엇을 해결하거나 검증하는가
* 왜 이 서비스를 선택했는가
* 대안은 무엇이며 왜 제외했는가
* 데이터는 어디서 들어와 어디로 이동하는가
* 어떤 IAM 권한이 왜 필요한가
* 보안, 품질, 비용, 운영 리스크는 무엇인가
* 기대 결과와 실제 검증 결과가 일치하는가
* 종료 후 무엇을 삭제하거나 확인해야 하는가

| Label          | Meaning                          |
| -------------- | -------------------------------- |
| `VERIFIED`     | 실행 결과, 테스트, 로그 또는 AWS 공식 문서로 확인함 |
| `ASSUMPTION`   | 아직 검증하지 않은 전제                    |
| `TODO`         | 미구현 또는 미검증 항목                    |
| `RISK`         | 보안, 비용, 데이터 품질, 운영 리스크           |
| `ANTI-PATTERN` | 학습 편의상 보일 수 있으나 운영 환경에는 부적절한 구성  |
| `CURRENT NOTE` | 강의 시점과 현재 AWS 동작 또는 시험 범위의 차이    |

## Security and Cost Guardrails

### Never commit

다음 항목은 README, 코드, IaC, SQL, 로그, 스크린샷, Git history를 포함해 공개하지 않는다.

* AWS Access Key ID, Secret Access Key, Session Token
* root 계정 정보, MFA 복구 정보, 비밀번호
* `.env`, `~/.aws/credentials`, `.pem`, `.key`, 인증서
* 실제 Account ID, 내부 ARN, 조직 ID, 운영 엔드포인트
* 개인정보, 운영 데이터, 원본 감사 로그

실제 값 대신 환경 변수 또는 예시 값을 사용한다.

```text
${AWS_ACCOUNT_ID}
${AWS_REGION}
${S3_BUCKET_NAME}
${DB_PASSWORD}
```

### Access design

* 기본은 거부이며 필요한 작업만 명시적으로 허용한다.
* `Action: "*"`, `Resource: "*"`, `AdministratorAccess`는 기본 예제로 사용하지 않는다.
* 워크로드는 장기 Access Key 대신 IAM Role과 임시 자격증명을 우선 사용한다.
* S3는 Block Public Access를 기본으로 유지하고, 공개 정책은 기본 구현에 사용하지 않는다.
* 권한 문서에는 Principal, Resource, Action, Condition, 선택 근거를 함께 기록한다.

### Cost control

* 실습마다 과금 가능 리소스와 삭제 절차를 기록한다.
* Redshift, EMR, OpenSearch, NAT Gateway, Elastic IP, CloudWatch Logs, S3 저장·쿼리 결과는 방치하지 않는다.
* 모든 생성 리소스에는 학습 목적 태그를 부여한다.

```text
Project=aws-dea-c01-study-lab
Environment=learning
Owner=<github-id>
AutoDeleteAfter=<YYYY-MM-DD>
```

* 실습 종료 후 리소스, CloudFormation stack, S3 결과 파일·버전·로그를 확인하고 정리한다.

## Lab Template

각 `labs/<lab-name>/README.md`는 아래 항목을 최소로 유지한다.

```text
1. 문제 정의
2. 성공 기준
3. 아키텍처와 데이터 흐름
4. 서비스 선택 근거와 대안 비교
5. 구현 및 사전 조건
6. IAM·보안 검토
7. 검증 결과
8. 실패·제한사항
9. 비용과 정리 절차
10. 출처와 확인일
```

## Progress

* [x] 학습 레포 운영·보안·비용 가드레일 정의
* [ ] 


## Reference Policy

* AWS 공식 문서를 우선 근거로 사용한다.
* 외부 강의, 블로그, 샘플 코드는 출처와 참고 범위를 표시한다.
* 타인의 스크립트, 슬라이드, 코드 전체를 재배포하지 않는다.
* 이 저장소에는 직접 이해하고 재구성한 설명, 직접 작성한 코드, 익명화된 검증 결과만 포함한다.

## Disclaimer

이 저장소는 개인 학습 및 포트폴리오 목적의 기록이다. 운영 환경 적용 전에는 최신 AWS 공식 문서, 조직 보안 정책, 비용 정책을 별도로 검토해야 한다.
