import csv
import os

# Path to the CSV file - lives in the same directory as this script
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata.csv")

# Column headers in the exact order required by the spec
CSV_HEADERS = [
    "Username",
    "Handle",
    "Password",
    "Total Rounds",
    "Total Wins",
    "Total Draws",
    "Total Losses",
    "Wins per Round",
    "Draws per Round",
    "Losses per Round",
]

def load_players() -> dict:
    """
    Read all player records from metadata.csv into memory.

    Returns a dictionary keyed by username (lowercase for case-insensitive
    lookups), where each value is a dict of that player's fields.

    If the CSV does not exist, it is created with headers only, and an
    empty dict is returned.

    If the CSV exists but is empty or contains only a header row, an
    empty dict is returned without crashing.
    """
    # Create the file with headers if it doesn't exist yet
    if not os.path.exists(CSV_PATH):
        _initialise_csv()
        return {}

    players = {}

    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Guard: if the file is completely blank, DictReader fieldnames
            # will be None and iteration will yield nothing — that's fine.
            for row in reader:
                username = row["Username"]
                if not username:          # skip any accidental blank rows
                    continue

                # Cast numeric fields from strings back to appropriate types
                players[username] = {
                    "Username":         username,
                    "Handle":           row["Handle"],
                    "Password":         row["Password"],
                    "Total Rounds":     int(row["Total Rounds"]),
                    "Total Wins":       int(row["Total Wins"]),
                    "Total Draws":      int(row["Total Draws"]),
                    "Total Losses":     int(row["Total Losses"]),
                    "Wins per Round":   float(row["Wins per Round"]),
                    "Draws per Round":  float(row["Draws per Round"]),
                    "Losses per Round": float(row["Losses per Round"]),
                }
    except (KeyError, ValueError):
        # Corrupted or structurally wrong CSV — treat as empty rather than crash
        print("[Warning] metadata.csv appears corrupted. Starting with no records.")
        return {}

    return players

def save_players(players: dict) -> None:
    """
    Write the full in-memory player dictionary back to metadata.csv.

    Overwrites the file completely each time to keep the on-disk state
    consistent with memory. Never truncates data — the entire dict is
    always written.

    Args:
        players: dict mapping username -> player record dict
    """
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for player in players.values():
            writer.writerow({
                "Username":         player["Username"],
                "Handle":           player["Handle"],
                "Password":         player["Password"],
                "Total Rounds":     player["Total Rounds"],
                "Total Wins":       player["Total Wins"],
                "Total Draws":      player["Total Draws"],
                "Total Losses":     player["Total Losses"],
                "Wins per Round":   player["Wins per Round"],
                "Draws per Round":  player["Draws per Round"],
                "Losses per Round": player["Losses per Round"],
            })

def update_stats(players: dict, username: str, rounds: int, wins: int,
                 draws: int, losses: int) -> None:
    """
    Add a match’s results to a player’s cumulative statistics, then
    recalculate the per-round ratios and persist everything to CSV.

    Args:
        players:  the in-memory players dict (modified in place)
        username: the player whose record to update
        rounds:   number of rounds played in this match
        wins:     rounds the player won
        draws:    rounds that ended in a draw
        losses:   rounds the player lost
    """
    record = players[username]

    # Accumulate totals
    record["Total Rounds"] += rounds
    record["Total Wins"]   += wins
    record["Total Draws"]  += draws
    record["Total Losses"] += losses

    # Recalculate ratios — guard against division by zero
    total = record["Total Rounds"]
    if total > 0:
        record["Wins per Round"]   = round(record["Total Wins"]   / total, 4)
        record["Draws per Round"]  = round(record["Total Draws"]  / total, 4)
        record["Losses per Round"] = round(record["Total Losses"] / total, 4)
    else:
        record["Wins per Round"]   = 0.0
        record["Draws per Round"]  = 0.0
        record["Losses per Round"] = 0.0

    # Persist the updated state to disk
    save_players(players)

def create_player_record(username: str, handle: str, password: str) -> dict:
    """
    Build and return a fresh player record with all stats initialised to 0.

    Does NOT add it to any dict or write to CSV — the caller is
    responsible for inserting the record and calling save_players().

    Args:
        username: unique identifier
        handle:   display name shown during gameplay
        password: plaintext password

    Returns:
        A dict with all CSV fields populated and numeric fields set to 0.
    """
    return {
        "Username":         username,
        "Handle":           handle,
        "Password":         password,
        "Total Rounds":     0,
        "Total Wins":       0,
        "Total Draws":      0,
        "Total Losses":     0,
        "Wins per Round":   0.0,
        "Draws per Round":  0.0,
        "Losses per Round": 0.0,
    }

# ── Private helpers ────────────────────────────────────────────────────────────

def _initialise_csv() -> None:
    """Create metadata.csv with headers only. Called when the file is absent."""
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()