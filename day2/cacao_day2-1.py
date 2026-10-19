import re


# ==========================================
# 1. 금지어 마스킹 함수
# ==========================================

def mask_bad_words(chat_message: str, bad_words: list[str]) -> str:
    """
    채팅 메시지에서 금지어를 찾아 글자 수만큼 '*'로 치환한다.

    입력:
        chat_message: 사용자가 입력한 채팅 메시지
        bad_words: 금지어 목록

    반환:
        금지어가 '*'로 치환된 문자열
    """

    # 1. 메시지가 비어 있거나 금지어 목록이 비어 있으면 원본 반환
    if not chat_message or not bad_words:
        return chat_message

    # 2. 빈 문자열인 금지어는 제외
    # 빈 문자열은 검색할 대상이 없으므로 처리하지 않는다.
    valid_bad_words = [word for word in bad_words if word]

    # 3. 유효한 금지어가 없으면 원본 반환
    if not valid_bad_words:
        return chat_message

    # 4. 금지어를 긴 순서대로 정렬
    # 예: ["바보", "보"] 순서로 검사하여 긴 단어를 먼저 찾는다.
    valid_bad_words.sort(key=len, reverse=True)

    # 5. 정규표현식에서 특별한 의미를 가진 문자를 안전하게 처리
    # re.escape()는 금지어를 일반적인 문자열로 검색할 수 있게 한다.
    escaped_words = [re.escape(word) for word in valid_bad_words]

    # 6. 여러 금지어를 하나의 검색 패턴으로 결합
    # | 는 정규표현식에서 OR(또는)을 의미한다.
    pattern = re.compile("|".join(escaped_words), re.IGNORECASE)

    # 7. 발견된 금지어를 글자 수만큼 '*'로 치환
    # match.group(0)은 실제로 발견된 문자열이다.
    # re.IGNORECASE를 사용하므로 영어 대소문자를 구분하지 않는다.
    masked_message = pattern.sub(
        lambda match: "*" * len(match.group(0)),
        chat_message
    )

    # 8. 마스킹된 메시지 반환
    return masked_message


# ==========================================
# 2. 테스트 케이스
# ==========================================

# 테스트 1: 한글 금지어 마스킹
assert mask_bad_words("안녕 바보야!", ["바보"]) == "안녕 **야!"

# 테스트 2: 영어 대소문자 구분 없이 마스킹
assert mask_bad_words("You are BAD!", ["bad"]) == "You are ***!"

# 테스트 3: 영어 금지어가 여러 번 등장하는 경우
assert mask_bad_words("bad BAD Bad", ["bad"]) == "*** *** ***"

# 테스트 4: 여러 금지어 마스킹
assert mask_bad_words("바보와 멍청이", ["바보", "멍청이"]) == "**와 ***"

# 테스트 5: 금지어가 없는 경우 원본 유지
assert mask_bad_words("안녕하세요!", ["바보", "멍청이"]) == "안녕하세요!"

# 테스트 6: 금지어 목록이 비어 있는 경우
assert mask_bad_words("안녕 바보야!", []) == "안녕 바보야!"

# 테스트 7: 빈 메시지 처리
assert mask_bad_words("", ["바보"]) == ""

# 테스트 8: 금지어 목록에 빈 문자열만 있는 경우
assert mask_bad_words("안녕하세요!", [""]) == "안녕하세요!"

# 테스트 9: 긴 금지어를 먼저 처리
assert mask_bad_words("바보야, 보!", ["보", "바보"]) == "**야, *!"

# 테스트 10: 문장 부호와 공백 유지
assert mask_bad_words("바보, 정말 바보야!", ["바보"]) == "**, 정말 **야!"

# 테스트 11: 대소문자가 섞인 금지어
assert mask_bad_words("HeLLo hello HELLO", ["hello"]) == "***** ***** *****"

# 테스트 12: 특수문자가 포함된 금지어
assert mask_bad_words("욕설: a.b!", ["a.b"]) == "욕설: ***!"


# ==========================================
# 3. 테스트 결과 출력
# ==========================================

print("모든 테스트 케이스를 통과했습니다!")


# ==========================================
# 4. 실제 사용 예제
# ==========================================

chat_message = "안녕 바보야! You are BAD!"
bad_words = ["바보", "bad"]

result = mask_bad_words(chat_message, bad_words)

print("원본 메시지:", chat_message)
print("마스킹 결과:", result)