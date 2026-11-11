import json  # JSON 파일 읽기/쓰기를 위한 표준 라이브러리
import os    # 파일 존재 여부 확인을 위한 표준 라이브러리


# ============================================================
# Quiz 클래스: 퀴즈 한 문제를 표현하는 클래스
# ============================================================
class Quiz:
    def __init__(self, question, choices, answer):
        # __init__: 객체가 생성될 때 자동으로 실행되는 초기화 메서드
        # self: 이 객체 자신을 가리키는 참조
        self.question = question  # 문제 텍스트 (str)
        self.choices = choices    # 선택지 리스트 (list, 4개)
        self.answer = answer      # 정답 번호 (int, 1~4)

    def display(self):
        # 문제와 선택지를 화면에 출력하는 메서드
        print(f"\n  {self.question}")
        for i, choice in enumerate(self.choices, 1):
            # enumerate: 리스트를 순서 번호와 함께 반복
            # 1부터 시작(start=1)해서 1.선택지1, 2.선택지2... 형태로 출력
            print(f"    {i}. {choice}")

    def check_answer(self, user_answer):
        # 사용자가 입력한 번호가 정답과 같은지 확인하는 메서드
        # 같으면 True, 다르면 False 반환
        return self.answer == user_answer

    def to_dict(self):
        # Quiz 객체를 딕셔너리(dict)로 변환하는 메서드
        # JSON 파일에 저장하려면 딕셔너리 형태가 필요하기 때문
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        # 딕셔너리에서 Quiz 객체를 만드는 정적 메서드 (JSON 불러오기 전용)
        # @staticmethod: self 없이 클래스 이름으로 직접 호출 가능
        return Quiz(data["question"], data["choices"], data["answer"])


# ============================================================
# QuizGame 클래스: 게임 전체 흐름을 관리하는 클래스
# ============================================================
class QuizGame:
    # 클래스 변수: 모든 QuizGame 객체가 공유하는 데이터 파일 경로
    FILE_PATH = "state.json"

    def __init__(self):
        # 게임 시작 시 초기화
        self.quizzes = []    # 퀴즈 목록 (Quiz 객체들의 리스트)
        self.best_score = 0  # 최고 점수 (정수, 0으로 시작)


# ============================================================
# 프로그램 진입점
# ============================================================
if __name__ == "__main__":
    # 이 파일을 직접 실행했을 때만 아래 코드가 실행됨
    game = QuizGame()  # QuizGame 객체 생성
    print("QuizGame 시작 준비 완료!")  # 임시 출력 (나중에 game.run()으로 교체)
