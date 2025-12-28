#!/bin/bash
# Quick start script for Bandit Kings ROM enhancement

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Bandit Kings of Ancient China - Quick Start             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if original ROM exists
if [ ! -f "bandit_kings_original.nes" ]; then
    echo "❌ ERROR: Original ROM not found!"
    echo ""
    echo "Please place your ROM file as: bandit_kings_original.nes"
    echo ""
    echo "Expected MD5: a0c8f6e2d8b4c3e1f9a7b5c2d3e4f5a6"
    echo ""
    exit 1
fi

echo "ROM file found! ✓"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi

echo "Python 3 found! ✓"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt -q

echo ""
echo "Choose your enhancement preset:"
echo ""
echo "  1) CHAOS    - Maximum randomization, wild gameplay"
echo "  2) BALANCED - Moderate changes, improved balance"
echo "  3) ENHANCED - Subtle improvements, original feel"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        preset="chaos"
        ;;
    2)
        preset="balanced"
        ;;
    3)
        preset="enhanced"
        ;;
    *)
        echo "Invalid choice. Using BALANCED."
        preset="balanced"
        ;;
esac

echo ""
echo "🎲 Generating random seed..."
seed=$RANDOM

echo "🔧 Patching ROM with $preset preset (seed: $seed)..."
echo ""

python3 patch_rom.py --preset $preset --seed $seed

echo ""
echo "✓ Done! Load bandit_kings_enhanced.nes in your NES emulator!"
echo ""
echo "Seed used: $seed (save this to recreate the same ROM later)"
echo ""
