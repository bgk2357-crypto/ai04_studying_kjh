from pydantic import BaseModel, Field


class Product(BaseModel):
    # TODO title: 최소 2자, 최대 60자
    # TODO price: 0보다 커야 함
    # TODO stock: 0 이상, 기본값 0
    # TODO sku: SKU-와 숫자 네 자리 패턴
    pass


def main() -> None:
    print('TODO: 정상 상품 및 잘못된 상품을 테스트하세요.')


if __name__ == '__main__':
    main()

##############################################################

from pydantic import BaseModel, Field, ValidationError


class Product(BaseModel):
    # title: 최소 2자, 최대 60자
    title: str = Field(min_length=2, max_length=60)

    # price: 0보다 커야 함
    price: float = Field(gt=0)

    # stock: 0 이상, 기본값 0
    stock: int = Field(default=0, ge=0)

    # sku: SKU-와 숫자 네 자리 패턴
    sku: str = Field(pattern=r'^SKU-[0-9]{4}$')


def main() -> None:
    # 정상 상품 테스트
    print('=== 정상 상품 테스트 ===')

    product1 = Product(
        title='노트북',
        price=1200.50,
        sku='SKU-0001'
    )

    print('상품 정보:', product1)
    print('딕셔너리 변환:', product1.model_dump())
    print('재고:', product1.stock)

    # 잘못된 상품 테스트
    print('\n=== 잘못된 상품 테스트 ===')

    try:
        product2 = Product(
            title='A',
            price=0,
            stock=-5,
            sku='SKU-001'
        )

        print(product2)

    except ValidationError as e:
        for error in e.errors():
            print('오류 필드:', error['loc'])
            print('오류 유형:', error['type'])
            print('오류 메시지:', error['msg'])
            print()


if __name__ == '__main__':
    main()