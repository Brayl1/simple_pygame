# 🎮 Monster Catcher

A **Python GUI monster-catching game** built with **Tkinter** and **Pillow**. The project focuses on meaningful use of Python **lists and nested lists** to manage monsters, inventory, captured monsters, encounter history, sorting, searching, and gameplay updates.

Players take the role of a trainer, encounter randomly selected monsters, use Capture Orbs and Rare Candy, build a collection, earn points based on monster rarity, and try to capture enough monsters to win.

---

## ✨ Features

- Pixel-art graphical interface using **Tkinter**
- Animated title screen with trainer name entry
- 9 unique monsters with different rarities, abilities, and capture difficulties
- Random monster encounters
- Capture system based on a random roll from **1 to 10**
- Capture Orbs used as limited attempts
- Rare Candy that reduces a monster's capture difficulty
- Scoring based on monster rarity
- Monster collection screen
- Search captured monsters by name
- Sort captured monsters alphabetically
- Rarity breakdown of captured monsters
- Encounter history showing captured, escaped, and skipped monsters
- Trainer ranking system
- Responsive/resizable GUI screens
- Pixel-art monster images and backgrounds

---

## 🎯 Objective

Capture at least **4 monsters** before you run out of Capture Orbs or available encounters.

The game starts with:

- **5 Capture Orbs**
- **3 Rare Candies**
- **9 possible monster encounters**

A Rare Candy reduces the current monster's difficulty by **3**, with a minimum difficulty of **1**.

---

## 👾 Monsters

| Monster | Difficulty | Rarity | Ability |
|---|---:|---|---|
| Leafling | 3 | Common | Vine Whip |
| Flameling | 4 | Common | Fire Blast |
| Aquafin | 5 | Uncommon | Water Splash |
| Voltwing | 6 | Uncommon | Thunder Strike |
| Rockhorn | 7 | Rare | Stone Crash |
| Shadowfang | 9 | Legendary | Dark Bite |
| Sandcoil | 4 | Common | Sand Toss |
| Frostail | 6 | Uncommon | Ice Shard |
| Stormtail | 10 | Epic | Thunder Storm |

---

## 🎲 Capture System

When the player presses **CAPTURE**, the program generates a random number from **1 to 10**.

A monster is captured when:

```text
random roll >= monster difficulty
```

Example:

```text
Monster Difficulty: 6
Random Roll: 8
Result: CAPTURED
```

If the roll is lower than the difficulty, the monster escapes.

### Approximate base capture chances

| Difficulty | Successful Rolls | Capture Chance |
|---:|---|---:|
| 3 | 3–10 | 80% |
| 4 | 4–10 | 70% |
| 5 | 5–10 | 60% |
| 6 | 6–10 | 50% |
| 7 | 7–10 | 40% |
| 9 | 9–10 | 20% |
| 10 | 10 | 10% |

Using a Rare Candy improves the chance of capture by lowering the monster's difficulty.

---

## 🏆 Scoring System

Points are awarded when a monster is successfully captured.

| Rarity | Points |
|---|---:|
| Common | 10 |
| Uncommon | 20 |
| Rare | 30 |
| Legendary | 50 |
| Epic | 70 |

### Trainer Ranks

| Score | Rank |
|---:|---|
| 0–49 | Bronze Trainer |
| 50–99 | Silver Trainer |
| 100–149 | Gold Trainer |
| 150+ | Platinum Trainer |

---

## 🎮 How to Play

1. Run the game.
2. Enter your trainer name on the title screen.
3. Click **START GAME**.
4. A random monster will appear.
5. Choose one of the available actions:
   - **CAPTURE** — uses one Capture Orb and attempts to catch the monster.
   - **USE RARE CANDY** — lowers the current monster's difficulty by 3.
   - **SKIP** — skips the current monster without using an Orb.
   - **COLLECTION** — opens your captured-monster collection.
   - **HISTORY** — shows the result of previous encounters.
6. Continue until you run out of encounters or Capture Orbs.
7. Capture at least **4 monsters** to win.

---

## 📋 Python List Requirements Demonstrated

This project uses lists as an important part of the actual gameplay instead of simply declaring unused lists.

### Main gameplay lists

