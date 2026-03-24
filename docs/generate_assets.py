#!/usr/bin/env python3
"""
Generates NeoGeo brand assets:
- Logo with transparent background (neogeo_logo.png, neogeo_logo_small.png)
- Professional architecture diagram (chart_architektur.png)

All assets use NeoGeo CI colors and are TrailerConnect-free.
"""

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

try:
    from PIL import Image
except ImportError:
    Image = None

BASE = Path(__file__).resolve().parent

# NeoGeo Brand Colors
NG_ORANGE = "#E67E22"
NG_GOLD = "#FFA500"
NG_BLACK = "#0A0A0A"
NG_CHARCOAL = "#212121"
NG_DARK_GRAY = "#424242"
NG_MID_GRAY = "#757575"
NG_LIGHT_GRAY = "#E0E0E0"
NG_OFF_WHITE = "#F5F5F5"
NG_BLUE = "#4A90D9"
NG_GREEN = "#5CB85C"
NG_WHITE = "#FFFFFF"


def fix_logo_background():
    """
    Regenerate NeoGeo logos with transparent/white background.
    If PIL is available, process existing logos. Otherwise generate text-based logos.
    """
    logo_path = BASE / "neogeo_logo.png"
    logo_small_path = BASE / "neogeo_logo_small.png"

    if Image is not None and logo_path.exists():
        # Try to make background transparent
        img = Image.open(logo_path).convert("RGBA")
        data = np.array(img)

        # Replace near-black pixels (background) with transparent
        # Threshold: R<40, G<40, B<40
        mask = (data[:, :, 0] < 40) & (data[:, :, 1] < 40) & (data[:, :, 2] < 40)
        data[mask] = [255, 255, 255, 0]  # transparent

        result = Image.fromarray(data, "RGBA")
        result.save(str(logo_path), "PNG")

        # Also create small version
        small = result.copy()
        small.thumbnail((200, 80), Image.LANCZOS)
        small.save(str(logo_small_path), "PNG")

        print(f"  -> {logo_path} (transparent background)")
        print(f"  -> {logo_small_path} (transparent background)")
        return

    # Fallback: generate text-based logos with matplotlib
    for path, width, height, fontsize in [
        (logo_path, 4, 1.5, 24),
        (logo_small_path, 2.5, 0.8, 14),
    ]:
        fig, ax = plt.subplots(figsize=(width, height))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Orange bar accent
        bar = FancyBboxPatch((0.02, 0.15), 0.06, 0.7,
                             boxstyle="round,pad=0.01",
                             facecolor=NG_ORANGE, edgecolor="none")
        ax.add_patch(bar)

        # Company name
        ax.text(0.15, 0.55, "NeoGeo", fontsize=fontsize, fontweight="bold",
                color=NG_CHARCOAL, va="center", fontfamily="sans-serif")
        ax.text(0.15, 0.2, "New Media", fontsize=fontsize * 0.5,
                color=NG_MID_GRAY, va="center", fontfamily="sans-serif")

        fig.savefig(str(path), dpi=200, bbox_inches="tight",
                    transparent=True, facecolor="none", pad_inches=0.05)
        plt.close(fig)
        print(f"  -> {path} (generated, transparent)")


