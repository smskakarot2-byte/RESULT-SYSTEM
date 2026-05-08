import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from ui.widgets import *
import database as db
from grading import compute_gpa, grade_color, gpa_color
import transcript as tr


class ProfessorFrame(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self.dept_id = user.get("department_id")
        self._build()
        self._show_page("upload")

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Sidebar ────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0, width=SIDEBAR_W)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(8, weight=1)

        logo_f = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_f.grid(row=0, column=0, padx=16, pady=(20, 8), sticky="ew")
        ctk.CTkLabel(logo_f, text="GCUF", text_color=ACCENT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(logo_f, text="Professor Portal",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).pack(anchor="w")

        tk.Frame(sidebar, bg=BORDER, height=1).grid(row=1, column=0, sticky="ew", padx=12, pady=4)

        dept_name = self.user.get("dept_name", "No Department")
        ctk.CTkLabel(sidebar, text=f"Dept: {dept_name}",
                     text_color=ACCENT2,
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).grid(
            row=2, column=0, padx=16, pady=(4, 8), sticky="w")

        self._nav_btns = {}
        nav_items = [
            ("upload",   "⊕", "Upload PDF"),
            ("courses",  "≡", "Course Results"),
            ("students", "⊙", "Student Lookup"),
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

        tk.Frame(sidebar, bg=BORDER, height=1).grid(row=8, column=0, sticky="ew", padx=12, pady=4)

        ctk.CTkLabel(sidebar, text=self.user.get("full_name", self.user["username"]),
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=11, weight="bold")).grid(
            row=9, column=0, padx=16, pady=(8, 0), sticky="w")
        ctk.CTkButton(sidebar, text="Logout", fg_color="transparent",
                      text_color=DANGER, hover_color=SURFACE2,
                      anchor="w", corner_radius=8, height=34,
                      font=ctk.CTkFont(family="Courier", size=11),
                      command=self.on_logout).grid(row=10, column=0, padx=8, pady=(0, 16), sticky="ew")

        # ── Content ────────────────────────────────────────────────
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
        pages = {
            "upload":   self._page_upload,
            "courses":  self._page_courses,
            "students": self._page_students,
        }
        pages.get(key, self._page_upload)()

    # ──────────────────────── PDF UPLOAD ─────────────────────────────────────

    def _page_upload(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Upload Award Sheet PDF", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))
        ctk.CTkLabel(frame, text="Parse and import GCUF Detailed Award Sheet automatically",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=1, column=0, sticky="w", padx=28, pady=(0, 16))

        if not self.dept_id:
            ctk.CTkLabel(frame, text="⚠  No department assigned. Ask Admin to assign your department.",
                         text_color=WARN,
                         font=ctk.CTkFont(family="Courier", size=12)).grid(
                row=2, column=0, padx=28, pady=20)
            return

        # Drop zone
        drop_card = card_frame(frame)
        drop_card.grid(row=2, column=0, sticky="ew", padx=24, pady=8)

        self._file_label = ctk.CTkLabel(drop_card, text="No file selected",
                                        text_color=MUTED,
                                        font=ctk.CTkFont(family="Courier", size=12))
        self._file_label.pack(pady=(20, 8))

        ctk.CTkButton(drop_card, text="⊕  Browse PDF File",
                      fg_color=SURFACE2, hover_color=BORDER,
                      text_color=ACCENT, border_color=ACCENT, border_width=1,
                      corner_radius=8, height=44, width=240,
                      font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                      command=self._browse_file).pack(pady=8)

        ctk.CTkLabel(drop_card, text="Supports: GCUF Detailed Award Sheet format (.pdf)",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).pack(pady=(0, 20))

        self._upload_btn = ctk.CTkButton(
            frame, text="▶  Parse & Import",
            fg_color=ACCENT, hover_color="#3a78e0",
            text_color="white", corner_radius=8, height=46, width=220,
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            command=self._do_parse, state="disabled")
        self._upload_btn.grid(row=3, column=0, pady=12)

        self._status_label = ctk.CTkLabel(frame, text="",
                                          text_color=MUTED,
                                          font=ctk.CTkFont(family="Courier", size=11))
        self._status_label.grid(row=4, column=0, pady=4)

        self._preview_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self._preview_frame.grid(row=5, column=0, sticky="ew", padx=24, pady=8)
        self._preview_frame.grid_columnconfigure(0, weight=1)
        self._selected_pdf = None

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select GCUF Award Sheet PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if path:
            self._selected_pdf = path
            self._file_label.configure(text=f"✓  {os.path.basename(path)}", text_color=ACCENT3)
            self._upload_btn.configure(state="normal")

    def _do_parse(self):
        if not self._selected_pdf:
            return
        self._upload_btn.configure(state="disabled", text="Parsing...")
        self._status_label.configure(text="⟳  Reading PDF...", text_color=ACCENT)

        def parse_thread():
            try:
                # Add app dir to path for imports
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from pdf_parser import parse_award_sheet
                result = parse_award_sheet(self._selected_pdf)
                self.after(0, lambda: self._on_parse_done(result))
            except Exception as e:
                self.after(0, lambda: self._on_parse_error(str(e)))

        threading.Thread(target=parse_thread, daemon=True).start()

    def _on_parse_error(self, err):
        self._status_label.configure(text=f"✕  Error: {err}", text_color=DANGER)
        self._upload_btn.configure(state="normal", text="▶  Parse & Import")

    def _on_parse_done(self, result):
        header = result.get("header", {})
        students = result.get("students", [])

        if not students:
            self._status_label.configure(text="✕  No student data found in PDF.", text_color=DANGER)
            self._upload_btn.configure(state="normal", text="▶  Parse & Import")
            return

        # Save to DB
        course_id = db.save_course(
            code=header.get("course_code", "UNKNOWN"),
            title=header.get("course_title", "Unknown Course"),
            credit_hours_raw=header.get("credit_hours_raw", "3(2-1)"),
            credit_hours=header.get("credit_hours", 3.0),
            session=header.get("session", ""),
            semester=header.get("semester", ""),
            department_id=self.dept_id,
            max_marks=header.get("max_marks", 60.0),
            uploaded_by=self.user["id"],
        )

        for s in students:
            sid = db.get_or_create_student(
                s["roll_no"], s["name"], s["father_name"], s["cnic"], s["session"])
            db.save_result(
                sid, course_id,
                s["internal"], s["mid_term"], s["final_term"], s["practical"],
                s["total_obtained"], s["percentage"],
                s["grade"], s["grade_point"], s["status"],
            )

        self._status_label.configure(
            text=f"✓  Imported {len(students)} students for {header.get('course_code','?')}",
            text_color=ACCENT3)
        self._upload_btn.configure(state="normal", text="▶  Parse & Import")

        # Show preview
        self._show_import_preview(header, students)

    def _show_import_preview(self, header, students):
        for w in self._preview_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(self._preview_frame, text="PARSED HEADER", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9, weight="bold")).grid(
            row=0, column=0, sticky="w", pady=(8, 4))

        info_card = card_frame(self._preview_frame)
        info_card.grid(row=1, column=0, sticky="ew", pady=4)
        info_pairs = [
            ("Course Code", header.get("course_code", "—")),
            ("Course Title", header.get("course_title", "—")),
            ("Session", header.get("session", "—")),
            ("Credit Hours", header.get("credit_hours_raw", "—")),
            ("Max Marks", str(header.get("max_marks", "—"))),
            ("Department", header.get("department", "—")),
        ]
        for i, (k, v) in enumerate(info_pairs):
            ctk.CTkLabel(info_card, text=f"{k}:", text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=10)).grid(
                row=i//2, column=(i%2)*2, padx=(14, 4), pady=4, sticky="w")
            ctk.CTkLabel(info_card, text=v, text_color=TEXT,
                         font=ctk.CTkFont(family="Courier", size=10, weight="bold")).grid(
                row=i//2, column=(i%2)*2+1, padx=(0, 20), pady=4, sticky="w")

        # Student count
        passed = sum(1 for s in students if s["status"] == "Pass")
        failed = len(students) - passed
        ctk.CTkLabel(self._preview_frame,
                     text=f"Imported: {len(students)} students  |  Pass: {passed}  |  Fail: {failed}",
                     text_color=ACCENT3,
                     font=ctk.CTkFont(family="Courier", size=12, weight="bold")).grid(
            row=2, column=0, pady=8, sticky="w")

    # ──────────────────────── COURSES ────────────────────────────────────────

    def _page_courses(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Department Courses", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))

        courses = db.get_courses_for_department(self.dept_id) if self.dept_id else []
        if not courses:
            ctk.CTkLabel(frame, text="No courses uploaded yet. Use PDF Upload to add results.",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=12)).grid(
                row=1, column=0, pady=40, padx=28)
            return

        for i, c in enumerate(courses):
            self._render_course_card(frame, c, i+1)

    def _render_course_card(self, parent, course, row):
        card = card_frame(parent)
        card.grid(row=row, column=0, sticky="ew", padx=24, pady=6)
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=14, pady=(12, 4))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text=f"{course['code']}  —  {course['title']}",
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold")).grid(
            row=0, column=0, sticky="w")
        ctk.CTkLabel(hdr,
                     text=f"Session: {course['session']}  |  Credits: {course['credit_hours_raw']}",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=10)).grid(
            row=1, column=0, sticky="w", pady=(2, 0))

        results = db.get_results_for_course(course["id"])
        passed = sum(1 for r in results if r["status"] == "Pass")
        avg_pct = sum(r["percentage"] for r in results) / len(results) if results else 0

        info_row = ctk.CTkFrame(card, fg_color="transparent")
        info_row.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 4))
        for j, (label, val, col) in enumerate([
            ("Students", len(results), TEXT),
            ("Passed", passed, ACCENT3),
            ("Failed", len(results)-passed, DANGER if (len(results)-passed) > 0 else MUTED),
            ("Avg %", f"{avg_pct:.1f}%", ACCENT),
        ]):
            ctk.CTkLabel(info_row, text=f"{label}: ", text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=10)).grid(row=0, column=j*2, padx=(8 if j else 0, 0))
            ctk.CTkLabel(info_row, text=str(val), text_color=col,
                         font=ctk.CTkFont(family="Courier", size=10, weight="bold")).grid(row=0, column=j*2+1, padx=(2, 16))

        def view(cid=course["id"]):
            self._show_course_results(cid)

        ctk.CTkButton(card, text="View Results →", fg_color=SURFACE2, hover_color=BORDER,
                      text_color=ACCENT, corner_radius=8, height=32, width=140,
                      font=ctk.CTkFont(family="Courier", size=11),
                      command=view).grid(row=0, column=1, padx=14, rowspan=2)

    def _show_course_results(self, course_id):
        for w in self.content.winfo_children():
            w.destroy()

        course = db.get_course(course_id)
        results = db.get_results_for_course(course_id)

        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # Back button
        ctk.CTkButton(frame, text="← Back to Courses",
                      fg_color="transparent", text_color=MUTED, hover_color=SURFACE2,
                      anchor="w", corner_radius=8, height=32, width=160,
                      font=ctk.CTkFont(family="Courier", size=11),
                      command=lambda: self._show_page("courses")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(16, 4))

        ctk.CTkLabel(frame, text=f"{course['code']}  —  {course['title']}",
                     text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=18, weight="bold")).grid(
            row=1, column=0, sticky="w", padx=24, pady=(4, 2))
        ctk.CTkLabel(frame, text=f"Session: {course['session']}  |  Credits: {course['credit_hours_raw']}  |  Max: {course['max_marks']}",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=2, column=0, sticky="w", padx=24, pady=(0, 12))

        for i, r in enumerate(results):
            self._render_student_card(frame, r, course, i + 3)

    def _render_student_card(self, parent, r, course, row):
        card = card_frame(parent)
        card.grid(row=row, column=0, sticky="ew", padx=24, pady=5)
        card.grid_columnconfigure(0, weight=1)

        # Gauge canvas
        gauge_w, gauge_h = 130, 70
        gauge_canvas = tk.Canvas(card, width=gauge_w, height=gauge_h,
                                 bg=SURFACE, highlightthickness=0)
        gauge_canvas.grid(row=0, column=2, rowspan=3, padx=14, pady=8)

        gpa_val = r.get("grade_point", 0) or 0
        from ui.widgets import draw_gpa_gauge
        gauge_canvas.after(50, lambda c=gauge_canvas, g=gpa_val:
                           draw_gpa_gauge(c, gauge_w//2, gauge_h - 10, 48, g))

        # Info
        ctk.CTkLabel(card, text=r.get("name", "—"), text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold")).grid(
            row=0, column=0, padx=16, pady=(10, 2), sticky="w")
        ctk.CTkLabel(card,
                     text=f"Roll: {r.get('roll_no','—')}  |  CNIC: {r.get('cnic','—')}  |  Father: {r.get('father_name','—')}",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).grid(
            row=1, column=0, padx=16, sticky="w")

        marks_text = (f"Int: {r['internal_marks']:.0f}  "
                      f"Mid: {r['mid_term']:.0f}  "
                      f"Final: {r['final_term']:.0f}  "
                      f"Pract: {r['practical_work']:.0f}  "
                      f"Total: {r['total_obtained']:.0f}/{course['max_marks']:.0f}")
        ctk.CTkLabel(card, text=marks_text, text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=9)).grid(
            row=2, column=0, padx=16, pady=(2, 10), sticky="w")

        # Grade pill + status
        grade = r.get("grade", "—")
        status = r.get("status", "—")
        pct = r.get("percentage", 0)
        g_color = grade_color(grade)
        s_color = ACCENT3 if status == "Pass" else DANGER

        info_col = ctk.CTkFrame(card, fg_color="transparent")
        info_col.grid(row=0, column=1, rowspan=3, padx=8, pady=8, sticky="e")
        ctk.CTkLabel(info_col, text=grade, text_color=g_color,
                     font=ctk.CTkFont(family="Courier", size=26, weight="bold")).pack()
        ctk.CTkLabel(info_col, text=f"{pct:.1f}%", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=12, weight="bold")).pack()
        ctk.CTkLabel(info_col, text=status, text_color=s_color,
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack()

        # Transcript button
        def gen_transcript(res=r, crs=course):
            self._generate_transcript_for(res, crs)

        ctk.CTkButton(card, text="Transcript", fg_color=SURFACE2, hover_color=BORDER,
                      text_color=ACCENT2, corner_radius=6, width=90, height=28,
                      font=ctk.CTkFont(family="Courier", size=10),
                      command=gen_transcript).grid(row=0, column=3, padx=(4, 14))

    def _generate_transcript_for(self, result, course):
        """Generate transcript for a student across all their courses."""
        roll = result.get("roll_no", "")
        session = result.get("session", "")
        all_results = db.get_student_results(roll, session)

        if not all_results:
            messagebox.showinfo("No Data", "No multi-course data found for this student.")
            return

        student_info = {
            "name": result.get("name", ""),
            "roll_no": roll,
            "father_name": result.get("father_name", ""),
            "cnic": result.get("cnic", ""),
            "session": session,
            "dept_name": course.get("dept_name", ""),
        }

        out_dir = os.path.expanduser("~")
        filename = f"Transcript_{roll}_{session}.pdf"
        out_path = os.path.join(out_dir, filename)

        try:
            tr.generate_transcript(student_info, all_results, out_path)
            messagebox.showinfo("Success", f"Transcript saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate transcript:\n{e}")

    # ──────────────────────── STUDENT LOOKUP ─────────────────────────────────

    def _page_students(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Student Lookup", text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4))
        ctk.CTkLabel(frame, text="Search by Roll Number and Session",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).grid(
            row=1, column=0, sticky="w", padx=28, pady=(0, 12))

        search_card = card_frame(frame)
        search_card.grid(row=2, column=0, sticky="ew", padx=24, pady=8)

        srow = ctk.CTkFrame(search_card, fg_color="transparent")
        srow.pack(padx=14, pady=14, fill="x")

        ctk.CTkLabel(srow, text="Roll#:", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(0, 6))
        self._roll_entry = ctk.CTkEntry(srow, placeholder_text="e.g. 109290",
                                        fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
                                        placeholder_text_color=MUTED, corner_radius=8, height=36, width=140,
                                        font=ctk.CTkFont(family="Courier", size=12))
        self._roll_entry.pack(side="left", padx=6)

        ctk.CTkLabel(srow, text="Session:", text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(8, 6))
        self._sess_entry = ctk.CTkEntry(srow, placeholder_text="e.g. 2025-2029",
                                        fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
                                        placeholder_text_color=MUTED, corner_radius=8, height=36, width=120,
                                        font=ctk.CTkFont(family="Courier", size=12))
        self._sess_entry.pack(side="left", padx=6)

        ctk.CTkButton(srow, text="Search →", fg_color=ACCENT, hover_color="#3a78e0",
                      text_color="white", corner_radius=8, height=36, width=100,
                      font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                      command=self._do_student_search).pack(side="left", padx=10)

        self._student_result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self._student_result_frame.grid(row=3, column=0, sticky="ew", padx=24, pady=8)
        self._student_result_frame.grid_columnconfigure(0, weight=1)

        self._roll_entry.bind("<Return>", lambda e: self._do_student_search())
        self._sess_entry.bind("<Return>", lambda e: self._do_student_search())

    def _do_student_search(self):
        for w in self._student_result_frame.winfo_children():
            w.destroy()

        roll = self._roll_entry.get().strip()
        sess = self._sess_entry.get().strip()
        if not roll:
            return

        results = db.get_student_results(roll, sess)
        if not results:
            ctk.CTkLabel(self._student_result_frame,
                         text="No results found for this roll number / session.",
                         text_color=DANGER,
                         font=ctk.CTkFont(family="Courier", size=12)).grid(
                row=0, column=0, pady=20, padx=4, sticky="w")
            return

        # Student header
        r0 = results[0]
        gpa = compute_gpa(results)
        gpa_col = gpa_color(gpa)

        profile = card_frame(self._student_result_frame)
        profile.grid(row=0, column=0, sticky="ew", pady=6)
        profile.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(profile, text=r0.get("name", "—"), text_color=TEXT,
                     font=ctk.CTkFont(family="Courier", size=18, weight="bold")).grid(
            row=0, column=0, padx=16, pady=(12, 2), sticky="w")
        ctk.CTkLabel(profile,
                     text=f"Roll: {r0.get('roll_no','—')}  |  CNIC: {r0.get('cnic','—')}  |  Session: {r0.get('session','')}",
                     text_color=MUTED,
                     font=ctk.CTkFont(family="Courier", size=10)).grid(
            row=1, column=0, padx=16, pady=(0, 12), sticky="w")

        # GPA gauge
        gw, gh = 150, 80
        gc_widget = tk.Canvas(profile, width=gw, height=gh, bg=SURFACE, highlightthickness=0)
        gc_widget.grid(row=0, column=1, rowspan=2, padx=16, pady=8)
        gc_widget.after(50, lambda: draw_gpa_gauge(gc_widget, gw//2, gh - 12, 55, gpa))

        ctk.CTkLabel(profile, text=f"CGPA: {gpa:.2f}", text_color=gpa_col,
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold")).grid(
            row=0, column=2, padx=16, pady=12)

        # Transcript button
        def gen():
            student_info = {
                "name": r0.get("name",""),
                "roll_no": roll,
                "father_name": r0.get("father_name",""),
                "cnic": r0.get("cnic",""),
                "session": r0.get("session",""),
                "dept_name": r0.get("dept_name",""),
            }
            out_path = os.path.join(os.path.expanduser("~"), f"Transcript_{roll}.pdf")
            try:
                tr.generate_transcript(student_info, results, out_path)
                messagebox.showinfo("Transcript", f"Saved to:\n{out_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(profile, text="Export Transcript", fg_color=ACCENT2, hover_color="#8b72e0",
                      text_color="white", corner_radius=8, height=36, width=140,
                      font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
                      command=gen).grid(row=1, column=2, padx=16)

        # Course results
        for i, r in enumerate(results):
            rc = card_frame(self._student_result_frame)
            rc.grid(row=i+1, column=0, sticky="ew", pady=3)
            rc.grid_columnconfigure(0, weight=1)

            grade = r.get("grade","—")
            status = r.get("status","—")
            g_col = grade_color(grade)
            s_col = ACCENT3 if status=="Pass" else DANGER

            ctk.CTkLabel(rc, text=f"{r.get('code','?')}  —  {r.get('title','?')[:40]}",
                         text_color=TEXT,
                         font=ctk.CTkFont(family="Courier", size=11, weight="bold")).grid(
                row=0, column=0, padx=14, pady=(8,2), sticky="w")
            ctk.CTkLabel(rc,
                         text=f"Total: {r.get('total_obtained',0):.0f}  |  {r.get('percentage',0):.1f}%  |  Credits: {r.get('credit_hours_raw',r.get('credit_hours','?'))}",
                         text_color=MUTED,
                         font=ctk.CTkFont(family="Courier", size=9)).grid(
                row=1, column=0, padx=14, pady=(0,8), sticky="w")

            ctk.CTkLabel(rc, text=grade, text_color=g_col,
                         font=ctk.CTkFont(family="Courier", size=18, weight="bold")).grid(
                row=0, column=1, padx=10, rowspan=2)
            ctk.CTkLabel(rc, text=status, text_color=s_col,
                         font=ctk.CTkFont(family="Courier", size=10, weight="bold")).grid(
                row=0, column=2, padx=(0, 14), rowspan=2)
