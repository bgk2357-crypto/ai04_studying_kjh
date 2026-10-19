"""실습 선택 메뉴와 프로그램 실행."""

from .addition import addition
from .score import check_score
from .even_numbers import print_even_numbers
from .multiplication import multiplication_table
from .guessing_game import guessing_game
from .input_utils import read_integer


def main():
    exercises = {
        1: addition,
        2: check_score,
        3: print_even_numbers,
        4: multiplication_table,
        5: guessing_game,
    }

    while True:
        print("\n===== 1일차 파이썬 실습 =====")
        print("1. 두 숫자 더하기")
        print("2. 점수 합격 판정")
        print("3. 숫자 5개 중 짝수 출력")
        print("4. 구구단 출력 (2~4단, ×1~×4)")
        print("5. 숫자 맞추기 게임")
        print("0. 종료")
        choice = read_integer("메뉴를 선택하세요: ", 0, 5)
        if choice == 0:
            print("프로그램을 종료합니다.")
            return
        print()
        exercises[choice]()


def run():
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