def create_architecture_diagram():
    """
    Professional, clean system architecture diagram.
    No product names, no TrailerConnect. NeoGeo CI colors.
    Uses a layered approach: Edge -> Connectivity -> Cloud -> Applications -> Users
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ---- Helper: rounded box with shadow effect ----
    def draw_box(x, y, w, h, facecolor, edgecolor, text, textcolor="white",
                 fontsize=8, fontstyle="normal", alpha=1.0):
        shadow = FancyBboxPatch((x + 0.04, y - 0.04), w, h,
                                boxstyle="round,pad=0.15",
                                facecolor="#D0D0D0", edgecolor="none", alpha=0.3,
                                zorder=1)
        ax.add_patch(shadow)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.15",
                             facecolor=facecolor, edgecolor=edgecolor,
                             linewidth=1.5, alpha=alpha, zorder=2)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, text, fontsize=fontsize,
                fontweight="bold", color=textcolor, ha="center", va="center",
                fontstyle=fontstyle, zorder=3)

    def draw_arrow(x1, y1, x2, y2, color=NG_MID_GRAY, style="->", lw=1.5):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw),
                    zorder=4)

    def draw_label(x, y, text, fontsize=7, color=NG_MID_GRAY):
        ax.text(x, y, text, fontsize=fontsize, ha="center", va="center",
                color=color, fontstyle="italic", zorder=5)

    # ================================================================
    # LAYER 1: Trailer / Edge (top) — blue boxes
    # ================================================================
    # Layer background
    layer_bg = FancyBboxPatch((0.3, 6.6), 13.4, 1.6,
                              boxstyle="round,pad=0.15",
                              facecolor="#EDF4FC", edgecolor="#B8D4F0",
                              linewidth=0.8, alpha=0.5, zorder=0)
    ax.add_patch(layer_bg)
    ax.text(0.6, 8.0, "EDGE / TRAILER", fontsize=9, fontweight="bold",
            color=NG_BLUE, va="center", zorder=5)

    sensors = [
        ("Steuergerät\n(CTU)", 1.2),
        ("Reifendruck\n(TPMS)", 3.6),
        ("Bremssystem\n(EBS/ABS)", 6.0),
        ("Türsensorik", 8.4),
        ("Temperatur-\nRecorder", 10.8),
    ]
    for label, x in sensors:
        draw_box(x, 6.8, 1.8, 1.1, NG_BLUE, "#3A7BC8", label,
                 textcolor="white", fontsize=7.5)

    # BLE box (separate)
    draw_box(12.5, 6.8, 1.0, 1.1, "#5CB85C", "#4A9A4A", "BLE\nTracking",
             textcolor="white", fontsize=7)

    # ================================================================
    # CONNECTIVITY (arrow band)
    # ================================================================
    # Gradient-like connectivity band
    conn_bg = FancyBboxPatch((0.3, 5.7), 13.4, 0.7,
                             boxstyle="round,pad=0.1",
                             facecolor=NG_ORANGE, edgecolor="none",
                             alpha=0.12, zorder=0)
    ax.add_patch(conn_bg)

    draw_arrow(7, 6.8, 7, 5.1, color=NG_ORANGE, style="-|>", lw=2.5)
    ax.text(7, 6.05, "LTE / Global Roaming  |  WLAN  |  Bluetooth LE",
            fontsize=8, ha="center", va="center", color=NG_ORANGE,
            fontweight="bold", fontstyle="italic", zorder=5)

    # ================================================================
    # LAYER 2: Cloud Platform (center) — orange
    # ================================================================
    layer_cloud = FancyBboxPatch((0.3, 3.2), 13.4, 2.0,
                                 boxstyle="round,pad=0.15",
                                 facecolor="#FEF5ED", edgecolor="#F0C8A0",
                                 linewidth=0.8, alpha=0.5, zorder=0)
    ax.add_patch(layer_cloud)
    ax.text(0.6, 5.0, "CLOUD-PLATTFORM", fontsize=9, fontweight="bold",
            color=NG_ORANGE, va="center", zorder=5)

    cloud_boxes = [
        ("Azure\nIoT Hub", 1.0, 3.5, 1.8, 1.3, NG_ORANGE, "#CC6600"),
        ("Event\nHubs", 3.3, 3.5, 1.8, 1.3, NG_ORANGE, "#CC6600"),
        ("Data\nExplorer", 5.6, 3.5, 1.8, 1.3, NG_ORANGE, "#CC6600"),
        ("Synapse\nAnalytics", 7.9, 3.5, 1.8, 1.3, NG_ORANGE, "#CC6600"),
        ("Sensor\nMiddleware", 10.2, 3.5, 1.8, 1.3, "#D4740E", "#B05E0A"),
        ("Zero Trust\nSecurity", 12.5, 3.5, 1.2, 1.3, NG_CHARCOAL, NG_BLACK),
    ]
    for label, x, y, w, h, fc, ec in cloud_boxes:
        draw_box(x, y, w, h, fc, ec, label, textcolor="white", fontsize=7.5)

    # Arrows from cloud to services
    for x_pos in [2.5, 7.0, 11.5]:
        draw_arrow(x_pos, 3.5, x_pos, 2.6, color=NG_MID_GRAY, style="-|>", lw=1.5)

    # ================================================================
    # LAYER 3: Applications / Services (bottom)
    # ================================================================
    layer_apps = FancyBboxPatch((0.3, 0.8), 13.4, 1.8,
                                boxstyle="round,pad=0.15",
                                facecolor="#F5F5F5", edgecolor=NG_LIGHT_GRAY,
                                linewidth=0.8, alpha=0.5, zorder=0)
    ax.add_patch(layer_apps)
    ax.text(0.6, 2.4, "APPLIKATIONEN & APIs", fontsize=9, fontweight="bold",
            color=NG_DARK_GRAY, va="center", zorder=5)

    apps = [
        ("Flottenmanagement\nWebportal", 1.0, 1.0, 2.5, 1.2, NG_DARK_GRAY, NG_CHARCOAL),
        ("Mobile Apps\n(Disponent / Fahrer)", 4.0, 1.0, 2.5, 1.2, NG_DARK_GRAY, NG_CHARCOAL),
        ("Data Management\nCenter", 7.0, 1.0, 2.5, 1.2, NG_DARK_GRAY, NG_CHARCOAL),
        ("REST APIs\n(TMS / ERP)", 10.0, 1.0, 2.0, 1.2, NG_DARK_GRAY, NG_CHARCOAL),
        ("SAP\nIntegration", 12.5, 1.0, 1.2, 1.2, NG_DARK_GRAY, NG_CHARCOAL),
    ]
    for label, x, y, w, h, fc, ec in apps:
        draw_box(x, y, w, h, fc, ec, label, textcolor="white", fontsize=7)

    # Title
    ax.text(7, 8.45, "Systemarchitektur — IoT-Telematik-Plattform",
            fontsize=13, fontweight="bold", color=NG_CHARCOAL,
            ha="center", va="center", zorder=5)

    # NeoGeo branding subtle
    ax.text(13.6, 0.25, "NeoGeo", fontsize=7, color=NG_MID_GRAY,
            ha="right", va="center", fontweight="bold", alpha=0.5, zorder=5)

    fig.tight_layout(pad=0.5)
    path = BASE / "chart_architektur.png"
    fig.savefig(str(path), dpi=200, bbox_inches="tight",
                transparent=False, facecolor="white")
    plt.close(fig)
    print(f"  -> {path}")
    return str(path)


def main():
    print("Fixing logo backgrounds...")
    fix_logo_background()

    print("Creating architecture diagram...")
    create_architecture_diagram()

    print("Done!")


if __name__ == "__main__":
    main()
