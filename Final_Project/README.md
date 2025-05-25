# Late for Lecture

Late for Lecture is a fast-paced side-scrolling runner game where you play as Professor Ishac or Professor Chitizadeh
who’s running late to COMP9001 Lecture. You’ve lost track of time, and now you must sprint across campus, dodging swooping magpies 
and students while dealing with unpredictable rainstorms with drifting umbrellas.

Make it to class before the clock hits 5:00 PM, or you're officially late for lecture.

## Features
- Character selection screen with animated previews
- Rain system with fade-in and fade-out transitions
- Animated umbrella hazards that appear only during storms
- Students wandering the path as moving obstacles
- Dynamic difficulty that increases game speed based on your score
- Birds that flap and change vertical position as they pass
- High score tracking

## How to Play
You're a professor on a mission to make it to class on time.
Run forward, jump over obstacles, and survive as long as you can.

Avoid:
- Birds flying across the screen
- Umbrellas drifting in during rain
- Students wandering across the path

If you hit any obstacle, you're late! You then must make the decision to quit and cancel lecture, or start over and keep running.

## Controls
Spacebar – Jump

C – Choose your character

Any Key – Start the game (after character selection)

ESC – Quit the game during the Game Over screen

# Installation Instructions
## 1. Clone (or Download) the Repository

```
git clone https://github.com/clairecropper/Final_Project.git
```
```
cd Final_Project
```

## 2. Create a Virtual Environment (recommended)

```
python -m venv .venv
```

## 3. Activate the Virtual Environment

On Windows:
```
.venv\Scripts\activate
```

On macOS/Linux:

```
source .venv/bin/activate
```

## 4. Install Requirements

```
pip install -r requirements.txt
```

The only required dependency is pygame, but the requirements.txt ensures version consistency in development.

## 5. Run the Game

python game.py
