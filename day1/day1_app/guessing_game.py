import random

from .input_utils import read_integer


def guessing_game():
    com_number = random.randint(1, 100)
    count = 0

    while True:
        user_number = read_integer("1~100 사이의 숫자를 입력하세요: ", 1, 100)
        count += 1

        if user_number > com_number:
            print("컴퓨터 랜덤 숫자보다 큽니다. 더 작은 숫자를 입력하세요.")
        elif user_number < com_number:
            print("컴퓨터 랜덤 숫자보다 작습니다. 더 큰 숫자를 입력하세요.")
        else:
            print("정답입니다!")
            print(f"정답 입력 횟수: {count}회")
            break
