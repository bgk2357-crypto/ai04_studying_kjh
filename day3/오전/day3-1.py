# class KDTStudent:
#     def __init__(self, name: str, track: str):
#         self.name = name
#         self.track = track
#         self.level = 1
#         self.energy = 100
#         self.completed_missions = []

#     def study_coding(self, topic: str, cost_energy: int = 25) -> str:
#         if self.energy < cost_energy:
#             return (
#                 f"[휴식 필요] {self.name}님의 에너지가 부족합니다! "
#                 f"(현재: {self.energy})"
#             )

#         self.energy -= cost_energy
#         self.level += 1
#         self.completed_missions.append(topic)

#         return (
#             f"[레벨업!] {self.name}님이 '{topic}' 실습을 완료했습니다! "
#             f"(Lv.{self.level}, 남은 에너지: {self.energy})"
#         )

#     def drink_coffee(self, boost: int = 40) -> str:
#         self.energy = min(100, self.energy + boost)

#         return (
#             f"[충전 완료] 아이스 아메리카노 수혈! "
#             f"현재 에너지: {self.energy}"
#         )


# # 학생 객체 생성
# student1 = KDTStudent("김루키", "AI 엔지니어링")

# # 코딩 공부하기
# print(student1.study_coding("Python 클래스 기초"))
# print(student1.study_coding("예외처리 마스터"))

# # 커피 마시기
# print(student1.drink_coffee())

# # 최종 학생 정보 확인
# print("\n===== 최종 학생 정보 =====")
# print(f"이름: {student1.name}")
# print(f"트랙: {student1.track}")
# print(f"레벨: {student1.level}")
# print(f"에너지: {student1.energy}")
# print(f"완료한 미션: {student1.completed_missions}")

class BaristaBot:
    def __init__(self, bot_name: str, bean_grams: int):
        self.bot_name = bot_name
        self.bean_grams = bean_grams
        self.total_cups = 0

    def brew_espresso(self, cups: int = 1) -> str:
        required_beans = cups * 18

        if self.bean_grams < required_beans:
            return (
                f"[{self.bot_name}] 원두 부족! "
                f"(필요: {required_beans}g, 현재: {self.bean_grams}g)"
            )

        self.bean_grams -= required_beans
        self.total_cups += cups

        return (
            f"[{self.bot_name}] 에스프레소 {cups}잔 추출 완료! "
            f"(남은 원두: {self.bean_grams}g, "
            f"누적: {self.total_cups}잔)"
        )


# 바리스타 봇 생성
bot = BaristaBot("코덱스바리스타-1호", 50)
bot2 = BaristaBot("KJH-1호", 99)

# 에스프레소 추출
print(bot.brew_espresso(2))
print(bot.brew_espresso(1))
print(bot2.brew_espresso(2))
print(bot2.brew_espresso(3))
print(bot2.brew_espresso(1))

# 추후 실습 원두가 19g 3잔이 주문 들어오면 1잔 추출하고 2잔은 원두 부족으로 실패하는 상황을 시뮬레이션