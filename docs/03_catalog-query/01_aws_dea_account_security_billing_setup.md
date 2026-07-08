# AWS DEA-C01 실습 전 계정 세팅 기록

목적: AWS DEA-C01 실습 전에 루트 계정 오남용, 과금 폭주, 권한 혼선을 줄이기 위한 최소 안전선 정리  
현재 판정: 실습 가능선 도달. 단, AWS Budgets 생성 여부와 Root Access Key 없음 여부는 별도 확인 필요

---

## 1. 전체 결론

```text
Root 계정
→ MFA 설정 완료
→ Billing/계정 복구/긴급 작업 전용
→ 평소 실습에서는 사용 금지

CloudWatch 결제 경보
→ us-east-1에서 EstimatedCharges 지표로 생성 완료
→ SNS 이메일 구독 확인 완료
→ 현재 임계값은 2 USD 초과로 확인됨

IAM 사용자 dea-admin
→ 생성 완료
→ MFA 할당 완료
→ 콘솔 로그인 성공
→ 서울 리전에서 실습 시작 가능
```

현재 구조는 완벽한 운영계 보안 구조는 아님. 하지만 무료 실습 계정 기준으로는 적절함.  
처음부터 IAM Identity Center 조직 인스턴스를 밀어붙이면 무료 플랜 경고와 충돌했기 때문에 IAM User 방식으로 우회한 판단이 맞음.

---

## 2. 세팅 순서 요약

| 순서 | 작업 | 상태 | 이유 |
|---:|---|---:|---|
| 1 | AWS 계정 생성 | 완료 | 실습 기반 계정 필요 |
| 2 | Root MFA 설정 | 완료 | 루트 탈취 시 계정 전체가 끝남 |
| 3 | Billing 접근 가능 확인 | 완료 | 과금 확인과 알림 설정을 위해 필요 |
| 4 | CloudWatch Billing Alerts 활성화 | 완료 추정 | 결제 지표를 CloudWatch로 보내기 위한 전제 |
| 5 | CloudWatch 결제 경보 생성 | 완료 | 예상 비용 초과 시 이메일 알림 |
| 6 | SNS 이메일 구독 확인 | 완료 | 경보가 실제 이메일로 발송되려면 구독 확인 필요 |
| 7 | IAM Identity Center 검토 | 보류 | 조직 생성 시 무료 플랜 경고 발생 |
| 8 | IAM 사용자 `dea-admin` 생성 | 완료 | Root 대신 평소 실습할 사용자 필요 |
| 9 | `dea-admin` MFA 설정 | 완료 | IAM 사용자 탈취 방지 |
| 10 | `dea-admin` 콘솔 로그인 검증 | 완료 | Root 봉인 전 실제 사용 가능성 확인 |
| 11 | Billing IAM 접근 | 보류 | 실습에는 필수 아님. Root에서만 확인해도 됨 |
| 12 | AWS Budgets | 미확인 | 월 예산 방어선. 별도 생성 확인 필요 |

---

## 3. 왜 이 순서인가

### 3.1 Root MFA가 먼저인 이유

Root 계정은 AWS 계정의 최상위 소유자임.  
IAM 권한으로도 막기 어려운 계정 수준 작업이 가능함.

따라서 실습 전에 가장 먼저 해야 할 일은 서비스 생성이 아니라 Root MFA 설정임.

```text
S3 먼저 생성
→ 틀린 순서

Root MFA
→ Billing 알림
→ IAM 사용자 분리
→ S3 실습
→ 맞는 순서
```

AWS 공식 문서도 루트 사용자는 필요한 작업에만 사용하고, 루트 자격 증명과 Access Key를 공유하지 말라고 권장함.

---

### 3.2 결제 경보가 IAM보다 먼저인 이유

초보 실습에서 제일 위험한 건 권한보다 비용임.  
특히 Glue, Redshift, Kinesis, EMR, NAT Gateway 같은 서비스는 켜놓고 잊으면 비용이 생길 수 있음.

그래서 최소한 아래 방어선을 먼저 둬야 함.

```text
CloudWatch EstimatedCharges Alarm
+ SNS Email Subscription
+ AWS Budgets
```

현재는 CloudWatch 결제 경보와 SNS 이메일 확인은 완료됨.  
AWS Budgets 생성 여부는 아직 미확인임.

