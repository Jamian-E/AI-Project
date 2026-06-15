import pygame
import sys
import random
import os

pygame.init()

WIDTH, HEIGHT = 900, 520
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors - Tournament Edition")

# Colors
WHITE = (255, 255, 255)
LIGHT = (230, 230, 230)
DARK = (40, 40, 40)
BLUE = (80, 140, 255)
GREEN = (70, 230, 140)
ACCENT = (255, 170, 50)

# --- IMAGE LOADING ---
script_dir = os.path.dirname(__file__) if "__file__" in locals() else ""

try:
    rock_img = pygame.image.load(os.path.join(script_dir, "rock.png"))
    paper_img = pygame.image.load(os.path.join(script_dir, "paper.png"))
    scissors_img = pygame.image.load(os.path.join(script_dir, "scissors.png"))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

IMAGES = {
    "rock": pygame.transform.scale(rock_img, (180, 180)),
    "paper": pygame.transform.scale(paper_img, (180, 180)),
    "scissors": pygame.transform.scale(scissors_img, (180, 180)),
}

FONT = pygame.font.SysFont("arial", 32, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 24)
TINY_FONT = pygame.font.SysFont("arial", 16)

choices = ["rock", "paper", "scissors"]

# Game States: "MENU", "LOADING", "GAME"
state = "MENU"
game_mode = "endless"  # endless, bo3, bo5, first5

# Scores
wins = 0
losses = 0
draws = 0
series_winner = None

# --- AI ADAPTATION MEMORY ---
# Tracks transitions: after playing choice X, how often does the player play Y?
ai_memory = {
    "rock": {"rock": 0, "paper": 0, "scissors": 0},
    "paper": {"rock": 0, "paper": 0, "scissors": 0},
    "scissors": {"rock": 0, "paper": 0, "scissors": 0}
}
last_player_choice = None


class Button:
    def __init__(self, x, y, w, h, text, action_value=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action_value = action_value

    def draw(self, win):
        mouse = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse) else LIGHT
        pygame.draw.rect(win, color, self.rect, border_radius=12)
        pygame.draw.rect(win, DARK, self.rect, 3, border_radius=12)

        label = SMALL_FONT.render(self.text.upper(), True, DARK)
        text_x = self.rect.x + (self.rect.width - label.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - label.get_height()) // 2
        win.blit(label, (text_x, text_y))

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


# Game Buttons
rock_button = Button(100, 410, 180, 60, "Rock")
paper_button = Button(360, 410, 180, 60, "Paper")
scissors_button = Button(620, 410, 180, 60, "Scissors")

# Menu Buttons
menu_buttons = [
    Button(320, 180, 260, 50, "Endless Mode", "endless"),
    Button(320, 250, 260, 50, "Best of 3", "bo3"),
    Button(320, 320, 260, 50, "Best of 5", "bo5"),
    Button(320, 390, 260, 50, "First to 5 Wins", "first5")
]

player_choice = None
cpu_choice = None
result_text = ""

# Loading Screen Variables
loading_progress = 0
loading_particles = []


def reset_game():
    global wins, losses, draws, player_choice, cpu_choice, result_text, series_winner, state, ai_memory, last_player_choice
    wins = 0
    losses = 0
    draws = 0
    player_choice = None
    cpu_choice = None
    result_text = ""
    series_winner = None
    state = "MENU"
    last_player_choice = None
    # Reset AI Memory
    ai_memory = {
        "rock": {"rock": 0, "paper": 0, "scissors": 0},
        "paper": {"rock": 0, "paper": 0, "scissors": 0},
        "scissors": {"rock": 0, "paper": 0, "scissors": 0}
    }


def get_adaptive_cpu_choice():
    """Predicts player behavior based on history and selects the counter-move."""
    global last_player_choice, ai_memory

    # If it's the first round or no tracking data yet, guess randomly
    if last_player_choice is None:
        return random.choice(choices)

    # Check what the player tends to do after their last move
    history = ai_memory[last_player_choice]
    total_tracked = sum(history.values())

    # If we haven't built enough pattern data yet, fall back to random
    if total_tracked == 0:
        return random.choice(choices)

    # Find what option the player picks most often after their last move
    predicted_player_move = max(history, key=history.get)

    # Counter that predicted move
    counters = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }

    return counters[predicted_player_move]


def update_ai_memory(current_player_choice):
    """Updates patterns based on what the player actually threw."""
    global last_player_choice, ai_memory
    if last_player_choice is not None:
        ai_memory[last_player_choice][current_player_choice] += 1
    last_player_choice = current_player_choice


