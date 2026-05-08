import os
from fpdf import FPDF
from grading import compute_gpa


def generate_transcript(student_info: dict, results: list, output_path: str) -> str:
    """
    Generate a professional PDF transcript for a student.
    student_info: {name, roll_no, father_name, cnic, session, dept_name}
    results: list of result dicts with course info
    """

    class TranscriptPDF(FPDF):
        def header(self):
            # Header bar
            self.set_fill_color(10, 11, 15)
            self.rect(0, 0, 210, 32, "F")

            self.set_font("Helvetica", "B", 14)
            self.set_text_color(79, 142, 247)
            self.set_xy(10, 6)
            self.cell(0, 7, "GOVERNMENT COLLEGE UNIVERSITY FAISALABAD", ln=True, align="C")

            self.set_font("Helvetica", "", 9)
            self.set_text_color(200, 200, 200)
            self.set_x(10)
            self.cell(0, 5, "Academic Transcript — Official Document", ln=True, align="C")

            self.set_font("Helvetica", "B", 10)
            self.set_text_color(167, 139, 250)
            self.set_x(10)
            self.cell(0, 5, "DETAILED RESULT CARD", ln=True, align="C")

            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"Page {self.page_no()} — Powered by GCUF Result Management System", align="C")

    pdf = TranscriptPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Student Info Block ─────────────────────────────────────────
    pdf.set_fill_color(17, 19, 24)
    pdf.set_draw_color(34, 38, 47)
    pdf.set_line_width(0.3)
    pdf.rect(10, pdf.get_y(), 190, 36, "FD")

    y = pdf.get_y() + 4
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(232, 234, 240)
    pdf.set_xy(14, y)
    pdf.cell(0, 7, student_info.get("name", "—").upper(), ln=True)

    y += 8
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(107, 114, 128)

    info_pairs = [
        ("Roll No",     student_info.get("roll_no", "—")),
        ("Father Name", student_info.get("father_name", "—")),
        ("CNIC",        student_info.get("cnic", "—")),
        ("Session",     student_info.get("session", "—")),
        ("Department",  student_info.get("dept_name", "—")),
    ]
    col_w = 94
    for i, (label, val) in enumerate(info_pairs):
        col = i % 2
        row = i // 2
        x = 14 + col * col_w
        cy = y + row * 7
        pdf.set_xy(x, cy)
        pdf.set_text_color(107, 114, 128)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(28, 5, f"{label}:", ln=False)
        pdf.set_text_color(232, 234, 240)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(60, 5, str(val), ln=False)

    pdf.set_y(y + (((len(info_pairs) - 1) // 2) + 1) * 7 + 2)

    # ── GPA Summary ────────────────────────────────────────────────
    pdf.ln(4)
    gpa = compute_gpa(results)
    total_credits = sum(float(r.get("credit_hours", 0)) for r in results)
    passed = sum(1 for r in results if r.get("status") == "Pass")
    failed = sum(1 for r in results if r.get("status") == "Fail")

    # GPA box
    pdf.set_fill_color(79, 142, 247)
    bx, by = 10, pdf.get_y()
    pdf.rect(bx, by, 190, 18, "F")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(bx + 4, by + 2)
    pdf.cell(45, 6, f"CGPA: {gpa:.2f} / 4.00", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(220, 230, 255)
    pdf.cell(50, 6, f"Total Credits: {total_credits:.1f}", ln=False)
    pdf.cell(40, 6, f"Passed: {passed}", ln=False)
    pdf.cell(40, 6, f"Failed: {failed}", ln=True)
    pdf.ln(2)

    # ── Results Table ──────────────────────────────────────────────
    pdf.ln(2)
    headers = ["Code", "Course Title", "Cr.Hr", "Int", "Mid", "Final", "Pract", "Total", "%", "Grade", "Status"]
    col_widths = [18, 54, 10, 9, 9, 10, 10, 12, 12, 12, 14]

    # Table header
    pdf.set_fill_color(17, 19, 24)
    pdf.set_text_color(79, 142, 247)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_line_width(0.2)
    for h, w in zip(headers, col_widths):
        pdf.set_draw_color(34, 38, 47)
        pdf.cell(w, 7, h, border=1, align="C", fill=True)
    pdf.ln()

    # Rows
    for i, r in enumerate(results):
        fill_color = (24, 27, 35) if i % 2 == 0 else (17, 19, 24)
        pdf.set_fill_color(*fill_color)
        pdf.set_text_color(200, 205, 215)
        pdf.set_font("Helvetica", "", 7)

        status = r.get("status", "Pass")
        pass_color = (52, 211, 153) if status == "Pass" else (248, 113, 113)

        vals = [
            r.get("code", ""),
            r.get("title", "")[:30],
            str(r.get("credit_hours_raw", r.get("credit_hours", ""))),
            f"{r.get('internal_marks',0):.1f}",
            f"{r.get('mid_term',0):.1f}",
            f"{r.get('final_term',0):.1f}",
            f"{r.get('practical_work',0):.1f}",
            f"{r.get('total_obtained',0):.1f}",
            f"{r.get('percentage',0):.1f}%",
            r.get("grade", ""),
            status,
        ]
        for j, (v, w) in enumerate(zip(vals, col_widths)):
            if j == len(vals) - 1:
                pdf.set_text_color(*pass_color)
                pdf.set_font("Helvetica", "B", 7)
            elif j == len(vals) - 2:
                pdf.set_text_color(167, 139, 250)
                pdf.set_font("Helvetica", "B", 7)
            else:
                pdf.set_text_color(200, 205, 215)
                pdf.set_font("Helvetica", "", 7)
            pdf.cell(w, 6, str(v), border=1, align="C", fill=True)
        pdf.ln()

    # ── Signature Block ────────────────────────────────────────────
    pdf.ln(12)
    pdf.set_draw_color(50, 55, 65)
    pdf.set_line_width(0.3)

    sig_y = pdf.get_y()
    sig_positions = [14, 80, 146]
    sig_labels = ["Internal Exam Coordinator", "Department Chairperson", "Affiliation Cell"]
    for x, label in zip(sig_positions, sig_labels):
        pdf.line(x, sig_y + 10, x + 56, sig_y + 10)
        pdf.set_xy(x, sig_y + 11)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(56, 4, label, align="C")

    pdf.output(output_path)
    return output_path
