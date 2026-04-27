from typing import Optional
import random
from data import create_player_record, save_players

# Range for random guest number generation

_GUEST_MIN = 1
_GUEST_MAX = 99999

# Special characters accepted during password validation (sign-up only)

_SPECIAL_CHARS = set("!@#$%^&*()_+-=[]{};':\",./<>?")

# ── Guest ──────────────────────────────────────────────────────────────────────

def generate_guest_username(players: dict) -> str:
    """
    Generate a unique guest username of the form guestN, where N is a
    random integer that does not collide with any existing username in
    the current player roster (including previously saved guest accounts).

    Args:
        players: the in-memory players dict (read-only here)

    Returns:
        A unique guest username string, e.g. "guest7391"
    """
    existing = set(players.keys())

    while True:
        number = random.randint(_GUEST_MIN, _GUEST_MAX)
        candidate = f"guest{number}"
        if candidate not in existing:
            return candidate

        
def create_guest(players: dict, guest_username: str) -> dict:
    """
    Create and persist a guest player record, then return it.

    Called the first time a guest accesses the game in a program run.
    The caller (main.py) is responsible for storing the returned record
    and reusing it for the remainder of the session.

    Args:
        players:        the in-memory players dict (modified in place)
        guest_username: the pre-generated guest username for this run

    Returns:
        The newly created guest player record dict.
    """
    record = create_player_record(
        username=guest_username,
        handle="Guest",
        password="password",
    )
    players[guest_username] = record
    save_players(players)
    return record

# ── Login ──────────────────────────────────────────────────────────────────────

def login(players: dict) -> Optional[dict]:
    """
    Prompt the user for credentials and authenticate against the player
    roster. Usernames are matched case-sensitively.

    The user may attempt login as many times as they like, or type
    'back' at the username prompt to return to the main menu.

    Args:
        players: the in-memory players dict (read-only here)

    Returns:
        The authenticated player's record dict on success, or None if
        the user chose to go back to the main menu.
    """
    print("\n── Login ──────────────────────────────")

    while True:
        username = input("Username (or 'back' to return): ").strip()

        if username.lower() == "back":
            return None

        if not username:
            print("  Username cannot be empty. Please try again.")
            continue

        password = input("Password: ").strip()

        if not password:
            print("  Password cannot be empty. Please try again.")
            continue

        # Case-sensitive username lookup
        record = players.get(username)

        if record is None or record["Password"] != password:
            # Deliberately vague — don't reveal whether the username exists
            print("  Incorrect username or password. Please try again.\n")
            continue

        print(f"\n  Welcome back, {record['Handle']}!")
        return record

# ── Sign Up ────────────────────────────────────────────────────────────────────

def signup(players: dict) -> Optional[dict]:
    """
    Walk the user through creating a new account: username, handle, and
    a validated password. On success the new record is added to `players`
    and persisted to CSV.

    The user may type 'back' at the username prompt to abort.

    Args:
        players: the in-memory players dict (modified in place on success)

    Returns:
        The newly created player record dict on success, or None if the
        user chose to go back to the main menu.
    """
    print("\n── Sign Up ─────────────────────────────")

    # ── Step 1: Username ───────────────────────────────────────────────────────
    while True:
        username = input("Choose a username (or 'back' to return): ").strip()

        if username.lower() == "back":
            return None

        if not username:
            print("  Username cannot be empty.")
            continue

        # Reject usernames that are only whitespace (already caught above,
        # but kept explicit for clarity)
        if username != username.strip():
            print("  Username must not start or end with spaces.")
            continue

        # Usernames must not contain spaces (documented design decision)
        if " " in username:
            print("  Username cannot contain spaces.")
            continue

        if username in players:
            print(f"  '{username}' is already taken. Please choose another.")
            continue

        break   # username is valid and unique

    # ── Step 2: Handle ─────────────────────────────────────────────────────────
    while True:
        handle = input("Choose a display name (handle): ").strip()

        if not handle:
            print("  Handle cannot be empty.")
            continue

        break

    # ── Step 3: Password ───────────────────────────────────────────────────────
    while True:
        password = input("Choose a password: ").strip()

        violations = validate_password(password)

        if violations:
            print("  Password does not meet requirements:")
            for v in violations:
                print(f"    • {v}")
            continue

        break   # password passed all checks

    # ── Create and persist the new record ──────────────────────────────────────
    record = create_player_record(username, handle, password)
    players[username] = record
    save_players(players)

    print(f"\n  Account created! Welcome, {handle}!")
    return record

# ── Password Validation ────────────────────────────────────────────────────────

def validate_password(password: str) -> list[str]:
    """
    Check a password string against all sign-up rules.

    This function is intentionally pure — it only reads the password and
    returns results. It does not prompt or print anything, making it
    independently testable.

    Rules checked:
        1. Not empty / not whitespace-only
        2. Minimum 8 characters
        3. At least one uppercase letter (A–Z)
        4. At least one lowercase letter (a–z)
        5. At least one digit (0–9)
        6. At least one special character from _SPECIAL_CHARS

    Args:
        password: the candidate password string

    Returns:
        A list of violation messages. An empty list means the password
        is fully compliant.
    """
    violations = []

    # Rule 1 — not blank or whitespace-only
    if not password or not password.strip():
        violations.append("Password cannot be empty or consist only of spaces.")
        # No point checking further rules on a blank password
        return violations

    # Rule 2 — minimum length
    if len(password) < 8:
        violations.append("Password must be at least 8 characters long.")

    # Rule 3 — uppercase
    if not any(c.isupper() for c in password):
        violations.append("Password must contain at least one uppercase letter (A–Z).")

    # Rule 4 — lowercase
    if not any(c.islower() for c in password):
        violations.append("Password must contain at least one lowercase letter (a–z).")

    # Rule 5 — digit
    if not any(c.isdigit() for c in password):
        violations.append("Password must contain at least one digit (0–9).")

    # Rule 6 — special character
    if not any(c in _SPECIAL_CHARS for c in password):
        violations.append(
            "Password must contain at least one special character "
            "( ! @ # $ % ^ & * ( ) _ + - = [ ] { } ; ' : \" , . < > ? / )."
        )

    return violations