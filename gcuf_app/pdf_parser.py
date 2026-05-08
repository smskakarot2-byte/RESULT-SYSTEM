import re
import pdfplumber
from typing import Optional
from grading import compute_percentage, compute_grade, parse_credit_hours


def _extract_value(text: str, pattern: str, default: str = "") -> str:
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else default


def parse_award_sheet(pdf_path: str) -> dict:
    """
    Parse a GCUF Detailed Award Sheet PDF.
    Returns:
      {
        'header': {department, course_code, course_title, session, credit_hours_raw,
                   credit_hours, max_marks, semester},
        'students': [ {roll_no, name, father_name, cnic, session, attempt,
                       internal, mid_term, final_term, practical,
                       total_obtained, percentage, grade, grade_point, status}, ...]
      }
    """
    students = []
    header = {}

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += (page.extract_text() or "") + "\n"

        # ── Header extraction ──────────────────────────────────────
        header["department"] = _extract_value(
            full_text, r"Department\s*:\s*([^\n\r]+?)(?:\s{2,}|\s*Class\s*:)")
        if not header["department"]:
            header["department"] = _extract_value(full_text, r"Department\s*:\s*(.+?)(?:\n|Class)")

        header["course_code"] = _extract_value(
            full_text, r"Course\s+Code\s*:\s*([A-Z]{2,6}-?\d{3})")
        header["course_title"] = _extract_value(
            full_text, r"Course\s+Title\s*:\s*(.+?)(?:Credit|$)", "Unknown Course")
        header["course_title"] = re.sub(r'\s+', ' ', header["course_title"]).strip()

        header["session"] = _extract_value(
            full_text, r"Session\s*:\s*(\d{4}-\d{4})")
        header["semester"] = _extract_value(
            full_text, r"Semester\s*:\s*([\w\s]+?Semester)")

        ch_raw = _extract_value(full_text, r"Credit\s+Hours\s*:\s*([\d]+\([\d-]+\)|[\d.]+)")
        if not ch_raw:
            ch_raw = "3(2-1)"
        header["credit_hours_raw"] = ch_raw
        header["credit_hours"] = parse_credit_hours(ch_raw)

        mm = _extract_value(full_text, r"Max\s+Marks\s*:\s*([\d.]+)")
        header["max_marks"] = float(mm) if mm else 60.0

        # ── Table extraction ───────────────────────────────────────
        seen_rolls = set()

        for page in pdf.pages:
            tables = page.extract_tables()
            page_text = page.extract_text() or ""

            if tables:
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        # Flatten and clean cells
                        cells = [str(c).strip() if c else "" for c in row]

                        # Skip header rows
                        if any(kw in " ".join(cells).lower() for kw in
                               ["roll#", "sr#", "student name", "internal marks", "grade"]):
                            continue

                        # Try to find a valid row: at least need Roll# (numeric)
                        roll_no = None
                        row_data = {}

                        for i, cell in enumerate(cells):
                            # Look for numeric roll number (4-6 digits)
                            if re.match(r"^\d{4,7}$", cell):
                                roll_no = cell
                                # Typical column layout after roll:
                                # name, father_name, cnic, session, attempt,
                                # internal(4), mid(8), final(28), practical(20), total, pct, grade, status
                                remaining = cells[i+1:]

                                def safe_float(s):
                                    try:
                                        return float(s.replace("%","").replace(",",""))
                                    except (ValueError, AttributeError):
                                        return 0.0

                                name = remaining[0] if len(remaining) > 0 else ""
                                father_name = remaining[1] if len(remaining) > 1 else ""
                                cnic = remaining[2] if len(remaining) > 2 else ""
                                sess = remaining[3] if len(remaining) > 3 else header.get("session","")
                                # attempt is remaining[4] — skip
                                # marks start at index 5
                                marks_start = 5
                                internal  = safe_float(remaining[marks_start]   if len(remaining) > marks_start   else "0")
                                mid       = safe_float(remaining[marks_start+1] if len(remaining) > marks_start+1 else "0")
                                final_t   = safe_float(remaining[marks_start+2] if len(remaining) > marks_start+2 else "0")
                                practical = safe_float(remaining[marks_start+3] if len(remaining) > marks_start+3 else "0")

                                total_obtained = internal + mid + final_t + practical
                                max_marks = header.get("max_marks", 60.0)
                                pct = compute_percentage(total_obtained, max_marks)
                                grade, gp, status = compute_grade(pct)

                                # Clean name (sometimes multi-line names get merged)
                                name = re.sub(r'\s+', ' ', name).strip()
                                father_name = re.sub(r'\s+', ' ', father_name).strip()

                                row_data = {
                                    "roll_no": roll_no,
                                    "name": name,
                                    "father_name": father_name,
                                    "cnic": cnic,
                                    "session": sess if re.match(r"\d{4}-\d{4}", sess) else header.get("session", ""),
                                    "internal": internal,
                                    "mid_term": mid,
                                    "final_term": final_t,
                                    "practical": practical,
                                    "total_obtained": total_obtained,
                                    "percentage": pct,
                                    "grade": grade,
                                    "grade_point": gp,
                                    "status": status,
                                }
                                break

                        if roll_no and roll_no not in seen_rolls and row_data.get("name"):
                            seen_rolls.add(roll_no)
                            students.append(row_data)

            # Fallback: raw text line-by-line parsing
            if not students or len(students) < 1:
                for line in page_text.split("\n"):
                    line = line.strip()
                    m = re.match(
                        r"^\s*\d+\s+(\d{4,7})\s+(.+?)\s{3,}(.+?)\s{2,}(\d{2}-\d{3}-\d{7}-\d)\s+"
                        r"(\d{4}-\d{4})\s+\d+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", line)
                    if m:
                        roll_no = m.group(1)
                        if roll_no in seen_rolls:
                            continue
                        seen_rolls.add(roll_no)
                        internal  = float(m.group(6))
                        mid       = float(m.group(7))
                        final_t   = float(m.group(8))
                        practical = float(m.group(9))
                        total_obtained = internal + mid + final_t + practical
                        max_marks = header.get("max_marks", 60.0)
                        pct = compute_percentage(total_obtained, max_marks)
                        grade, gp, status = compute_grade(pct)
                        students.append({
                            "roll_no": roll_no,
                            "name": m.group(2).strip(),
                            "father_name": m.group(3).strip(),
                            "cnic": m.group(4),
                            "session": m.group(5),
                            "internal": internal,
                            "mid_term": mid,
                            "final_term": final_t,
                            "practical": practical,
                            "total_obtained": total_obtained,
                            "percentage": pct,
                            "grade": grade,
                            "grade_point": gp,
                            "status": status,
                        })

    return {"header": header, "students": students}
