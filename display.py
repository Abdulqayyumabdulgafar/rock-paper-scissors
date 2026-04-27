import os
# ── Utility ────────────────────────────────────────────────────────────────────
def clear() -> None:
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")
def divider(char: str = "─", width: int = 50) -> None:
    """Print a horizontal divider line."""
    print(char * width)
# ── Program Banner ─────────────────────────────────────────────────────────────
_BANNER = r"""
██████╗  ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝
██████╔╝██║   ██║██║     █████╔╝
██╔══██╗██║   ██║██║     ██╔═██╗
██║  ██║╚██████╔╝╚██████╗██║  ██╗
╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
██████╗  █████╗ ██████╗ ███████╗██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║     ██║  ██║██║     ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
███████╗ ██████╗██╗███████╗███████╗ ██████╗ ██████╗ ███████╗
██╔════╝██╔════╝██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
███████╗██║     ██║███████╗███████╗██║   ██║██████╔╝███████╗
╚════██║██║     ██║╚════██║╚════██║██║   ██║██╔══██╗╚════██║
███████║╚██████╗██║███████║███████║╚██████╔╝██║  ██║███████║
 ╚══════╝ ╚═════╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
"""
def display_banner() -> None:
    """Print the program title ASCII art banner."""
    print(_BANNER)
# ── Move Art ───────────────────────────────────────────────────────────────────
# Each move is stored as a list of lines so they can be printed side-by-side.
_ROCK_LINES = [
    "    _______    ",
    "---'   ____)   ",
          " (_____) ",
    "      (_____)  ",
    "      (____)   ",
    "---.__(___)    ",
]
_PAPER_LINES = [
    "    _______    ",
    "---'   ____)__ ",
    "          ____)",
    "          ___) ",
    "         __)   ",
    "---.__(___)    ",
]

_SCISSORS_LINES = [
    "    _______    ",
    "---'   ____)__ ",
    "          ____)",
    "       __(___) ",
    "   ---(____)   ",
    "      (____)   ",
]
# Map move names to their art lines for easy lookup
_MOVE_ART = {
    "rock":     _ROCK_LINES,
    "paper":    _PAPER_LINES,
    "scissors": _SCISSORS_LINES,
}
# Labels shown above each move column

_MOVE_LABELS = {
    "rock":     "  ✊ ROCK   ",
    "paper":    "  ✋ PAPER  ",
    "scissors": "  ✌️ SCISSORS ",
}

def display_moves(player_move: str, computer_move: str) -> None:
    """
    Print both the player's and the computer's chosen moves side by side
    using ASCII art, with a 'VS' column in the middle.
    Args:
        player_move:   one of 'rock', 'paper', 'scissors' (lowercase)
        computer_move: one of 'rock', 'paper', 'scissors' (lowercase)
    """
    player_lines   = _MOVE_ART[player_move]
    computer_lines = _MOVE_ART[computer_move]
    # VS column — vertically centred on the middle row
    vs_column = ["      "] * len(player_lines)
    mid = len(player_lines) // 2
    vs_column[mid] = " VS  "
    print()
    print(f"  YOU: {_MOVE_LABELS[player_move]}")
    divider()
    print(f"  CPU: {_MOVE_LABELS[computer_move]}")
    print()
    for p_line, vs, c_line in zip(player_lines, vs_column, computer_lines):
        print(f"  {p_line}  {vs}  {c_line}")
    print()
# ── Round Result Banners ───────────────────────────────────────────────────────
_WIN_BANNER = r"""
 __  __ ____  _   _  __        _____ _   _
|  \/  |  _ \| | | | \ \      / /_ _| \ | |
| |\/| | |_) | | | |  \ \ /\ / / | ||  \| |
| |  | |  _ <| |_| |   \ V  V /  | || |\  |
|_|  |_|_| \_\\___/     \_/\_/  |___|_| \_|
"""
 