```python
self.inventory = ["Capture Orb"] * STARTING_ORBS
self.candies = ["Rare Candy"] * STARTING_CANDY
self.captured_monsters = []
self.encounter_history = []
self.encounters = [row.copy() for row in MONSTER_TEMPLATES]
```

### Nested list monster data

Each monster is stored as:

```python
[Name, Difficulty, Rarity, Ability]
```

Example:

```python
["Leafling", 3, "Common", "Vine Whip"]
```

### List operations used during gameplay

The game demonstrates:

- **Traversal** using `for` loops
- **Indexing** such as `monster[0]`, `monster[1]`, and `monster[2]`
- **Updating** list elements when Rare Candy changes difficulty
- **append()** for captured monsters and encounter history
- **pop()** for Capture Orbs and Rare Candy
- **remove()** for completed encounters
- **sort()** for alphabetical collection sorting
- **count()** for rarity statistics
- **Searching** through captured monsters by name
- **Nested lists** for monster records and encounter history

---

## 📁 Project Structure

```text
monster_catcher_project_g3/
│
├── main.py
├── app.py
├── game_state.py
├── constants.py
├── monsters_data.py
├── sprites.py
├── PressStart2P-Regular.ttf
├── README.md
│
├── assets/
│   ├── bg.png
│   ├── bg2.png
│   ├── bg3.png
│   ├── bg4.png
│   ├── bg5.png
│   ├── mscreen.gif
│   │
│   └── monsters/
│       ├── m1.png
│       ├── m2.png
│       ├── m3.png
│       ├── m4.png
│       ├── m5.png
│       ├── m6.png
│       ├── m7.png
│       ├── m8.png
│       └── m9.png
│
└── screens/
    ├── __init__.py
    ├── title_screen.py
    ├── game_screen.py
    ├── collection_screen.py
    ├── history_screen.py
    └── end_screen.py
```

---

## 🧩 Main Files

| File | Purpose |
|---|---|
| `main.py` | Starts the Tkinter application |
| `app.py` | Controls screen navigation and owns the game state |
| `game_state.py` | Contains the gameplay logic, lists, capture system, scoring, and game rules |
| `constants.py` | Stores game-wide settings, scores, colors, and starting values |
| `monsters_data.py` | Stores the master nested list of monster data |
| `sprites.py` | Loads and displays the monster pixel-art images |
| `screens/title_screen.py` | Title screen and trainer-name input |
| `screens/game_screen.py` | Main monster encounter/gameplay screen |
| `screens/collection_screen.py` | Captured-monster collection, search, sort, and rarity breakdown |
| `screens/history_screen.py` | Encounter history screen |
| `screens/end_screen.py` | Final results, score, rank, replay, collection, and exit screen |

---

## 🛠️ Requirements

- **Python 3.10+** recommended
- **Tkinter**
- **Pillow**

Tkinter is normally included with the standard Windows Python installation.

Install Pillow with:

```bash
pip install pillow
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Brayl1/simple_pygame.git
```

### 2. Open the project folder

```bash
cd simple_pygame
```

### 3. Install Pillow

```bash
pip install pillow
```

### 4. Start the game

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

> Run `main.py` from the project root so the game can correctly locate the files inside the `assets/` folder.

---

## 🖼️ Assets

The game uses custom pixel-style backgrounds, an animated title-screen GIF, and individual PNG sprites for each monster. Images are loaded through Pillow, and monster sprites use nearest-neighbor resizing to preserve the pixel-art appearance.

---

## 🧠 Program Design

The project separates **game logic** from the **graphical interface**:

- `GameState` handles the data and gameplay rules.
- Screen modules handle the Tkinter interface.
- `App` acts as the controller between the game state and screens.
- `monsters_data.py` stores monster data separately from the game logic.
- `sprites.py` handles monster image loading and rendering.

This structure makes the project easier to understand, maintain, and expand with additional monsters, items, screens, or game mechanics.

---

## 🚀 Possible Future Improvements

- Add different types of Capture Orbs
- Add monster health and battles
- Add more monsters and rarity tiers
- Add sound effects and background music
- Save and load player progress
- Add monster evolution or leveling
- Add achievements
- Add a leaderboard
- Add keyboard controls

---

## 📚 Course Project

This project was developed as a Python programming activity focused on redesigning a game so that **lists and nested lists control meaningful gameplay data** such as monsters, inventory, collection, and game history.

---

## 📄 License

This project is intended for educational purposes.
