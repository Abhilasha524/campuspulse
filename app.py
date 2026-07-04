import streamlit as st
import pandas as pd
from logic import load_csv, apply_risk_to_df, get_stats

st.set_page_config(page_title="CampusPulse", layout="centered")

st.title("CampusPulse")
st.caption("Student Risk Detection Tool — Upload a CSV to get started")
st.divider()

uploaded_file = st.file_uploader("Upload Student Data (CSV)", type=["csv"])

if uploaded_file is not None:

    df, error = load_csv(uploaded_file)

    if error:
        st.error(error)
        st.stop()

    df = apply_risk_to_df(df)
    stats = get_stats(df)

    #Summary Stats
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", stats["total"])
    col2.metric("High Risk", stats["high"])
    col3.metric("Medium Risk", stats["medium"])
    col4.metric("Avg Attendance", f"{stats['avg_attendance']}%")

    st.divider()

    # Risk Table
    st.subheader("Student Risk Summary")

    def color_risk(val):
        if val == "High Risk":
            return "color: red"
        elif val == "Medium Risk":
            return "color: orange"
        else:
            return "color: green"

    display_df = df[["student_name", "attendance_%", "avg_grade", "missed_assignments", "risk_score", "risk_level"]]
    styled = display_df.style.map(color_risk, subset=["risk_level"])
    st.dataframe(styled, use_container_width=True)

    st.divider()

    # Charts 
    st.subheader("Attendance by Student")
    st.bar_chart(df.set_index("student_name")["attendance_%"])

    st.subheader("Average Grade by Student")
    st.bar_chart(df.set_index("student_name")["avg_grade"])

    st.divider()

    # Filter: High Risk Only
    st.subheader("High Risk Students")
    high_risk_df = df[df["risk_level"] == "High Risk"][["student_name", "attendance_%", "avg_grade", "missed_assignments"]]

    if len(high_risk_df) == 0:
        st.success("No high risk students found.")
    else:
        st.warning(f"{len(high_risk_df)} student(s) flagged as High Risk")
        st.dataframe(high_risk_df, use_container_width=True)

else:
    st.info("Please upload a CSV file with columns: student_name, attendance_%, math_grade, science_grade, missed_assignments")

    st.subheader("Expected Format")
    sample = pd.DataFrame({
        "student_name": ["Riya Sharma", "Aman Verma", "Rohit Gupta"],
        "attendance_%": [92, 45, 30],
        "math_grade": [85, 40, 35],
        "science_grade": [78, 38, 40],
        "missed_assignments": [1, 8, 12]
    })
    st.dataframe(sample, use_container_width=True)