class BaseAIModel:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def predict(self, input_data: str) -> str:
        return f"[{self.name} v{self.version}] 기본 추론: {input_data}"


class VisionClassifier(BaseAIModel):
    def __init__(self, name: str, version: str, resolution: str):
        super().__init__(name, version)  # 부모 클래스의 초기화 코드 재사용
        self.resolution = resolution

    def predict(self, input_data: str) -> str:
        # 부모 클래스의 predict() 메서드를 오버라이딩
        return (
            f"[Vision {self.name} ({self.resolution})] "
            f"이미지 '{input_data}' 분석 결과 -> "
            f"'고양이 (확률 98.4%)'"
        )


class TextSummarizerLLM(BaseAIModel):
    def __init__(self, name: str, version: str, max_tokens: int):
        super().__init__(name, version)
        self.max_tokens = max_tokens

    def predict(self, input_data: str) -> str:
        # 부모 클래스의 predict() 메서드를 오버라이딩
        summary = input_data[:18] + "..." if len(input_data) > 18 else input_data

        return (
            f"[LLM {self.name} (max={self.max_tokens})] "
            f"텍스트 요약 결과 -> '{summary}'"
        )


# 다형성: 서로 다른 모델을 하나의 리스트로 관리
pipeline: list[BaseAIModel] = [
    VisionClassifier("YOLO-KDT", "8.2", "640x640"),
    TextSummarizerLLM("Codex-Mini", "2.0", 512),
]

# 모든 모델을 동일한 방식으로 실행
for model in pipeline:
    print(model.predict("실습 데이터 샘플 입력입니다"))