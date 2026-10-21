# 필수 / 기본값, 모델 생성 / 검증
import day6_2

member = day6_2.Member(username='홍길동',age=20,active=True,nickname=None)
if member.age > 19:
    print('성인입니다')

print('main.py',__name__)