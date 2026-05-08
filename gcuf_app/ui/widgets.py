"""Shared UI widget helpers and constants."""
import math
import tkinter as tk
import customtkinter as ctk

# ── Color Palette ────────────────────────────────────────────────────────────
BG       = "#0a0b0f"
SURFACE  = "#111318"
SURFACE2 = "#181b23"
BORDER   = "#22262f"
ACCENT   = "#4f8ef7"
ACCENT2  = "#a78bfa"
ACCENT3  = "#34d399"
WARN     = "#fb923c"
DANGER   = "#f87171"
TEXT     = "#e8eaf0"
MUTED    = "#6b7280"
SIDEBAR_W = 220


def configure_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


def sidebar_button(parent, text, icon="", command=None, active=False):
    bg = ACCENT + "22" if active else "transparent"
    fg = TEXT if active else MUTED
    btn = ctk.CTkButton(
        parent,
        text=f"  {icon}  {text}" if icon else f"   {text}",
        fg_color=bg,
        text_color=fg,
        hover_color=SURFACE2,
        anchor="w",
        corner_radius=8,
        height=40,
        font=ctk.CTkFont(family="Courier", size=13, weight="bold" if active else "normal"),
        command=command,
    )
    return btn


def section_label(parent, text):
    return ctk.CTkLabel(
        parent, text=text.upper(),
        text_color=MUTED,
        font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
    )


def card_frame(parent, **kwargs):
    return ctk.CTkFrame(parent, fg_color=SURFACE, border_color=BORDER,
                        border_width=1, corner_radius=12, **kwargs)


def accent_button(parent, text, command=None, color=ACCENT, width=120):
    return ctk.CTkButton(
        parent, text=text,
        fg_color=color, hover_color=color + "cc",
        text_color="white", corner_radius=8,
        font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
        command=command, width=width,
    )


def danger_button(parent, text, command=None):
    return accent_button(parent, text, command=command, color=DANGER)


def input_field(parent, placeholder="", width=200, **kwargs):
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        fg_color=SURFACE2, border_color=BORDER,
        text_color=TEXT, placeholder_text_color=MUTED,
        width=width, corner_radius=8,
        font=ctk.CTkFont(family="Courier", size=12),
        **kwargs,
    )


def heading(parent, text, size=18):
    return ctk.CTkLabel(
        parent, text=text, text_color=TEXT,
        font=ctk.CTkFont(family="Courier", size=size, weight="bold"),
    )


def muted_label(parent, text, size=11):
    return ctk.CTkLabel(
        parent, text=text, text_color=MUTED,
        font=ctk.CTkFont(family="Courier", size=size),
    )


def stat_card(parent, title, value, color=ACCENT):
    frame = card_frame(parent)
    ctk.CTkLabel(frame, text=title.upper(), text_color=MUTED,
                 font=ctk.CTkFont(family="Courier", size=9, weight="bold")).pack(anchor="w", padx=14, pady=(12,0))
    ctk.CTkLabel(frame, text=str(value), text_color=color,
                 font=ctk.CTkFont(family="Courier", size=22, weight="bold")).pack(anchor="w", padx=14, pady=(2,12))
    return frame


# ── GPA Semicircle Gauge ─────────────────────────────────────────────────────

def draw_gpa_gauge(canvas: tk.Canvas, cx: int, cy: int, r: int, gpa: float,
                   max_gpa: float = 4.0):
    """Draw a semicircle GPA gauge on a tk.Canvas."""
    canvas.delete("gauge")

    # Background arc (180° semicircle, left to right, bottom flat)
    # tkinter arc: start=0 is 3 o'clock, goes counter-clockwise
    # We want a bottom semicircle: start=180 (9 o'clock), extent=180
    start_angle = 180
    extent = 180

    # Track
    canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                      start=start_angle, extent=extent,
                      outline=BORDER, width=10, style=tk.ARC, tags="gauge")

    # Colored fill
    ratio = min(max(gpa / max_gpa, 0), 1)
    sweep = ratio * extent
    color = _gpa_arc_color(gpa)
    if sweep > 0:
        canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                          start=start_angle, extent=sweep,
                          outline=color, width=10, style=tk.ARC, tags="gauge")

    # Needle
    needle_angle_deg = 180 + ratio * 180  # 180° (left) to 360°/0° (right)
    needle_angle_rad = math.radians(needle_angle_deg)
    nx = cx + (r - 4) * math.cos(needle_angle_rad)
    ny = cy - (r - 4) * math.sin(needle_angle_rad)
    canvas.create_line(cx, cy, nx, ny, fill=color, width=3, capstyle=tk.ROUND, tags="gauge")
    canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=SURFACE2, outline=color, width=2, tags="gauge")

    # Labels
    canvas.create_text(cx - r - 4, cy + 6, text="0.0", fill=MUTED,
                       font=("Courier", 8), tags="gauge")
    canvas.create_text(cx + r + 4, cy + 6, text="4.0", fill=MUTED,
                       font=("Courier", 8), tags="gauge")

    # Center value
    canvas.create_text(cx, cy - 14, text=f"{gpa:.2f}",
                       fill=color, font=("Courier", 18, "bold"), tags="gauge")
    canvas.create_text(cx, cy + 4, text="CGPA",
                       fill=MUTED, font=("Courier", 9), tags="gauge")


def _gpa_arc_color(gpa: float) -> str:
    if gpa >= 3.5:
        return ACCENT3
    elif gpa >= 3.0:
        return ACCENT
    elif gpa >= 2.5:
        return ACCENT2
    elif gpa >= 2.0:
        return WARN
    else:
        return DANGER
