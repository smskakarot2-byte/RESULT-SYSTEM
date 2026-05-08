from typing import Tuple


# GCUF Grading Scale
GRADE_SCALE = [
    (90, 100, "A",  4.00),
    (85,  89, "A-", 3.67),
    (80,  84, "B+", 3.33),
    (75,  79, "B",  3.00),
    (70,  74, "B-", 2.67),
    (65,  69, "C+", 2.33),
    (60,  64, "C",  2.00),
    (55,  59, "C-", 1.67),
    (50,  54, "D",  1.33),
    (45,  49, "D-", 1.00),
    ( 0,  44, "F",  0.00),
]

GRADE_COLORS = {
    "A":  "#34d399",
    "A-": "#4ade80",
    "B+": "#86efac",
    "B":  "#4f8ef7",
    "B-": "#60a5fa",
    "C+": "#a78bfa",
    "C":  "#c084fc",
    "C-": "#fb923c",
    "D":  "#fbbf24",
    "D-": "#f87171",
    "F":  "#ef4444",
}


def compute_grade(percentage: float) -> Tuple[str, float, str]:
    """Returns (grade_letter, grade_point, status)."""
    for low, high, letter, gp in GRADE_SCALE:
        if low <= percentage <= high:
            status = "Fail" if letter == "F" else "Pass"
            return letter, gp, status
    if percentage > 100:
        return "A", 4.00, "Pass"
    return "F", 0.00, "Fail"


def compute_percentage(total_obtained: float, max_marks: float) -> float:
    if max_marks <= 0:
        return 0.0
    return round((total_obtained / max_marks) * 100, 2)


def compute_gpa(results: list) -> float:
    """
    results: list of dicts with keys: grade_point, credit_hours, status
    Failure rule: if status == 'Fail', grade_point counts as 0.00
    """
    total_weighted = 0.0
    total_credits = 0.0
    for r in results:
        ch = float(r.get("credit_hours", 0))
        gp = float(r.get("grade_point", 0)) if r.get("status") == "Pass" else 0.0
        total_weighted += gp * ch
        total_credits += ch
    if total_credits == 0:
        return 0.0
    return round(total_weighted / total_credits, 2)


def parse_credit_hours(raw: str) -> float:
    """Parse '3(2-1)' → 3.0, or '3' → 3.0"""
    raw = raw.strip()
    if "(" in raw:
        return float(raw.split("(")[0].strip())
    try:
        return float(raw)
    except ValueError:
        return 3.0


def grade_color(grade: str) -> str:
    return GRADE_COLORS.get(grade, "#6b7280")


def gpa_color(gpa: float) -> str:
    if gpa >= 3.5:
        return "#34d399"
    elif gpa >= 3.0:
        return "#4f8ef7"
    elif gpa >= 2.5:
        return "#a78bfa"
    elif gpa >= 2.0:
        return "#fb923c"
    else:
        return "#f87171"
