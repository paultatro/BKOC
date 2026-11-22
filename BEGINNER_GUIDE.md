# Beginner's Guide

## The quick way

A ready-made shuffled ROM (seed 1101) is in your Google Drive Mesen folder as
`Bandit Kings - Shuffle Edition (seed 1101).nes`. Open Mesen, choose File → Open, and pick it. Done.

## Making your own shuffle

1. **Get Python 3.** On Windows, install it from python.org and tick "Add Python to PATH".
2. **Download this project.** On GitHub, click Code → Download ZIP, then unzip it.
3. **Put your ROM in the project folder.** Copy `Bandit Kings of Ancient China (U).nes`
   (the unmodified one, 384 KB) into the unzipped folder.
4. **Open a terminal in that folder.** On Windows, open the folder in Explorer,
   click the address bar, type `cmd`, and press Enter.
5. **Run:**
   ```
   python bkoc_shuffle.py "Bandit Kings of Ancient China (U).nes" my_game.nes --seed 42
   ```
   Change `42` to any number to get a different shuffle. Share the number with a friend
   and they get the exact same game.
6. **Open `my_game.nes` in Mesen.** The file `my_game.spoiler.txt` tells you what changed.
   Don't read it if you want surprises.

## If something goes wrong

- **"ROM is not the canonical … dump"**: your ROM is a different or already-modified copy.
  Use the untouched `Bandit Kings of Ancient China (U).nes`. Some old copies are 393,231 bytes
  and spell "Black Qirlwind"; that bad dump won't work.
- **"python is not recognized"**: reinstall Python with "Add Python to PATH" ticked, or try `py`
  instead of `python`.
- **Old save states**: Mesen save states from the original ROM won't match the shuffled one.
  Start a new game.
