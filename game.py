from typing import Optional
import random
from data import update_stats
from display import (
    clear,
    divider,
    display_moves,
    display_result,
    display_score,
    display_match_summary,
)
 
# Constants
 
# Valid moves and their display labels
_MOVES = ["rock", "paper", "scissors"]
 
_MOVE_MENU = """
  Choose your move:
    1. ✊  Rock
    2. 🖐  Paper
    3. ✌️  Scissors
"""
 
# Outcome lookup: _OUTCOMES[player][computer] -> 'win' | 'draw' | 'loss'
_OUTCOMES = {
    "rock":     {"rock": "draw", "paper": "loss", "scissors": "win"},
    "paper":    {"rock": "win",  "paper": "draw", "scissors": "loss"},
    "scissors": {"rock": "loss", "paper": "win",  "scissors": "draw"},
}
 
 
# Public entry point
 
def play_match(players: dict, player: dict) -> None:
    """
    Run a full match for the given player: prompt for round count, loop
    through rounds, show the summary, and persist updated stats.
 
    Args:
        players: the in-memory players dict (passed to update_stats)
        player:  the current player's record dict
    """
    rounds = _prompt_round_count()
    if rounds is None:
        return  # user backed out
 
    # Match-level accumulators
    wins   = 0
    draws  = 0
    losses = 0
 
    for round_num in range(1, rounds + 1):
        clear()
        divider("═")
        print(f"  ROUND {round_num} of {rounds}  —  {player['Handle']}")
        divider("═")
 
        result = play_round()
 
        # Accumulate
        if result == "win":
            wins += 1
        elif result == "draw":
            draws += 1
        else:
            losses += 1
 
        display_result(result)
        display_score(player["Handle"], wins, draws, losses,
                      rounds_left=rounds - round_num)
 
        # Pause between rounds so the player can read the result
        if round_num < rounds:
            input("  Press Enter for the next round...")
 
    # Match conclusion
    clear()
 
    if wins > losses:
        match_result = "win"
    elif losses > wins:
        match_result = "loss"
    else:
        match_result = "draw"
 
    display_match_summary(
        handle=player["Handle"],
        wins=wins,
        draws=draws,
        losses=losses,
        rounds=rounds,
        match_result=match_result,
    )
 
    # Persist updated statistics
    update_stats(players, player["Username"], rounds, wins, draws, losses)
 
    # Also update the local record so the in-memory object stays consistent
    # (update_stats mutates players[username], which IS player if passed by ref,
    # but we keep this explicit for clarity)
    player["Total Rounds"] += rounds
    player["Total Wins"]   += wins
    player["Total Draws"]  += draws
    player["Total Losses"] += losses
 
    input("  Press Enter to return to the menu...")
 
 
# Round execution
 
def play_round() -> str:
    """
    Execute a single round: prompt the player for a move, generate the
    computer's move, display both, and return the outcome.
 
    Returns:
        'win', 'draw', or 'loss' from the player's perspective.
    """
    player_move   = _prompt_move()
    computer_move = random.choice(_MOVES)
 
    clear()
    display_moves(player_move, computer_move)
 
    result = _determine_outcome(player_move, computer_move)
    return result
 
 
# Input helpers
 
def _prompt_round_count() ->    Optional[int]:
    """
    Ask the player how many rounds to play. Accepts only positive integers.
    The player may type 'back' to abort and return to the main menu.
 
    Returns:
        A positive integer, or None if the user typed 'back'.
    """
    print()
    while True:
        raw = input("  How many rounds would you like to play? (or 'back'): ").strip()
 
        if raw.lower() == "back":
            return None
 
        if not raw:
            print("  Please enter a number.")
            continue
 
        # Reject non-integer input (e.g. "five", "2.5")
        if not raw.lstrip("-").isdigit():
            print("  That's not a valid number. Please enter a positive whole number.")
            continue
 
        value = int(raw)
 
        if value <= 0:
            print("  Number of rounds must be greater than zero.")
            continue
 
        return value
 
 
def _prompt_move() -> str:
    """
    Display the move menu and return the player's validated choice.
 
    Accepts option numbers 1–3 only. Loops until a valid choice is made.
 
    Returns:
        One of 'rock', 'paper', 'scissors' (lowercase).
    """
    print(_MOVE_MENU)
 
    while True:
        raw = input("  Enter 1, 2, or 3: ").strip()
 
        if raw == "1":
            return "rock"
        elif raw == "2":
            return "paper"
        elif raw == "3":
            return "scissors"
        else:
            print("  Invalid choice. Please enter 1, 2, or 3.")
 
 
# Game logic
 
def _determine_outcome(player_move: str, computer_move: str) -> str:
    """
    Determine the round outcome using standard RPS rules.
 
    Args:
        player_move:   one of 'rock', 'paper', 'scissors'
        computer_move: one of 'rock', 'paper', 'scissors'
 
    Returns:
        'win', 'draw', or 'loss' from the player's perspective.
    """
    return _OUTCOMES[player_move][computer_move]
