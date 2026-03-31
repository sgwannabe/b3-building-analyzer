#!/usr/bin/env python3
"""
B³ Building Analyzer — Instagram Carousel Generator
Generates 1080x1080 square images optimized for Instagram posts.

Usage: python generate_instagram.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

os.makedirs('./output/instagram', exist_ok=True)

# ─── Design Tokens ───
BG = '#0D1B2A'
BG_CARD = '#1B2838'
GOLD = '#C9A84C'
WHITE = '#F0F0F0'
LIGHT = '#A0B0C0'
BLUE = '#4A90D9'
GREEN = '#5CB85C'
RED = '#D9534F'
ORANGE = '#F0AD4E'

DPI = 216  # 1080px / 5in = 216 dpi
SIZE = (5, 5)  # 5x5 inches at 216dpi = 1080x1080

def setup_slide(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    # YRE branding footer
    ax.text(50, 2.5, 'YRE  ·  B³ Building Analysis  ·  yeonyc.com', 
            ha='center', va='center', fontsize=6.5, color=LIGHT, alpha=0.5,
            fontfamily='sans-serif')

# ═══════════════════════════════════════════
# SLIDE 1: Cover / Hero
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

# Gold accent line
ax.plot([15, 85], [62, 62], color=GOLD, linewidth=2.5)

# Title
ax.text(50, 78, '45 CHRISTOPHER ST', ha='center', va='center',
        fontsize=22, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.text(50, 71, 'WEST VILLAGE  ·  MANHATTAN', ha='center', va='center',
        fontsize=10, color=GOLD, fontfamily='sans-serif')

# Score box
box = FancyBboxPatch((28, 38), 44, 20, boxstyle="round,pad=2", 
                      facecolor=BG_CARD, edgecolor=GOLD, linewidth=1.5)
ax.add_patch(box)
ax.text(50, 52, 'B³ COMPOSITE', ha='center', va='center',
        fontsize=9, color=LIGHT, fontfamily='sans-serif')
ax.text(50, 44, '81.15', ha='center', va='center',
        fontsize=32, fontweight='bold', color=GOLD, fontfamily='sans-serif')

# Classification badge
badge = FancyBboxPatch((25, 24), 50, 10, boxstyle="round,pad=1.5",
                        facecolor=GOLD, edgecolor='none')
ax.add_patch(badge)
ax.text(50, 29, 'CORE / DEFENSIVE', ha='center', va='center',
        fontsize=12, fontweight='bold', color=BG, fontfamily='sans-serif')

# Building specs
ax.text(50, 16, 'Pre-war Condo (1931)  ·  112 Units  ·  17 Floors',
        ha='center', va='center', fontsize=8, color=LIGHT, fontfamily='sans-serif')

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_1_cover.png', dpi=DPI, facecolor=BG)
plt.close()

# ═══════════════════════════════════════════
# SLIDE 2: B³ Scores Breakdown
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

ax.text(50, 90, 'B³ SCORE BREAKDOWN', ha='center', va='center',
        fontsize=16, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.plot([20, 80], [85, 85], color=GOLD, linewidth=1.5)

metrics = [
    ('LIQUIDITY', 85, '47-day median DOM', BLUE),
    ('RENT CAPTURE', 92, '$100–$123/SF', GREEN),
    ('APPRECIATION', 68, 'E-line 4.8% CAGR', ORANGE),
]

for i, (name, score, detail, color) in enumerate(metrics):
    y = 68 - i * 22
    
    # Label
    ax.text(15, y + 5, name, ha='left', va='center',
            fontsize=11, fontweight='bold', color=WHITE, fontfamily='sans-serif')
    ax.text(85, y + 5, f'{score}/100', ha='right', va='center',
            fontsize=14, fontweight='bold', color=color, fontfamily='sans-serif')
    
    # Bar background
    bar_bg = FancyBboxPatch((15, y - 3), 70, 5, boxstyle="round,pad=0.5",
                             facecolor=BG_CARD, edgecolor='none')
    ax.add_patch(bar_bg)
    
    # Bar fill
    bar_width = score / 100 * 70
    bar_fill = FancyBboxPatch((15, y - 3), bar_width, 5, boxstyle="round,pad=0.5",
                               facecolor=color, edgecolor='none', alpha=0.85)
    ax.add_patch(bar_fill)
    
    # Detail
    ax.text(15, y - 7, detail, ha='left', va='center',
            fontsize=8, color=LIGHT, fontfamily='sans-serif')

# Composite at bottom
box = FancyBboxPatch((20, 6), 60, 12, boxstyle="round,pad=1.5",
                      facecolor=BG_CARD, edgecolor=GOLD, linewidth=1.5)
ax.add_patch(box)
ax.text(50, 12, 'COMPOSITE: 81.15  →  Core / Defensive',
        ha='center', va='center', fontsize=10, fontweight='bold', color=GOLD, fontfamily='sans-serif')

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_2_scores.png', dpi=DPI, facecolor=BG)
plt.close()

# ═══════════════════════════════════════════
# SLIDE 3: Thesis / Key Insight
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

ax.text(50, 90, 'INVESTMENT THESIS', ha='center', va='center',
        fontsize=16, fontweight='bold', color=GOLD, fontfamily='sans-serif')
ax.plot([20, 80], [85, 85], color=GOLD, linewidth=1.5)

# Three converging metrics
facts = [
    ('▲', 'Rent +40%', 'in 2–3 years'),
    ('●', '47-day DOM', 'median time to sell'),
    ('★', 'New highs', '2024–25 PPSF records'),
]

for i, (emoji, headline, sub) in enumerate(facts):
    y = 70 - i * 15
    ax.text(20, y, emoji, ha='center', va='center', fontsize=16)
    ax.text(30, y + 1, headline, ha='left', va='center',
            fontsize=13, fontweight='bold', color=WHITE, fontfamily='sans-serif')
    ax.text(30, y - 4, sub, ha='left', va='center',
            fontsize=9, color=LIGHT, fontfamily='sans-serif')

# Arrow converging
ax.text(50, 30, '↓', ha='center', va='center', fontsize=20, color=GOLD)

# Thesis box
thesis_box = FancyBboxPatch((8, 8), 84, 18, boxstyle="round,pad=2",
                             facecolor=BG_CARD, edgecolor=GOLD, linewidth=1.5)
ax.add_patch(thesis_box)
ax.text(50, 20, '"INCOME FORTRESS"', ha='center', va='center',
        fontsize=14, fontweight='bold', color=GOLD, fontfamily='sans-serif')
ax.text(50, 13, 'Elite yield + rapid exit optionality\nIdeal for risk-averse wealth preservation',
        ha='center', va='center', fontsize=8.5, color=LIGHT, fontfamily='sans-serif', linespacing=1.6)

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_3_thesis.png', dpi=DPI, facecolor=BG)
plt.close()

# ═══════════════════════════════════════════
# SLIDE 4: Line Performance (Alpha vs Avoid)
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

ax.text(50, 90, 'LINE PERFORMANCE', ha='center', va='center',
        fontsize=16, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.plot([20, 80], [85, 85], color=GOLD, linewidth=1.5)

# Alpha section
alpha_box = FancyBboxPatch((8, 48), 84, 32, boxstyle="round,pad=2",
                            facecolor='#0a2a0a', edgecolor=GREEN, linewidth=1.2)
ax.add_patch(alpha_box)
ax.text(15, 75, 'ALPHA LINE', ha='left', va='center',
        fontsize=10, fontweight='bold', color=GREEN, fontfamily='sans-serif')
ax.text(15, 68, 'E-Line (2BR)', ha='left', va='center',
        fontsize=14, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.text(15, 62, '4.8% CAGR  ·  Unit 8E: +22% in 4yr', ha='left', va='center',
        fontsize=9, color=LIGHT, fontfamily='sans-serif')
ax.text(15, 56, 'Consistently outperforms building average', ha='left', va='center',
        fontsize=8, color=LIGHT, fontfamily='sans-serif', alpha=0.7)

# Avoid section
avoid_box = FancyBboxPatch((8, 10), 84, 32, boxstyle="round,pad=2",
                            facecolor='#2a0a0a', edgecolor=RED, linewidth=1.2)
ax.add_patch(avoid_box)
ax.text(15, 37, 'AVOID', ha='left', va='center',
        fontsize=10, fontweight='bold', color=RED, fontfamily='sans-serif')
ax.text(15, 30, 'B-Line (2BR)', ha='left', va='center',
        fontsize=14, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.text(15, 24, '1.5% CAGR  ·  Unit 10B: 8yr for +13.5%', ha='left', va='center',
        fontsize=9, color=LIGHT, fontfamily='sans-serif')
ax.text(15, 18, 'Trails NYXRCSA benchmark — barely beats inflation', ha='left', va='center',
        fontsize=8, color=LIGHT, fontfamily='sans-serif', alpha=0.7)

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_4_lines.png', dpi=DPI, facecolor=BG)
plt.close()

# ═══════════════════════════════════════════
# SLIDE 5: Rent Growth Story
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

ax.text(50, 92, 'RENT GROWTH', ha='center', va='center',
        fontsize=16, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.plot([20, 80], [87, 87], color=GOLD, linewidth=1.5)

# Unit 8D
box1 = FancyBboxPatch((8, 52), 84, 30, boxstyle="round,pad=2",
                        facecolor=BG_CARD, edgecolor='none')
ax.add_patch(box1)
ax.text(15, 77, 'UNIT 8D  ·  STUDIO', ha='left', va='center',
        fontsize=9, fontweight='bold', color=GOLD, fontfamily='sans-serif')
ax.text(15, 70, '$3,495', ha='left', va='center',
        fontsize=16, color=LIGHT, fontfamily='sans-serif')
ax.text(42, 70, '→', ha='center', va='center', fontsize=16, color=GOLD)
ax.text(52, 70, '$4,800', ha='left', va='center',
        fontsize=16, fontweight='bold', color=GREEN, fontfamily='sans-serif')
ax.text(15, 62, 'Mar 2021 → Jun 2024', ha='left', va='center',
        fontsize=8, color=LIGHT, fontfamily='sans-serif')
ax.text(85, 62, '+37%', ha='right', va='center',
        fontsize=16, fontweight='bold', color=GREEN, fontfamily='sans-serif')
# Bar
bar_bg1 = FancyBboxPatch((15, 56), 70, 3, boxstyle="round,pad=0.3",
                           facecolor='#1a3a1a', edgecolor='none')
ax.add_patch(bar_bg1)
bar_fill1 = FancyBboxPatch((15, 56), 70 * 0.37, 3, boxstyle="round,pad=0.3",
                             facecolor=GREEN, edgecolor='none')
ax.add_patch(bar_fill1)

# Unit 2F
box2 = FancyBboxPatch((8, 16), 84, 30, boxstyle="round,pad=2",
                        facecolor=BG_CARD, edgecolor='none')
ax.add_patch(box2)
ax.text(15, 41, 'UNIT 2F  ·  1-BED', ha='left', va='center',
        fontsize=9, fontweight='bold', color=GOLD, fontfamily='sans-serif')
ax.text(15, 34, '$5,000', ha='left', va='center',
        fontsize=16, color=LIGHT, fontfamily='sans-serif')
ax.text(42, 34, '→', ha='center', va='center', fontsize=16, color=GOLD)
ax.text(52, 34, '$7,000', ha='left', va='center',
        fontsize=16, fontweight='bold', color=GREEN, fontfamily='sans-serif')
ax.text(15, 26, 'Sep 2021 → Nov 2023', ha='left', va='center',
        fontsize=8, color=LIGHT, fontfamily='sans-serif')
ax.text(85, 26, '+40%', ha='right', va='center',
        fontsize=16, fontweight='bold', color=GREEN, fontfamily='sans-serif')
bar_bg2 = FancyBboxPatch((15, 20), 70, 3, boxstyle="round,pad=0.3",
                           facecolor='#1a3a1a', edgecolor='none')
ax.add_patch(bar_bg2)
bar_fill2 = FancyBboxPatch((15, 20), 70 * 0.40, 3, boxstyle="round,pad=0.3",
                             facecolor=GREEN, edgecolor='none')
ax.add_patch(bar_fill2)

# Bottom note
ax.text(50, 9, 'Post-COVID rental boom driving cap rate improvement',
        ha='center', va='center', fontsize=8, color=LIGHT, fontfamily='sans-serif', alpha=0.7)

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_5_rent.png', dpi=DPI, facecolor=BG)
plt.close()

# ═══════════════════════════════════════════
# SLIDE 6: CTA / Summary
# ═══════════════════════════════════════════
fig, ax = plt.subplots(figsize=SIZE)
setup_slide(fig, ax)

ax.text(50, 85, '45 CHRISTOPHER ST', ha='center', va='center',
        fontsize=18, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.text(50, 79, 'West Village  ·  B³ Score: 81.15', ha='center', va='center',
        fontsize=10, color=GOLD, fontfamily='sans-serif')
ax.plot([20, 80], [74, 74], color=GOLD, linewidth=1.5)

# Key stats grid
stats_data = [
    ('85', 'Liquidity'),
    ('92', 'Rent Capture'),
    ('68', 'Appreciation'),
    ('47d', 'Median DOM'),
    ('$123', 'Top Rent/SF'),
    ('4.8%', 'Best CAGR'),
]

for i, (val, label) in enumerate(stats_data):
    col = i % 3
    row = i // 3
    x = 20 + col * 27
    y = 60 - row * 22
    
    stat_box = FancyBboxPatch((x - 10, y - 8), 22, 18, boxstyle="round,pad=1",
                               facecolor=BG_CARD, edgecolor='#2a3a4a', linewidth=0.8)
    ax.add_patch(stat_box)
    ax.text(x + 1, y + 4, val, ha='center', va='center',
            fontsize=14, fontweight='bold', color=GOLD, fontfamily='sans-serif')
    ax.text(x + 1, y - 3, label, ha='center', va='center',
            fontsize=7, color=LIGHT, fontfamily='sans-serif')

# CTA
cta_box = FancyBboxPatch((15, 6), 70, 12, boxstyle="round,pad=1.5",
                          facecolor=GOLD, edgecolor='none')
ax.add_patch(cta_box)
ax.text(50, 12, 'Full analysis at blog.yeonyc.com', ha='center', va='center',
        fontsize=10, fontweight='bold', color=BG, fontfamily='sans-serif')

plt.tight_layout(pad=0.5)
plt.savefig('./output/instagram/slide_6_cta.png', dpi=DPI, facecolor=BG)
plt.close()

print("✅ 6 Instagram carousel slides generated:")
for i in range(1, 7):
    names = ['cover', 'scores', 'thesis', 'lines', 'rent', 'cta']
    path = f'./output/instagram/slide_{i}_{names[i-1]}.png'
    size = os.path.getsize(path) // 1024
    print(f"   Slide {i}: slide_{i}_{names[i-1]}.png ({size}KB)")
