import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database as db
from ui.widgets import *


class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self._current_page = None
        self._build()
        self._show_page("dashboard")

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Sidebar ───────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0, width=SIDEBAR_W,
                               border_width=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(10, weight=1)

        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=16, pady=(20, 8), sticky="ew")
        ctk.CTkLabel(logo_frame, text="GCUF", text_color=ACCENT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="Result Management",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).pack(anchor="w")

        # Divider
        tk.Frame(sidebar, bg=BORDER, height=1).grid(row=1, column=0, sticky="ew", padx=12, pady=4)

        # Role badge
        badge = ctk.CTkLabel(sidebar, text=f"● ADMIN",
                             text_color=ACCENT,
                             fg_color="#4f8ef720",
                             corner_radius=6,
                             font=ctk.CTkFont(family="Courier", size=9, weight="bold"))
        badge.grid(row=2, column=0, padx=16, pady=(4, 8), sticky="w")

        # Nav buttons
        self._nav_btns = {}
        nav_items = [
            ("dashboard",    "◈", "Dashboard"),
            ("departments",  "⊞", "Departments"),
            ("users",        "⊙", "User Management"),
            ("analytics",    "▦", "Analytics"),
            ("toppers",      "★", "Toppers / Rankings"),
            ("all_results",  "≡", "All Results"),
        ]
        for i, (key, icon, label) in enumerate(nav_items):
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {label}",
                fg_color="transparent", text_color=MUTED,
                hover_color=SURFACE2, anchor="w", corner_radius=8, height=40,
                font=ctk.CTkFont(family="Courier", size=12),
                command=lambda k=key: self._show_page(k))
            btn.grid(row=3 + i, column=0, padx=8, pady=2, sticky="ew")
            self._nav_btns[key] = btn

        tk.Frame(sidebar, bg=BORDER, height=1).grid(row=10, column=0, sticky="ew", padx=12, pady=4)

        # User info + logout
        ctk.CTkLabel(sidebar, text=self.user.get("full_name", self.user["username"]),
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=11, weight="bold")).grid(
            row=11, column=0, padx=16, pady=(8, 0), sticky="w")

        ctk.CTkButton(sidebar, text="Logout", fg_color="transparent",
                      text_color=DANGER, hover_color=SURFACE2,
                      anchor="w", corner_radius=8, height=34,
                      font=ctk.CTkFont(family="Courier", size=11),
                      command=self.on_logout).grid(row=12, column=0, padx=8, pady=(0, 16), sticky="ew")

        # ── Content Area ─────────────────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    def _show_page(self, key):
        for k, btn in self._nav_btns.items():
            active = k == key
            btn.configure(
                fg_color=ACCENT + "22" if active else "transparent",
                text_color=TEXT if active else MUTED,
                font=ctk.CTkFont(family="Courier", size=12, weight="bold" if active else "normal"),
            )
        for w in self.content.winfo_children():
            w.destroy()
        self._current_page = key
        pages = {
            "dashboard":   self._page_dashboard,
            "departments": self._page_departments,
            "users":       self._page_users,
            "analytics":   self._page_analytics,
            "toppers":     self._page_toppers,
            "all_results": self._page_all_results,
        }
        pages.get(key, self._page_dashboard)()

    # ────────────────────────── DASHBOARD ───────────────────────────────────

    def _page_dashboard(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # Header
        hdr = ctk.CTkFrame(frame, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 8))
        ctk.CTkLabel(hdr, text="Global Dashboard", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(hdr, text="System-wide overview of all departments and results",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(anchor="w", pady=(2, 0))

        # Stats
        courses   = db.get_all_courses()
        depts     = db.get_departments()
        users     = db.get_all_users()
        dept_data = db.get_dept_avg_gpa()

        total_students = sum(d.get("student_count", 0) for d in dept_data)

        stats_row = ctk.CTkFrame(frame, fg_color="transparent")
        stats_row.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        for i in range(4):
            stats_row.grid_columnconfigure(i, weight=1)

        stat_data = [
            ("Departments", len(depts), ACCENT),
            ("Courses",     len(courses), ACCENT2),
            ("Students",    total_students, ACCENT3),
            ("Users",       len(users), WARN),
        ]
        for i, (title, val, color) in enumerate(stat_data):
            c = stat_card(stats_row, title, val, color)
            c.grid(row=0, column=i, padx=6, pady=4, sticky="ew")

        # Department overview table
        ctk.CTkLabel(frame, text="DEPARTMENT OVERVIEW", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=30, pady=(18, 6))

        table_frame = card_frame(frame)
        table_frame.grid(row=3, column=0, sticky="ew", padx=24, pady=4)

        headers = ["Department", "Students", "Avg %", "Status"]
        col_ws = [3, 1, 1, 1]
        for i, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h.upper(), text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=9, weight="bold")).grid(
                row=0, column=i, padx=14, pady=(12, 6), sticky="w")

        if not dept_data:
            ctk.CTkLabel(table_frame, text="No data yet. Upload PDFs to see results.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=11)).grid(
                row=1, column=0, columnspan=4, pady=20, padx=14, sticky="w")
        else:
            for r, d in enumerate(dept_data):
                avg = d.get("avg_pct", 0) or 0
                color = ACCENT3 if avg >= 70 else (WARN if avg >= 50 else DANGER)
                ctk.CTkLabel(table_frame, text=d["dept_name"], text_color=TEXT,
                             font=ctk.CTkFont(family="Courier", size=12)).grid(
                    row=r+1, column=0, padx=14, pady=5, sticky="w")
                ctk.CTkLabel(table_frame, text=str(d.get("student_count", 0)), text_color=TEXT,
                             font=ctk.CTkFont(family="Courier", size=12)).grid(
                    row=r+1, column=1, padx=14, pady=5, sticky="w")
                ctk.CTkLabel(table_frame, text=f"{avg:.1f}%", text_color=color,
                             font=ctk.CTkFont(family="Courier", size=12, weight="bold")).grid(
                    row=r+1, column=2, padx=14, pady=5, sticky="w")
                status_t = "Good" if avg >= 70 else ("Average" if avg >= 50 else "Needs Attention")
                ctk.CTkLabel(table_frame, text=status_t, text_color=color,
                             font=ctk.CTkFont(family="Courier", size=11)).grid(
                    row=r+1, column=3, padx=14, pady=5, sticky="w")

    # ────────────────────────── DEPARTMENTS ─────────────────────────────────

    def _page_departments(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(frame, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 8))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="Department Management", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(hdr, text="Create, rename, or remove departments",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(row=1, column=0, sticky="w")

        # Add form
        add_card = card_frame(frame)
        add_card.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        ctk.CTkLabel(add_card, text="ADD NEW DEPARTMENT", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=14, pady=(12, 6), sticky="w")

        self._dept_entry = ctk.CTkEntry(
            add_card, placeholder_text="Department name (e.g. Physics, Zoology, IT)",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            placeholder_text_color=MUTED, corner_radius=8, height=38, width=320,
            font=ctk.CTkFont(family="Courier", size=12))
        self._dept_entry.grid(row=1, column=0, padx=14, pady=(0, 12))
        ctk.CTkButton(add_card, text="+ Add Department", fg_color=ACCENT,
                      hover_color="#3a78e0", text_color="white", corner_radius=8,
                      height=38, font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                      command=self._add_dept).grid(row=1, column=1, padx=8, pady=(0, 12))

        # List
        self._dept_list_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self._dept_list_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=4)
        self._dept_list_frame.grid_columnconfigure(0, weight=1)
        self._refresh_dept_list()

    def _add_dept(self):
        name = self._dept_entry.get().strip()
        if not name:
            return
        try:
            db.add_department(name)
            self._dept_entry.delete(0, "end")
            self._refresh_dept_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh_dept_list(self):
        for w in self._dept_list_frame.winfo_children():
            w.destroy()
        depts = db.get_departments()
        if not depts:
            ctk.CTkLabel(self._dept_list_frame, text="No departments yet.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=12)).grid(row=0, column=0, pady=16, sticky="w")
            return
        for i, d in enumerate(depts):
            row_f = card_frame(self._dept_list_frame)
            row_f.grid(row=i, column=0, sticky="ew", pady=4)
            row_f.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row_f, text=d["name"], text_color=TEXT,
                         font=ctk.CTkFont(family="Courier", size=13, weight="bold")).grid(
                row=0, column=0, padx=16, pady=12, sticky="w")
            ctk.CTkLabel(row_f, text=f"ID: {d['id']}", text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=10)).grid(
                row=0, column=1, padx=8)

            def rename(did=d["id"], dname=d["name"]):
                new = simpledialog.askstring("Rename", f"New name for '{dname}':", initialvalue=dname)
                if new and new.strip():
                    db.rename_department(did, new.strip())
                    self._refresh_dept_list()

            def delete(did=d["id"], dname=d["name"]):
                if messagebox.askyesno("Delete", f"Delete department '{dname}'? All courses/results will be removed!"):
                    db.delete_department(did)
                    self._refresh_dept_list()

            ctk.CTkButton(row_f, text="Rename", fg_color=SURFACE2, hover_color=BORDER,
                          text_color=ACCENT, corner_radius=6, width=80, height=30,
                          font=ctk.CTkFont(family="Courier", size=11),
                          command=rename).grid(row=0, column=2, padx=4)
            ctk.CTkButton(row_f, text="Delete", fg_color=SURFACE2, hover_color=BORDER,
                          text_color=DANGER, corner_radius=6, width=80, height=30,
                          font=ctk.CTkFont(family="Courier", size=11),
                          command=delete).grid(row=0, column=3, padx=(4, 14))

    # ────────────────────────── USER MANAGEMENT ──────────────────────────────

    def _page_users(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="User Management", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))
        ctk.CTkLabel(frame, text="Add professors and manage system access",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=1, column=0, sticky="w", padx=28, pady=(0, 12))

        # Add user form
        form = card_frame(frame)
        form.grid(row=2, column=0, sticky="ew", padx=24, pady=8)
        ctk.CTkLabel(form, text="CREATE NEW USER", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold")).grid(
            row=0, column=0, columnspan=6, padx=14, pady=(12, 6), sticky="w")

        fields = {}
        labels = ["Full Name", "Username", "Password", "Role", "Department"]
        for i, l in enumerate(labels):
            ctk.CTkLabel(form, text=l, text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=9)).grid(
                row=1, column=i, padx=10, pady=(0, 4), sticky="w")

        self._new_fullname = ctk.CTkEntry(form, placeholder_text="Full Name",
                                          fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
                                          placeholder_text_color=MUTED, corner_radius=8, height=34, width=130,
                                          font=ctk.CTkFont(family="Courier", size=11))
        self._new_fullname.grid(row=2, column=0, padx=10, pady=(0, 12))

        self._new_username = ctk.CTkEntry(form, placeholder_text="Username",
                                          fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
                                          placeholder_text_color=MUTED, corner_radius=8, height=34, width=110,
                                          font=ctk.CTkFont(family="Courier", size=11))
        self._new_username.grid(row=2, column=1, padx=10, pady=(0, 12))

        self._new_password = ctk.CTkEntry(form, placeholder_text="Password",
                                          fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
                                          placeholder_text_color=MUTED, corner_radius=8, height=34, width=110,
                                          show="●", font=ctk.CTkFont(family="Courier", size=11))
        self._new_password.grid(row=2, column=2, padx=10, pady=(0, 12))

        self._new_role = ctk.CTkOptionMenu(form, values=["professor", "admin"],
                                           fg_color=SURFACE2, button_color=SURFACE2,
                                           button_hover_color=BORDER, text_color=TEXT,
                                           dropdown_fg_color=SURFACE2, dropdown_text_color=TEXT,
                                           width=100, height=34,
                                           font=ctk.CTkFont(family="Courier", size=11))
        self._new_role.grid(row=2, column=3, padx=10, pady=(0, 12))

        depts = db.get_departments()
        dept_names = ["(None)"] + [d["name"] for d in depts]
        self._dept_map = {d["name"]: d["id"] for d in depts}
        self._new_dept = ctk.CTkOptionMenu(form, values=dept_names,
                                           fg_color=SURFACE2, button_color=SURFACE2,
                                           button_hover_color=BORDER, text_color=TEXT,
                                           dropdown_fg_color=SURFACE2, dropdown_text_color=TEXT,
                                           width=120, height=34,
                                           font=ctk.CTkFont(family="Courier", size=11))
        self._new_dept.grid(row=2, column=4, padx=10, pady=(0, 12))

        ctk.CTkButton(form, text="Create", fg_color=ACCENT, hover_color="#3a78e0",
                      text_color="white", corner_radius=8, height=34, width=80,
                      font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
                      command=self._create_user).grid(row=2, column=5, padx=10, pady=(0, 12))

        # User list
        self._user_list_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self._user_list_frame.grid(row=3, column=0, sticky="ew", padx=24, pady=8)
        self._user_list_frame.grid_columnconfigure(0, weight=1)
        self._refresh_user_list()

    def _create_user(self):
        fn = self._new_fullname.get().strip()
        un = self._new_username.get().strip()
        pw = self._new_password.get().strip()
        role = self._new_role.get()
        dept_name = self._new_dept.get()
        dept_id = self._dept_map.get(dept_name)
        if not un or not pw:
            messagebox.showerror("Error", "Username and password required.")
            return
        try:
            db.create_user(un, pw, role, fn, dept_id)
            for e in [self._new_fullname, self._new_username, self._new_password]:
                e.delete(0, "end")
            self._refresh_user_list()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create user:\n{e}")

    def _refresh_user_list(self):
        for w in self._user_list_frame.winfo_children():
            w.destroy()
        users = db.get_all_users()
        header_row = ctk.CTkFrame(self._user_list_frame, fg_color="transparent")
        header_row.grid(row=0, column=0, sticky="ew", pady=(4, 0))
        for i, h in enumerate(["Username", "Full Name", "Role", "Department", ""]):
            ctk.CTkLabel(header_row, text=h.upper(), text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=9, weight="bold")).grid(
                row=0, column=i, padx=14, pady=4, sticky="w")

        for r, u in enumerate(users):
            row_f = card_frame(self._user_list_frame)
            row_f.grid(row=r+1, column=0, sticky="ew", pady=3)
            role_color = ACCENT if u["role"] == "admin" else ACCENT2
            vals = [u["username"], u.get("full_name","—"), u["role"].upper(),
                    u.get("dept_name","—")]
            for c, v in enumerate(vals):
                col = role_color if c == 2 else TEXT
                ctk.CTkLabel(row_f, text=v, text_color=col,
                             font=ctk.CTkFont(family="Courier", size=11,
                                              weight="bold" if c == 2 else "normal")).grid(
                    row=0, column=c, padx=14, pady=9, sticky="w")

            if u["role"] != "admin":
                def del_user(uid=u["id"], uname=u["username"]):
                    if messagebox.askyesno("Delete User", f"Delete user '{uname}'?"):
                        db.delete_user(uid)
                        self._refresh_user_list()
                ctk.CTkButton(row_f, text="Delete", fg_color=SURFACE2, hover_color=BORDER,
                              text_color=DANGER, corner_radius=6, width=70, height=28,
                              font=ctk.CTkFont(family="Courier", size=10),
                              command=del_user).grid(row=0, column=4, padx=10)

    # ────────────────────────── ANALYTICS ───────────────────────────────────

    def _page_analytics(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Cross-Department Analytics", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))
        ctk.CTkLabel(frame, text="Average performance comparison across departments",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=1, column=0, sticky="w", padx=28, pady=(0, 16))

        dept_data = db.get_dept_avg_gpa()
        if not dept_data:
            ctk.CTkLabel(frame, text="No result data available yet. Upload PDFs to generate analytics.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=13)).grid(
                row=2, column=0, pady=60)
            return

        names = [d["dept_name"] for d in dept_data]
        avgs  = [d.get("avg_pct", 0) or 0 for d in dept_data]
        counts= [d.get("student_count", 0) or 0 for d in dept_data]

        # Bar chart
        chart_card = card_frame(frame)
        chart_card.grid(row=2, column=0, sticky="ew", padx=24, pady=8)

        fig = Figure(figsize=(9, 4), dpi=96, facecolor="#111318")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#111318")
        fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.22)

        colors = ["#4f8ef7" if a >= 70 else "#fb923c" if a >= 50 else "#f87171" for a in avgs]
        bars = ax.bar(names, avgs, color=colors, width=0.5, zorder=3)

        for bar, val in zip(bars, avgs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f"{val:.1f}%", ha="center", va="bottom", color="#e8eaf0",
                    fontsize=9, fontfamily="monospace")

        ax.set_ylim(0, 105)
        ax.set_xlabel("Department", color="#6b7280", fontsize=10, fontfamily="monospace")
        ax.set_ylabel("Average Percentage (%)", color="#6b7280", fontsize=10, fontfamily="monospace")
        ax.set_title("Average Score by Department", color="#e8eaf0", fontsize=13, fontfamily="monospace", pad=10)
        ax.tick_params(colors="#6b7280", labelsize=9)
        ax.grid(axis="y", color="#22262f", linewidth=0.8, zorder=0)
        for spine in ax.spines.values():
            spine.set_color("#22262f")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=20, ha="right", color="#e8eaf0", fontfamily="monospace")

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=12)

        # Student count chart
        if len(names) >= 2:
            chart_card2 = card_frame(frame)
            chart_card2.grid(row=3, column=0, sticky="ew", padx=24, pady=8)

            fig2 = Figure(figsize=(9, 3.2), dpi=96, facecolor="#111318")
            ax2  = fig2.add_subplot(111)
            ax2.set_facecolor("#111318")
            fig2.subplots_adjust(left=0.10, right=0.97, top=0.85, bottom=0.22)
            ax2.bar(names, counts, color="#a78bfa", width=0.4, zorder=3)
            ax2.set_title("Student Count by Department", color="#e8eaf0", fontsize=12,
                          fontfamily="monospace", pad=8)
            ax2.tick_params(colors="#6b7280", labelsize=9)
            ax2.grid(axis="y", color="#22262f", linewidth=0.8, zorder=0)
            for spine in ax2.spines.values():
                spine.set_color("#22262f")
            ax2.set_xticks(range(len(names)))
            ax2.set_xticklabels(names, rotation=20, ha="right", color="#e8eaf0", fontfamily="monospace")

            canvas2 = FigureCanvasTkAgg(fig2, master=chart_card2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    # ────────────────────────── TOPPERS ──────────────────────────────────────

    def _page_toppers(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Toppers & Rankings", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))
        ctk.CTkLabel(frame, text="Ranked strictly by average percentage across courses",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=1, column=0, sticky="w", padx=28, pady=(0, 12))

        # Session toppers
        sessions = db.get_all_sessions()
        if not sessions:
            ctk.CTkLabel(frame, text="No results uploaded yet.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=13)).grid(
                row=2, column=0, pady=40)
            return

        # Filter row
        filter_row = ctk.CTkFrame(frame, fg_color="transparent")
        filter_row.grid(row=2, column=0, sticky="w", padx=24, pady=8)
        ctk.CTkLabel(filter_row, text="Session:", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(0, 8))
        self._topper_session = ctk.CTkOptionMenu(
            filter_row, values=sessions,
            fg_color=SURFACE2, button_color=SURFACE2,
            button_hover_color=BORDER, text_color=TEXT,
            dropdown_fg_color=SURFACE2, dropdown_text_color=TEXT,
            width=140, height=34, font=ctk.CTkFont(family="Courier", size=11),
            command=lambda _: self._refresh_toppers())
        self._topper_session.pack(side="left")

        self._toppers_container = ctk.CTkFrame(frame, fg_color="transparent")
        self._toppers_container.grid(row=3, column=0, sticky="ew", padx=24, pady=8)
        self._toppers_container.grid_columnconfigure(0, weight=1)
        self._toppers_container.grid_columnconfigure(1, weight=1)
        self._refresh_toppers()

    def _refresh_toppers(self):
        for w in self._toppers_container.winfo_children():
            w.destroy()
        session = self._topper_session.get() if hasattr(self, "_topper_session") else ""

        # Session toppers
        s_top = db.get_session_toppers(session, 10)
        self._render_topper_card(self._toppers_container, "SESSION TOPPERS", s_top, 0)

        # Department toppers per dept
        depts = db.get_departments()
        for i, d in enumerate(depts):
            d_top = db.get_department_toppers(d["id"], 5)
            self._render_topper_card(self._toppers_container, f"{d['name'].upper()} TOPPERS", d_top, i+1)

    def _render_topper_card(self, parent, title, toppers, col):
        card = card_frame(parent)
        card.grid(row=0, column=col % 2, padx=6, pady=6, sticky="new")
        ctk.CTkLabel(card, text=title, text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold")).pack(
            anchor="w", padx=14, pady=(12, 6))
        medals = ["🥇", "🥈", "🥉"]
        if not toppers:
            ctk.CTkLabel(card, text="No data", text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=11)).pack(padx=14, pady=8)
            return
        for i, t in enumerate(toppers):
            r = ctk.CTkFrame(card, fg_color="transparent")
            r.pack(fill="x", padx=8, pady=2)
            medal = medals[i] if i < 3 else f"#{i+1}"
            ctk.CTkLabel(r, text=str(medal), text_color=ACCENT,
                         font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                         width=34).pack(side="left")
            info = ctk.CTkFrame(r, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(info, text=t.get("name","—"), text_color=TEXT,
                         font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(info, text=f"Roll: {t.get('roll_no','—')} | {t.get('session','')}",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=9),
                         anchor="w").pack(anchor="w")
            pct = t.get("avg_pct", 0) or 0
            ctk.CTkLabel(r, text=f"{pct:.1f}%", text_color=ACCENT3,
                         font=ctk.CTkFont(family="Courier", size=13, weight="bold")).pack(side="right", padx=8)

    # ────────────────────────── ALL RESULTS ──────────────────────────────────

    def _page_all_results(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="All Uploaded Courses", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))

        courses = db.get_all_courses()
        if not courses:
            ctk.CTkLabel(frame, text="No courses uploaded yet.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=13)).grid(
                row=1, column=0, pady=40)
            return

        for i, c in enumerate(courses):
            self._render_course_row(frame, c, i+1)

    def _render_course_row(self, parent, course, row):
        card = card_frame(parent)
        card.grid(row=row, column=0, sticky="ew", padx=24, pady=4)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=f"{course['code']}  —  {course['title']}",
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=12, weight="bold")).grid(
            row=0, column=0, padx=14, pady=(10, 2), sticky="w")
        ctk.CTkLabel(card,
                     text=f"Dept: {course.get('dept_name','?')}  |  Session: {course.get('session','')}  |  Credits: {course.get('credit_hours_raw','')}",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=10)).grid(
            row=1, column=0, padx=14, pady=(0, 10), sticky="w")

        results = db.get_results_for_course(course["id"])
        ctk.CTkLabel(card, text=f"{len(results)} students",
                     text_color=ACCENT,
                     font=ctk.CTkFont(family="Courier", size=11, weight="bold")).grid(
            row=0, column=1, padx=14, rowspan=2)
