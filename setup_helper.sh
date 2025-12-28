#!/bin/bash
# Setup helper script - Checks your installation and guides you through setup

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Bandit Kings ROM Patcher - Setup Helper              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "patch_rom.py" ]; then
    echo "❌ ERROR: Not in the correct directory!"
    echo ""
    echo "Please run this from the BKOC folder:"
    echo "  cd /home/user/BKOC"
    echo "  ./setup_helper.sh"
    exit 1
fi

echo "✓ In correct directory: $(pwd)"
echo ""

# Check for Python
echo "Checking for Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ Found: $PYTHON_VERSION"
    echo "  (Note: Use 'python' instead of 'python3' in commands)"
else
    echo "❌ Python not found!"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Mac: brew install python3"
    echo "  Windows: Download from python.org"
    exit 1
fi
echo ""

# Check for pip
echo "Checking for pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3 found"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✓ pip found"
    PIP_CMD="pip"
else
    echo "❌ pip not found!"
    echo "Try: sudo apt install python3-pip"
    exit 1
fi
echo ""

# Check for ROM file
echo "Checking for ROM file..."
if [ -f "bandit_kings_original.nes" ]; then
    ROM_SIZE=$(ls -lh bandit_kings_original.nes | awk '{print $5}')
    echo "✓ ROM file found! (Size: $ROM_SIZE)"
    echo ""

    # Offer to install dependencies and run
    echo "Ready to patch! Would you like to:"
    echo "  1) Install dependencies and patch now"
    echo "  2) Just install dependencies"
    echo "  3) Exit (I'll do it manually)"
    echo ""
    read -p "Choose (1-3): " choice

    case $choice in
        1)
            echo ""
            echo "Installing dependencies..."
            $PIP_CMD install -r requirements.txt
            echo ""
            echo "Dependencies installed! Running quick start..."
            ./quickstart.sh
            ;;
        2)
            echo ""
            echo "Installing dependencies..."
            $PIP_CMD install -r requirements.txt
            echo ""
            echo "✓ Done! Now run: ./quickstart.sh"
            ;;
        *)
            echo ""
            echo "OK! When ready, run:"
            echo "  $PIP_CMD install -r requirements.txt"
            echo "  ./quickstart.sh"
            ;;
    esac
else
    echo "❌ ROM file NOT found!"
    echo ""
    echo "I'm looking for: bandit_kings_original.nes"
    echo "In this directory: $(pwd)"
    echo ""

    # Check if there are any .nes files
    NES_FILES=$(ls *.nes 2>/dev/null)
    if [ ! -z "$NES_FILES" ]; then
        echo "I found these .nes files:"
        ls -lh *.nes
        echo ""
        echo "If one of these is Bandit Kings, rename it:"
        echo "  mv \"filename.nes\" bandit_kings_original.nes"
    else
        echo "No .nes files found in this directory."
        echo ""
        echo "WHERE IS YOUR ROM FILE?"
        echo ""
        echo "Let me help you find it..."
        echo ""

        # Search common locations
        echo "Searching Downloads folder..."
        DOWNLOADS_ROMS=$(find ~/Downloads -name "*.nes" -type f 2>/dev/null | head -5)
        if [ ! -z "$DOWNLOADS_ROMS" ]; then
            echo "Found .nes files in Downloads:"
            echo "$DOWNLOADS_ROMS"
            echo ""
        fi

        echo "Searching Desktop..."
        DESKTOP_ROMS=$(find ~/Desktop -name "*.nes" -type f 2>/dev/null | head -5)
        if [ ! -z "$DESKTOP_ROMS" ]; then
            echo "Found .nes files on Desktop:"
            echo "$DESKTOP_ROMS"
            echo ""
        fi

        echo "════════════════════════════════════════════════════════"
        echo ""
        echo "TO FIX THIS:"
        echo ""
        echo "Option 1 - Copy from Downloads:"
        echo "  cp ~/Downloads/YourROM.nes bandit_kings_original.nes"
        echo ""
        echo "Option 2 - Copy from Desktop:"
        echo "  cp ~/Desktop/YourROM.nes bandit_kings_original.nes"
        echo ""
        echo "Option 3 - Copy from anywhere:"
        echo "  cp /full/path/to/your/rom.nes bandit_kings_original.nes"
        echo ""
        echo "Replace 'YourROM.nes' with your actual filename!"
        echo ""
        echo "Need help getting a ROM legally? Read: ROM_ACQUISITION.md"
        echo ""
    fi
fi