def determine_winner(player, cpu):
    global wins, losses, draws, series_winner, game_mode

    if player == cpu:
        draws += 1
        return "Draw!"

    if (player == "rock" and cpu == "scissors") or \
            (player == "paper" and cpu == "rock") or \
            (player == "scissors" and cpu == "paper"):
        wins += 1
        res = "You win!"
    else:
        losses += 1
        res = "You lose!"

    # Check Series Win Conditions
    if game_mode == "bo3" and wins == 2:
        series_winner = "Player"
    elif game_mode == "bo3" and losses == 2:
        series_winner = "CPU"
    elif game_mode == "bo5" and wins == 3:
        series_winner = "Player"
    elif game_mode == "bo5" and losses == 3:
        series_winner = "CPU"
    elif game_mode == "first5" and wins == 5:
        series_winner = "Player"
    elif game_mode == "first5" and losses == 5:
        series_winner = "CPU"

    return res


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # Lock to 60 FPS for reliable loading animations
    WIN.fill(WHITE)

    # ----------------------------------------------------
    # STATE: MAIN MENU
    # ----------------------------------------------------
    if state == "MENU":
        title = FONT.render("ROCK PAPER SCISSORS", True, DARK)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        subtitle = SMALL_FONT.render("Select Your Match Type:", True, DARK)
        WIN.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 120))

        for btn in menu_buttons:
            btn.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in menu_buttons:
                    if btn.clicked():
                        game_mode = btn.action_value
                        state = "LOADING"
                        loading_progress = 0
                        loading_particles = []

    # ----------------------------------------------------
    # STATE: LOADING SCREEN (WITH PARTICLES)
    # ----------------------------------------------------
    elif state == "LOADING":
        title = FONT.render("PREPARING ARENA...", True, DARK)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        # Skip Prompt
        skip_tip = TINY_FONT.render("Press SPACEBAR to skip loading", True, GRAY := (130, 130, 130))
        WIN.blit(skip_tip, (WIDTH // 2 - skip_tip.get_width() // 2, HEIGHT - 50))

        # Progress Bar Frame
        bar_x, bar_y, bar_w, bar_h = WIDTH // 4, HEIGHT // 2, WIDTH // 2, 25
        pygame.draw.rect(WIN, LIGHT, (bar_x, bar_y, bar_w, bar_h), border_radius=6)

        # Increment progress dynamically
        loading_progress += 1.5
        if loading_progress > bar_w:
            loading_progress = bar_w
            state = "GAME"

        # Draw Filled Progress
        if loading_progress > 0:
            pygame.draw.rect(WIN, GREEN, (bar_x, bar_y, loading_progress, bar_h), border_radius=6)

        # Particle FX at the tip of the loading bar
        if loading_progress < bar_w and random.random() < 0.4:
            loading_particles.append(
                [bar_x + loading_progress, bar_y + bar_h // 2, random.randint(-2, 2), random.randint(-4, -1),
                 random.randint(3, 6)])

        # Update and draw particles
        for p in loading_particles[:]:
            p[0] += p[2]  # speed x
            p[1] += p[3]  # speed y
            p[4] -= 0.1  # shrink size
            if p[4] <= 0:
                loading_particles.remove(p)
            else:
                pygame.draw.circle(WIN, ACCENT, (int(p[0]), int(p[1])), int(p[4]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Skip feature
                    state = "GAME"

    # ----------------------------------------------------
    # STATE: ACTUAL GAMEPLAY
    # ----------------------------------------------------
    elif state == "GAME":
        # Header Info & Navigation Controls
        mode_labels = {"endless": "Endless Match", "bo3": "Best of 3", "bo5": "Best of 5", "first5": "First to 5"}
        mode_title = FONT.render(f"Mode: {mode_labels[game_mode]}", True, DARK)
        WIN.blit(mode_title, (WIDTH // 2 - mode_title.get_width() // 2, 15))

        reset_tip = TINY_FONT.render("Press 'R' to return to Menu / Reset Score", True, DARK)
        WIN.blit(reset_tip, (15, 15))

        score = SMALL_FONT.render(f"Wins: {wins}   Losses: {losses}   Draws: {draws}", True, DARK)
        WIN.blit(score, (WIDTH // 2 - score.get_width() // 2, 65))

        # Show Results or Series Winner Screen
        if series_winner:
            big_result = FONT.render(f"SERIES OVER! {series_winner.upper()} WINS!", True, ACCENT)
            WIN.blit(big_result, (WIDTH // 2 - big_result.get_width() // 2, 110))
            restart_lbl = SMALL_FONT.render("Press 'R' to return to menu.", True, DARK)
            WIN.blit(restart_lbl, (WIDTH // 2 - restart_lbl.get_width() // 2, 230))
        else:
            # Draw game action buttons if tournament isn't over
            rock_button.draw(WIN)
            paper_button.draw(WIN)
            scissors_button.draw(WIN)

            if result_text:
                result = FONT.render(result_text, True, DARK)
                WIN.blit(result, (WIDTH // 2 - result.get_width() // 2, 110))

        # Show Selected Assets
        if player_choice:
            WIN.blit(IMAGES[player_choice], (150, 150))
        if cpu_choice:
            WIN.blit(IMAGES[cpu_choice], (570, 150))

        WIN.blit(SMALL_FONT.render("You", True, DARK), (220, 340))
        WIN.blit(SMALL_FONT.render("CPU", True, DARK), (640, 340))

        # Event management inside Match Screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Manual reset shortcut
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not series_winner:
                if rock_button.clicked():
                    player_choice = "rock"
                elif paper_button.clicked():
                    player_choice = "paper"
                elif scissors_button.clicked():
                    player_choice = "scissors"
                else:
                    continue

                # Get predictive adaptive move from CPU
                cpu_choice = get_adaptive_cpu_choice()

                # Update memory with what the player just chose
                update_ai_memory(player_choice)

                # Calculate outcome
                result_text = determine_winner(player_choice, cpu_choice)

    pygame.display.update()

pygame.quit()
sys.exit()
