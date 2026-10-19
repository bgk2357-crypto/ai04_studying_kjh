class AIServiceError(Exception):
    """AI 서비스 최상위 기본 예외 클래스"""
    pass


class PromptEmptyError(AIServiceError):
    """프롬프트가 비어 있을 때 발생하는 예외"""
    pass


class TokenQuotaExceededError(AIServiceError):
    """토큰 한도 초과 시 요청량과 잔여 한도 정보를 전달하는 예외"""

    def __init__(self, requested: int, remaining: int):
        self.requested = requested
        self.remaining = remaining

        super().__init__(
            f"토큰 한도 초과! "
            f"(요청: {requested}개, 잔여 한도: {remaining}개)"
        )


class CodexClient:
    def __init__(self, daily_quota: int = 100):
        self.remaining_tokens = daily_quota

    def generate_code(self, prompt: str, estimated_tokens: int) -> str:
        # 프롬프트가 비어 있는지 검사
        if not prompt.strip():
            raise PromptEmptyError(
                "프롬프트에 최소 1글자 이상의 명령어를 입력해주세요."
            )

        # 토큰 한도 초과 여부 검사
        if estimated_tokens > self.remaining_tokens:
            raise TokenQuotaExceededError(
                estimated_tokens,
                self.remaining_tokens
            )

        # 사용한 토큰 차감
        self.remaining_tokens -= estimated_tokens

        return (
            f"[생성 성공] '{prompt}' 코드 생성 완료 "
            f"(남은 토큰: {self.remaining_tokens})"
        )


# AI 클라이언트 생성: 일일 토큰 한도 50개
client = CodexClient(daily_quota=50)


# 테스트 요청 목록
test_requests = [
    ("클래스 리팩토링 코드 작성", 30),
    ("   ", 10),
    ("대규모 프로젝트 전체 변환", 40),
]


# 요청 처리 및 예외 처리
for prompt_text, tokens in test_requests:
    try:
        result = client.generate_code(prompt_text, tokens)
        print(result)

    except PromptEmptyError as e:
        print(f"[입력 검증 실패] {e}")

    except TokenQuotaExceededError as e:
        print(
            f"[쿼터 경보] {e} -> "
            f"기본 요금제를 업그레이드하거나 요청 길이를 줄이세요."
        )