# Local data workspace

## 목적

이 디렉터리는 AWS DEA-C01 실습에 필요한 **작은 로컬 샘플 데이터**만 둠.

실제 데이터 레이크의 기준 저장소는 이후 S3임.  
따라서 이 경로는 운영 데이터 저장소가 아니라, 업로드·변환·검증을 위한 로컬 작업 공간임.

## 구조

```text
data/
├─ sample/     Git에 포함 가능한 작은 예제 데이터
├─ raw/        실습 중 받은 원본 복사본 또는 임시 원본 파일
├─ processed/  변환 중간 결과
└─ curated/    분석·확인용 최종 결과
```

## 규칙

- `sample/`에는 작고 비민감한 예제 데이터만 둠.
- `raw/`, `processed/`, `curated/`에는 실제 API 키, 개인정보, 대용량 산출물을 넣지 않음.
- 원본 데이터는 수정하지 않고, 변환 결과는 `processed/` 또는 `curated/`에 새 파일로 생성함.
- AWS S3 실습에서는 `data/sample/orders.csv`를 S3의 `raw/...` Prefix로 올리는 것으로 시작함.
