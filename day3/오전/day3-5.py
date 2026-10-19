raw_logs = [
    "epoch=1,loss=0.45,acc=88.5",
    "epoch=2,loss=invalid,acc=91.0",  # ValueError 발생
    "epoch=3,loss=0.31",              # KeyError 발생: acc 키 누락
    "epoch=4,loss=0.22,acc=94.2",
]


def parse_training_logs(logs: list[str]) -> list[dict]:
    valid_records = []

    for idx, line in enumerate(logs, start=1):
        try:
            parts = dict(item.split("=") for item in line.split(","))

            record = {
                "epoch": int(parts["epoch"]),
                "loss": float(parts["loss"]),
                "acc": float(parts["acc"]),
            }

        except ValueError as e:
            print(
                f"[Line {idx} 변환 오류] 숫자 형식이 아닙니다: "
                f"'{line}' ({e})"
            )

        except KeyError as e:
            print(
                f"[Line {idx} 필드 누락] 필수 키 {e}가 없습니다: "
                f"'{line}'"
            )

        else:
            valid_records.append(record)
            print(
                f"[Line {idx} 정상 수집] "
                f"Epoch {record['epoch']} -> "
                f"Accuracy: {record['acc']}%"
            )

        finally:
            pass  # 각 라인 검사 완료 후 스트림 상태 점검 위치

    print(
        f"[파서 종료] 총 {len(logs)}건 중 "
        f"{len(valid_records)}건 정상 로드 완료."
    )

    return valid_records


# 학습 로그 파싱 실행
parsed = parse_training_logs(raw_logs)

# 정상적으로 수집된 데이터 확인
print("\n최종 파싱 결과:")
print(parsed)