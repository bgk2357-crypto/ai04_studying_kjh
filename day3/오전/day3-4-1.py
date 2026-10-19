from dataclasses import dataclass


@dataclass
class PaymentReceipt:
    method: str
    buyer: str
    amount: int
    fee: int
    status: str

    @property
    def net_amount(self) -> int:
        return self.amount - self.fee


# 객체 생성 (클래스 바깥에서 실행)
obj = PaymentReceipt("card", "홍길동", 100, 5, "normal")

# 정산 금액 출력
print(obj.net_amount)