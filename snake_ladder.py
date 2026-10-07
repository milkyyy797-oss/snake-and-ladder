import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# GAME SETTINGS
# -----------------------------

BOARD_SIZE = 600
CELL_SIZE = 60

# Snakes: head -> tail
SNAKES = {
    97: 78,
    95: 56,
    88: 48,
    62: 18,
    64: 36,
    49: 11,
    47: 26,
    16: 6,
}

# Ladders: bottom -> top
LADDERS = {
    4: 25,
    9: 31,
    20: 38,
    28: 84,
    40: 59,
    51: 67,
    63: 81,
    71: 91,
}

COLORS = ["#e63946", "#457b9d"]


# -----------------------------
# MAIN GAME CLASS
# -----------------------------

class SnakeLadderGame:

    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake & Ladder 🎲")
        self.root.resizable(False, False)
        self.root.configure(bg="#1d3557")

        self.players = [0, 0]
        self.current_player = 0

        self.create_title()
        self.create_board()
        self.create_controls()

        self.draw_board()

    # -------------------------
    # TITLE
    # -------------------------

    def create_title(self):
        title = tk.Label(
            self.root,
            text="🐍 SNAKE & LADDER 🎲",
            font=("Arial", 24, "bold"),
            bg="#1d3557",
            fg="#f1faee"
        )
        title.pack(pady=10)

    # -------------------------
    # BOARD
    # -------------------------

    def create_board(self):
        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_SIZE,
            height=BOARD_SIZE,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(padx=15)

    # -------------------------
    # CONTROLS
    # -------------------------

    def create_controls(self):

        control_frame = tk.Frame(
            self.root,
            bg="#1d3557"
        )
        control_frame.pack(pady=12)

        self.turn_label = tk.Label(
            control_frame,
            text="Player 1's Turn",
            font=("Arial", 16, "bold"),
            bg="#1d3557",
            fg="#f1faee"
        )
        self.turn_label.grid(row=0, column=0, padx=10)

        self.dice_label = tk.Label(
            control_frame,
            text="🎲",
            font=("Arial", 35),
            bg="#1d3557",
            fg="white"
        )
        self.dice_label.grid(row=0, column=1, padx=15)

        self.roll_button = tk.Button(
            control_frame,
            text="ROLL DICE",
            font=("Arial", 14, "bold"),
            bg="#f4a261",
            fg="black",
            padx=15,
            pady=8,
            command=self.roll_dice
        )
        self.roll_button.grid(row=0, column=2, padx=10)

        self.reset_button = tk.Button(
            control_frame,
            text="NEW GAME",
            font=("Arial", 12, "bold"),
            bg="#2a9d8f",
            fg="white",
            padx=12,
            pady=8,
            command=self.reset_game
        )
        self.reset_button.grid(row=0, column=3, padx=10)

    # -------------------------
    # DRAW BOARD
    # -------------------------

    def draw_board(self):

        self.canvas.delete("all")

        for number in range(1, 101):

            row = (number - 1) // 10
            col = (number - 1) % 10

            # Zig-zag board
            if row % 2 == 0:
                actual_col = col
            else:
                actual_col = 9 - col

            x1 = actual_col * CELL_SIZE
            y1 = BOARD_SIZE - (row + 1) * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Cell colors
            if (row + actual_col) % 2 == 0:
                color = "#fefae0"
            else:
                color = "#a8dadc"

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#1d3557",
                width=2
            )

            self.canvas.create_text(
                x1 + 8,
                y1 + 8,
                text=str(number),
                anchor="nw",
                font=("Arial", 9, "bold"),
                fill="#1d3557"
            )

        self.draw_ladders()
        self.draw_snakes()
        self.draw_players()

    # -------------------------
    # GET CELL CENTER
    # -------------------------

    def get_center(self, position):

        row = (position - 1) // 10
        col = (position - 1) % 10

        if row % 2 == 0:
            actual_col = col
        else:
            actual_col = 9 - col

        x = actual_col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_SIZE - row * CELL_SIZE - CELL_SIZE // 2

        return x, y

    # -------------------------
    # DRAW LADDERS
    # -------------------------

    def draw_ladders(self):

        for start, end in LADDERS.items():

            x1, y1 = self.get_center(start)
            x2, y2 = self.get_center(end)

            # Ladder sides
            dx = 8
            self.canvas.create_line(
                x1 - dx, y1,
                x2 - dx, y2,
                fill="#2a9d8f",
                width=6
            )

            self.canvas.create_line(
                x1 + dx, y1,
                x2 + dx, y2,
                fill="#2a9d8f",
                width=6
            )

            # Ladder steps
            steps = 6

            for i in range(1, steps):
                t = i / steps

                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t

                self.canvas.create_line(
                    x - dx,
                    y,
                    x + dx,
                    y,
                    fill="#2a9d8f",
                    width=4
                )

    # -------------------------
    # DRAW SNAKES
    # -------------------------

    def draw_snakes(self):

        for head, tail in SNAKES.items():

            x1, y1 = self.get_center(head)
            x2, y2 = self.get_center(tail)

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#e63946",
                width=9,
                smooth=True
            )

            # Snake head
            self.canvas.create_oval(
                x1 - 13,
                y1 - 13,
                x1 + 13,
                y1 + 13,
                fill="#e63946",
                outline="#9d0208",
                width=2
            )

            # Eyes
            self.canvas.create_oval(
                x1 - 7,
                y1 - 6,
                x1 - 2,
                y1 - 1,
                fill="white"
            )

            self.canvas.create_oval(
                x1 + 2,
                y1 - 6,
                x1 + 7,
                y1 - 1,
                fill="white"
            )

    # -------------------------
    # DRAW PLAYERS
    # -------------------------

    def draw_players(self):

        positions = {}

        for player_index, position in enumerate(self.players):

            if position == 0:
                continue

            if position not in positions:
                positions[position] = []

            positions[position].append(player_index)

        for position, player_list in positions.items():

            for offset, player_index in enumerate(player_list):

                x, y = self.get_center(position)

                if len(player_list) > 1:
                    x += -12 if offset == 0 else 12
                    y += 12

                radius = 16

                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=COLORS[player_index],
                    outline="white",
                    width=3
                )

                self.canvas.create_text(
                    x,
                    y,
                    text=str(player_index + 1),
                    fill="white",
                    font=("Arial", 11, "bold")
                )

    # -------------------------
    # ROLL DICE
    # -------------------------

    def roll_dice(self):

        self.roll_button.config(state="disabled")

        dice = random.randint(1, 6)

        dice_faces = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }

        self.dice_label.config(text=dice_faces[dice])

        player = self.current_player
        old_position = self.players[player]
        new_position = old_position + dice

        # Cannot go beyond 100
        if new_position > 100:
            self.turn_label.config(
                text=f"Player {player + 1} needs exact number!"
            )

            self.switch_turn()
            return

        self.players[player] = new_position

        # Snake
        if new_position in SNAKES:

            self.players[player] = SNAKES[new_position]
            self.turn_label.config(
                text=f"🐍 Player {player + 1} got bitten!"
            )

        # Ladder
        elif new_position in LADDERS:

            self.players[player] = LADDERS[new_position]

            self.turn_label.config(
                text=f"🪜 Player {player + 1} climbed a ladder!"
            )

        else:

            self.turn_label.config(
                text=f"Player {player + 1} moved {dice} steps"
            )

        self.draw_board()

        # Winner
        if self.players[player] == 100:

            self.roll_button.config(state="disabled")

            messagebox.showinfo(
                "🎉 GAME OVER 🎉",
                f"🏆 Player {player + 1} WINS!\n\nCongratulations!"
            )

            return

        # Extra turn on 6
        if dice == 6:

            self.turn_label.config(
                text=f"🎉 Player {player + 1} rolled 6 — Roll again!"
            )

            self.roll_button.config(state="normal")

        else:

            self.switch_turn()

    # -------------------------
    # SWITCH TURN
    # -------------------------

    def switch_turn(self):

        self.current_player = 1 - self.current_player

        self.turn_label.config(
            text=f"Player {self.current_player + 1}'s Turn"
        )

        self.roll_button.config(state="normal")

    # -------------------------
    # RESET GAME
    # -------------------------

    def reset_game(self):

        self.players = [0, 0]
        self.current_player = 0

        self.dice_label.config(text="🎲")

        self.turn_label.config(
            text="Player 1's Turn"
        )

        self.roll_button.config(state="normal")

        self.draw_board()


# -----------------------------
# START GAME
# -----------------------------

root = tk.Tk()

game = SnakeLadderGame(root)

root.mainloop()
