import pandas as pd

REQUIRED_COLUMNS = ["student_name", "attendance_%", "math_grade", "science_grade", "missed_assignments"]

def load_csv(file):
    """Load and validate uploaded CSV file."""
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return None, f"Missing columns: {', '.join(missing)}"
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"


def calculate_risk(row):
    """
    Risk scoring logic based on 3 factors:
    - Attendance %
    - Average grade
    - Missed assignments
    Returns: score (int), level (str)
    """
    score = 0

    # Factor 1: Attendance
    if row["attendance_%"] < 60:
        score += 2
    elif row["attendance_%"] < 75:
        score += 1

    # Factor 2: Average grade
    avg_grade = (row["math_grade"] + row["science_grade"]) / 2
    if avg_grade < 50:
        score += 2
    elif avg_grade < 65:
        score += 1

    # Factor 3: Missed assignments
    if row["missed_assignments"] > 10:
        score += 2
    elif row["missed_assignments"] > 5:
        score += 1

    # Map score to risk level
    if score >= 4:
        return score, "High Risk"
    elif score >= 2:
        return score, "Medium Risk"
    else:
        return score, "Low Risk"


def apply_risk_to_df(df):
    """Add risk score and risk level columns to dataframe."""
    df = df.copy()
    df["avg_grade"] = ((df["math_grade"] + df["science_grade"]) / 2).round(1)
    results = df.apply(calculate_risk, axis=1)
    df["risk_score"] = [r[0] for r in results]
    df["risk_level"] = [r[1] for r in results]
    return df


def get_stats(df):
    """Return basic summary statistics."""
    total = len(df)
    high = len(df[df["risk_level"] == "High Risk"])
    medium = len(df[df["risk_level"] == "Medium Risk"])
    low = len(df[df["risk_level"] == "Low Risk"])
    avg_attendance = round(df["attendance_%"].mean(), 1)
    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "avg_attendance": avg_attendance
    }