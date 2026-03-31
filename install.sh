#!/bin/bash
# B³ Building Analyzer — OpenClaw Install Script
# Usage: curl -sSL https://raw.githubusercontent.com/sgwannabe/b3-building-analyzer/main/install.sh | bash

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/b3-building-analyzer"
REPO_URL="https://github.com/sgwannabe/b3-building-analyzer.git"

echo "🏗️  B³ Building Analyzer — Installing..."

# Check if OpenClaw workspace exists
if [ ! -d "$HOME/.openclaw/workspace" ]; then
    echo "⚠️  OpenClaw workspace not found at ~/.openclaw/workspace"
    echo "   Run 'openclaw onboard' first, then retry."
    exit 1
fi

# Clone or update
if [ -d "$SKILL_DIR" ]; then
    echo "📦  Updating existing installation..."
    cd "$SKILL_DIR" && git pull --ff-only
else
    echo "📦  Cloning into $SKILL_DIR..."
    git clone "$REPO_URL" "$SKILL_DIR"
fi

# Check Python deps
echo "🐍  Checking Python dependencies..."
python3 -c "import pandas" 2>/dev/null || {
    echo "   Installing pandas..."
    pip install pandas --break-system-packages -q 2>/dev/null || pip install pandas -q
}
python3 -c "import matplotlib" 2>/dev/null || {
    echo "   Installing matplotlib..."
    pip install matplotlib --break-system-packages -q 2>/dev/null || pip install matplotlib -q
}

echo ""
echo "✅  B³ Building Analyzer installed!"
echo ""
echo "   Restart OpenClaw to load the skill:"
echo "   $ openclaw gateway restart"
echo ""
echo "   Then try:"
echo "   '이 건물 B³ 분석해줘' + 거래 데이터 첨부"
echo ""
