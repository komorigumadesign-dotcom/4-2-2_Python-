"""数字当てゲーム (tkinter版)

1. スタートボタンを押す
2. 1～100の数字をランダムに選び、伏字「＊＊＊」で表示
3. 入力欄に数字を入力して「決定」を押す
4. 「正解」「もっと大きい」「もっと小さい」を表示
5. 正解時のみ試行回数を表示し、伏字を開示する
"""
import random
import tkinter as tk

MIN_NUM, MAX_NUM = 1, 100
MASK = "＊＊＊"


def clear_level(attempts: int) -> str:
    """試行回数からクリアレベル(星)を返す"""
    if attempts <= 2:
        stars = 5
    elif attempts <= 4:
        stars = 4
    elif attempts <= 7:
        stars = 3
    elif attempts <= 9:
        stars = 2
    else:
        stars = 1
    return "★" * stars


class NumberGuessGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("数字当てゲーム")
        self.root.resizable(False, False)

        self.answer = None
        self.attempts = 0

        font_big = ("Meiryo", 28, "bold")
        font_norm = ("Meiryo", 12)

        tk.Label(root, text=f"{MIN_NUM}～{MAX_NUM}の数字を当てよう！", font=font_norm).pack(padx=20, pady=(16, 4))

        self.secret_label = tk.Label(root, text="", font=font_big, width=8)
        self.secret_label.pack(pady=4)

        self.start_button = tk.Button(root, text="スタート", font=font_norm, width=12, command=self.start)
        self.start_button.pack(pady=6)

        frame = tk.Frame(root)
        frame.pack(pady=6)
        self.entry = tk.Entry(frame, font=font_norm, width=10, justify="center", state="disabled")
        self.entry.pack(side="left", padx=(0, 8))
        self.entry.bind("<Return>", lambda _e: self.submit())
        self.submit_button = tk.Button(frame, text="決定", font=font_norm, width=8, state="disabled", command=self.submit)
        self.submit_button.pack(side="left")

        self.result_label = tk.Label(root, text="スタートを押してください", font=font_norm, height=2)
        self.result_label.pack(padx=20, pady=4)

        self.attempts_label = tk.Label(root, text="", font=font_norm)
        self.attempts_label.pack(pady=(0, 16))

    def _set_input_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.entry.config(state=state)
        self.submit_button.config(state=state)

    def start(self) -> None:
        self.answer = random.randint(MIN_NUM, MAX_NUM)
        self.attempts = 0
        self.secret_label.config(text=MASK)
        self.result_label.config(text="数字を入力してください")
        self.attempts_label.config(text="")
        self._set_input_enabled(True)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def submit(self) -> None:
        if self.answer is None:
            return
        text = self.entry.get().strip()
        try:
            guess = int(text)
        except ValueError:
            self.result_label.config(text="整数を入力してください")
            return
        if not MIN_NUM <= guess <= MAX_NUM:
            self.result_label.config(text=f"{MIN_NUM}～{MAX_NUM}の数字を入力してください")
            return

        self.attempts += 1
        self.entry.delete(0, tk.END)

        if guess == self.answer:
            self.result_label.config(text="正解！")
            self.attempts_label.config(
                text=f"試行回数: {self.attempts}回\nクリアレベル: {clear_level(self.attempts)}"
            )
            self.secret_label.config(text=str(self.answer))
            self._set_input_enabled(False)
            self.answer = None
        elif guess < self.answer:
            self.result_label.config(text="もっと大きい")
        else:
            self.result_label.config(text="もっと小さい")


if __name__ == "__main__":
    window = tk.Tk()
    NumberGuessGame(window)
    window.mainloop()
