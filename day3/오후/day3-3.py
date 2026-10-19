# def calc_order_legacy(u_type, price, qty, coupon):
#     # 문제점 1: u_type의 숫자가 어떤 회원 등급인지 알기 어려움 (매직 넘버)
#     # 문제점 2: price와 qty에 음수가 입력되어도 검증하지 않음

#     # 총 주문 금액 계산
#     total = price * qty

#     # 회원 등급별 할인 적용
#     if u_type == 1:
#         total = total * 0.95
#     elif u_type == 2:
#         total = total * 0.90
#     elif u_type == 3:
#         total = total * 0.80

#     # 쿠폰 할인 적용
#     if coupon == "YES":
#         total = total - 3000

#     # 최종 금액이 음수이면 0원으로 설정
#     if total < 0:
#         total = 0

#     # 최종 금액을 정수로 반환
#     return int(total)


# # 함수 실행 예제
# result = calc_order_legacy(
#     u_type=2,
#     price=10000,
#     qty=3,
#     coupon="YES"
# )

# print(f"최종 주문 금액: {result:,}원")

# def calc_order(u_type, price, qty, coupon):
#     # 1. 가격과 수량 검증
#     if price < 0:
#         print("[입력 오류] 상품 가격은 음수가 될 수 없습니다.")
#         return None

#     if qty < 0:
#         print("[입력 오류] 상품 수량은 음수가 될 수 없습니다.")
#         return None

#     # 2. 회원 등급별 할인율 설정
#     discount_rates = {
#         "A": 0.05,  # A등급: 5% 할인
#         "B": 0.10,  # B등급: 10% 할인
#         "C": 0.20,  # C등급: 20% 할인
#     }

#     # 회원 등급 검증
#     u_type = u_type.upper()

#     if u_type not in discount_rates:
#         print("[입력 오류] 회원 등급은 A, B, C 중 하나여야 합니다.")
#         return None

#     # 3. 총 주문 금액 계산
#     total = price * qty

#     # 4. 회원 등급 할인 적용
#     discount_rate = discount_rates[u_type]
#     total = total * (1 - discount_rate)

#     # 5. 쿠폰 적용 여부 확인
#     # 대문자, 소문자 모두 인식하고 앞뒤 공백도 제거
#     coupon = coupon.strip().upper()

#     if coupon == "YES":
#         # 회원 등급 할인 적용 후 금액이 15,000원 이상일 때 쿠폰 적용
#         if total >= 15000:
#             total -= 3000
#             print("[쿠폰 적용] 3,000원 할인이 적용되었습니다.")
#         else:
#             print("[쿠폰 미적용] 주문 금액이 15,000원 미만입니다.")

#     # 6. 최종 금액이 음수가 되지 않도록 처리
#     if total < 0:
#         total = 0

#     # 7. 최종 주문 금액 반환
#     return int(total)


# # ==================================
# # 테스트 1: 정상 주문 및 쿠폰 적용
# # ==================================
# print("\n[테스트 1: 정상 주문]")

# result = calc_order("B", 10000, 3, "YES")

# if result is not None:
#     print(f"최종 주문 금액: {result:,}원")


# # ==================================
# # 테스트 2: 소문자 쿠폰 적용
# # ==================================
# print("\n[테스트 2: 소문자 쿠폰]")

# result = calc_order("A", 10000, 2, "yes")

# if result is not None:
#     print(f"최종 주문 금액: {result:,}원")


# # ==================================
# # 테스트 3: 최소 금액 미달로 쿠폰 미적용
# # ==================================
# print("\n[테스트 3: 쿠폰 최소 금액 미달]")

# result = calc_order("A", 10000, 1, "YES")

# if result is not None:
#     print(f"최종 주문 금액: {result:,}원")


# # ==================================
# # 테스트 4: 음수 가격 입력
# # ==================================
# print("\n[테스트 4: 음수 가격]")

# result = calc_order("A", -10000, 2, "YES")

# if result is not None:
#     print(f"최종 주문 금액: {result:,}원")


# # ==================================
# # 테스트 5: 음수 수량 입력
# # ==================================
# print("\n[테스트 5: 음수 수량]")

