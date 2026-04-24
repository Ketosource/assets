#!/usr/bin/env python3
"""Generate Ketosource Value Chain v17 diagram."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Brand colors (from v16)
DARK_PURPLE  = '#60269E'
LIGHT_PURPLE = '#C8A4EC'   # section header pill backgrounds
LIGHTEST_PUR = '#EDE0FF'   # container backgrounds
WHITE        = '#FFFFFF'
GREEN        = '#1B6B3A'

W, H = 1930, 1310

fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=100)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor(WHITE)


def rrect(x, y, w, h, fc, ec=None, lw=1.5, dashed=False, r=10, zorder=2):
    """Rounded rectangle.  x, y = bottom-left corner."""
    rr = min(r, w / 2 - 0.1, h / 2 - 0.1)
    patch = mpatches.FancyBboxPatch(
        (x + rr, y + rr), w - 2 * rr, h - 2 * rr,
        boxstyle=f"round,pad={rr}",
        facecolor=fc,
        edgecolor=ec or 'none',
        linewidth=lw,
        zorder=zorder,
    )
    if dashed:
        patch.set_linestyle((0, (6, 4)))
    ax.add_patch(patch)


def txt(x, y, s, fs=11, fc=WHITE, ha='center', va='center', rot=0):
    ax.text(x, y, s, fontsize=fs, color=fc, fontweight='bold',
            ha=ha, va=va, rotation=rot, zorder=10, multialignment='center')


def arrow(x1, x2, y, lw=2.5, head=15):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=DARK_PURPLE,
                                lw=lw, mutation_scale=head))


# ── Layout constants ──────────────────────────────────────────────────────────
PAD = 30   # outer page margin
IP  = 12   # inner padding within containers
GAP = 22   # vertical gap between the three main sections

L  = PAD
R  = W - PAD
FW = R - L          # full usable width = 1870

STRAT_H = 195
SUPP_H  = 370
MID_H   = H - 2 * PAD - STRAT_H - SUPP_H - 2 * GAP   # 1310-60-195-370-44 = 641

SUPP_Y  = PAD                           #   30
MID_Y   = SUPP_Y + SUPP_H + GAP        #  422
STRAT_Y = MID_Y  + MID_H  + GAP        # 1085


# ════════════════════════════════════════════════════════════════════════════
# 1. STRATEGY (top band)
# ════════════════════════════════════════════════════════════════════════════
rrect(L, STRAT_Y, FW, STRAT_H, fc=LIGHTEST_PUR, ec=DARK_PURPLE, lw=2,
      dashed=True, r=14)

# Header pill
SH  = 52
SHY = STRAT_Y + STRAT_H - IP - SH
rrect(L + IP, SHY, FW - 2 * IP, SH, fc=DARK_PURPLE, r=8)
txt(L + FW / 2, SHY + SH / 2, "1. Strategy", fs=18)

# Sub-pills: Vision | Ketosource O/S
sub_h = SHY - STRAT_Y - 2 * IP
sub_y = STRAT_Y + IP
sub_w = (FW - 3 * IP) / 2

rrect(L + IP,           sub_y, sub_w, sub_h, fc=DARK_PURPLE, r=8)
txt(L + IP + sub_w / 2, sub_y + sub_h / 2, "Vision", fs=14)

rrect(L + 2 * IP + sub_w, sub_y, sub_w, sub_h, fc=DARK_PURPLE, r=8)
txt(L + 2 * IP + sub_w + sub_w / 2, sub_y + sub_h / 2, "Ketosource O/S", fs=14)


# ════════════════════════════════════════════════════════════════════════════
# 2-4. MIDDLE: Solutions → Ops → Experience  + Customer
# ════════════════════════════════════════════════════════════════════════════
CUST_W    = 185   # customer box width
ARROW_GAP = 48    # space (incl. arrow) between Experience right edge and Customer
VC_W      = FW - CUST_W - ARROW_GAP   # width for three value-chain columns = 1637

COL_GAP = 52
COL_W   = (VC_W - 2 * COL_GAP) / 3   # ≈ 511

cols = [
    {
        "label": "2. Solutions",
        "items": ["R&D\nCode / Data", "R&D\nKnowledge", "R&D Nutrition\nProducts"],
    },
    {
        "label": "3. Ops",
        "items": ["Production\nSourcing", "Production", "Logistics &\nTrade", "Fulfilment"],
    },
    {
        "label": "4. Experience",
        "items": ["Marketing", "Community\nExperience", "Distribution\nPartners"],
    },
]

HDR_H = 50

for i, col in enumerate(cols):
    cx = L + i * (COL_W + COL_GAP)

    # Outer container
    rrect(cx, MID_Y, COL_W, MID_H, fc=LIGHTEST_PUR, ec=DARK_PURPLE,
          lw=1.5, dashed=True, r=10)

    # Column header (light purple, dark text)
    hdr_y = MID_Y + MID_H - IP - HDR_H
    rrect(cx + IP, hdr_y, COL_W - 2 * IP, HDR_H, fc=LIGHT_PURPLE, r=7)
    txt(cx + COL_W / 2, hdr_y + HDR_H / 2, col["label"], fs=13, fc=DARK_PURPLE)

    # Sub-item pills
    items  = col["items"]
    n      = len(items)
    avail  = hdr_y - MID_Y - 2 * IP
    ig     = 9
    ih     = (avail - (n - 1) * ig) / n

    for j, item in enumerate(items):
        # j=0 at top (just below header), j=n-1 at bottom
        iy = hdr_y - IP - (j + 1) * ih - j * ig
        rrect(cx + IP, iy, COL_W - 2 * IP, ih, fc=DARK_PURPLE, r=7)
        txt(cx + COL_W / 2, iy + ih / 2, item, fs=10)

    # Arrow to next column — centred in the gap, prominent
    if i < len(cols) - 1:
        arrow(cx + COL_W + 5, cx + COL_W + COL_GAP - 5, MID_Y + MID_H / 2,
              lw=3, head=22)

# Arrow from Experience column to Customer
exp_right = L + 2 * (COL_W + COL_GAP) + COL_W
cust_x    = L + VC_W + ARROW_GAP
arrow(exp_right + 3, cust_x - 3, MID_Y + MID_H / 2, lw=3.5, head=20)

# Customer box (green — external)
CUST_H  = 135
cust_y  = MID_Y + MID_H / 2 - CUST_H / 2
rrect(cust_x, cust_y, CUST_W, CUST_H, fc=GREEN, r=10)
txt(cust_x + CUST_W / 2, MID_Y + MID_H / 2, "Customer", fs=14)


# ════════════════════════════════════════════════════════════════════════════
# 5-6. BOTTOM: Support (outer) containing Foundation (inner)
# ════════════════════════════════════════════════════════════════════════════
# Support outer container
rrect(L, SUPP_Y, FW, SUPP_H, fc=LIGHTEST_PUR, ec=DARK_PURPLE, lw=2,
      dashed=True, r=14)

# Support header at top of section
SUPP_HDR_H = 48
supp_hdr_y = SUPP_Y + SUPP_H - IP - SUPP_HDR_H
rrect(L + IP, supp_hdr_y, FW - 2 * IP, SUPP_HDR_H, fc=DARK_PURPLE, r=8)
txt(L + FW / 2, supp_hdr_y + SUPP_HDR_H / 2, "6. Support", fs=16)

# Foundation inner container (nested at bottom of Support)
FOUND_H = 145
found_y = SUPP_Y + IP
found_w = FW - 2 * IP
rrect(L + IP, found_y, found_w, FOUND_H, fc=LIGHTEST_PUR, ec=DARK_PURPLE,
      lw=1.5, dashed=True, r=9)

# Foundation header
FOUND_HDR_H = 40
found_hdr_y = found_y + FOUND_H - IP - FOUND_HDR_H
rrect(L + 2 * IP, found_hdr_y, found_w - 2 * IP, FOUND_HDR_H, fc=LIGHT_PURPLE, r=6)
txt(L + IP + found_w / 2, found_hdr_y + FOUND_HDR_H / 2,
    "5. Foundation", fs=13, fc=DARK_PURPLE)

# Foundation sub-items (horizontal)
found_items = ["Resourcing", "Accounting & Finance", "Legal"]
n_fi   = len(found_items)
fi_gap = 10
fi_w   = (found_w - 2 * IP - (n_fi - 1) * fi_gap) / n_fi
fi_h   = found_hdr_y - found_y - 2 * IP
fi_y   = found_y + IP

for k, item in enumerate(found_items):
    fx = L + 2 * IP + k * (fi_w + fi_gap)
    rrect(fx, fi_y, fi_w, fi_h, fc=DARK_PURPLE, r=6)
    txt(fx + fi_w / 2, fi_y + fi_h / 2, item, fs=12)

# Support activity bars (between Foundation top and Support header bottom)
supp_acts_bot = found_y + FOUND_H + 8
supp_acts_top = supp_hdr_y - 8
supp_acts_h   = supp_acts_top - supp_acts_bot

supp_acts = ["Core Sourcing", "Core Execution", "TECH"]
n_sa  = len(supp_acts)
sa_ig = 8
sa_h  = (supp_acts_h - (n_sa - 1) * sa_ig) / n_sa

for k, act in enumerate(supp_acts):
    # k=0 at top (just below Support header), k=n-1 at bottom
    say = supp_acts_top - (k + 1) * sa_h - k * sa_ig
    rrect(L + IP, say, FW - 2 * IP, sa_h, fc=DARK_PURPLE, r=6)
    txt(L + FW / 2, say + sa_h / 2, act, fs=13)


# ── Save ──────────────────────────────────────────────────────────────────────
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(
    'diagrams/ketosource-value-chain-v17.png',
    dpi=100,
    bbox_inches=None,
    facecolor=WHITE,
)
plt.close()
print("Saved: diagrams/ketosource-value-chain-v17.png")
