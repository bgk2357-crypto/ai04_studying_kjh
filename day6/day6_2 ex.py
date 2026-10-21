from pydantic import BaseModel, ValidationError


# Book 모델 정의
class Book(BaseModel):
    title: str
    price: int
    in_stock: bool = True
    note: str | None = None


def main() -> None:
    # 1. Book 객체 생성
    book = Book(title='파이썬 기초', price='19000')

    print('도서 정보:', book)

    # 2. model_dump()로 딕셔너리 변환
    print('딕셔너리 변환:', book.model_dump())

    # 3. price의 타입 확인
    print('가격:', book.price)
    print('가격 타입:', type(book.price))

    # 4. title을 누락했을 때 ValidationError 확인
    try:
        book2 = Book(price=15000)
        print(book2)

    except ValidationError as e:
        print('데이터 검증 오류 발생!')
        print('error', e.errors()[0])
        print('데이터 검증 오류 발생!')
        print(e)
        print('데이터 검증 오류 발생!')


if __name__ == '__main__':
    main()

# from pydantic import BaseModel


# # TODO: Book 모델의 필드를 정의하세요.
# # title:str (필수), price:int (필수), in_stock:bool=True, note:str|None=None
# class Book(BaseModel):
#     pass


# def main() -> None:
#     # TODO: Book(title='파이썬 기초', price='19000') 만들기
#     # TODO: model_dump() 호출, 가격이 int로 변환되었는지 확인
#     # TODO: title 누락 시 ValidationError 확인
#     print('TODO를 완성하세요.')


# if __name__ == '__main__':
#     main()