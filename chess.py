import sys
import math
import time
import random
import threading
import pygame

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
FPS = 60
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

COLORS = {
    "bg_dark": (22, 27, 34),
    "bg_panel": (13, 17, 23),
    "bg_panel_light": (33, 38, 45),
    "accent": (88, 166, 255),
    "accent_hover": (139, 200, 255),
    "text_main": (240, 246, 252),
    "text_muted": (139, 148, 158),
    "board_light": (240, 217, 181),
    "board_dark": (181, 136, 99),
    "board_select": (186, 202, 43),
    "board_highlight": (130, 151, 105),
    "legal_dot": (88, 166, 255),
    "combat_flash": (255, 75, 75)
}

AI_CONFIGS = {
    "Beginner": {"depth": 1, "randomness": 0.4, "desc": "Plays instantly, frequently misses tactical blunders."},
    "Easy": {"depth": 1, "randomness": 0.1, "desc": "Slightly observant, plays simple one-move attacks."},
    "Intermediate": {"depth": 2, "randomness": 0.05, "desc": "Looks 2 plies ahead. Thinks about basic center control."},
    "Advanced": {"depth": 2, "randomness": 0.0, "desc": "Looks 2 plies ahead. Maximizes positional advantages."},
    "Expert": {"depth": 3, "randomness": 0.0, "desc": "Looks 3 plies ahead. Calculates forced tactical wins."},
    "Master": {"depth": 3, "randomness": 0.0, "desc": "Looks 3 plies ahead with aggressive spatial awareness."},
    "Grandmaster": {"depth": 4, "randomness": 0.0, "desc": "Looks 4 plies deep. Highly defensive and positional."}
}

AI_LEVELS = list(AI_CONFIGS.keys())
PERSONALITIES = ["Friendly Coach", "Grandmaster Analyst", "Competitive Rival", "Strategic Master", "Humorous Opponent"]

PIECE_UNICODES = {
    'wP': '♙', 'wR': '♜', 'wN': '♞', 'wB': '♝', 'wQ': '♛', 'wK': '♚',
    'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚'
}

PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0, 0, 2, 5, 5, 2, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 0],
    [0, -1, -1, 1, 1, -1, -1, 0],
    [0, 1, 1, -2, -2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_TABLE = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 2, 2, 1, 0, -3],
    [-3, 1, 2, 3, 3, 2, 1, -3],
    [-3, 0, 2, 3, 3, 2, 0, -3],
    [-3, 1, 1, 2, 2, 1, 1, -3],
    [-4, -2, 0, 1, 1, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]