---

### 3.3 IAM Identity Center를 보류한 이유

원래 권장 구조는 IAM Identity Center 기반 접근임.

```text
IAM Identity Center
→ 사용자 생성
→ Permission Set 생성
→ AWS 계정에 권한 할당
→ 임시 자격증명 기반 접근
```

하지만 현재 콘솔에서 아래 경고가 확인됨.

```text
조직을 생성하면 무료 플랜에서 종량제 요금의 유료 플랜으로 자동 업그레이드
프리 티어 크레딧 즉시 만료
```

따라서 현재 목표가 무료 플랜 유지라면, 조직 인스턴스 생성은 보류하는 게 맞음.  
대체안으로 IAM User `dea-admin`을 생성했고, MFA를 붙여 Root 대신 사용하는 구조로 전환함.

---

### 3.4 IAM User를 쓴 이유

이번 구조는 임시 실습용 차선책임.

```text
최선: IAM Identity Center + Permission Set + 임시 자격증명
현재 차선: IAM User + 콘솔 로그인 + MFA
최악: Root 계정으로 계속 실습
```

IAM User는 장기 자격증명을 가질 수 있으므로 운영계에서는 신중히 써야 함.  
하지만 현재는 Access Key를 만들지 않고 콘솔 로그인만 쓰는 구조라 위험을 줄인 상태임.

---

## 4. 현재 구성 상세

## 4.1 Root 계정

| 항목 | 상태 | 설명 |
|---|---:|---|
| 계정 생성 | 완료 | AWS 실습 계정 생성됨 |
| MFA | 완료 | 외부 인증 앱 기반 MFA 설정됨 |
| Billing 접근 | 완료 | Billing 메뉴 접근 가능해짐 |
| 평소 사용 | 금지 | 계정 복구, 결제, 긴급 작업 전용 |
| Root Access Key | 미확인 | 생성하지 않는 것이 원칙. 별도 확인 필요 |

Root는 관리자 계정이 아니라 비상키로 봐야 함.  
평소 실습을 Root로 하면 권한 감각이 박살남.

---

## 4.2 CloudWatch 결제 경보

| 항목 | 값 |
|---|---|
| 서비스 | Amazon CloudWatch |
| 리전 | US East, N. Virginia, `us-east-1` |
| 지표 | `EstimatedCharges` |
| 네임스페이스 | Billing |
| 통화 | USD |
| 통계 | Maximum |
| 기간 | 6시간 |
| 현재 임계값 | `EstimatedCharges > 2` |
| 알림 방식 | SNS Email |
| SNS 구독 상태 | 확인됨 |

중요한 점: 결제 경보는 서울 리전이 아님.

```text
결제 경보 리전 = us-east-1
실습 리전 = ap-northeast-2 서울
```

이유는 CloudWatch Billing 지표가 us-east-1에 저장되고 전 세계 요금을 대표하기 때문임.

### 임계값 판단

현재 화면 기준 경보 조건은 다음과 같음.

```text
EstimatedCharges > 2
```

즉 예상 AWS 요금이 2 USD를 초과하면 경보 발생.

초보 실습 기준 더 보수적으로 가려면 다음이 나음.

```text
EstimatedCharges > 1
```

현재 2 USD도 작동은 정상.  
다만 초기 실습 계정에서는 1 USD가 더 빠른 경고선임.

---

## 4.3 SNS 이메일 구독

| 항목 | 상태 |
|---|---:|
| SNS 주제 | 생성됨 |
| 프로토콜 | EMAIL |
| 구독 상태 | 확인됨 |
| 목적 | CloudWatch 경보 발생 시 이메일 수신 |

SNS에서 `확인됨` 상태가 확인됨.  
따라서 CloudWatch 경보가 발생하면 메일 발송 가능 상태임.

주의:

```text
SNS 구독이 Pending confirmation이면 경보가 있어도 메일이 안 감
```

이번에는 이메일의 Confirm subscription 처리가 완료됐으므로 정상.

---

## 4.4 IAM 사용자 `dea-admin`

| 항목 | 상태 |
|---|---:|
| 사용자 이름 | `dea-admin` |
| 콘솔 로그인 | 성공 |
| MFA | 할당 완료 |
| 권한 | 관리자 권한 부여한 것으로 추정 |
| Access Key | 생성하지 않는 것이 원칙. 현재 생성 여부 별도 확인 필요 |
| 사용 목적 | Root 대체 실습 관리자 |

