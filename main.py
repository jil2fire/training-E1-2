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
        self.load_data()     # 저장된 파일이 있으면 데이터 불러오기

    def load_data(self):
        # state.json 파일에서 퀴즈 목록과 최고 점수를 불러오는 메서드
        if not os.path.exists(self.FILE_PATH):
            # os.path.exists(): 파일이 존재하는지 확인 (없으면 False)
            # 파일이 없으면 기본 퀴즈 데이터 사용 (첫 실행 상황)
            self.quizzes = self.get_default_quizzes()
            return

        try:
            # with open(): 파일을 안전하게 열고, 블록이 끝나면 자동으로 닫음
            # encoding="utf-8": 한글 깨짐 방지
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)  # JSON 텍스트 → 파이썬 딕셔너리로 변환

            # 불러온 딕셔너리의 "quizzes" 항목을 Quiz 객체 리스트로 변환
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            # .get("key", 기본값): 해당 키가 없을 때 기본값 사용 (오류 방지)
            self.best_score = data.get("best_score", 0)

            print(f"  📂 저장된 데이터를 불러왔습니다. "
                  f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        except (json.JSONDecodeError, KeyError):
            # json.JSONDecodeError: 파일 내용이 올바른 JSON 형식이 아닐 때
            # KeyError: 필요한 키가 딕셔너리에 없을 때
            # → 파일이 손상된 경우 기본 데이터로 복구
            print("  ⚠️  데이터 파일이 손상되었습니다. 기본 퀴즈로 초기화합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    def save_data(self):
        # 현재 퀴즈 목록과 최고 점수를 state.json에 저장하는 메서드
        try:
            data = {
                # Quiz 객체 → 딕셔너리로 변환한 리스트
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score
            }
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                # json.dump(): 파이썬 딕셔너리 → JSON 텍스트로 파일에 저장
                # ensure_ascii=False: 한글을 유니코드 코드가 아닌 한글 그대로 저장
                # indent=4: 보기 좋게 4칸 들여쓰기
                json.dump(data, f, ensure_ascii=False, indent=4)

        except IOError as e:
            # IOError: 파일 쓰기 권한이 없거나 디스크가 꽉 찼을 때
            print(f"  ⚠️  저장 중 오류가 발생했습니다: {e}")

    def get_default_quizzes(self):
        # 파일이 없거나 손상됐을 때 사용할 기본 퀴즈 목록을 반환하는 메서드
        return [
            Quiz(
                "코디세이 올인원 입학 연수 과정에서 부여받은 미션 갯수 (개인 미션, 팀 미션 포함)",
                ["1개", "2개", "3개", "4개"],
                4
            ),
            Quiz(
                "코디세이 올인원 입학 연수 중, 개인 미션 한 개를 통과하려면 몇 번의 평가를 PASS 받아야 하는가?",
                ["1번", "2번", "3번", "4번"],
                3
            ),
            Quiz(
                "코디세이 올인원 입학 연수 과정에서 매 주 치르는 시험은 무슨 요일?",
                ["월요일", "수요일", "금요일", "일요일"],
                3
            ),
            Quiz(
                "코디세이 올인원 교육장 출석 인정 시간은 하루 최대 몇 시간인가?",
                ["6시간", "12시간", "18시간", "24시간"],
                2
            ),
            Quiz(
                "코디세이 학습 도우미의 이름은 무엇인가?",
                ["네이토", "네이버", "네이트", "네이스"],
                1
            ),
            Quiz(
                "코디세이 올인원 교육장의 건물 이름은 무엇인가? (경남대학교는 생략)",
                ["제5공학관", "한마미래관", "중앙도서관", "혁신융합관"],
                1
            ),
        ]


    def play_quiz(self):
        # 퀴즈를 순서대로 출제하고 결과를 보여주는 메서드
        if not self.quizzes:
            # 퀴즈 목록이 비어있을 때 (빈 리스트는 False로 평가됨)
            print("\n  📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return  # 메서드 조기 종료

        total = len(self.quizzes)  # 전체 문제 수
        correct = 0                # 맞춘 문제 수 (0으로 초기화)

        print(f"\n  📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(self.quizzes, 1):
            # enumerate: (인덱스, 값) 쌍으로 반복, 1부터 번호 시작
            print(f"\n  ----------------------------------------")
            print(f"  [문제 {i}/{total}]")
            quiz.display()  # 문제와 선택지 출력

            user_answer = self.get_int_input("\n  정답 입력 (1-4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("  ✅ 정답입니다!")
                correct += 1  # 정답이면 카운터 증가
            else:
                print(f"  ❌ 오답입니다. 정답은 {quiz.answer}번이었습니다.")

        # 점수 계산: 정답 수 / 전체 문제 수 × 100 (백분율)
        score = int((correct / total) * 100)

        print(f"\n  ========================================")
        print(f"  🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        # 최고 점수보다 높으면 갱신 후 즉시 저장
        if score > self.best_score:
            self.best_score = score
            print("  🎉 새로운 최고 점수입니다!")
            self.save_data()  # 최고 점수 갱신 시 파일에 저장
        print("  ========================================")

    def add_quiz(self):
        # 새로운 퀴즈를 입력받아 목록에 추가하는 메서드
        print("\n  📌 새로운 퀴즈를 추가합니다.")

        # 문제 입력 (빈 값이면 재입력 요청)
        while True:
            question = input("\n  문제를 입력하세요: ").strip()
            if question:
                break  # 내용이 있으면 반복 종료
            print("  ⚠️  문제를 입력해주세요.")

        # 선택지 4개 입력
        choices = []  # 선택지를 담을 빈 리스트
        for i in range(1, 5):  # 1, 2, 3, 4 반복
            while True:
                choice = input(f"  선택지 {i}: ").strip()
                if choice:
                    choices.append(choice)  # 리스트에 선택지 추가
                    break
                print("  ⚠️  선택지를 입력해주세요.")

        # 정답 번호 입력 (공통 입력 처리 메서드 사용)
        answer = self.get_int_input("  정답 번호 (1-4): ", 1, 4)

        # Quiz 객체 생성 후 퀴즈 목록에 추가
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_data()  # 추가 직후 파일에 저장

        print("\n  ✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        # 현재 등록된 퀴즈 목록을 출력하는 메서드
        if not self.quizzes:
            # 빈 리스트는 False로 평가됨 → 퀴즈가 없는 경우 처리
            print("\n  📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n  📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("  ----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            # 문제 번호와 문제 텍스트만 간략하게 표시
            print(f"  [{i}] {quiz.question}")
        print("  ----------------------------------------")

    def show_score(self):
        # 최고 점수를 출력하는 메서드
        print("\n  ========================================")
        if self.best_score == 0:
            # 한 번도 퀴즈를 풀지 않았을 때
            print("  📊 아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"  🏆 최고 점수: {self.best_score}점")
        print("  ========================================")

    def show_menu(self):
        # 메인 메뉴 화면을 출력하는 메서드
        print("\n  ========================================")
        print("         🎯 코디세이 올인원 퀴즈 🎯")
        print("  ========================================")
        print("    1. 퀴즈 풀기")
        print("    2. 퀴즈 추가")
        print("    3. 퀴즈 목록")
        print("    4. 점수 확인")
        print("    5. 종료")
        print("  ========================================")

    def get_int_input(self, prompt, min_val, max_val):
        # 정수 입력을 안전하게 받는 공통 메서드
        # 잘못된 입력(문자, 빈값, 범위 초과)이면 메시지 출력 후 재입력 요청
        while True:  # 올바른 입력이 들어올 때까지 반복
            try:
                user_input = input(prompt).strip()  # .strip(): 앞뒤 공백 제거

                if not user_input:
                    # 빈 입력 (그냥 Enter만 눌렀을 때)
                    print(f"  ⚠️  값을 입력해주세요.")
                    continue  # while 루프 처음으로 돌아가 재입력

                num = int(user_input)  # 문자열 → 정수 변환 시도

                if min_val <= num <= max_val:
                    return num  # 유효한 범위면 값 반환 후 메서드 종료
                else:
                    print(f"  ⚠️  {min_val}~{max_val} 사이의 숫자를 입력하세요.")

            except ValueError:
                # int() 변환 실패 시 발생 (예: "abc", "1.5" 등)
                print(f"  ⚠️  숫자를 입력해주세요.")

    def run(self):
        # 게임의 메인 루프: 종료를 선택할 때까지 메뉴를 반복 출력
        try:
            while True:  # 무한 반복 (break로 빠져나감)
                self.show_menu()
                choice = self.get_int_input("  선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("\n  👋 프로그램을 종료합니다. 수고하셨습니다!")
                    self.save_data()  # 종료 전 데이터 저장
                    break  # while 루프 종료

        except KeyboardInterrupt:
            # Ctrl+C를 눌렀을 때 발생하는 예외
            # 프로그램이 갑자기 꺼지지 않도록 안전하게 처리
            print("\n\n  ⚠️  프로그램이 중단되었습니다. 데이터를 저장합니다...")
            self.save_data()

        except EOFError:
            # 입력 스트림이 끊겼을 때 발생하는 예외 (파이프 입력 종료 등)
            print("\n\n  ⚠️  입력이 종료되었습니다. 데이터를 저장합니다...")
            self.save_data()


# ============================================================
# 프로그램 진입점
# ============================================================
if __name__ == "__main__":
    # 이 파일을 직접 실행했을 때만 아래 코드가 실행됨
    game = QuizGame()  # QuizGame 객체 생성
    game.run()         # 게임 시작
