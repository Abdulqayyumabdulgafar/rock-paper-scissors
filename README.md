🪨📄✂️ Rock Paper Scissors

A terminal-based Rock Paper Scissors game built in Python with user authentication, persistent player statistics, and ASCII art.

FEATURES
- **Guest, Login & Sign Up** — play instantly as a guest or create a full account
- **Password Validation** — enforces uppercase, lowercase, digit, and special character rules
- **Persistent Stats** — wins, draws, losses and ratios saved to CSV across sessions
- **ASCII Art** — banner, move displays, and result banners
- **Input Validation** — nothing crashes on bad input

## Project Structure


rock_paper/
├── main.py       # Entry point and menu loop
├── auth.py       # Guest, login, and sign-up logic
├── game.py       # Round and match execution
├── display.py    # All ASCII art and terminal output
├── data.py       # CSV read/write and stats management
└── .gitignore


## How to Run

**Requirements:** Python 3.10 or higher

bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Run the game
python3 main.py
```

`metadata.csv` will be auto-generated on first run — no setup needed.

## How to Play

1. Choose to play as **Guest**, **Login**, or **Sign Up**
2. Select how many rounds to play
3. Pick **Rock**, **Paper**, or **Scissors** each round
4. Your stats are saved automatically after every match

## Password Requirements (Sign Up)

- Minimum 8 characters
- At least one uppercase letter (A–Z)
- At least one lowercase letter (a–z)
- At least one digit (0–9)
- At least one special character (e.g. `!@#$%^&*`)
