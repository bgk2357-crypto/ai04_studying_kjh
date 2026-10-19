from .input_utils import read_integer


def check_score():
    score = read_integer("점수를 입력하세요 (0~100): ", 0, 100)
    print("합격" if score >= 60 else "불합격")
