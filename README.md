# Wizard101 Card Duel Game

A Wizard101-inspired card duel game built for local 2-player pass-and-play. Battle as **Pyromancer Bob** (Fire school) vs **Necromancer Alice** (Death school)!

## How to Set Up and Play

### Step 1: Install Python

You need Python installed on your computer. Check if you already have it by opening your terminal (Mac/Linux) or Command Prompt (Windows) and typing:

```
python3 --version
```

If you see a version number (like `Python 3.10.0`), you're good — skip to Step 2.

If not, download Python from [python.org/downloads](https://www.python.org/downloads/) and install it. During installation on Windows, **make sure to check "Add Python to PATH"**.

### Step 2: Install Flask

In your terminal / Command Prompt, run:

```
pip3 install flask
```

(If `pip3` doesn't work, try `pip install flask` instead.)

### Step 3: Download the Game

If you haven't already, download or clone this repository:

```
git clone https://github.com/abhiz123/wiz101.git
```

Or just download the ZIP from GitHub and unzip it.

### Step 4: Run the Game

Open your terminal, navigate to the game folder, and start the server:

```
cd wiz101
python3 app.py
```

(If `python3` doesn't work, try `python app.py` instead.)

You should see output like:

```
 * Running on http://0.0.0.0:5001
```

### Step 5: Play!

Open your web browser (Chrome, Firefox, Safari, etc.) and go to:

```
http://localhost:5001
```

The game board will load with both players visible.

## How to Play

1. **Draw Pip** — Click "Draw Pip" to start your turn. This draws a pip (your casting resource) and a card (if your hand has room).
2. **Cast a Spell** — Click on a lit-up card in your hand to cast it. Greyed-out cards can't be played (not enough pips). Choose your target in the popup.
3. **Pass Turn** — Click "Pass Turn" to end your turn and let the other player go.
4. **Reset Match** — Click "Reset Match" to start a new game.

### Pip Types

- 🔥 / 💀 **School Pips** — Worth 2 pips for your school's spells
- **PP (Power Pips)** — Worth 2 pips for your own school, 1 for others
- **N (Normal Pips)** — Worth 1 pip
- **Sh (Shadow Pips)** — Used for Shadow spells only
- **Fz (Fizzle)** — A dud pip, still counts as 1
- ★ **(Critical)** — Worth 1 pip

### Card Types

- **Damage Spells** — Deal flat damage to the opponent
- **DoT Spells** — Deal initial damage + damage over multiple rounds
- **Blades** — Consume all your pips to store bonus damage for your next attack (+X per pip consumed)
- **Traps** — Placed on the opponent, consume your pips to store bonus damage (+X per pip consumed)
- **Shields** — Block a flat amount of damage from the next attack
- **Heals** — Restore health

### Tips

- Save up pips before casting a blade or trap — the bonus scales with how many pips you have!
- Shields block a flat amount of damage, so use them against big attacks.
- Feint is powerful (+300 trap on opponent) but places a +100 backlash trap on yourself.
- Critical hits (lucky rolls) double your damage or healing!

## Stopping the Game

Press `Ctrl + C` in your terminal to stop the server.
