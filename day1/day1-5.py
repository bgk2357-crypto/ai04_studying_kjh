# 숫자 맞추기 게임
# 규칙
# 컴퓨터가 1~100사이의 값을 임의로 생성한 후
# 사용자가 맞추는 게임
# 사용자가 입력한 값이 크면 크다 작으면 작다라고 알려줌

# --필요한 기능
# 입력 : int(input())
# 컴퓨터가 1~100사이의 임의의 숫자를 선택
# 비교연산자를 통해 크다 작다 판별
# 순환문, 조건문, break

# import random

# for i in range(3):
#     number = random.randint(1, 100)
#     print(number)

# import random

# com_number = random.randint(1, 100)
# user_number = int(input("1~100 : "))
# if user_number > com_number:
#     print("컴퓨터 렌덤 숫자보다 큽니다.")
# if user_number < com_number:
#     print("컴퓨터 렌덤 숫자보다 작습니다.")
# if user_number == com_number:
#     print("정답입니다.")

# import random

# com_number = random.randint(1, 100)

# while True:
#     user_number = int(input("1~100 사이의 숫자를 입력하세요: "))

#     if user_number > com_number:
#         print("컴퓨터 랜덤 숫자보다 큽니다. 더 작은 숫자를 입력하세요.")

#     elif user_number < com_number:
#         print("컴퓨터 랜덤 숫자보다 작습니다. 더 큰 숫자를 입력하세요.")

#     else:
#         print("정답입니다!")
#         break

    
    
import random

com_number = random.randint(1, 100)
count = 0

while True:
    user_number = int(input("1~100 사이의 숫자를 입력하세요: "))
    count += 1

    if user_number > com_number:
        print("컴퓨터 랜덤 숫자보다 큽니다. 더 작은 숫자를 입력하세요.")

    elif user_number < com_number:
        print("컴퓨터 랜덤 숫자보다 작습니다. 더 큰 숫자를 입력하세요.")

    else:
        print("정답입니다!")
        print(f"정답 입력 횟수: {count}회")
        break