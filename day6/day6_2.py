# 필수 / 기본값, 모델 생성 / 검증
from pydantic import BaseModel, ValidationError

class Member(BaseModel):
    username : str
    age : int
    active : bool = True
    nickname : str | None = None

if __name__ == '__main__':
    m = Member(
        username='홍길동',
        age=20,
        active=True,
        nickname=None
    )

    print('회원 정보:', m)
    print('사용자 이름:', m.username)
    print('나이:', m.age)
    print('활성 상태:', m.active)
    print('닉네임:', m.nickname)
    print('딕셔너리 변환:', m.model_dump())