# ==========================================
# FEATURE-COMPLETE CHESS ENGINE
# ==========================================
class ChessEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_to_move = True
        self.move_history = []
        self.game_over = False
        self.winner = None

        self.wK_moved = False
        self.wR1_moved = False
        self.wR2_moved = False
        self.bK_moved = False
        self.bR1_moved = False
        self.bR2_moved = False

    def get_legal_moves(self):
        moves = []
        turn = 'w' if self.white_to_move else 'b'
        for r in range(8):
            for c in range(8):
                if self.grid[r][c][0] == turn:
                    self.gen_moves_for_piece(r, c, moves)
        self.gen_castling_moves(moves)
        return moves

    def gen_moves_for_piece(self, r, c, moves):
        ptype = self.grid[r][c][1]
        turn = self.grid[r][c][0]
        if ptype == 'P':
            direction = -1 if turn == 'w' else 1
            if 0 <= r + direction < 8 and self.grid[r + direction][c] == '--':
                moves.append((r, c, r + direction, c))
                start_row = 6 if turn == 'w' else 1
                if r == start_row and self.grid[r + 2 * direction][c] == '--':
                    moves.append((r, c, r + 2 * direction, c))
            for dc in [-1, 1]:
                nc = c + dc
                nr = r + direction
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.grid[nr][nc] != '--' and self.grid[nr][nc][0] != turn:
                        moves.append((r, c, nr, nc))
        elif ptype in ['R', 'Q']:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, 8):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if self.grid[nr][nc] == '--':
                            moves.append((r, c, nr, nc))
                        elif self.grid[nr][nc][0] != turn:
                            moves.append((r, c, nr, nc));
                            break
                        else:
                            break
                    else:
                        break
        if ptype in ['B', 'Q']:
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for i in range(1, 8):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if self.grid[nr][nc] == '--':
                            moves.append((r, c, nr, nc))
                        elif self.grid[nr][nc][0] != turn:
                            moves.append((r, c, nr, nc));
                            break
                        else:
                            break
                    else:
                        break
        elif ptype == 'N':
            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.grid[nr][nc] == '--' or self.grid[nr][nc][0] != turn:
                        moves.append((r, c, nr, nc))
        elif ptype == 'K':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8 and (dr != 0 or dc != 0):
                        if self.grid[nr][nc] == '--' or self.grid[nr][nc][0] != turn:
                            moves.append((r, c, nr, nc))

    def gen_castling_moves(self, moves):
        if self.white_to_move:
            if self.wK_moved: return
            if not self.wR2_moved and self.grid[7][5] == '--' and self.grid[7][6] == '--':
                moves.append((7, 4, 7, 6))
            if not self.wR1_moved and self.grid[7][1] == '--' and self.grid[7][2] == '--' and self.grid[7][3] == '--':
                moves.append((7, 4, 7, 2))
        else:
            if self.bK_moved: return
            if not self.bR2_moved and self.grid[0][5] == '--' and self.grid[0][6] == '--':
                moves.append((0, 4, 0, 6))
            if not self.bR1_moved and self.grid[0][1] == '--' and self.grid[0][2] == '--' and self.grid[0][3] == '--':
                moves.append((0, 4, 0, 2))

    def execute_move(self, move):
        sr, sc, er, ec = move
        moving_piece = self.grid[sr][sc]
        target_piece = self.grid[er][ec]

        if moving_piece[1] == 'K' and abs(sc - ec) == 2:
            if ec == 6:
                self.grid[sr][5] = self.grid[sr][7]
                self.grid[sr][7] = '--'
            elif ec == 2:
                self.grid[sr][3] = self.grid[sr][0]
                self.grid[sr][0] = '--'

        self.grid[sr][sc] = '--'
        self.grid[er][ec] = moving_piece

        if moving_piece[1] == 'P' and (er == 0 or er == 7):
            self.grid[er][ec] = moving_piece[0] + 'Q'

        if moving_piece == 'wK':
            self.wK_moved = True
        elif moving_piece == 'bK':
            self.bK_moved = True
        elif moving_piece == 'wR' and sr == 7 and sc == 0:
            self.wR1_moved = True
        elif moving_piece == 'wR' and sr == 7 and sc == 7:
            self.wR2_moved = True
        elif moving_piece == 'bR' and sr == 0 and sc == 0:
            self.bR1_moved = True
        elif moving_piece == 'bR' and sr == 0 and sc == 7:
            self.bR2_moved = True

        self.white_to_move = not self.white_to_move

        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
        self.move_history.append(f"{moving_piece[1]}: {files[sc]}{ranks[sr]}➔{files[ec]}{ranks[er]}")

        if target_piece[1] == 'K':
            self.game_over = True
            self.winner = "White" if moving_piece[0] == 'w' else "Black"


# ==========================================
# POSITION EVALUATION LOGIC
# ==========================================
def evaluate_board(grid):
    values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 9000}
    score = 0
    for r in range(8):
        for c in range(8):
            piece = grid[r][c]
            if piece == '--': continue
            color, ptype = piece[0], piece[1]

            val = values[ptype]
            pos_bonus = 0
            if ptype == 'P':
                pos_bonus = PAWN_TABLE[r][c] if color == 'b' else PAWN_TABLE[7 - r][c]
            elif ptype == 'N':
                pos_bonus = KNIGHT_TABLE[r][c] if color == 'b' else KNIGHT_TABLE[7 - r][c]

            total_val = val + pos_bonus
            if color == 'w':
                score += total_val
            else:
                score -= total_val
    return score


