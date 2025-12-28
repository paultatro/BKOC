# Beginner's Installation Guide

## What You Need

**A ROM file** - This is a digital copy of the Bandit Kings of Ancient China NES game. It's a file that ends with `.nes` (like `BanditKings.nes` or similar).

## Step-by-Step Setup

### Step 1: Find Your ROM File

Your ROM file could be:

**On Windows:**
- In your Downloads folder: `C:\Users\YourName\Downloads\`
- On your Desktop: `C:\Users\YourName\Desktop\`
- In a "ROMs" or "Games" folder you created

**On Mac:**
- In your Downloads folder: `/Users/YourName/Downloads/`
- On your Desktop: `/Users/YourName/Desktop/`
- In a "ROMs" or "Games" folder

**On Linux:**
- In your Downloads: `~/Downloads/`
- On your Desktop: `~/Desktop/`

**The file might be named something like:**
- `Bandit Kings of Ancient China (USA).nes`
- `BanditKings.nes`
- `Suikoden.nes`
- Or something similar ending in `.nes`

### Step 2: Find This Project Folder

This project is located at: `/home/user/BKOC`

**To navigate there:**

**Windows (using File Explorer):**
1. Open File Explorer
2. Type in the address bar: `\\wsl$\Ubuntu\home\user\BKOC`
3. Press Enter

**Mac/Linux (using Terminal):**
```bash
cd /home/user/BKOC
```

**Or using a file browser on Linux:**
1. Open your file manager
2. Navigate to `/home/user/BKOC`

### Step 3: Copy Your ROM File

Now copy your ROM file into the BKOC folder and rename it.

#### Option A: Using Graphical Interface (Easiest)

**Windows:**
1. Find your ROM file (from Step 1)
2. Right-click it → Copy
3. Navigate to `\\wsl$\Ubuntu\home\user\BKOC`
4. Right-click in empty space → Paste
5. Right-click the pasted file → Rename
6. Name it exactly: `bandit_kings_original.nes`

**Mac/Linux:**
1. Find your ROM file
2. Copy it (Cmd+C or Ctrl+C)
3. Navigate to `/home/user/BKOC`
4. Paste it (Cmd+V or Ctrl+V)
5. Rename it to: `bandit_kings_original.nes`

#### Option B: Using Command Line

**If your ROM is in Downloads:**

```bash
# Navigate to the project
cd /home/user/BKOC

# Copy from Downloads (adjust the filename to match yours)
cp ~/Downloads/BanditKings.nes bandit_kings_original.nes

# Or if it has spaces in the name:
cp ~/Downloads/"Bandit Kings of Ancient China (USA).nes" bandit_kings_original.nes
```

**If your ROM is on Desktop:**

```bash
cd /home/user/BKOC
cp ~/Desktop/BanditKings.nes bandit_kings_original.nes
```

**If your ROM is somewhere else:**

```bash
cd /home/user/BKOC
cp /path/to/your/rom/file.nes bandit_kings_original.nes
```

### Step 4: Verify It's in the Right Place

**Using Command Line:**

```bash
cd /home/user/BKOC
ls -lh bandit_kings_original.nes
```

**You should see something like:**
```
-rw-r--r-- 1 user user 256K Dec 28 20:30 bandit_kings_original.nes
```

**Using File Browser:**
1. Open `/home/user/BKOC`
2. You should see a file named `bandit_kings_original.nes`
3. Size should be around 256 KB

### Step 5: Install Python Requirements

**Open a terminal in the BKOC folder:**

```bash
cd /home/user/BKOC
pip3 install -r requirements.txt
```

**Or if pip3 doesn't work, try:**

```bash
pip install -r requirements.txt
```

**Or:**

```bash
python3 -m pip install -r requirements.txt
```

### Step 6: Run the Patcher!

**Easy Mode (Interactive):**

```bash
cd /home/user/BKOC
./quickstart.sh
```

**Or Manual Mode:**

```bash
cd /home/user/BKOC
python3 patch_rom.py --preset balanced
```

### Step 7: Play Your Enhanced ROM!

After patching, you'll have a new file: `bandit_kings_enhanced.nes`

**To play it:**

1. **Download an NES emulator** (if you don't have one):
   - **FCEUX** - [fceux.com](http://fceux.com)
   - **Mesen** - [mesen.ca](https://www.mesen.ca)
   - **RetroArch** - [retroarch.com](https://www.retroarch.com)

2. **Open the emulator**

3. **Load the ROM:**
   - File → Open ROM
   - Navigate to `/home/user/BKOC`
   - Select `bandit_kings_enhanced.nes`
   - Play!

## Troubleshooting

### "File not found" error

**Problem:** The script can't find your ROM file.

**Solution:**

```bash
# Check if the file exists
cd /home/user/BKOC
ls -la

# Look for bandit_kings_original.nes in the list
# If it's not there, go back to Step 3
```

### "Permission denied"

**Solution:**

```bash
# Make scripts executable
chmod +x /home/user/BKOC/patch_rom.py
chmod +x /home/user/BKOC/quickstart.sh
```

### "Python not found"

**Solution:**

Try these commands to see what works:

```bash
python3 --version
python --version
py --version
```

Whichever one works, use that instead of `python3` in the commands.

### ROM file has the wrong name

**Check what your file is actually named:**

```bash
cd /home/user/BKOC
ls *.nes
```

**If you see your ROM but it has a different name, rename it:**

```bash
mv "your-actual-filename.nes" bandit_kings_original.nes
```

### File is in the wrong place

**Where is the file currently?**

```bash
# Search for .nes files
find ~ -name "*.nes" -type f 2>/dev/null
```

This will show you all .nes files. Copy the right one to `/home/user/BKOC`.

## Quick Reference

**Required file location:**
```
/home/user/BKOC/bandit_kings_original.nes
```

**Commands to run (in order):**
```bash
cd /home/user/BKOC
pip3 install -r requirements.txt
python3 patch_rom.py --preset balanced
```

**Output file (to play):**
```
/home/user/BKOC/bandit_kings_enhanced.nes
```

## Still Stuck?

**Check the current directory:**
```bash
pwd
```
Should show: `/home/user/BKOC`

**Check what files are here:**
```bash
ls -la
```
Should include: `patch_rom.py`, `quickstart.sh`, `requirements.txt`, and ideally `bandit_kings_original.nes`

**Test if Python works:**
```bash
python3 --version
```
Should show Python 3.7 or higher.

## Visual Directory Structure

After setup, your folder should look like this:

```
/home/user/BKOC/
├── patch_rom.py                    ← The patcher script
├── quickstart.sh                   ← Easy mode script
├── bandit_kings_original.nes       ← YOUR ROM (you provide this)
├── bandit_kings_enhanced.nes       ← Created after patching
├── tools/                          ← ROM hacking code
├── docs/                           ← Documentation
└── data/                           ← Reference info
```

The key is getting `bandit_kings_original.nes` into the `/home/user/BKOC/` folder!