로그인 화면에서 실수했던 부분도 정리함.

```text
Account ID or alias = 12자리 AWS 계정 ID 또는 계정 별칭
IAM username = dea-admin
Password = dea-admin 비밀번호
```

처음에 `Account ID or alias` 칸에 `dea-admin`을 넣어서 인증 실패 발생.  
이 칸은 사용자명이 아니라 계정 식별자임.

---

## 4.5 IAM 사용자 MFA

| 항목 | 상태 |
|---|---:|
| MFA 디바이스 이름 | `dea-admin-mfa` 계열로 설정 |
| MFA 타입 | 인증 앱 기반 가상 MFA |
| 할당 상태 | 완료 |

AWS는 Root 사용자와 IAM 사용자에 MFA 디바이스를 최대 8개까지 등록할 수 있음.  
로그인 시에는 등록된 MFA 중 1개만 있으면 됨.

의미:

```text
비밀번호만 알아도 로그인 불가
비밀번호 + MFA 코드가 있어야 로그인 가능
```

---

## 4.6 Billing 접근 제한

`dea-admin`으로 로그인 후 콘솔 홈에서 다음 상태가 확인됨.

```text
비용 및 사용량: 액세스 거부됨
이번 달: 액세스 거부됨
예상 월말: 액세스 거부됨
```

이건 오류가 아님.  
AWS는 기본적으로 IAM 사용자와 Role의 Billing 접근을 막음.  
관리자 권한이 있어도 Root 계정에서 `Activate IAM Access`를 켜지 않으면 Billing 콘솔 접근이 제한됨.

현재 판단:

```text
실습에는 치명 문제 아님
Billing은 Root로 확인하거나 결제 경보 이메일로 감시 가능
```

따라서 지금은 Billing IAM 접근을 열지 않아도 됨.

---

## 5. 주요 용어 정리

| 용어 | 뜻 | 이번 실습에서의 의미 |
|---|---|---|
| Root user | AWS 계정 최상위 소유자 | 평소 사용 금지. 비상키 |
| IAM | Identity and Access Management | 사용자, 권한, 역할 관리 서비스 |
| IAM User | AWS 안에 만든 개별 사용자 | `dea-admin`이 여기에 해당 |
| IAM Role | 특정 주체가 임시로 맡는 권한 | Lambda, Glue 실습 때 별도 생성 예정 |
| Policy | 권한 규칙 문서 | 어떤 행동을 허용/거부하는지 정의 |
| AdministratorAccess | 거의 모든 AWS 작업 허용 정책 | 초기 실습 관리자용으로 사용 |
| MFA | Multi-Factor Authentication | 비밀번호 외 추가 인증 수단 |
| SNS | Simple Notification Service | 경보 이메일 발송 통로 |
| CloudWatch | 모니터링과 경보 서비스 | 결제 지표 감시용으로 사용 |
| EstimatedCharges | AWS 예상 요금 지표 | 2 USD 초과 시 경보 설정됨 |
| Billing Alarm | 예상 비용 경보 | 과금 폭주 조기 감지 |
| us-east-1 | 미국 동부 버지니아 북부 리전 | 결제 경보 생성 리전 |
| ap-northeast-2 | 서울 리전 | 실제 S3, Glue, Athena 실습 리전 |
| IAM Identity Center | 중앙 사용자 접근 관리 서비스 | 무료 플랜 경고 때문에 보류 |
| AWS Organizations | 여러 AWS 계정 중앙 관리 서비스 | 지금은 생성하지 않음 |
| AWS Budgets | 예산과 비용 예측 알림 서비스 | 아직 생성 여부 미확인 |

---

## 6. 보안 원칙

## 6.1 Root 봉인

```text
Root는 평소 로그인 금지
Root는 계정 복구, 결제 설정, Billing IAM 접근 같은 특수 작업만 사용
```

Root로 계속 실습하면 모든 권한이 열린 상태라 권한 학습이 안 됨.  
또 실수했을 때 피해 범위가 너무 큼.

---

## 6.2 Access Key 생성 금지

현재 단계에서는 Access Key 만들 필요 없음.

