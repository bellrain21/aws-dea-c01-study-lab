# AWS DEA-C01 실습 전 보안/과금 및 사전 제반사항에 대한 계정 세팅 기록

목적: AWS DEA-C01 실습 전에 루트 계정 오남용, 과금 폭주, 권한 혼선을 줄이기 위한 최소 안전선 정리  
현재 판정: 실습 가능선 도달. Root 계정은 평소 사용하지 않고, `dea-admin`을 본 실습 계정으로 주력 사용함. Billing IAM 접근 제한은 의도적으로 유지함. 단, AWS Budgets 생성 여부와 Root Access Key 없음 여부는 별도 확인 필요

---

## 1. 전체 결론

```text
Root 계정
→ MFA 설정 완료
→ 평소 사용 안 함
→ Billing/계정 복구/긴급 작업 전용
→ 실습에서는 사용 금지

CloudWatch 결제 경보
→ us-east-1에서 EstimatedCharges 지표로 생성 완료
→ SNS 이메일 구독 확인 완료
→ 현재 임계값은 2 USD 초과로 확인됨

IAM 사용자 dea-admin
→ 생성 완료
→ MFA 할당 완료
→ 콘솔 로그인 성공
→ 본 실습 계정으로 주력 사용
→ 서울 리전에서 실습 시작 가능
```

현재 구조는 완벽한 운영계 보안 구조는 아님. 하지만 무료 실습 계정 기준으로는 적절함.  
처음부터 IAM Identity Center 조직 인스턴스를 밀어붙이면 무료 플랜 경고와 충돌했기 때문에 IAM User 방식으로 우회한 판단이 맞음.

현재 운영 정책은 다음으로 고정함.

```text
Root 계정 사용 안 함
본 실습 계정은 dea-admin
Billing 접근 제한은 유지
```


---

## 2. Root 계정과 하위 계정의 차이

정확한 용어부터 정리함. AWS에서 `dea-admin`은 엄밀히 말해 "하위 계정"이 아님.  
현재 구조에서는 하나의 AWS 계정 안에 존재하는 **IAM 사용자**임.

```text
AWS Account
├─ Root user
│  └─ 계정 생성 이메일과 연결된 최상위 소유자
│
└─ IAM user: dea-admin
   └─ 같은 AWS 계정 안에서 권한을 위임받은 실습 사용자
```

AWS Organizations를 사용하면 별도의 member account를 만들 수 있지만, 현재는 무료 플랜 경고 때문에 Organizations를 만들지 않음.  
따라서 이 문서에서 말하는 "하위 계정"은 실제 별도 AWS 계정이 아니라 `dea-admin` IAM 사용자로 해석함.

### 2.1 Root user와 IAM user 비교

| 구분 | Root user | IAM user `dea-admin` |
|---|---|---|
| 소속 | AWS 계정 자체의 최초 소유자 | 같은 AWS 계정 내부의 사용자 ID |
| 로그인 식별자 | 계정 생성 이메일 | Account ID 또는 alias + IAM username |
| 권한 범위 | 계정 전체에 대한 최상위 권한 | 부여된 IAM 정책 범위 안에서 동작 |
| 권한 축소 방식 | 단일 계정 기준으로 일상 작업용 권한 축소 대상이 아님 | 그룹, 정책, MFA, Access Key 관리로 통제 가능 |
| 사용 목적 | 계정 복구, 결제 핵심 설정, Root 전용 작업 | S3, Glue, Athena 등 일반 실습 |
| 사고 시 피해 | 계정 전체 장악 가능 | 권한 범위 안에서 피해 발생. 삭제/비활성화 가능 |
| 이번 정책 | 평소 사용 금지 | 본 실습 계정으로 사용 |

핵심은 이거임.

```text
Root = 계정의 마스터키
IAM user = 계정 안에서 권한을 빌려 쓰는 작업자 계정
```

마스터키로 매일 문 열고 다니면 안 됨. 잃어버리면 집 전체가 끝남. 작업자 계정은 잃어버려도 비활성화, 비밀번호 교체, MFA 재설정, 정책 제거로 피해를 줄일 수 있음.

### 2.2 왜 Root 계정을 평소 사용하면 안 되는가

