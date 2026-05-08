#!/usr/bin/env python3
"""
GCUF Science Exhibition Result Management System
Entry point — run with: python main.py
"""
import sys
import os

# Ensure the gcuf_app directory is on the Python path so all modules import correctly
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import customtkinter as ctk
import database as db
from ui.widgets import configure_theme, BG, SURFACE, BORDER, TEXT, ACCENT, MUTED
from ui.login_frame import LoginFrame
from ui.admin_frame import AdminFrame
from ui.professor_frame import ProfessorFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GCUF Result Management System")
        self.geometry("1280x800")
        self.minsize(1100, 720)
        self.configure(fg_color="#0a0b0f")

        # Center window
        self.update_idletasks()
        w, h = 1280, 800
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        configure_theme()
        db.init_db()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._show_login()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_login(self):
        self._clear()
        login = LoginFrame(self, on_login=self._on_login)
        login.grid(row=0, column=0, sticky="nsew")

    def _on_login(self, user):
        self._clear()
        if user["role"] == "admin":
            frame = AdminFrame(self, user, on_logout=self._show_login)
        else:
            frame = ProfessorFrame(self, user, on_logout=self._show_login)
        frame.grid(row=0, column=0, sticky="nsew")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
