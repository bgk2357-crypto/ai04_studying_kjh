# 사용자로부터 데이터를 입력받아서(5개) 리스트에 저장하고
# 저장된 리스트의 값 중에서 짝수만 출력해 보기
# number1 = int(input("첫번째 슷자를 입력하세요":))
# number2 = int(input("두번째 슷자를 입력하세요":))
# number3 = int(input("세번째 슷자를 입력하세요":))
# number4 = int(input("네번째 슷자를 입력하세요":))
# number5 = int(input("다섯번째 슷자를 입력하세요":))

scores = []
for i in range(5):
    score = int(input(f"{i+1} : 슷자를 입력하세요 : "))
    scores.append(score)


print('리스트변수의 값 : ', scores)

for i in scores:
    if i % 2 == 0:
        print(i)
        