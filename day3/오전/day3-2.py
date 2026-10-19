class DigitalWallet:
    def __init__(self, owner: str, initial_balance: int = 0):
        self.owner = owner
        self.__balance = 0
        self.balance = initial_balance  # setter를 거쳐 안전하게 초기화

    @property
    def balance(self) -> int:
        return self.__balance

    @balance.setter
    def balance(self, amount: int) -> None:
        if amount < 0:
            print(
                f"[보안 경고] 잔액은 음수가 될 수 없습니다! "
                f"(입력값: {amount}원 -> 거부됨)"
            )
            return

        self.__balance = amount

    def deposit(self, amount: int) -> str:
        if amount <= 0:
            return "[오류] 입금액은 0원보다 커야 합니다."

        self.balance += amount

        return (
            f"[{self.owner}] {amount:,}원 입금 완료 "
            f"(현재 잔액: {self.balance:,}원)"
        )


# 디지털 지갑 생성
wallet = DigitalWallet("이코딩", 10000)
wallet2 = DigitalWallet("kjh", 50000)

# 5,000원 입금
print(wallet.deposit(5000))
print(wallet2.deposit(10000))

# 외부에서 음수 잔액 설정 시도
wallet.balance = 50 # setter가 음수 입력을 차단

# 최종 잔액 확인
print(f"\n최종 안전 잔액: {wallet.balance:,}원")
print(f"\n최종 안전 잔액: {wallet2.balance:,}원")

print(wallet.deposit(2000))


# class ModelConfig:
#     def __init__(self, model_name: str, learning_rate: float, epochs: int):
#         self.model_name = model_name
#         self.__learning_rate = 0.001
#         self.learning_rate = learning_rate
#         self.epochs = epochs

#     @property
#     def learning_rate(self) -> float:
#         return self.__learning_rate

#     @learning_rate.setter
#     def learning_rate(self, value: float) -> None:
#         if not (0.0 < value <= 1.0):
#             print(
#                 f"[검증 경고] 비정상 학습률({value}) 감지! "
#                 f"기존 안전값({self.__learning_rate})을 유지합니다."
#             )
#             return

#         self.__learning_rate = value

#     def __str__(self) -> str:
#         return (
#             f"ModelConfig(name='{self.model_name}', "
#             f"lr={self.learning_rate}, epochs={self.epochs})"
#         )


# # 모델 설정 객체 생성
# cfg = ModelConfig("ResNet-50", 0.01, 30)

# # 현재 모델 설정 출력
# print(cfg)

# # 허용 범위를 초과하는 학습률 설정 시도
# cfg.learning_rate = 5.0

# # 변경 후 모델 설정 출력
# print(cfg)