# result = calc_order("B", 10000, -2, "NO")

# if result is not None:
#     print(f"최종 주문 금액: {result:,}원")

# def calc_order(u_type, price, qty, coupon):
#     # 1. 가격과 수량 검증
#     if price < 0:
#         print("[입력 오류] 상품 가격은 음수가 될 수 없습니다.")
#         return None

#     if qty < 0:
#         print("[입력 오류] 상품 수량은 음수가 될 수 없습니다.")
#         return None

#     # 2. 회원 등급별 할인율 설정
#     discount_rates = {
#         "A": 0.05,  # A등급: 5% 할인
#         "B": 0.10,  # B등급: 10% 할인
#         "C": 0.20,  # C등급: 20% 할인
#     }

#     # 3. 회원 등급 검증
#     u_type = u_type.strip().upper()

#     if u_type not in discount_rates:
#         print("[입력 오류] 회원 등급은 A, B, C 중 하나여야 합니다.")
#         return None

#     # 4. 총 주문 금액 계산
#     total = price * qty

#     # 5. 회원 등급별 할인 적용
#     discount_rate = discount_rates[u_type]
#     member_discount = int(total * discount_rate)
#     total -= member_discount

#     print(f"\n[주문 정보]")
#     print(f"회원 등급: {u_type}등급")
#     print(f"상품 가격: {price:,}원")
#     print(f"구매 수량: {qty}개")
#     print(f"상품 총액: {price * qty:,}원")
#     print(f"회원 할인: {member_discount:,}원")

#     # 6. 쿠폰 입력값 검증
#     coupon = coupon.strip().upper()

#     if coupon not in ("YES", "NO"):
#         print("[입력 오류] 쿠폰 사용 여부는 YES 또는 NO로 입력해주세요.")
#         return None

#     # 7. 쿠폰 적용
#     if coupon == "YES":
#         if total >= 15000:
#             total -= 3000
#             print("쿠폰 할인: 3,000원")
#         else:
#             print("쿠폰 미적용: 회원 할인 후 금액이 15,000원 미만입니다.")
#     else:
#         print("쿠폰 미사용")

#     # 8. 최종 결제 금액 계산
#     total = max(0, int(total))

#     print("-" * 35)
#     print(f"최종 결제 금액: {total:,}원")
#     print("-" * 35)

#     return total


# # =====================================
# # 사용자 입력
# # =====================================

# print("=" * 35)
# print("       온라인 주문 금액 계산기")
# print("=" * 35)

# try:
#     # 회원 등급 입력
#     u_type = input("회원 등급을 입력하세요 (A/B/C): ")

#     # 상품 가격 입력
#     price = int(input("상품 가격을 입력하세요 (원): "))

#     # 구매 수량 입력
#     qty = int(input("구매 수량을 입력하세요 (개): "))

#     # 쿠폰 사용 여부 입력
#     coupon = input("쿠폰을 사용하시겠습니까? (YES/NO): ")

#     # 주문 금액 계산
#     result = calc_order(u_type, price, qty, coupon)

# except ValueError:
#     print("[입력 오류] 가격과 수량은 정수로 입력해주세요.")


