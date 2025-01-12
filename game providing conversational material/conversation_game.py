import tkinter as tk
from tkinter import messagebox
import openai
import os

# API 키 설정
openai.api_key = os.getenv("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")  # 환경 변수에서 API 키 가져오기
# 직접 설정하려면 아래 줄을 사용하세요:
# openai.api_key = "your-valid-api-key"

class ConversationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("대화 주제 게임")

        self.players = []
        self.scores = {}
        self.current_speaker = None
        self.votes = {"찬성": 0, "반대": 0}
        self.topic = ""

        # 첫 화면
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        tk.Label(self.main_frame, text="참가자 수를 입력하세요 (2명 이상):", font=("Arial", 14)).pack(pady=10)
        self.player_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.player_entry.pack(pady=5)

        tk.Button(self.main_frame, text="시작", command=self.start_game).pack(pady=10)

        # 주제 화면
        self.topic_frame = tk.Frame(root)
        self.topic_label = tk.Label(self.topic_frame, text="", font=("Arial", 16))
        self.topic_label.pack(pady=20)

        self.turn_buttons_frame = tk.Frame(self.topic_frame)
        self.turn_buttons_frame.pack(pady=10)

        # 투표 화면
        self.vote_frame = tk.Frame(root)
        self.vote_label = tk.Label(self.vote_frame, text="", font=("Arial", 14))
        self.vote_label.pack(pady=20)

        self.vote_result_label = tk.Label(self.vote_frame, text="", font=("Arial", 12))
        self.vote_result_label.pack(pady=10)

        tk.Button(self.vote_frame, text="찬성", command=lambda: self.vote("찬성")).pack(side="left", padx=20)
        tk.Button(self.vote_frame, text="반대", command=lambda: self.vote("반대")).pack(side="right", padx=20)

    def start_game(self):
        """게임 시작: 참가자 수 입력"""
        try:
            num_players = int(self.player_entry.get())
            if num_players < 2:
                raise ValueError("참가자 수는 2명 이상이어야 합니다.")
            self.players = [f"Player {i+1}" for i in range(num_players)]
            self.scores = {player: 0 for player in self.players}
            self.main_frame.pack_forget()
            self.generate_topic()
        except ValueError as e:
            messagebox.showerror("오류", str(e))

    def generate_topic(self):
        """새로운 대화 주제 생성"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Generate a fun conversation topic for a group of friends."}],
                max_tokens=50,
                temperature=0.7,
            )
            self.topic = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            self.topic = "대화 주제를 가져오는 데 실패했습니다."
            print(f"Error: {e}")
        self.show_topic_screen()

    def show_topic_screen(self):
        """대화 주제 화면 표시"""
        self.topic_frame.pack()
        self.topic_label.config(text=f"대화 주제: {self.topic}")

        for widget in self.turn_buttons_frame.winfo_children():
            widget.destroy()

        for player in self.players:
            tk.Button(
                self.turn_buttons_frame,
                text=f"{player} My Turn",
                command=lambda p=player: self.start_turn(p),
            ).pack(side="left", padx=10)

    def start_turn(self, player):
        """발언자 설정"""
        self.current_speaker = player
        self.topic_frame.pack_forget()
        self.vote_frame.pack()
        self.vote_label.config(text=f"{player}의 발언 시간입니다!")
        self.votes = {"찬성": 0, "반대": 0}

    def vote(self, choice):
        """투표 처리"""
        self.votes[choice] += 1
        total_votes = sum(self.votes.values())
        if total_votes == len(self.players) - 1:
            self.calculate_votes()

    def calculate_votes(self):
        """투표 결과 계산"""
        agree_count = self.votes["찬성"]
        disagree_count = self.votes["반대"]

        if agree_count > disagree_count:
            self.scores[self.current_speaker] += 1
            result_text = f"{self.current_speaker}가 찬성을 얻어 1점을 획득했습니다!"
        else:
            result_text = f"{self.current_speaker}가 찬성을 얻지 못했습니다."

        self.vote_result_label.config(text=result_text)

        if self.scores[self.current_speaker] >= 10:
            messagebox.showinfo("게임 종료", f"{self.current_speaker}가 10점을 달성하여 승리했습니다!")
            self.root.quit()
        else:
            self.vote_frame.pack_forget()
            self.generate_topic()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConversationApp(root)
    root.mainloop()
