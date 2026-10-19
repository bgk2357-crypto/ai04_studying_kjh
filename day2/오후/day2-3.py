# 리스트 컴프리핸션
# result = []
# list_1 = [1, 2, 3, 4, 5]
# # for i in list_1:
# #     if i % 2 == 0:
# #         result.append(i)
# result = [i for i in list_1 if i % 2 == 0]

# print(result)

# result = []
# list_1 = ['1', '2', '3', '4', '5']
# result = [int(i) for i in list_1]
# print(result)

# menu = ['아메리카노', '카페라떼', '카푸치노']
# ice_menu = ['아이스' + i for i in menu]
# print(ice_menu)

# ['참' if 조건 else '거짓' for i in 집합]

ages = [20, 15, 60, 25, 30,45,5]
print([ i for i in ages if i>= 20])
print([ '성인' if i >= 20 else '미성년자' for i in ages])