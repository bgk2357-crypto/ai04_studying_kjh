# from pydantic import BaseModel, ValidationError
# import typing 
# class student(BaseModel):
#     name: str
#     age: int
#     interest: list[str]
#     # 선택적으로 입력받는 nickname 필드 추가 (기본값은 None)
#     nickname : typing.Optional[str] = None
#     # 한번 student_id 필드 추가(정수 또는 문자열 모두 허용)
#     student_id : typing.Uion[int, str]
# def main() -> None:
#     # 아래 데이터를 문자열 age = '123' 으로 바꿔 실행한 뒤 결과 타입 확인
#     student = student(name ='하늘', age=23, interests=['AI', 'python'],nickname='a',student_id='23')
#     print('학생', student)
#     print('age타입'), type(student.age)
#     print('dictionary 변환', student.model_dump())
# # age에 스물셋을 전달하고 validationError를 처리하는 코드 작성
# if __name__== '__main__':
#     main()'

from pydantic import BaseModel, ValidationError
from typing import Optional, Union


class Student(BaseModel):
    name: str
    age: int
    interests: list[str]

    # 선택적 필드: 생략하면 None
    nickname: Optional[str] = None

    # 정수 또는 문자열 허용
    student_id: Union[int, str]


def main() -> None:
    # 정상적인 데이터 입력
    student = Student(
        name='하늘',
        age='23',
        interests=['AI', 'python'],
        student_id=23
    )

    print('학생:', student)
    print('age 타입:', type(student.age))
    print('dictionary 변환:', student.model_dump())

    # 잘못된 데이터 입력: age에 숫자가 아닌 문자열 전달
    try:
        student2 = Student(
            name='하늘',
            age='스물셋',
            interests=['AI', 'python'],
            student_id='S001'
        )
        print(student2)

    except ValidationError as e:
        print('데이터 검증 오류 발생!')
        print(e)


if __name__ == '__main__':
    main()


# from pydantic import BaseModel, ValidationError
# from typing import Optional, Union


# class student(BaseModel):
#     name: str
#     age: int
#     interest: list[str]

#     # 선택적으로 입력받는 nickname 필드 추가 (기본값은 None)
#     nickname: Optional[str]

#     # 한번 student_id 필드 추가(정수 또는 문자열 모두 허용)
#     student_id: Uion[int, str]


# def main() -> None:
#     # 아래 데이터를 문자열 age = '123' 으로 바꿔 실행한 뒤 결과 타입 확인
#     student = student(name='하늘', age=23, interests=['AI', 'python'])

#     print('학생', student)
#     print('age타입'), type(student.age))
#     print('dictionary 변환', student.model_dump())


# # age에 스물셋을 전달하고 validationError를 처리하는 코드 작성
# if __name__ == '__main__':
#     main()

