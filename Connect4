import tkinter as tk
from tkinter import messagebox
import random
import copy
import time

# --- CONSTANTS ---
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

# Modern Color Palette (Dark Mode)
BG_MAIN = "#1e1e24"  # Deep charcoal
BG_BOARD = "#2a2b36"  # Sleek slate gray
COLOR_PANEL = "#111116"  # Dark sidebar
COLOR_EMPTY = "#3a3b45"  # Unfilled slot
COLOR_PLAYER = "#ff4a5a"  # Vibrant Neon Red
COLOR_AI = "#2ec4b6"  # Brilliant Turquoise
COLOR_TEXT = "#f4f4f9"  # Off-white
COLOR_ACCENT = "#7209b7"  # Deep Purple for menus


class Connect4Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 - Advanced AI")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        # Game State Variables
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_turn = PLAYER
        self.ai_difficulty = "Medium"  # Default
        self.game_active = False
        self.is_animating = False

        # Start with the loading screen
        self.show_loading_screen()

    # --- 1. LOADING SCREEN ---
    def show_loading_screen(self):
        self.loading_frame = tk.Frame(self.root, bg=COLOR_PANEL)
        self.loading_frame.pack(fill="both", expand=True)

        # Title
        lbl_title = tk.Label(self.loading_frame, text="CONNECT FOUR", font=("Helvetica", 36, "bold"), fg=COLOR_PLAYER,
                             bg=COLOR_PANEL)
        lbl_title.pack(pady=(150, 10))

        lbl_subtitle = tk.Label(self.loading_frame, text="Advanced AI Edition", font=("Helvetica", 16, "italic"),
                                fg=COLOR_AI, bg=COLOR_PANEL)
        lbl_subtitle.pack(pady=10)

        # Animated Loading Bar Canvas
        self.load_canvas = tk.Canvas(self.loading_frame, width=400, height=20, bg=BG_BOARD, highlightthickness=0)
        self.load_canvas.pack(pady=40)
        self.load_bar = self.load_canvas.create_rectangle(0, 0, 0, 20, fill=COLOR_ACCENT, width=0)

        # Skip Button
        self.btn_skip = tk.Button(self.loading_frame, text="Skip Intro →", font=("Helvetica", 11, "bold"),
                                  fg=COLOR_TEXT, bg=BG_MAIN,
                                  activebackground=COLOR_ACCENT, activeforeground=COLOR_TEXT, bd=0, cursor="hand2",
                                  command=self.skip_loading)
        self.btn_skip.pack(pady=10)

        self.loading_progress = 0
        self.loading_cancelled = False
        self.animate_loading()

    def animate_loading(self):
        if self.loading_cancelled:
            return
        if self.loading_progress < 400:
            self.loading_progress += 8
            self.load_canvas.coords(self.load_bar, 0, 0, self.loading_progress, 20)
            self.root.after(30, self.animate_loading)
        else:
            self.transition_to_menu()

    def skip_loading(self):
        self.loading_cancelled = True
        self.transition_to_menu()

    def transition_to_menu(self):
        self.loading_frame.destroy()
        self.show_main_menu()

    # --- 2. MAIN MENU ---
    def show_main_menu(self):
        self.menu_frame = tk.Frame(self.root, bg=BG_MAIN)
        self.menu_frame.pack(fill="both", expand=True)

        lbl_menu_title = tk.Label(self.menu_frame, text="SELECT DIFFICULTY", font=("Helvetica", 24, "bold"),
                                  fg=COLOR_TEXT, bg=BG_MAIN)
        lbl_menu_title.pack(pady=(120, 40))

        # Difficulty Buttons Setup
        diff_frame = tk.Frame(self.menu_frame, bg=BG_MAIN)
        diff_frame.pack(pady=20)

        self.diff_var = tk.StringVar(value="Medium")
        difficulties = [("Easy (Casual)", "Easy", COLOR_AI),
                        ("Medium (Challenging)", "Medium", COLOR_ACCENT),
                        ("Hard (Expert Minimax)", "Hard", COLOR_PLAYER)]

        for text, mode, color in difficulties:
            btn = tk.Radiobutton(diff_frame, text=text, variable=self.diff_var, value=mode, indicatoron=False,
                                 font=("Helvetica", 14, "bold"), width=25, fg=COLOR_TEXT, bg=BG_BOARD,
                                 activebackground=color, activeforeground=COLOR_TEXT, selectcolor=color,
                                 bd=3, relief="raised", cursor="hand2", padx=10, pady=10)
            btn.pack(pady=10)

        # Start Game Button
        btn_start = tk.Button(self.menu_frame, text="LAUNCH GAME", font=("Helvetica", 16, "bold"), fg=COLOR_TEXT,
                              bg="#06d6a0",
                              activebackground="#2ec4b6", activeforeground=COLOR_TEXT, width=15, bd=0, cursor="hand2",
                              command=self.start_game)
        btn_start.pack(pady=40)

    def start_game(self):
        self.ai_difficulty = self.diff_var.get()
        self.menu_frame.destroy()
        self.setup_game_screen()
        self.game_active = True

    # --- 3. MAIN GAME SCREEN INTERFACE ---
    def setup_game_screen(self):
        # Left Panel - Game Board
        self.board_frame = tk.Frame(self.root, bg=BG_MAIN, padx=20, pady=20)
        self.board_frame.pack(side="left", fill="both", expand=True)

        # Right Panel - Controls & Status
        self.sidebar = tk.Frame(self.root, bg=COLOR_PANEL, width=250, padx=20, pady=20)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        # Dynamic Status Display
        self.lbl_status = tk.Label(self.sidebar, text="Your Turn!", font=("Helvetica", 18, "bold"), fg=COLOR_PLAYER,
                                   bg=COLOR_PANEL)
        self.lbl_status.pack(pady=(20, 10))

        lbl_diff = tk.Label(self.sidebar, text=f"AI Level: {self.ai_difficulty}", font=("Helvetica", 12), fg=COLOR_TEXT,
                            bg=COLOR_PANEL)
        lbl_diff.pack(pady=(0, 40))

        # Legend panels
        self.create_legend_item(COLOR_PLAYER, "You (Red)")
        self.create_legend_item(COLOR_AI, "AI (Turquoise)")

        # Menu navigation items
        btn_reset = tk.Button(self.sidebar, text="Reset Game", font=("Helvetica", 12, "bold"), fg=COLOR_TEXT,
                              bg=BG_BOARD,
                              activebackground=COLOR_ACCENT, activeforeground=COLOR_TEXT, width=15, bd=0,
                              cursor="hand2", command=self.reset_game)
        btn_reset.pack(side="bottom", pady=10)

        btn_back = tk.Button(self.sidebar, text="Main Menu", font=("Helvetica", 12, "bold"), fg=COLOR_TEXT, bg=BG_MAIN,
                             activebackground=COLOR_PLAYER, activeforeground=COLOR_TEXT, width=15, bd=0, cursor="hand2",
                             command=self.return_to_menu)
        btn_back.pack(side="bottom", pady=10)

        # Canvas for the Connect 4 Board Grid
        self.canvas = tk.Canvas(self.board_frame, width=620, height=530, bg=BG_BOARD, highlightthickness=0)
        self.canvas.pack(anchor="center", expand=True)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_hover)

        self.draw_board_grid()

    def create_legend_item(self, color, text):
        f = tk.Frame(self.sidebar, bg=COLOR_PANEL)
        f.pack(pady=5, anchor="w")
        lbl_color = tk.Label(f, bg=color, width=3, height=1)
        lbl_color.pack(side="left", padx=(10, 10))
        lbl_txt = tk.Label(f, text=text, font=("Helvetica", 12), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_txt.pack(side="left")

    def draw_board_grid(self):
        self.canvas.delete("all")
        # Pre-calculated spacing variables
        self.cell_width = 620 // COLS
        self.cell_height = 530 // ROWS
        self.radius = min(self.cell_width, self.cell_height) // 2 - 6

        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * self.cell_width + (self.cell_width // 2) - self.radius
                y1 = r * self.cell_height + (self.cell_height // 2) - self.radius
                x2 = x1 + 2 * self.radius
                y2 = y1 + 2 * self.radius

                # Draw base empty structural holes
                color = COLOR_EMPTY
                if self.board[r][c] == PLAYER:
                    color = COLOR_PLAYER
                elif self.board[r][c] == AI:
                    color = COLOR_AI

                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#1a1b24", width=2, tags=f"cell_{r}_{c}")

    # --- 4. GAMEPLAY ANIMATION & MECHANICS ---
    def handle_hover(self, event):
        if not self.game_active or self.current_turn != PLAYER or self.is_animating:
            return
        col = event.x // (620 // COLS)
        if 0 <= col < COLS:
            self.canvas.delete("hover_indicator")
            # Draw a subtle top track indicator showing column selection
            cw = 620 // COLS
            self.canvas.create_rectangle(col * cw + 5, 2, (col + 1) * cw - 5, 8, fill=COLOR_PLAYER, outline="",
                                         tags="hover_indicator")

    def handle_click(self, event):
        if not self.game_active or self.current_turn != PLAYER or self.is_animating:
            return

        col = event.x // (620 // COLS)
        if 0 <= col < COLS:
            if self.is_valid_location(self.board, col):
                self.canvas.delete("hover_indicator")
                self.make_move(col, PLAYER)

    def make_move(self, col, player):
        row = self.get_next_open_row(self.board, col)
        self.board[row][col] = player
        self.animate_piece_drop(row, col, player)

    def animate_piece_drop(self, target_row, col, player):
        self.is_animating = True
        cw = 620 // COLS
        ch = 530 // ROWS
        cx = col * cw + (cw // 2)

        # Spawn initial piece at topmost row boundary coordinates
        current_y_row = 0
        color = COLOR_PLAYER if player == PLAYER else COLOR_AI

        def step_animation():
            nonlocal current_y_row
            # Reset previous step slot appearance
            if current_y_row > 0:
                self.update_cell_color(current_y_row - 1, col, COLOR_EMPTY)

            # Colour current drop step slot
            self.update_cell_color(current_y_row, col, color)

            if current_y_row < target_row:
                current_y_row += 1
                self.root.after(40, step_animation)
            else:
                self.finalize_move(target_row, col, player)

        step_animation()

    def update_cell_color(self, r, c, color):
        tag = f"cell_{r}_{c}"
        self.canvas.itemconfig(tag, fill=color)

    def finalize_move(self, row, col, player):
        self.is_animating = False
        if self.check_winning_move(self.board, player):
            self.end_game(f"{'You win!' if player == PLAYER else 'AI Wins!'}")
            return

        if self.is_board_full():
            self.end_game("It's a Draw!")
            return

        # Handle Turn Switching Logic
        if player == PLAYER:
            self.current_turn = AI
            self.lbl_status.config(text="AI is thinking...", fg=COLOR_AI)
            # Run AI move calculations slightly delayed to allow UI buffer frame processing
            self.root.after(400, self.trigger_ai_turn)
        else:
            self.current_turn = PLAYER
            self.lbl_status.config(text="Your Turn!", fg=COLOR_PLAYER)

    def trigger_ai_turn(self):
        if not self.game_active: return
        ai_col = self.get_ai_move()
        if ai_col is not None:
            self.make_move(ai_col, AI)

    def is_board_full(self):
        return all(not self.is_valid_location(self.board, c) for c in range(COLS))

    def end_game(self, message):
        self.game_active = False
        self.lbl_status.config(text="Game Over", fg=COLOR_TEXT)
        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_turn = PLAYER
        self.game_active = True
        self.is_animating = False
        self.lbl_status.config(text="Your Turn!", fg=COLOR_PLAYER)
        self.draw_board_grid()

    def return_to_menu(self):
        self.game_active = False
        self.board_frame.destroy()
        self.sidebar.destroy()
        self.show_main_menu()

    # --- 5. CORE CONNECT 4 GAME ENGINE ENGINE LOGIC ---
    def is_valid_location(self, board, col):
        return board[0][col] == EMPTY

    def get_next_open_row(self, board, col):
        for r in range(ROWS - 1, -1, -1):
            if board[r][col] == EMPTY:
                return r

    def check_winning_move(self, board, piece):
        # Check horizontal spaces
        for c in range(COLS - 3):
            for r in range(ROWS):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True
        # Check vertical spaces
        for c in range(COLS):
            for r in range(ROWS - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True
        # Check positively sloped diagonals
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True
        # Check negatively sloped diagonals
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True
        return False

    # --- 6. ADVANCED HEURISTIC AI SYSTEM (MINIMAX + ALPHA-BETA) ---
    def get_ai_move(self):
        valid_cols = [c for c in range(COLS) if self.is_valid_location(self.board, c)]
        if not valid_cols: return None

        if self.ai_difficulty == "Easy":
            # Easy Mode: Mostly random choices, basic 1-step offensive winning checks.
            for c in valid_cols:
                temp_board = copy.deepcopy(self.board)
                r = self.get_next_open_row(temp_board, c)
                temp_board[r][c] = AI
                if self.check_winning_move(temp_board, AI):
                    return c
            return random.choice(valid_cols)

        elif self.ai_difficulty == "Medium":
            # Medium Mode: Evaluates options up to 3 turns deep.
            col, _ = self.minimax(self.board, 3, -float('inf'), float('inf'), True)
            return col if col is not None else random.choice(valid_cols)

        else:
            # Hard Mode: Deep 5-ply positional lookahead engine. Highly tactical.
            col, _ = self.minimax(self.board, 5, -float('inf'), float('inf'), True)
            return col if col is not None else random.choice(valid_cols)

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER if piece == AI else AI

        if window.count(piece) == 4:
            score += 10000
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 100
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 10

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 80  # Blocks opponent chains aggressively

        return score

    def score_position(self, board, piece):
        score = 0

        # Highly evaluate center column control positional priority
        center_array = [board[r][COLS // 2] for r in range(ROWS)]
        center_count = center_array.count(piece)
        score += center_count * 6

        # Score Horizontal
        for r in range(ROWS):
            row_array = board[r]
            for c in range(COLS - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLS):
            col_array = [board[r][c] for r in range(ROWS)]
            for r in range(ROWS - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score Positive Diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [board[r + i][c + i] for ii, i in enumerate(range(4))]
                score += self.evaluate_window(window, piece)

        # Score Negative Diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = [c for c in range(COLS) if self.is_valid_location(board, c)]
        is_terminal = self.check_winning_move(board, PLAYER) or self.check_winning_move(board, AI) or len(
            valid_locations) == 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winning_move(board, AI):
                    return (None, 100000000 + depth)  # Prefer immediate pathways
                elif self.check_winning_move(board, PLAYER):
                    return (None, -100000000 - depth)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, AI))

        # Re-order move evaluation mapping left-to-center to compute alpha-beta cutoffs faster
        valid_locations.sort(key=lambda col: abs(col - (COLS // 2)))

        if maximizingPlayer:
            value = -float('inf')
            column = random.choice(valid_locations) if valid_locations else None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = copy.deepcopy(board)
                b_copy[row][col] = AI
                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player options optimization
            value = float('inf')
            column = random.choice(valid_locations) if valid_locations else None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = copy.deepcopy(board)
                b_copy[row][col] = PLAYER
                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4Game(root)
    root.mainloop()