AWS 공식 문서는 Root user를 필요한 작업에만 사용하라고 강하게 권장함. 이유는 Root user가 AWS 계정 생성 시 만들어지는 기본 자격 증명이며, 계정 안의 모든 서비스와 리소스에 완전한 접근 권한을 갖기 때문임.

Root 계정 평소 사용이 나쁜 이유는 다음임.

| 이유 | 설명 |
|---|---|
| 폭발 반경이 너무 큼 | Root가 털리면 S3, IAM, 결제, 계정 설정까지 계정 전체가 위험해짐 |
| 최소 권한 원칙 위반 | S3 실습에 계정 해지급 권한은 필요 없음 |
| 실수 방어가 어려움 | 관리자 실습 중 결제, 보안, 계정 설정까지 건드릴 수 있음 |
| 감사 추적 품질 저하 | 모든 작업이 Root로 찍히면 사람별·용도별 책임 분리가 약해짐 |
| 복구 키 노출 증가 | Root는 계정 복구와 소유권 증명에 가까운 자격 증명이라 노출 빈도를 낮춰야 함 |
| Root Access Key 리스크 | Root Access Key는 장기 자격증명 + 전체 권한이라 유출 시 최악 |

따라서 실습 기준 불변식은 다음임.

```text
Root는 로그인 횟수를 최소화함
Root Access Key는 만들지 않음
Root는 MFA 필수
일상 실습은 dea-admin으로만 수행함
```

### 2.3 AWS 권고 사항과 현재 적용 상태

| AWS 권고 방향 | 왜 필요한가 | 현재 적용 상태 |
|---|---|---|
| Root user는 일상 작업에 사용하지 않음 | 전체 권한 자격 증명의 노출 빈도를 줄이기 위함 | 적용. Root 평소 사용 안 함 |
| Root user에 MFA 적용 | 비밀번호 유출만으로 계정 탈취되는 것을 방지 | 적용 완료 |
| Root Access Key 생성 금지 | 장기 자격증명 + 전체 권한 조합이 최악의 리스크 | 미확인. 별도 확인 필요 |
| 일반 작업은 별도 사용자 또는 Role 사용 | 권한 경계와 감사 추적을 만들기 위함 | 적용. `dea-admin` 사용 |
| 가능한 경우 IAM Identity Center 또는 Role 기반 접근 사용 | 장기 자격증명보다 임시 자격증명이 안전함 | 검토했으나 무료 플랜 경고로 보류 |
| MFA를 IAM 사용자에도 적용 | 실습 계정 탈취 방지 | 적용 완료 |
| Billing 접근은 명시적으로 위임 | 비용 정보와 결제 설정 접근을 별도 통제하기 위함 | 제한 유지 |

현재 구조는 최선의 엔터프라이즈 구조는 아님.  
하지만 무료 실습 계정 기준으로는 다음 세 조건을 만족함.

```text
Root 노출 최소화
실습 주체 분리
Billing 접근 제한 유지
```

### 2.4 왜 Billing 접근 제한을 유지하는가

AWS는 기본적으로 IAM 사용자와 Role이 Billing and Cost Management 콘솔에 접근하지 못하게 막음. 관리자 정책이 있어도 Root가 `Activate IAM Access`를 켜지 않으면 Billing 콘솔 접근이 제한됨.

이 구조가 있는 이유는 단순함.

```text
리소스 생성 권한과 결제 정보 접근 권한은 같은 문제가 아님
```

예를 들어 `dea-admin`은 S3, Glue, Athena 실습을 위해 관리자 권한이 필요할 수 있음.  
하지만 실습 계정이 결제 설정, 세금 문서, 결제 정보까지 볼 필요는 없음.

현재 정책은 다음으로 유지함.

```text
실습 = dea-admin
비용 확인 = Root 또는 결제 경보 이메일
Billing IAM access = 활성화하지 않음
```

단, 이 제한은 과금 자체를 막는 기능이 아님. `dea-admin`이 유료 리소스를 만들면 비용은 같은 AWS 계정에 발생함.  
그래서 CloudWatch 결제 경보와 AWS Budgets가 필요함.

### 2.5 현재 구조의 한계

