# zip
# list_1 = ["a", "b", "c"]
# list_2 = [100, 200, 300]
# result = zip(list_1, list_2)
# for i in result:
#     print(i)
# # zip을 생성한 객체를 dictionary로 변환
# result = dict(zip(list_1, list_2))
# print(result)

# R I O C
# Role : 역할
# I Input : 입력
# O Output : 출력
# C Constraints : 제약조건(어떤 알고리즘/ 규칙, 뭘할지)


# [Role]
# 너는 온라인 게임 채팅 시스템의 백엔드 파이썬 개발자야.

# [Task]
# 채팅 메시지에서 금지 단어를 찾아 마스킹(*) 처리하는 함수를 작성해줘.

# [Input]
# 1. chat_message (str): 사용자가 입력한 채팅 메시지
# 2. bad_words (list[str]): 금지 단어 목록

# [Output]
# - masked_message (str): 금지어가 '*'로 치환된 최종 문자열

# [Constraints & Logic]
# - 함수명: mask_bad_words(chat_message: str, bad_words: list[str]) -> str
# - 금지 단어의 글자 수만큼 '*'로 치환할 것 (예: "바보" -> "**")
# - 대소문자를 구분하지 않고 찾되, 원본 메시지의 다른 문장 구조는 그대로 보존할 것
# - 주석으로 각 핵심 라인이 어떻게 동작하는지 초보자도 알기 쉽게 달아줄 것
# -생성하는 코드는 대중적으로 해석하기 쉬운 기본문법과 라이브러리만을 사용할것
# -생성된 코드는 오류가 없는지 확인할것
# -예측가능한 테스트케이스를 (assert를 사용) 다양하게 만들고 실행해서 오류가 있으면 수정할것

import re


def mask_bad_words(chat_message: str, bad_words: list[str]) -> str:
    # 각 글자를 가릴지 기록합니다. 처음에는 모두 False입니다.
    mask_positions = [False] * len(chat_message)

    for word in bad_words:
        # 빈 문자열은 검색하지 않고 건너뜁니다.
        if word == "":
            continue

        # escape: '.', '+' 같은 특수문자도 일반 글자로 검색합니다.
        # IGNORECASE: 영문 대소문자를 구분하지 않습니다.
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        search_start = 0

        while True:
            # 지정한 위치부터 다음 금지어를 찾습니다.
            match = pattern.search(chat_message, search_start)

            # 더 이상 찾을 수 없으면 이 금지어의 검색을 끝냅니다.
            if match is None:
                break

            # 금지어가 차지하는 위치를 모두 표시합니다.
            for index in range(match.start(), match.end()):
                mask_positions[index] = True

            # 시작 위치에서 한 글자 이동해 겹치는 금지어도 찾습니다.
            search_start = match.start() + 1

    # 표시된 글자만 '*'로 바꾸고 나머지 글자는 그대로 연결합니다.
    return "".join(
        "*" if mask_positions[index] else character
        for index, character in enumerate(chat_message)
    )


# 1. 한글 금지어
assert mask_bad_words("너는 바보야!", ["바보"]) == "너는 **야!"

# 2~3. 대소문자 구분 없이 검색
assert mask_bad_words("BAD bad BaD", ["bad"]) == "*** *** ***"
assert mask_bad_words("bad BAD", ["BAD"]) == "*** ***"

# 4. 여러 금지어
assert mask_bad_words("바보와 멍청이", ["바보", "멍청이"]) == "**와 ***"

# 5. 금지어가 없는 메시지
assert mask_bad_words("안녕하세요!", ["바보"]) == "안녕하세요!"

# 6~9. 빈 메시지, 빈 목록, 빈 금지어
assert mask_bad_words("", ["bad"]) == ""
assert mask_bad_words("hello", []) == "hello"
assert mask_bad_words("hello", [""]) == "hello"
assert mask_bad_words("bad", ["", "bad"]) == "***"

# 10. 연속해서 등장하는 금지어
assert mask_bad_words("badbad", ["bad"]) == "******"

# 11. 같은 금지어가 겹치는 경우
assert mask_bad_words("ababa", ["aba"]) == "*****"

# 12~13. 서로 다른 금지어가 겹쳐도 목록 순서와 무관하게 처리
assert mask_bad_words("abc", ["ab", "bc"]) == "***"
assert mask_bad_words("abc", ["bc", "ab"]) == "***"

# 14. 다른 단어 안에 포함된 금지어도 처리
assert mask_bad_words("badly", ["bad"]) == "***ly"

# 15. 특수문자를 포함한 금지어
assert mask_bad_words(
    "a.b aXb C++ [x]", ["a.b", "c++", "[x]"]
) == "*** aXb *** ***"

# 16. 공백, 줄바꿈, 탭, 문장부호 보존
assert mask_bad_words(
    "  BAD,\n바보!\t끝  ", ["bad", "바보"]
) == "  ***,\n**!\t끝  "

# 17. 중복 금지어
assert mask_bad_words("bad", ["bad", "bad"]) == "***"

# 18. 메시지보다 긴 금지어
assert mask_bad_words("hi", ["longword"]) == "hi"

# 19~20. 이모지 및 다른 유니코드 문자 보존
assert mask_bad_words("🙂바보🙂", ["바보"]) == "🙂**🙂"
assert mask_bad_words("İbad", ["bad"]) == "İ***"

print("모든 테스트를 통과했습니다.")