_DRAW_BANNER = r"""
 ____  ____      ___        __
|  _ \|  _ \    / \ \      / /
| | | | |_) |  / _ \ \ /\ / /
| |_| |  _ <  / ___ \ V  V /
|____/|_| \_\/_/   \_\_/\_/
"""
 
_LOSS_BANNER = r"""
 __  __ ____  _   _   _     ___  ____  _____
|  \/  |  _ \| | | | | |   / _ \/ ___|| ____|
| |\/| | |_) | |_| | | |  | | | \___ \|  _|
| |  | |  _ <|  _  | | |__| |_| |___) | |___
|_|  |_|_| \_\_| |_| |_____\___/|____/|_____|
"""

def display_result(result: str) -> None:
    """
    Print the ASCII art result banner for a single round outcome.
    Args:
        result: 'win', 'draw', or 'loss' (lowercase)
    """
    if result == "win":
        print(_WIN_BANNER)
    elif result == "draw":
        print(_DRAW_BANNER)
    else:
        print(_LOSS_BANNER)
# ── Match Summary ──────────────────────────────────────────────────────────────
_MATCH_WIN_BANNER = r"""
 __  __ _____ ____    __  ____     ____  ___  ____  ____  _____
|  \/  |  ___/ ___|  / / | __ )   / ___|/ _ \|  _ \|  _ \| ____|
| |\/| | |_  \___ \ / /  |  _ \  | |  _| | | | | | | | | |  _|
| |  | |  _|  ___) / /   | |_) | | |_| | |_| | |_| | |_| | |___
|_|  |_|_|   |____/_/    |____/   \____|\___/|____/|____/|_____|
"""
 
_MATCH_LOSS_BANNER = r"""
 __  __ _____ ____    __  ____     _     ___  ____ _____ _
|  \/  |  ___/ ___|  / / | __ )   | |   / _ \/ ___|_   _| |
| |\/| | |_  \___ \ / /  |  _ \   | |  | | | \___ \ | | | |
| |  | |  _|  ___) / /   | |_) |  | |__| |_| |___) || | |_|
|_|  |_|_|   |____/_/    |____/   |_____\___/|____/ |_| (_)
"""
 
_MATCH_DRAW_BANNER = r"""
 __  __ _____ ____    __  _____ _____ ____
|  \/  |  ___/ ___|  / / |_   _|_ _| ____| |
| |\/| | |_  \___ \ / /    | |  | ||  _|    |
| |  | |  _|  ___) / /     | |  | || |___   |
|_|  |_|_|   |____/_/      |_| |___|_____|  |
"""

def display_match_summary(handle: str, wins: int, draws: int,
                           losses: int, rounds: int, match_result: str) -> None:
    """
    Print the final match result screen with ASCII art and full scoreboard.
Args:
    handle:
player's display name
rounds the player won this match
rounds drawn this match
rounds the player lost this match
total rounds played this match
wins:
draws:
losses:
rounds:
match_result: 'win', 'draw', or 'loss' (overall match outcome)
    """
    print()
    divider("═")
    print("  MATCH OVER")
    divider("═")
    if match_result == "win":
        print(_MATCH_WIN_BANNER)
    elif match_result == "loss":
        print(_MATCH_LOSS_BANNER)
    else:
        print(_MATCH_DRAW_BANNER)
    divider()
    print(f"  Player : {handle}")
    print(f"  Rounds : {rounds}")
    print(f"  Wins   : {wins}")
    print(f"  Draws  : {draws}")
    print(f"  Losses : {losses}")
    divider()
    print()
# ── Running Score ──────────────────────────────────────────────────────────────
def display_score(handle: str, wins: int, draws: int,
                  losses: int, rounds_left: int) -> None:
    """
    Print the running tally after each round.
 
    Args:
        handle:      player's display name
        wins:        rounds won so far this match
        draws:       rounds drawn so far this match
        losses:      rounds lost so far this match
        rounds_left: rounds still to be played
    """
    divider("·")
    print(f"  {handle}  |  W: {wins}  D: {draws}  L: {losses}  |  Rounds left: {rounds_left}")
    divider("·")
    print()