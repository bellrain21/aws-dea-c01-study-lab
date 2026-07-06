"""S3에 로컬 샘플 파일을 업로드하는 최소 실습 스크립트.

목적:
    S3의 Bucket, Object, Object Key, Prefix를 콘솔과 코드 양쪽에서 확인함.

왜 필요한가:
    콘솔에서 파일을 업로드하는 것만으로는 Object Key와 Prefix가 API 관점에서
    어떻게 전달되는지 확인하기 어려움. 이 스크립트는 로컬 파일 하나를 지정한
    Bucket과 Object Key로 업로드해 그 관계를 명확히 보여줌.

입력:
    --bucket       업로드할 기존 S3 Bucket 이름
    --source-file  업로드할 로컬 파일 경로
    --object-key   S3 Object Key. 예: raw/2026/07/06/orders.csv
    --dry-run      AWS 호출 없이 입력값과 업로드 대상을 검증만 함

출력:
    성공 시 지정한 Bucket에 Object 하나가 생성됨.
    Object Key의 '/'는 S3 실제 폴더가 아니라 Prefix를 표현하는 문자열 관례임.

핵심 불변식:
    - AWS 자격증명, Bucket 이름, 리전은 코드에 하드코딩하지 않음.
    - 원본 파일은 로컬에서 수정하지 않음.
    - --dry-run에서는 AWS API를 호출하지 않음.
    - Object Key가 비어 있으면 업로드하지 않음.

실패·예외:
    - 로컬 파일이 없으면 종료함.
    - boto3가 설치되지 않았거나 AWS 자격증명이 없으면 원인을 표시하고 종료함.
    - Bucket 접근 권한이 없거나 Bucket이 없으면 AWS 오류를 그대로 표시함.

실행 예시:
    # AWS 호출 없이 대상만 확인
    python src/s3_upload_sample.py \
        --bucket my-dea-c01-lab-bucket \
        --source-file data/sample/orders.csv \
        --object-key raw/2026/07/06/orders.csv \
        --dry-run

    # 실제 업로드
    python src/s3_upload_sample.py \
        --bucket my-dea-c01-lab-bucket \
        --source-file data/sample/orders.csv \
        --object-key raw/2026/07/06/orders.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """명령행 입력을 읽고, 실습에 필요한 최소 인자만 검증함."""
    parser = argparse.ArgumentParser(
        description="Upload one local file to an existing Amazon S3 bucket."
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="Existing S3 bucket name. Do not include s3://.",
    )
    parser.add_argument(
        "--source-file",
        required=True,
        type=Path,
        help="Local file path to upload.",
    )
    parser.add_argument(
        "--object-key",
        required=True,
        help="S3 object key, for example raw/2026/07/06/orders.csv.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the target without calling AWS.",
    )
    return parser.parse_args(argv)


def validate_inputs(source_file: Path, object_key: str) -> None:
    """업로드 전에 파일 존재와 Object Key 최소 조건을 확인함."""
    if not source_file.is_file():
        raise FileNotFoundError(f"Local source file does not exist: {source_file}")

    if not object_key.strip():
        raise ValueError("Object key must not be empty.")

    if object_key.startswith("/"):
        raise ValueError(
            "Object key must not start with '/'. "
            "Use raw/2026/07/06/orders.csv instead."
        )


def upload_file(bucket: str, source_file: Path, object_key: str) -> None:
    """boto3를 사용해 검증된 로컬 파일 하나를 S3 Object로 업로드함."""
    try:
        import boto3
    except ImportError as error:
        raise RuntimeError(
            "boto3 is required for actual upload. "
            "Install it with: pip install boto3"
        ) from error

    s3_client = boto3.client("s3")
    s3_client.upload_file(str(source_file), bucket, object_key)


def main(argv: Sequence[str] | None = None) -> int:
    """입력 검증 후 Dry run 또는 실제 S3 업로드를 수행함."""
    args = parse_args(argv)

    try:
        validate_inputs(args.source_file, args.object_key)
    except (FileNotFoundError, ValueError) as error:
        print(f"Input validation failed: {error}", file=sys.stderr)
        return 2

    target = f"s3://{args.bucket}/{args.object_key}"
    print(f"Source file : {args.source_file}")
    print(f"Object key  : {args.object_key}")
    print(f"Target      : {target}")

    if args.dry_run:
        print("Dry run complete. No AWS API call was made.")
        return 0

    try:
        upload_file(args.bucket, args.source_file, args.object_key)
    except Exception as error:
        # AWS SDK 오류는 인증·권한·Bucket 존재 여부 등 여러 원인을 가질 수 있으므로
        # 이 단계에서는 원본 오류 메시지를 유지해 원인 추적 근거를 보존함.
        print(f"S3 upload failed: {error}", file=sys.stderr)
        return 1

    print("Upload complete. Confirm the Object and Prefix in the S3 console.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
