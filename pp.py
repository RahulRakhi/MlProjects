import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import plotly.express as px
import io

# --- Setup ---
st.set_page_config(page_title="🎯 Career Guidance Dashboard", layout="wide")
st.title("🎓 Student Career Guidance System")
st.markdown("Predict your Dream Job Score and assess your Job Readiness based on your skills.")

# --- Simulate Dataset ---
@st.cache_data
def generate_data():
    np.random.seed(42)
    num_samples = 20
    data = {
        "GPA": np.round(np.random.uniform(6.0, 10.0, num_samples), 2),
        "Projects": np.random.randint(0, 6, num_samples),
        "Communication_Score": np.random.randint(1, 11, num_samples),
        "Internships": np.random.randint(0, 3, num_samples),
        "Coding_Skills_Score": np.random.randint(1, 11, num_samples),
    }
    coefficients = [7, 5, 3, 6, 8]
    intercept = 20
    noise = np.random.normal(0, 5, num_samples)
    data["Dream_Job_Score"] = (
        data["GPA"] * coefficients[0]
        + data["Projects"] * coefficients[1]
        + data["Communication_Score"] * coefficients[2]
        + data["Internships"] * coefficients[3]
        + data["Coding_Skills_Score"] * coefficients[4]
        + intercept
        + noise
    ).astype(int)
    return pd.DataFrame(data)

df = generate_data()

# --- Train Model ---
X = df.drop("Dream_Job_Score", axis=1)
y = df["Dream_Job_Score"]
model = LinearRegression()
model.fit(X, y)

# --- Sidebar Input ---
st.sidebar.header("📋 Enter Your Profile")

user_gpa = st.sidebar.slider("GPA", 6.0, 10.0, step=0.1)
user_projects = st.sidebar.slider("Projects Completed", 0, 10)
user_communication = st.sidebar.slider("Communication Score", 1, 10)
user_internships = st.sidebar.slider("Number of Internships", 0, 3)
user_coding = st.sidebar.slider("Coding Skills Score", 1, 10)

user_input = np.array([[user_gpa, user_projects, user_communication, user_internships, user_coding]])
predicted_score = model.predict(user_input)[0]

# --- Dream Job Prediction ---
st.subheader("🎯 Dream Job Score Prediction")
st.success(f"Your Predicted Dream Job Score: **{predicted_score:.2f}/100**")

# --- Suggested Career Role ---
def suggest_role(score):
    if score >= 90:
        return "🧠 AI/ML Engineer, Research Scientist"
    elif score >= 75:
        return "💻 Full Stack Developer, Data Analyst"
    elif score >= 60:
        return "🔧 QA Engineer, Support Engineer"
    else:
        return "📘 Continue Learning, Explore Internships"

career = suggest_role(predicted_score)
st.info(f"✅ Suggested Career Path: **{career}**")

# --- Readiness Score Calculation ---
def compute_readiness(gpa, projects, comm, intern, coding):
    gpa_score = (gpa / 10) * 100
    proj_score = (projects / 10) * 100
    comm_score = (comm / 10) * 100
    intern_score = (intern / 3) * 100
    coding_score = (coding / 10) * 100

    readiness_score = (
        gpa_score * 0.20 +
        proj_score * 0.20 +
        comm_score * 0.15 +
        intern_score * 0.15 +
        coding_score * 0.30
    )
    return readiness_score, {
        "GPA": gpa_score,
        "Projects": proj_score,
        "Communication": comm_score,
        "Internships": intern_score,
        "Coding Skills": coding_score
    }

readiness_score, breakdown = compute_readiness(user_gpa, user_projects, user_communication, user_internships, user_coding)

# --- Job Readiness Report ---
st.subheader("🧭 Job Readiness Report")
st.info(f"**Your Job Readiness Score:** {readiness_score:.2f}/100")

# --- Strengths & Weaknesses ---
strengths = [k for k, v in breakdown.items() if v >= 75]
weaknesses = [k for k, v in breakdown.items() if v < 50]

st.write("### ✅ Strength Areas:")
st.write(", ".join(strengths) if strengths else "No strong areas yet.")

st.write("### ⚠️ Areas to Improve:")
st.write(", ".join(weaknesses) if weaknesses else "You're doing well in all areas!")

# --- Tips Section ---
st.markdown("### 💡 Personalized Tips:")
if "Coding Skills" in weaknesses:
    st.write("- Practice coding on LeetCode, HackerRank, or Codeforces.")
if "Communication" in weaknesses:
    st.write("- Join a speaking club, take communication courses, practice interviews.")
if "Projects" in weaknesses:
    st.write("- Start simple GitHub projects or join hackathons.")
if "Internships" in weaknesses:
    st.write("- Apply on LinkedIn, Internshala, or college placement cell.")
if "GPA" in weaknesses:
    st.write("- Plan studies, attend classes, and use Notion or calendar to track study goals.")

# --- Radar Chart Visualization ---
with st.expander("📊 Visual Skill Balance (Radar Chart)"):
    radar_df = pd.DataFrame(dict(
        Skill=list(breakdown.keys()),
        Score=list(breakdown.values())
    ))
    fig_radar = px.line_polar(radar_df, r='Score', theta='Skill', line_close=True)
    fig_radar.update_traces(fill='toself')
    fig_radar.update_layout(height=400, width=600)
    st.plotly_chart(fig_radar)

# --- View Sample Dataset ---
with st.expander("📂 Sample Student Data"):
    st.dataframe(df)

# --- Coefficient Display ---
with st.expander("📈 Model Insights"):
    st.write(dict(zip(X.columns, model.coef_)))

# --- Download Data Button ---
with st.expander("⬇️ Download Simulated Data"):
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='StudentData')
    st.download_button("📥 Download Excel File", data=output.getvalue(),
                       file_name="student_dream_job_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