| 한계 | 의미 | 대응 |
|---|---|---|
| `dea-admin`이 별도 AWS 계정은 아님 | 비용과 리소스는 같은 AWS 계정에 귀속됨 | 결제 경보와 Budgets로 감시 |
| `AdministratorAccess`는 강한 권한임 | IAM, S3, Glue 등 대부분 작업 가능 | MFA 적용, Access Key 생성 보류 |
| Billing 제한은 비용 발생 차단이 아님 | 비용 화면 접근만 제한됨 | 과금 위험 서비스는 별도 체크 후 사용 |
| IAM User는 장기 자격증명 구조임 | 운영계 최선은 아님 | 무료 실습 때문에 Identity Center 보류한 차선책 |

따라서 현재 실습 원칙은 다음임.

```text
Root는 봉인
실습은 dea-admin
Access Key는 아직 만들지 않음
Billing 접근 제한 유지
유료 리소스는 만들기 전 비용 구조 확인
```


## 3. 세팅 순서 요약

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
| 11 | Billing IAM 접근 | 제한 유지 | 실습에는 필수 아님. `dea-admin`에서 비용 화면을 열지 않음 |

---

## 4. 왜 이 순서인가

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

## 5. 현재 구성 상세

## 5.1 Root 계정

| 항목 | 상태 | 설명 |
|---|---:|---|
| 계정 생성 | 완료 | AWS 실습 계정 생성됨 |
| MFA | 완료 | 외부 인증 앱 기반 MFA 설정됨 |
| Billing 접근 | 완료 | Billing 메뉴 접근 가능해짐 |
| 평소 사용 | 사용 안 함 | 계정 복구, 결제, 긴급 작업 전용 |
| Root Access Key | 미확인 | 생성하지 않는 것이 원칙. 별도 확인 필요 |

Root는 관리자 계정이 아니라 비상키로 봐야 함.  
현재 정책은 Root 계정을 평소 사용하지 않는 것임. 실습은 `dea-admin`으로 진행함.

평소 실습을 Root로 하면 권한 감각이 박살남.

---

## 5.2 CloudWatch 결제 경보

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

---

## 5.3 SNS 이메일 구독

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

## 5.4 IAM 사용자 `dea-admin`

| 항목 | 상태 |
|---|---:|
| 사용자 이름 | `dea-admin` |
| 콘솔 로그인 | 성공 |
| MFA | 할당 완료 |
| 권한 | 관리자 권한 부여한 것으로 추정 |
| Access Key | 생성하지 않는 것이 원칙. 현재 생성 여부 별도 확인 필요 |
| 사용 목적 | Root 대체 본 실습 계정 |

현재 실습의 기본 로그인 주체는 `dea-admin`임. Root는 사용하지 않음.

로그인 화면에서 실수했던 부분도 정리함.

```text
Account ID or alias = 12자리 AWS 계정 ID 또는 계정 별칭
IAM username = dea-admin
Password = dea-admin 비밀번호
```

처음에 `Account ID or alias` 칸에 `dea-admin`을 넣어서 인증 실패 발생.  
이 칸은 사용자명이 아니라 계정 식별자임.

---

## 5.5 IAM 사용자 MFA

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

