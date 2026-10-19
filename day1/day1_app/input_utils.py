"""공통 정수 입력 및 범위 검사."""

def read_integer(prompt, minimum=None, maximum=None):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("정수를 입력해주세요.")
            continue

        if minimum is not None and number < minimum:
            print(f"{minimum} 이상의 숫자를 입력해주세요.")
        elif maximum is not None and number > maximum:
            print(f"{maximum} 이하의 숫자를 입력해주세요.")
        else:
            return number
