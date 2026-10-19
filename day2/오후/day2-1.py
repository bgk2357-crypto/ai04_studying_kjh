# what            : 무엇을 만들지
# Consistanats    : 어떤 제약으로 동작해야 하는지
# How             : 구현은 어떻게 
# vibe Check      : 결과를 검증
# 3대 핵심 롤 p(Prompt)->g(Genenrator)->v(Validator) 사이클
# p(Prompt) : 입력(input),출력(output), 알고리즘 제약 조건,  함수 명시
# Validator : 결과검증, 테스트케이스 검증

# 1부터 N까지의 짝수 합과 개수 구하기
# Bed : 짝수 합 구해줘

# [Problem] 1부터 n까지의 정수 중 짝수들의 합과 짝수의 총 개수를 계산한다
# [Function] calculate_even_sum_and_count(n)
# [Rules]
#     - n이 1 미만인 경우 합 0, 개수 0을 반환할것
#     - for 문과 if 문을 활용하여 짝수(i % 2 ==0)를 판단할 것
# [Output]    {"Sum": int, "Count":int  } 


# # 실습규칙
# ...
# 문제정의 / 입력값 / 출력값 / 제약조건을 작성
# assert 함수를 활용하여 테스트케이스를 작성
# ...

# [Mission 1: Smart FizzBuzz Analyzer]
# - 함수명: analyze_fizzbuzz(limit: int) -> dict
# - 로직 제약:
#   1. 1부터 limit까지 순회한다.
#   2. 3의 배수이면서 5의 배수이면: "FizzBuzz" 카운트 증가
#   3. 3의 배수이면: "Fizz" 카운트 증가
#   4. 5의 배수이면: "Buzz" 카운트 증가
#   5. 그 외의 숫자이면: "Number" 카운트 증가
# - 반환값 형식:
#   {"FizzBuzz": int, "Fizz": int, "Buzz": int, "Number": int}
# - 엣지 케이스: limit가 1 미만인 경우 모든 카운트가 0인 딕셔너리 반환


# ==========================================
# Mission 1: Smart FizzBuzz Analyzer
# ==========================================

# 1. 함수 정의
def analyze_fizzbuzz(limit: int) -> dict:
    """
    1부터 limit까지의 정수를 순회하면서
    FizzBuzz, Fizz, Buzz, Number의 개수를 계산한다.

    반환값:
    {
        "FizzBuzz": int,
        "Fizz": int,
        "Buzz": int,
        "Number": int
    }
    """

    # 카운트 초기화
    result = {
        "FizzBuzz": 0,
        "Fizz": 0,
        "Buzz": 0,
        "Number": 0
    }

    # 엣지 케이스: limit가 1 미만이면 0 반환
    if limit < 1:
        return result

    # 1부터 limit까지 순회
    for i in range(1, limit + 1):

        # 3과 5의 공배수
        if i % 3 == 0 and i % 5 == 0:
            result["FizzBuzz"] += 1

        # 3의 배수
        elif i % 3 == 0:
            result["Fizz"] += 1

        # 5의 배수
        elif i % 5 == 0:
            result["Buzz"] += 1

        # 그 외의 숫자
        else:
            result["Number"] += 1

    # 결과 반환
    return result


# ==========================================
# 2. 테스트 케이스
# ==========================================

# Test Case 1: limit = 15
assert analyze_fizzbuzz(15) == {
    "FizzBuzz": 1,
    "Fizz": 4,
    "Buzz": 2,
    "Number": 8
}

# Test Case 2: limit = 10
assert analyze_fizzbuzz(10) == {
    "FizzBuzz": 0,
    "Fizz": 3,
    "Buzz": 2,
    "Number": 5
}

# Test Case 3: limit = 1
assert analyze_fizzbuzz(1) == {
    "FizzBuzz": 0,
    "Fizz": 0,
    "Buzz": 0,
    "Number": 1
}

# Test Case 4: limit = 0
assert analyze_fizzbuzz(0) == {
    "FizzBuzz": 0,
    "Fizz": 0,
    "Buzz": 0,
    "Number": 0
}

# Test Case 5: limit = -5
assert analyze_fizzbuzz(-5) == {
    "FizzBuzz": 0,
    "Fizz": 0,
    "Buzz": 0,
    "Number": 0
}

# Test Case 6: limit = 3
assert analyze_fizzbuzz(3) == {
    "FizzBuzz": 0,
    "Fizz": 1,
    "Buzz": 0,
    "Number": 2
}

# Test Case 7: limit = 5
assert analyze_fizzbuzz(5) == {
    "FizzBuzz": 0,
    "Fizz": 1,
    "Buzz": 1,
    "Number": 3
}


# ==========================================
# 3. 테스트 결과 출력
# ==========================================

print("===================================")
print("모든 테스트 케이스를 통과했습니다!")
print("===================================")


# ==========================================
# 4. 실제 실행 결과 확인
# ==========================================

test_limit = 0

print(f"\n입력값: {test_limit}")
print("분석 결과:")

result = analyze_fizzbuzz(test_limit)

for key, value in result.items():
    print(f"{key}: {value}")