```text
콘솔 실습 = 비밀번호 + MFA
CLI 실습 = 나중에 별도 판단
```

Access Key는 장기 자격증명임.  
깃허브, 노션, 스크린샷, `.env` 유출 시 바로 계정 호출 가능해짐.

따라서 지금은 만들지 않는 게 맞음.

---

## 6.3 리전 분리

```text
결제 감시 = us-east-1
실습 리소스 = 서울 ap-northeast-2
```

리전 혼동하면 CloudWatch Billing 지표를 못 찾거나, 실습 리소스를 엉뚱한 리전에 만들 수 있음.

---

## 6.4 스크린샷 주의

이번 스크린샷에는 다음 정보가 노출됐음.

```text
AWS Account ID
SNS ARN
이메일 주소
IAM 사용자명
```

이 정보들은 비밀키는 아니지만 공개하면 공격자에게 계정 식별 단서가 됨.  
깃허브, 블로그, 커뮤니티에 올릴 때는 반드시 마스킹해야 함.

---

## 7. 현재 남은 확인 사항

| 항목 | 필요 여부 | 이유 |
|---|---:|---|
| AWS Budgets 생성 | 필요 | CloudWatch 경보와 별개로 월 예산/예측 알림 필요 |
| Root Access Key 없음 확인 | 필요 | Root Access Key는 절대 만들면 안 됨 |
| IAM User Access Key 없음 확인 | 권장 | CLI 실습 전까지는 불필요 |
| CloudWatch 경보 임계값 1 USD로 수정 | 선택 | 더 빠른 과금 감지 원하면 수정 |
| Billing IAM access 활성화 | 선택 | `dea-admin`에서 비용 화면을 보고 싶을 때만 필요 |

---

## 8. 다음 실습 진입 조건

다음 실습은 S3부터 시작하면 됨.

진입 조건:

```text
[완료] Root MFA
[완료] CloudWatch 결제 경보
[완료] SNS 이메일 구독 확인
[완료] IAM 사용자 dea-admin
[완료] dea-admin MFA
[완료] dea-admin 콘솔 로그인
[미확인] AWS Budgets
```

S3 소량 실습은 지금 진행 가능함.  
단, Glue, Redshift, Kinesis, EMR 같은 과금 위험 서비스로 넘어가기 전에는 AWS Budgets까지 끝내는 게 맞음.

---

## 9. 다음 실습 순서

```text
1. AWS Budgets 생성 여부 확인
2. S3 버킷 생성
3. raw / processed / curated 경로 생성
4. CSV 업로드
5. Glue Data Catalog 연결
6. Athena SQL 조회
```

처음부터 Redshift, Kinesis, EMR을 만들면 안 됨.  
S3와 Athena 흐름을 먼저 잡아야 데이터 엔지니어링 기본 구조가 보임.

---

## 10. 참고 근거

- AWS CloudWatch Billing Alarm 공식 문서: 결제 경보는 US East, N. Virginia 리전에서 생성해야 하며, Billing metric data는 이 리전에 저장되고 전 세계 요금을 대표한다고 설명함.
- AWS IAM Root User Best Practices 공식 문서: Root user는 필요한 작업에만 사용하고 루트 자격증명과 Access Key를 보호하라고 권장함.
- AWS IAM MFA 공식 문서: Root user와 IAM user는 MFA 디바이스를 최대 8개까지 등록할 수 있고 로그인에는 하나의 MFA만 필요하다고 설명함.
- AWS Billing Access 공식 문서: IAM 사용자와 Role은 기본적으로 Billing 콘솔에 접근할 수 없고, Root가 Activate IAM Access를 켜야 한다고 설명함.
- AWS IAM Identity Center 공식 문서: Free tier 계정에서 AWS Organization을 생성하면 paid plan으로 자동 업그레이드되고 Free Tier credits가 즉시 만료된다고 설명함.

---

## 최종 요약

```text
계정 안전선은 실습 가능 수준까지 올라옴.
Root는 봉인.
dea-admin으로 실습.
결제 경보는 us-east-1에서 정상 생성.
SNS 이메일 구독 확인 완료.
현재 과금 경보선은 2 USD.
Budgets는 아직 확인 필요.
다음은 S3 실습 전 AWS Budgets 확인 또는 생성.
```
