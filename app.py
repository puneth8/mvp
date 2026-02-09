import streamlit as st
import pandas as pd

from database import create_tables, get_connection
from auth import register_user, login_user
from admin_auth import admin_login

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Job Recommendation Portal", layout="wide")
create_tables()

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "admin" not in st.session_state:
    st.session_state.admin = None

# ---------------- SIDEBAR MODE ----------------
st.sidebar.title("🔐 Portal Access")
mode = st.sidebar.radio("Login as", ["User", "Admin"])

# =================================================
# ================= ADMIN LOGIN ===================
# =================================================
if mode == "Admin" and st.session_state.admin is None:
    st.title("🛡️ Admin Control Panel Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        admin_user = st.text_input("Admin Username")
        admin_pass = st.text_input("Password", type="password")

        if st.button("🚀 Login as Admin", use_container_width=True):
            admin = admin_login(admin_user, admin_pass)
            if admin:
                st.session_state.admin = admin
                st.success("Welcome Admin!")
                st.rerun()

            else:
                st.error("Invalid Admin Credentials")

    st.stop()

# =================================================
# ================= ADMIN DASHBOARD ===============
# =================================================
if st.session_state.admin:
    st.title("📊 Admin Dashboard")

    conn = get_connection()
    users_df = pd.read_sql("SELECT id, username, skills, interest, experience FROM users", conn)
    rec_df = pd.read_sql("SELECT * FROM recommendations", conn)
    conn.close()

    # ---- METRICS ----
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Total Users", len(users_df))
    c2.metric("📌 Total Recommendations", len(rec_df))
    c3.metric("🔥 Active Jobs", 15)

    # ---- CHARTS ----
    st.subheader("📈 Recommendation Trends")
    if not rec_df.empty:
        st.bar_chart(rec_df.groupby("job_title").count()["id"])

    st.subheader("🎯 User Career Interests")
    if not users_df.empty:
        interest_counts = users_df["interest"].value_counts()
        st.bar_chart(interest_counts)
    else:
        st.info("No user interest data available")


    # ---- TABLES ----
    st.subheader("👤 Registered Users")
    st.dataframe(users_df, use_container_width=True)

    st.subheader("🗂 Recommendation Logs")
    st.dataframe(rec_df, use_container_width=True)

    if st.sidebar.button("🚪 Logout Admin"):
        st.session_state.admin = None
        st.rerun()


    st.stop()

# =================================================
# ================= USER LOGIN ====================
# =================================================
st.title("🚀 Smart Internship & Job Recommendation System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if st.session_state.user is None:
    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid credentials")

    else:
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")

        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful. Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# =================================================
# ================= USER DASHBOARD ================
# =================================================
jobs = pd.read_csv("jobs.csv")
user = st.session_state.user
user_id = user[0]

st.sidebar.header("🧑 User Profile")

user_skills = st.sidebar.text_input("Enter your skills (comma separated)", user[3] or "")
preferred_location = st.sidebar.selectbox("Preferred Location", jobs['location'].unique())
career_interest = st.sidebar.selectbox("Career Interest", jobs['interest'].unique())
experience = st.sidebar.slider("Your Experience (years)", 0, 3, user[6] or 0)

st.sidebar.markdown("---")
min_score_filter = st.sidebar.slider("Minimum Match Score to Display", 0, 20, 5)

# ---------------- MATCHING LOGIC ----------------
def calculate_score(job, skills, location, interest, exp):
    score = 0
    reasons = []

    job_skills = job['skills'].lower().split(", ")

    skill_matches = [skill for skill in skills if skill in job_skills]
    score += len(skill_matches) * 3
    if skill_matches:
        reasons.append(f"Skill match: {', '.join(skill_matches)}")

    if job['location'].lower() == location.lower():
        score += 4
        reasons.append("Preferred location match")

    if job['interest'].lower() == interest.lower():
        score += 5
        reasons.append("Career interest match")

    if job['experience'] <= exp:
        score += 4
        reasons.append("Experience suitable")

    return score, reasons

# ---------------- FIND JOBS ----------------
if st.button("🔍 Find Best Matches"):
    skills_list = [s.strip().lower() for s in user_skills.split(",")]

    results = []

    for _, job in jobs.iterrows():
        score, reasons = calculate_score(
            job, skills_list, preferred_location, career_interest, experience
        )
        if score >= min_score_filter:
            results.append({
                "Title": job['title'],
                "Company": job['company'],
                "Location": job['location'],
                "Score": score,
                "Why Recommended": ", ".join(reasons)
            })

    if results:
        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        # ---- SAVE TO DB ----
        conn = get_connection()
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO recommendations (user_id, job_title, company, score)
                VALUES (?, ?, ?, ?)
            """, (user_id, row["Title"], row["Company"], row["Score"]))
        conn.commit()
        conn.close()

        st.subheader("🏆 Top Recommendations")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Match Score Distribution")
        st.bar_chart(df.set_index("Title")["Score"])

    else:
        st.warning("No jobs match your criteria. Try adjusting filters.")

# ---------------- HISTORY ----------------
st.subheader("🕘 Your Recommendation History")

conn = get_connection()
history = pd.read_sql_query(
    f"SELECT job_title, company, score FROM recommendations WHERE user_id={user_id}",
    conn
)
conn.close()

if not history.empty:
    st.dataframe(history, use_container_width=True)
else:
    st.info("No recommendations yet")
