# def preprocess_legacy(data):
#     res = []

#     for row in data:
#         # 치명적 결함: 'score' 키가 없거나 'N/A' 문자열이면 즉시 프로그램 강제 종료!
#         # 치명적 결함: 100점을 초과하는 이상치(120점)도 걸러내지 못하고 1.2로 잘못 정규화함!
#         score = float(row["score"])
#         res.append(round(score / 100.0, 4))

#     return res

# data = [
#     {"name": "김철수", "score": 80},
#     {"name": "이영희", "score": 95},
#     {"name": "박민수", "score": 70},
#     {"name": "김지훈", "score": 110},  # 이상치
#     {"name": "이지영", "score": "N/A"}  # 결함
# ]

# result = preprocess_legacy(data)

# print(result)


def preprocess_legacy(data):
    res = []

    for row in data:
        # 학생 이름 가져오기
        name = row.get("name", "이름 없음")

        # score 값 가져오기
        raw_score = row.get("score")

        # 1. 점수가 없거나 공백, N/A인 경우
        if (
            raw_score is None
            or str(raw_score).strip() == ""
            or str(raw_score).strip().upper() == "N/A"
        ):
            processed_score = "N/A"

        else:
            try:
                # 점수를 숫자로 변환
                score = float(raw_score)

                # 2. 100점 초과 여부 확인
                if score > 100:
                    processed_score = "초과값 입력 오류"

                # 정상 점수 정규화
                else:
                    processed_score = round(score / 100.0, 4)

            except (ValueError, TypeError):
                # 숫자로 변환할 수 없는 값 처리
                processed_score = "N/A"

        # 3. 이름과 처리 결과를 함께 저장
        res.append({
            "name": name,
            "score": processed_score
        })

    return res


# ==========================================
# 테스트 데이터
# ==========================================

data = [
    {"name": "김철수", "score": 80},
    {"name": "이영희", "score": 95},
    {"name": "박민수", "score": "N/A"},
    {"name": "최유진", "score": "   "},
    {"name": "정민호"},
    {"name": "강서연", "score": 101},
    {"name": "윤지호", "score": 120},
    {"name": "한예린", "score": 100},
    {"name": "오준호", "score": 0},
    {"name": "배수빈", "score": "abc"}
]


# ==========================================
# 데이터 전처리 실행
# ==========================================

result = preprocess_legacy(data)


# ==========================================
# 결과 출력
# ==========================================

print("=" * 50)
print("          학생 점수 전처리 결과")
print("=" * 50)

for item in result:
    print(f"학생 이름: {item['name']:<10} | 점수: {item['score']}")

print("=" * 50)