def calc_order(products, grade, coupon):
    # 1. 회원 등급별 할인율 설정
    discount_rates = {
        "A": 0.20,  # A등급: 20% 할인
        "B": 0.10,  # B등급: 10% 할인
        "C": 0.05,  # C등급: 5% 할인
    }

    # 2. 쿠폰 할인 설정
    COUPON_DISCOUNT = 3000
    MIN_COUPON_AMOUNT = 15000

    # 3. 전체 상품 금액 계산
    subtotal = sum(
        product["price"] * product["qty"]
        for product in products
    )

    # 4. 회원 등급별 할인 계산
    discount_rate = discount_rates[grade]
    member_discount = int(subtotal * discount_rate)

    # 회원 할인 적용
    total = subtotal - member_discount

    # 5. 쿠폰 할인 적용
    coupon_discount = 0

    if coupon == "YES":
        if total >= MIN_COUPON_AMOUNT:
            coupon_discount = COUPON_DISCOUNT
            total -= coupon_discount

            print("\n[쿠폰 적용] 3,000원 할인이 적용되었습니다.")

        else:
            print(
                "\n[쿠폰 미적용] 회원 할인 후 금액이 "
                "15,000원 미만입니다."
            )

    else:
        print("\n[쿠폰 미사용] 쿠폰 할인이 적용되지 않았습니다.")

    # 6. 주문 내역 출력
    print("\n" + "=" * 45)
    print("                 주문 내역")
    print("=" * 45)

    for index, product in enumerate(products, start=1):
        item_total = product["price"] * product["qty"]

        print(f"\n상품 {index}: {product['name']}")
        print(f"  상품 가격: {product['price']:,}원")
        print(f"  구매 수량: {product['qty']}개")
        print(f"  상품 금액: {item_total:,}원")

    # 7. 최종 결제 금액 출력
    print("\n" + "-" * 45)
    print(f"회원 등급        : {grade}등급")
    print(f"상품 총액        : {subtotal:>12,}원")
    print(
        f"회원 할인({discount_rate:.0%})   : "
        f"{member_discount:>12,}원"
    )
    print(f"쿠폰 할인        : {coupon_discount:>12,}원")
    print("-" * 45)
    print(f"최종 결제 금액   : {total:>12,}원")
    print("=" * 45)

    return total


# ==========================================
# 메인 프로그램
# ==========================================

print("=" * 45)
print("             회원 주문 계산기")
print("=" * 45)

print("\n[회원 등급별 할인율]")
print("A등급: 20% 할인")
print("B등급: 10% 할인")
print("C등급: 5% 할인")

# 1. 회원 등급 입력 및 검증
while True:
    grade = input(
        "\n회원 등급을 입력하세요 (A/B/C): "
    ).strip().upper()

    if grade in ("A", "B", "C"):
        break

    print("[입력 오류] 회원 등급은 A, B, C 중 하나여야 합니다.")


# 2. 상품 목록 생성
products = []

print("\n상품 입력을 시작합니다.")
print("상품 입력을 마치려면 상품명에 '종료'를 입력하세요.")


# 3. 상품을 원하는 만큼 입력
while True:
    print("\n" + "-" * 45)

    product_name = input(
        "상품명을 입력하세요 (종료하려면 '종료'): "
    ).strip()

    # 종료 명령어 확인
    if product_name == "종료":
        break

    # 상품명 검증
    if not product_name:
        print("[입력 오류] 상품명을 입력해주세요.")
        continue

    # 상품 가격 입력
    try:
        price = int(input("상품 가격을 입력하세요 (원): "))

        if price < 0:
            print("[입력 오류] 상품 가격은 음수가 될 수 없습니다.")
            continue

    except ValueError:
        print("[입력 오류] 상품 가격은 정수로 입력해주세요.")
        continue

    # 구매 수량 입력
    try:
        qty = int(input("구매 수량을 입력하세요 (개): "))

        if qty <= 0:
            print("[입력 오류] 구매 수량은 1개 이상이어야 합니다.")
            continue

    except ValueError:
        print("[입력 오류] 구매 수량은 정수로 입력해주세요.")
        continue

    # 상품 정보를 리스트에 저장
    products.append({
        "name": product_name,
        "price": price,
        "qty": qty
    })

    print(
        f"[상품 추가 완료] {product_name} / "
        f"{price:,}원 / {qty}개"
    )

    print(f"현재 등록된 상품 종류: {len(products)}개")


# 4. 상품 입력 종료 후 주문 처리
if not products:
    print("\n[주문 취소] 등록된 상품이 없습니다.")

else:
    # 쿠폰 사용 여부 입력
    while True:
        coupon = input(
            "\n쿠폰을 사용하시겠습니까? (YES/NO): "
        ).strip().upper()

        if coupon in ("YES", "NO"):
            break

        print("[입력 오류] YES 또는 NO로 입력해주세요.")

    # 5. 최종 주문 금액 계산
    calc_order(products, grade, coupon)

    print("\n주문 처리가 완료되었습니다.")