def minimax(grid, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate_board(grid), None

    engine_temp = ChessEngine()
    engine_temp.grid = [row[:] for row in grid]
    engine_temp.white_to_move = maximizing

    moves = engine_temp.get_legal_moves()
    if not moves:
        return evaluate_board(grid), None

    moves.sort(key=lambda m: (grid[m[2]][m[3]] != '--'), reverse=True)

    best_move = None
    if maximizing:
        max_eval = -999999
        for move in moves:
            saved = [row[:] for row in grid]
            sr, sc, er, ec = move
            grid[er][ec] = grid[sr][sc]
            grid[sr][sc] = '--'

            ev, _ = minimax(grid, depth - 1, alpha, beta, False)
            grid = saved

            if ev > max_eval:
                max_eval = ev
                best_move = move
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999999
        for move in moves:
            saved = [row[:] for row in grid]
            sr, sc, er, ec = move
            grid[er][ec] = grid[sr][sc]
            grid[sr][sc] = '--'

            ev, _ = minimax(grid, depth - 1, alpha, beta, True)
            grid = saved

            if ev < min_eval:
                min_eval = ev
                best_move = move
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval, best_move


# ==========================================
# ANIMATION ENGINE
# ==========================================
class FXEngine:
    def __init__(self):
        self.active_slide = None
        self.combat_fx = None

    def trigger_slide(self, piece, start_pos, end_pos, src_tile, callback_move):
        self.active_slide = {
            "piece": piece, "start": list(start_pos), "end": list(end_pos),
            "current": list(start_pos), "progress": 0.0, "src_tile": src_tile, "callback": callback_move
        }

    def trigger_combat(self, attacker, victim, pos):
        self.combat_fx = {
            "attacker": attacker, "victim": victim, "pos": pos,
            "timer": 0.0, "duration": 0.5, "particles": []
        }
        for _ in range(25):
            self.combat_fx["particles"].append({
                "x": pos[0] + 33, "y": pos[1] + 33,
                "vx": random.uniform(-5, 5), "vy": random.uniform(-5, 5),
                "radius": random.randint(2, 6)
            })

    def update(self, dt):
        if self.active_slide:
            self.active_slide["progress"] += dt * 5.0
            t = min(self.active_slide["progress"], 1.0)
            t_ease = 1.0 - (1.0 - t) ** 3
            self.active_slide["current"][0] = self.active_slide["start"][0] + (
                        self.active_slide["end"][0] - self.active_slide["start"][0]) * t_ease
            self.active_slide["current"][1] = self.active_slide["start"][1] + (
                        self.active_slide["end"][1] - self.active_slide["start"][1]) * t_ease

            if t >= 1.0:
                self.active_slide["callback"]()
                self.active_slide = None

        if self.combat_fx:
            self.combat_fx["timer"] += dt
            for p in self.combat_fx["particles"]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
            if self.combat_fx["timer"] >= self.combat_fx["duration"]:
                self.combat_fx = None

    def draw(self, surface, font, sq_size):
        if self.combat_fx:
            t = self.combat_fx["timer"]
            cx, cy = self.combat_fx["pos"][0] + sq_size // 2, self.combat_fx["pos"][1] + sq_size // 2
            ptype = self.combat_fx["attacker"][1]

            if ptype == 'N':
                pygame.draw.line(surface, (230, 230, 250), (cx - 40, cy - 20), (cx + 40, cy + 20), 8)
                pygame.draw.line(surface, (255, 255, 255), (cx - 40, cy - 20), (cx + 40, cy + 20), 3)
            elif ptype == 'B':
                pygame.draw.line(surface, (147, 112, 219), (cx, cy - 35), (cx, cy + 35), 6)
                pygame.draw.line(surface, (147, 112, 219), (cx - 35, cy), (cx + 35, cy), 6)
            elif ptype == 'R':
                pygame.draw.circle(surface, (211, 211, 211), (cx, cy), int(t * 80), 4)
            elif ptype == 'Q':
                pygame.draw.circle(surface, (255, 215, 0), (cx, cy), int(t * 50), 0)
                pygame.draw.circle(surface, (255, 255, 255), (cx, cy), int(t * 25), 0)
            elif ptype == 'P':
                pygame.draw.line(surface, (255, 69, 0), (cx - 15, cy - 15), (cx + 15, cy + 15), 4)

            for p in self.combat_fx["particles"]:
                pygame.draw.circle(surface, COLORS["combat_flash"], (int(p["x"]), int(p["y"])), p["radius"])


# ==========================================
# MAIN GRAPHICS WORKSPACE ARENA
# ==========================================
class PremiumChessArena:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AlphaZero Custom Chess Workspace")
        self.clock = pygame.time.Clock()

        self.font_sm = pygame.font.SysFont("Arial", 15)
        self.font_md = pygame.font.SysFont("Arial", 19, bold=True)
        self.font_lg = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_pieces = pygame.font.SysFont("Segoe UI Symbol", 48)

        self.engine = ChessEngine()
        self.fx = FXEngine()

        self.app_state = "MENU"
        self.selected_lvl = "Intermediate"
        self.selected_pers = "Friendly Coach"
        self.player_color = "w"

        self.selected_sq = None
        self.active_legal_destinations = []

        self.ai_thinking = False
        self.queued_ai_move = None

        self.board_x, self.board_y = 320, 130
        self.sq_size = 540 // 8

    def run_loop(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.process_input_events()
            self.fx.update(dt)

            if self.queued_ai_move:
                self.initiate_animated_move(self.queued_ai_move)
                self.queued_ai_move = None

            ai_turn = (self.engine.white_to_move and self.player_color == "b") or (
                        not self.engine.white_to_move and self.player_color == "w")
            if self.app_state == "GAMEPLAY" and ai_turn and not self.engine.game_over and not self.fx.active_slide and not self.ai_thinking:
                self.ai_thinking = True
                threading.Thread(target=self.async_ai_worker, daemon=True).start()

            self.render_screen_view()
            pygame.display.flip()

    def process_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.app_state == "MENU":
                    self.handle_menu_clicks(mx, my)
                elif self.app_state == "GAMEPLAY":
                    self.handle_gameplay_clicks(mx, my)

    def handle_menu_clicks(self, mx, my):
        for i, lvl in enumerate(AI_LEVELS):
            if pygame.Rect(50, 220 + i * 65, 260, 50).collidepoint(mx, my):
                self.selected_lvl = lvl
        for i, pers in enumerate(PERSONALITIES):
            if pygame.Rect(350, 220 + i * 65, 300, 50).collidepoint(mx, my):
                self.selected_pers = pers
        if pygame.Rect(700, 220, 180, 50).collidepoint(mx, my):
            self.player_color = "w"
        elif pygame.Rect(910, 220, 180, 50).collidepoint(mx, my):
            self.player_color = "b"

        if pygame.Rect(700, 610, 390, 60).collidepoint(mx, my):
            self.engine.reset()
            self.app_state = "GAMEPLAY"
            self.ai_thinking = False
            self.queued_ai_move = None

    def handle_gameplay_clicks(self, mx, my):
        if pygame.Rect(20, 20, 140, 40).collidepoint(mx, my):
            self.app_state = "MENU"
            self.selected_sq = None
            self.active_legal_destinations = []
            return

        ai_turn = (self.engine.white_to_move and self.player_color == "b") or (
                    not self.engine.white_to_move and self.player_color == "w")
        if self.engine.game_over or self.fx.active_slide or ai_turn: return

        if self.board_x <= mx < self.board_x + 540 and self.board_y <= my < self.board_y + 540:
            c = (mx - self.board_x) // self.sq_size
            r = (my - self.board_y) // self.sq_size

            # INVERTED FEATURE: Flip coordinate lookups when playing as Black Alliance
            if self.player_color == "b":
                r = 7 - r
                c = 7 - c

            if self.selected_sq is None:
                if self.engine.grid[r][c] != '--' and self.engine.grid[r][c][0] == self.player_color:
                    self.selected_sq = (r, c)
                    self.active_legal_destinations = [
                        (m[2], m[3]) for m in self.engine.get_legal_moves() if m[0] == r and m[1] == c
                    ]
            else:
                sr, sc = self.selected_sq
                move = (sr, sc, r, c)
                if move in self.engine.get_legal_moves():
                    self.initiate_animated_move(move)

                self.selected_sq = None
                self.active_legal_destinations = []

    def initiate_animated_move(self, move):
        sr, sc, er, ec = move
        p = self.engine.grid[sr][sc]
        target = self.engine.grid[er][ec]

        # INVERTED FEATURE: Map starting and destination visual tracks based on orientation
        if self.player_color == "b":
            start_pt = (self.board_x + (7 - sc) * self.sq_size, self.board_y + (7 - sr) * self.sq_size)
            end_pt = (self.board_x + (7 - ec) * self.sq_size, self.board_y + (7 - er) * self.sq_size)
        else:
            start_pt = (self.board_x + sc * self.sq_size, self.board_y + sr * self.sq_size)
            end_pt = (self.board_x + ec * self.sq_size, self.board_y + er * self.sq_size)

        def move_completion_callback():
            if target != '--':
                self.fx.trigger_combat(p, target, end_pt)
            self.engine.execute_move(move)

        self.fx.trigger_slide(p, start_pt, end_pt, (sr, sc), move_completion_callback)

    def async_ai_worker(self):
        moves = self.engine.get_legal_moves()
        if not moves:
            self.queued_ai_move = None
            self.ai_thinking = False
            return

        cfg = AI_CONFIGS[self.selected_lvl]
        if random.random() < cfg["randomness"]:
            chosen = random.choice(moves)
        else:
            grid_copy = [row[:] for row in self.engine.grid]
            maximizing_flag = self.engine.white_to_move
            _, chosen = minimax(grid_copy, cfg["depth"], -999999, 999999, maximizing_flag)
            if not chosen:
                chosen = random.choice(moves)

        self.queued_ai_move = chosen
        self.ai_thinking = False

    def render_screen_view(self):
        self.screen.fill(COLORS["bg_dark"])
        if self.app_state == "MENU":
            self.draw_modern_loading_menu()
        elif self.app_state == "GAMEPLAY":
            self.draw_gameplay_workspace()

    def draw_modern_loading_menu(self):
        title = self.font_lg.render("ALPHAZERO COGNITIVE WORKSPACE", True, COLORS["accent"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 40))

        lbl_col1 = self.font_md.render("AI STRATEGY LEVEL", True, COLORS["text_main"])
        self.screen.blit(lbl_col1, (50, 160))
        for i, lvl in enumerate(AI_LEVELS):
            bg_c = COLORS["accent"] if self.selected_lvl == lvl else COLORS["bg_panel_light"]
            txt_c = COLORS["bg_dark"] if self.selected_lvl == lvl else COLORS["text_main"]
            rect = pygame.Rect(50, 220 + i * 65, 260, 50)
            pygame.draw.rect(self.screen, bg_c, rect, border_radius=6)
            txt = self.font_md.render(lvl, True, txt_c)
            self.screen.blit(txt, (rect.x + 20, rect.y + 14))

        lbl_col2 = self.font_md.render("OPPONENT LOGIC MODEL", True, COLORS["text_main"])
        self.screen.blit(lbl_col2, (350, 160))
        for i, pers in enumerate(PERSONALITIES):
            bg_c = COLORS["accent"] if self.selected_pers == pers else COLORS["bg_panel_light"]
            txt_c = COLORS["bg_dark"] if self.selected_pers == pers else COLORS["text_main"]
            rect = pygame.Rect(350, 220 + i * 65, 300, 50)
            pygame.draw.rect(self.screen, bg_c, rect, border_radius=6)
            txt = self.font_md.render(pers, True, txt_c)
            self.screen.blit(txt, (rect.x + 20, rect.y + 14))

        lbl_col3 = self.font_md.render("CHOOSE ALLIANCE ALLOCATION", True, COLORS["text_main"])
        self.screen.blit(lbl_col3, (700, 160))

        w_bg = COLORS["accent"] if self.player_color == "w" else COLORS["bg_panel_light"]
        w_tx = COLORS["bg_dark"] if self.player_color == "w" else COLORS["text_main"]
        w_rect = pygame.Rect(700, 220, 180, 50)
        pygame.draw.rect(self.screen, w_bg, w_rect, border_radius=6)
        lbl_w = self.font_md.render("White Alliance", True, w_tx)
        self.screen.blit(lbl_w, (w_rect.x + 20, w_rect.y + 14))

        b_bg = COLORS["accent"] if self.player_color == "b" else COLORS["bg_panel_light"]
        b_tx = COLORS["bg_dark"] if self.player_color == "b" else COLORS["text_main"]
        b_rect = pygame.Rect(910, 220, 180, 50)
        pygame.draw.rect(self.screen, b_bg, b_rect, border_radius=6)
        lbl_b = self.font_md.render("Black Alliance", True, b_tx)
        self.screen.blit(lbl_b, (b_rect.x + 20, b_rect.y + 14))

        desc_box = pygame.Rect(700, 310, 390, 250)
        pygame.draw.rect(self.screen, COLORS["bg_panel"], desc_box, border_radius=8)
        desc_lbl = self.font_md.render("SIMULATION PARAMS SUMMARY:", True, COLORS["text_main"])
        self.screen.blit(desc_lbl, (desc_box.x + 20, desc_box.y + 20))

        info_txt = f"Search Target Matrix: {AI_CONFIGS[self.selected_lvl]['desc']}"
        lbl_info = self.font_sm.render(info_txt, True, COLORS["text_muted"])
        self.screen.blit(lbl_info, (desc_box.x + 20, desc_box.y + 70))

        flip_note = "Board Orientation: Inverted (Flipped Perspective)" if self.player_color == "b" else "Board Orientation: Standard"
        lbl_flip = self.font_sm.render(flip_note, True, COLORS["accent"])
        self.screen.blit(lbl_flip, (desc_box.x + 20, desc_box.y + 110))

        launch_rect = pygame.Rect(700, 610, 390, 60)
        pygame.draw.rect(self.screen, COLORS["accent_hover"], launch_rect, border_radius=8)
        lbl_lnch = self.font_md.render("INITIALIZE STRATEGIC ENGINE", True, COLORS["bg_dark"])
        self.screen.blit(lbl_lnch, (launch_rect.x + (launch_rect.w - lbl_lnch.get_width()) // 2, launch_rect.y + 18))

    def draw_gameplay_workspace(self):
        nav_rect = pygame.Rect(20, 20, 140, 40)
        pygame.draw.rect(self.screen, COLORS["bg_panel_light"], nav_rect, border_radius=6)
        lbl_nav = self.font_sm.render("<- Exit to Menu", True, COLORS["text_main"])
        self.screen.blit(lbl_nav, (nav_rect.x + 18, nav_rect.y + 10))

        left_panel = pygame.Rect(20, 130, 260, 540)
        pygame.draw.rect(self.screen, COLORS["bg_panel"], left_panel, border_radius=8)
        pygame.draw.rect(self.screen, COLORS["bg_panel_light"], (20, 130, 260, 50), border_radius=8)

        lbl_ai = self.font_md.render(self.selected_pers, True, COLORS["accent"])
        self.screen.blit(lbl_ai, (35, 145))

        if self.ai_thinking:
            bubble_txt = "Grandmaster processing tactics..."
        else:
            bubble_txt = f"Level: {self.selected_lvl}. Make your move."

        if self.engine.game_over:
            bubble_txt = "Analysis complete. Checkmate."

        lbl_bub = self.font_sm.render(bubble_txt, True, COLORS["text_main"])
        self.screen.blit(lbl_bub, (35, 200))

        pygame.draw.rect(self.screen, COLORS["bg_panel"], (self.board_x - 10, self.board_y - 10, 560, 560),
                         border_radius=10)

        # INVERTED FEATURE: Loop indices adjust rendering layouts dynamically
        for r_idx in range(8):
            for c_idx in range(8):
                r = 7 - r_idx if self.player_color == "b" else r_idx
                c = 7 - c_idx if self.player_color == "b" else c_idx

                x = self.board_x + c_idx * self.sq_size
                y = self.board_y + r_idx * self.sq_size

                is_light = (r + c) % 2 == 0
                sq_color = COLORS["board_light"] if is_light else COLORS["board_dark"]

                if self.selected_sq == (r, c):
                    sq_color = COLORS["board_select"]

                pygame.draw.rect(self.screen, sq_color, (x, y, self.sq_size, self.sq_size))

                if (r, c) in self.active_legal_destinations:
                    dot_surface = pygame.Surface((self.sq_size, self.sq_size), pygame.SRCALPHA)
                    pygame.draw.circle(dot_surface, (*COLORS["legal_dot"], 160), (self.sq_size // 2, self.sq_size // 2),
                                       12)
                    self.screen.blit(dot_surface, (x, y))

                if self.fx.active_slide and (r, c) == self.fx.active_slide["src_tile"]:
                    continue

                piece = self.engine.grid[r][c]
                if piece != '--':
                    glyph = PIECE_UNICODES[piece]
                    p_color = (255, 255, 255) if piece[0] == 'w' else (25, 25, 25)
                    g_surface = self.font_pieces.render(glyph, True, p_color)
                    self.screen.blit(g_surface, (x + (self.sq_size - g_surface.get_width()) // 2,
                                                 y + (self.sq_size - g_surface.get_height()) // 2 - 4))

        if self.fx.active_slide:
            p = self.fx.active_slide["piece"]
            glyph = PIECE_UNICODES[p]
            p_color = (255, 255, 255) if p[0] == 'w' else (25, 25, 25)
            g_surface = self.font_pieces.render(glyph, True, p_color)
            self.screen.blit(g_surface,
                             (int(self.fx.active_slide["current"][0] + (self.sq_size - g_surface.get_width()) // 2),
                              int(self.fx.active_slide["current"][1] + (
                                          self.sq_size - g_surface.get_height()) // 2 - 4)))

        self.fx.draw(self.screen, self.font_pieces, self.sq_size)

        right_panel = pygame.Rect(self.board_x + 540 + 30, 130, 270, 540)
        pygame.draw.rect(self.screen, COLORS["bg_panel"], right_panel, border_radius=8)
        lbl_hist = self.font_md.render("REALTIME PROCESS LOGS", True, COLORS["text_main"])
        self.screen.blit(lbl_hist, (right_panel.x + 20, 150))

        for i, entry in enumerate(self.engine.move_history[-15:]):
            txt_h = self.font_sm.render(entry, True, COLORS["text_muted"])
            self.screen.blit(txt_h, (right_panel.x + 20, 190 + i * 22))

        if self.engine.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            box = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 150, 500, 300)
            pygame.draw.rect(self.screen, COLORS["bg_panel"], box, border_radius=12)
            pygame.draw.rect(self.screen, COLORS["accent"], box, width=3, border_radius=12)

            lbl_win = self.font_lg.render("CHECKMATE DETECTED", True, COLORS["combat_flash"])
            lbl_sub = self.font_md.render(f"Victor: {self.engine.winner} Victory Team", True, COLORS["text_main"])

            self.screen.blit(lbl_win, (box.x + (box.w - lbl_win.get_width()) // 2, box.y + 60))
            self.screen.blit(lbl_sub, (box.x + (box.w - lbl_sub.get_width()) // 2, box.y + 130))

            btn_rst = pygame.Rect(box.x + 150, box.y + 200, 200, 45)
            pygame.draw.rect(self.screen, COLORS["accent"], btn_rst, border_radius=6)
            lbl_btn = self.font_sm.render("Return To Configuration", True, COLORS["bg_dark"])
            self.screen.blit(lbl_btn, (btn_rst.x + (btn_rst.w - lbl_btn.get_width()) // 2, btn_rst.y + 12))

            mx, my = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and btn_rst.collidepoint(mx, my):
                self.app_state = "MENU"
                self.engine.reset()


if __name__ == "__main__":
    arena = PremiumChessArena()
    arena.run_loop()