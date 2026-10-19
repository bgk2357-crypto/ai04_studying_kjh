# from abc import ABC, abstractmethod
# from dataclasses import dataclass


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


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, buyer: str, amount: int) -> PaymentReceipt:
        """
        모든 결제 수단 클래스가 반드시 구현해야 하는 추상 메서드
        """
        pass


class CreditCardGateway(PaymentGateway):
    def process_payment(self, buyer: str, amount: int) -> PaymentReceipt:
        fee = int(amount * 0.025)
        return PaymentReceipt("신용카드", buyer, amount, fee, "APPROVED")


class KakaoPayGateway(PaymentGateway):
    def process_payment(self, buyer: str, amount: int) -> PaymentReceipt:
        fee = int(amount * 0.01)
        return PaymentReceipt("카카오페이", buyer, amount, fee, "APPROVED")


# 여러 결제 수단을 하나의 리스트로 관리
gateways: list[PaymentGateway] = [
    CreditCardGateway(),
    KakaoPayGateway(),
]

# 모든 결제 수단으로 결제 처리
for gw in gateways:
    receipt = gw.process_payment("박파이썬", 50000)
#     print(f"{receipt} | 정산 금액: {receipt.net_amount:,}원")

# from abc import ABC, abstractmethod

# class PaymentGateway(ABC):
#     @abstractmethod
#     def process_payment(self, item: str, amount: int) -> str:
#         pass
# class CreditCardGateway(PaymentGateway):
#     def process_payment(self, item: str, amount: int) -> str:
#             return f"구매품목2 : {item} 수량2 : {amount}"
# class bankGateway(PaymentGateway):
#     pass

# obj =CreditCardGateway()
# print(obj.process_payment("책", 3))