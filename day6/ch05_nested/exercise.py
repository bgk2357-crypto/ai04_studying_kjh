# """05장 학생 실습: 강좌와 수강생의 중첩 관계 모델링."""
# from pydantic import BaseModel


# # TODO 1: Learner(name:str, score:int 0~100)
# class learner(BaseModel):
#     pass

# # TODO 2: Course(title:str, learners:list[Learner] 최소 1명)
# class Course(BaseModel):
#     pass


# def main() -> None:
#     print('TODO: dict 데이터를 중첩 모델로 검증하세요.')


# if __name__ == '__main__':
#     main()

#####################################################################################


"""05장 학생 실습: 강좌와 수강생의 중첩 관계 모델링."""

from pydantic import BaseModel, Field, ValidationError


# TODO 1: Learner(name: str, score: int 0~100)
class Learner(BaseModel):
    name: str
    score: int = Field(ge=0, le=100)


# TODO 2: Course(title: str, learners: list[Learner] 최소 1명)
class Course(BaseModel):
    title: str
    learners: list[Learner] = Field(min_length=1)


def main() -> None:
    # dict 데이터를 중첩 모델로 검증
    data = {
        "title": "Python 기초",
        "learners": [
            {"name": "홍길동", "score": 95},
            {"name": "김철수", "score": 80},
            {"name": "이영희", "score": 70}
        ]
    }

    try:
        course = Course(**data)

        print("검증 성공!")
        print("강좌명:", course.title)
        print("수강생 목록:")

        for learner in course.learners:
            print(f"이름: {learner.name}, 점수: {learner.score}")

        print("\n딕셔너리 변환:")
        print(course.model_dump())

    except ValidationError as e:
        print("데이터 검증 오류!")
        print(e)

    # 잘못된 데이터 검증
    print("\n=== 잘못된 데이터 테스트 ===")

    try:
        invalid_course = Course(
            title="Python 기초",
            learners=[
                {"name": "박민수", "score": 120}
            ]
        )

    except ValidationError as e:
        print("검증 실패!")
        for error in e.errors():
            print("오류 위치:", error["loc"])
            print("오류 유형:", error["type"])


if __name__ == "__main__":
    main()