from data import load_players
from auth import generate_guest_username, create_guest, login, signup
from game import play_match
from display import clear, divider, display_banner
 
 
# Main menu 

_MAIN_MENU = """
  What would you like to do?
    1. Play as Guest
    2. Login
    3. Sign Up
    4. Quit
"""
 
_GAME_MENU = """
  What would you like to do?
    1. Play
    2. Logout
"""
 
 
def main() -> None:
    """
    Entry point. Loads player data, generates the session guest username,
    then runs the main menu loop until the user quits.
    """
    # Startup
    players = load_players()
 
    # Generate the guest username once for the entire program run.
    # It is reused any time the user chooses guest access this session.
    session_guest_username = generate_guest_username(players)
    # Track whether the guest record has been created in CSV yet this run
    guest_record = None
 
    clear()
    display_banner()
    print("  Welcome to Rock Paper Scissors!\n")
 
    # Main menu loop
    while True:
        divider()
        print(_MAIN_MENU, end="")
        divider()
 
        choice = input("  Enter 1, 2, 3, or 4: ").strip()
 
        # Guest
        if choice == "1":
            # Reuse the same guest account for the entire session
            if guest_record is None:
                guest_record = create_guest(players, session_guest_username)
 
            clear()
            _game_menu_loop(players, guest_record)
 
        # Login
        elif choice == "2":
            clear()
            player = login(players)
 
            if player is not None:
                clear()
                _game_menu_loop(players, player)
 
        # Sign Up
        elif choice == "3":
            clear()
            player = signup(players)
 
            if player is not None:
                clear()
                _game_menu_loop(players, player)
 
        # Quit
        elif choice == "4":
            clear()
            print("\n  Thanks for playing. See you next time!\n")
            break
 
        # Invalid input
        else:
            print("\n  Invalid choice. Please enter 1, 2, 3, or 4.\n")
 
 
# Game menu (post-authentication)
 
def _game_menu_loop(players: dict, player: dict) -> None:
    """
    Present the in-game menu to an authenticated player. Loops until the
    player chooses to log out, then returns to the main menu.
 
    Args:
        players: the in-memory players dict
        player:  the current player's record dict
    """
    while True:
        divider()
        print(f"  Logged in as: {player['Handle']}  ({player['Username']})")
        print(_GAME_MENU, end="")
        divider()
 
        choice = input("  Enter 1 or 2: ").strip()
 
        if choice == "1":
            clear()
            play_match(players, player)
            clear()
 
        elif choice == "2":
            print(f"\n  Goodbye, {player['Handle']}!\n")
            break
 
        else:
            print("\n  Invalid choice. Please enter 1 or 2.\n")
 
 
# Run
 
if __name__ == "__main__":
    main()
