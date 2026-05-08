import tkinter as tk
import customtkinter as ctk
from ui.widgets import *
import database as db


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, on_login):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.on_login = on_login
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center box
        box = ctk.CTkFrame(self, fg_color=SURFACE, border_color=BORDER,
                           border_width=1, corner_radius=16, width=420)
        box.grid(row=0, column=0)
        box.grid_propagate(False)
        box.configure(width=420, height=520)

        # Top accent line
        accent_bar = tk.Canvas(box, height=3, bg=BG, highlightthickness=0, width=420)
        accent_bar.pack(fill="x")
        accent_bar.create_rectangle(0, 0, 420, 3, fill=ACCENT, outline="")

        # Logo / Title
        ctk.CTkLabel(box, text="GCUF", text_color=ACCENT,
                     font=ctk.CTkFont(family="Courier", size=38, weight="bold")).pack(pady=(30, 0))
        ctk.CTkLabel(box, text="Result Management System",
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold")).pack()
        ctk.CTkLabel(box, text="Gov. College University Faisalabad",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=10)).pack(pady=(2, 28))

        # Badge
        badge = ctk.CTkLabel(box, text="● SECURE PORTAL",
                             text_color=ACCENT,
                             fg_color="#4f8ef722",
                             corner_radius=20,
                             font=ctk.CTkFont(family="Courier", size=9, weight="bold"))
        badge.pack(pady=(0, 24))

        # Fields
        fields_frame = ctk.CTkFrame(box, fg_color="transparent")
        fields_frame.pack(padx=40, fill="x")

        ctk.CTkLabel(fields_frame, text="USERNAME", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold"),
                     anchor="w").pack(fill="x", pady=(0, 4))
        self.username_entry = ctk.CTkEntry(
            fields_frame, placeholder_text="Enter username",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            placeholder_text_color=MUTED, corner_radius=8, height=42,
            font=ctk.CTkFont(family="Courier", size=13))
        self.username_entry.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(fields_frame, text="PASSWORD", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold"),
                     anchor="w").pack(fill="x", pady=(0, 4))
        self.password_entry = ctk.CTkEntry(
            fields_frame, placeholder_text="Enter password",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            placeholder_text_color=MUTED, corner_radius=8, height=42,
            show="●", font=ctk.CTkFont(family="Courier", size=13))
        self.password_entry.pack(fill="x", pady=(0, 6))

        self.error_label = ctk.CTkLabel(fields_frame, text="",
                                        text_color=DANGER,
                                        font=ctk.CTkFont(family="Courier", size=11))
        self.error_label.pack(pady=(4, 0))

        # Login button
        btn = ctk.CTkButton(
            fields_frame, text="LOGIN →",
            fg_color=ACCENT, hover_color="#3a78e0",
            text_color="white", corner_radius=8, height=44,
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            command=self._do_login)
        btn.pack(fill="x", pady=(14, 0))

        # Footer
        ctk.CTkLabel(box, text="Admin default: admin / admin123",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).pack(pady=(20, 0))

        # Enter key binding
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._do_login())

        # Auto-focus
        self.after(100, self.username_entry.focus)

    def _do_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        if not u or not p:
            self.error_label.configure(text="Please enter username and password.")
            return
        user = db.authenticate(u, p)
        if user:
            self.error_label.configure(text="")
            self.on_login(user)
        else:
            self.error_label.configure(text="✕  Invalid credentials. Try again.")
            self.password_entry.delete(0, "end")