## 5.6 Billing 접근 제한

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
Billing 접근 제한은 유지
Billing은 Root로 확인하거나 결제 경보 이메일로 감시 가능
```

따라서 지금은 Billing IAM 접근을 열지 않음. `dea-admin`은 본 실습 계정이지만 Billing 확인 계정은 아님.

---

## 6. 주요 용어 정리

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

---

## 7. 보안 원칙

## 7.1 Root 봉인

```text
Root는 평소 사용 안 함
Root는 계정 복구, 결제 설정, 긴급 복구 같은 특수 작업만 사용
본 실습은 dea-admin으로 진행
```

Root로 계속 실습하면 모든 권한이 열린 상태라 권한 학습이 안 됨.  
또 실수했을 때 피해 범위가 너무 큼.

---

## 7.2 Access Key 생성 금지

현재 단계에서는 Access Key 만들 필요 없음.

```text
콘솔 실습 = 비밀번호 + MFA
CLI 실습 = 나중에 별도 판단
```

Access Key는 장기 자격증명임.  
깃허브, 노션, 스크린샷, `.env` 유출 시 바로 계정 호출 가능해짐.

따라서 지금은 만들지 않는 게 맞음.

---

## 7.3 리전 분리

```text
결제 감시 = us-east-1
실습 리소스 = 서울 ap-northeast-2
```

리전 혼동하면 CloudWatch Billing 지표를 못 찾거나, 실습 리소스를 엉뚱한 리전에 만들 수 있음.

---

## 7.4 스크린샷 주의

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

## 8. 현재 남은 확인 사항

| 항목 | 필요 여부 | 이유 |
|---|---:|---|
| AWS Budgets 생성 | 필요 | CloudWatch 경보와 별개로 월 예산/예측 알림 필요 |
| Root Access Key 없음 확인 | 필요 | Root Access Key는 절대 만들면 안 됨 |
| IAM User Access Key 없음 확인 | 권장 | CLI 실습 전까지는 불필요 |
| CloudWatch 경보 임계값 1 USD로 수정 | 선택 | 더 빠른 과금 감지 원하면 수정 |
| Billing IAM access 활성화 | 현재 보류 | 현재 정책은 접근 제한 유지. 비용은 경보와 Root 확인으로 관리 |

---

## 9. 다음 실습 진입 조건

다음 실습은 S3부터 시작하면 됨.

진입 조건:

```text
[완료] Root MFA
[완료] CloudWatch 결제 경보
[완료] SNS 이메일 구독 확인
[완료] IAM 사용자 dea-admin
[완료] dea-admin MFA
[완료] dea-admin 콘솔 로그인
[유지] Billing IAM 접근 제한
```

Glue, Redshift, Kinesis, EMR 같은 과금 위험 서비스로 넘어가기 전에는 AWS Budgets까지 끝내는 게 맞음.

---

## 10. 다음 실습 순서

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

## 11. 참고 근거

- [AWS CloudWatch Billing Alarm 공식 문서](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html): 결제 경보는 US East, N. Virginia 리전에서 생성해야 하며, Billing metric data는 이 리전에 저장되고 전 세계 요금을 대표한다고 설명함.
- [AWS Root user best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html): Root user는 필요한 작업에만 사용하고 루트 자격 증명과 계정 복구 수단을 보호하라고 권장함.
- [AWS Sign-In user types](https://docs.aws.amazon.com/signin/latest/userguide/user-types-list.html): Root user는 AWS 계정 생성 시 만들어지는 신원이며 모든 AWS 서비스와 리소스에 완전한 접근 권한을 가진다고 설명함.
- [AWS Well-Architected Security - Secure account root user](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_aws_account.html): Root user는 일상 작업에 사용하지 말고, Root 전용 작업에만 사용하라고 설명함.
- [AWS Prescriptive Guidance - Restrict use of the root user](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-02.html): Root MFA 적용과 일상 작업용 administrative user 생성을 권고함.
- [AWS IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html): 가능한 경우 IAM Role과 phishing-resistant MFA 사용을 권장함.
- [AWS IAM access keys 공식 문서](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): Root 자격 증명으로 Access Key를 만들지 말고, Access Key를 코드나 애플리케이션 파일에 넣지 말라고 경고함.
- [AWS IAM MFA 공식 문서](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html): Root user와 IAM user는 MFA 디바이스를 최대 8개까지 등록할 수 있고 로그인에는 하나의 MFA만 필요하다고 설명함.
- [AWS Billing access 공식 문서](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/control-access-billing.html): IAM 사용자와 Role은 기본적으로 Billing 콘솔에 접근할 수 없고, Root가 Activate IAM Access를 켜야 한다고 설명함.
- [AWS IAM Identity Center enable 공식 문서](https://docs.aws.amazon.com/singlesignon/latest/userguide/enable-identity-center.html): Free tier 계정에서 AWS Organization 생성 시 paid plan 전환 및 Free Tier credit 만료 경고가 있음을 설명함.

---

## 최종 요약

```text
계정 안전선은 실습 가능 수준까지 올라옴.
Root는 AWS 계정의 마스터키이며 평소 사용하지 않음.
dea-admin은 별도 AWS 계정이 아니라 같은 계정 안의 IAM 실습 사용자임.
dea-admin을 본 실습 계정으로 사용.
Billing IAM 접근 제한은 유지.
결제 경보는 us-east-1에서 정상 생성.
SNS 이메일 구독 확인 완료.
현재 과금 경보선은 2 USD.
Budgets는 아직 확인 필요.
다음은 S3 실습 전 AWS Budgets 확인 또는 생성.
```
