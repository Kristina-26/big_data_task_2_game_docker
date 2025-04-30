import tkinter as tk  # for GUI
from tkinter import messagebox
import random
import sys


class SimonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simon Game")
        self.root.geometry("400x500")
        self.root.configure(bg="#011F3F")

        # game variables
        self.button_colors = ["red", "blue", "green", "yellow"]
        self.game_pattern = []
        self.user_pattern = []
        self.started = False
        self.level = 0

        # tracking of active animation
        self.animation_ids = {}  # keep track of pending animations for each button

        # title label
        self.title_label = tk.Label(self.root, text="Press any key to start", font=("Press Start 2P", 24), bg="#011F3F",
                                    fg="#FEF2BF")
        self.title_label.pack(pady=20)

        # button container
        self.button_frame = tk.Frame(root, bg="#011F3F")
        self.button_frame.pack(expand=True)

        # grid for equal sized cells
        for i in range(2):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="simon")
            self.button_frame.grid_rowconfigure(i, weight=1, uniform="simon")

        # buttons
        self.buttons = {}
        positions = {
            "green": (0, 0),
            "red": (0, 1),
            "yellow": (1, 0),
            "blue": (1, 1),
        }

        button_size = 150  # in pixels

        for color, (row, col) in positions.items():
            button = tk.Button(
                self.button_frame,
                width=button_size // 10,
                height=button_size // 20,
                bg=color,
                activebackground=color,
                relief=tk.RAISED,
                bd=10
            )
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            button.configure(command=lambda c=color: self.button_clicked(c))
            self.buttons[color] = button
            # initializing animation tracker for this button
            self.animation_ids[color] = None

        # key press event
        self.root.bind("<Key>", self.start_game)

    def start_game(self, event=None):
        if not self.started:
            self.started = True
            self.level = 0
            self.game_pattern = []
            self.next_sequence()

    def next_sequence(self):
        self.user_pattern = []
        self.level += 1
        self.title_label.configure(text=f"Level {self.level}")

        # picking a random color
        random_color = random.choice(self.button_colors)
        self.game_pattern.append(random_color)

        # allowing UI updates between flashes
        self.root.after(500, lambda: self.play_sequence(0))

    def play_sequence(self, index):
        if index < len(self.game_pattern):
            color = self.game_pattern[index]
            self.flash_button(color)
            self.root.after(800, lambda: self.play_sequence(index + 1))

    def flash_button(self, color):
        button = self.buttons[color]
        original_bg = button.cget("bg")

        # cancelling any pending animation for this button
        if self.animation_ids[color] is not None:
            self.root.after_cancel(self.animation_ids[color])
            self.animation_ids[color] = None

        # flash effect
        button.configure(bg="grey")

        # simple sound indicator
        self.root.bell()

        # scheduling color restoration and saving the animation id
        self.animation_ids[color] = self.root.after(400, lambda: self.restore_button_color(color, original_bg))

    def restore_button_color(self, color, original_bg):
        # restoring the button color and clearing animation id
        self.buttons[color].configure(bg=original_bg)
        self.animation_ids[color] = None

    def button_clicked(self, color):
        if not self.started:
            return

        self.user_pattern.append(color)
        self.flash_button(color)

        # checking answer - fixed the index to match the current input
        self.check_answer(len(self.user_pattern) - 1)

    def check_answer(self, current_level):
        # comparing user pattern with game pattern at the same index
        if self.user_pattern[current_level] == self.game_pattern[current_level]:
            # correct
            if len(self.user_pattern) == len(self.game_pattern):
                # complete sequence
                self.root.after(1000, self.next_sequence)
        else:
            # wrong answer
            self.root.bell()  # beep for wrong answer
            self.title_label.configure(text="Game over! \n Press any key to restart")
            self.root.configure(bg="red")
            self.started = False

            # cancelling all pending animations
            for color in self.animation_ids:
                if self.animation_ids[color] is not None:
                    self.root.after_cancel(self.animation_ids[color])
                    self.animation_ids[color] = None
                # resetting all button colors
                self.buttons[color].configure(bg=color)

            # resetting background after 200 ms
            self.root.after(200, lambda: self.root.configure(bg="#011F3F"))

            # show score
            messagebox.showinfo("Game over", f"Your score: {self.level - 1}")
            print(f"Game over! Your score: {self.level - 1}")


def main():
    root = tk.Tk()

    # exit handler
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            root.destroy()
            sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        game = SimonGame(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()