from .input_utils import read_integer


def print_even_numbers():
    numbers = []
    for i in range(5):
        numbers.append(read_integer(f"{i + 1}번째 숫자를 입력하세요: "))

    print("리스트변수의 값:", numbers)
    print("짝수:")
    even_numbers = [number for number in numbers if number % 2 == 0]
    if even_numbers:
        for number in even_numbers:
            print(number)
    else:
        print("입력한 숫자에 짝수가 없습니다.")
