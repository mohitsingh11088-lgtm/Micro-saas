import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEO SaaS MVP", layout="wide")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""


# -----------------------------
# SIMPLE USER STORE (MVP ONLY)
# -----------------------------
users = {
    "admin": "admin123",
    "seo": "seo123"
}


# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():

    st.title("🔐 SEO SaaS Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful ✔")
            st.rerun()
        else:
            st.error("Invalid credentials")


# -----------------------------
# SIGNUP PAGE (SIMPLE DEMO)
# -----------------------------
def signup_page():

    st.title("🆕 Sign Up (Demo)")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Create Account"):

        if new_user in users:
            st.error("User already exists")
        else:
            users[new_user] = new_pass
            st.success("Account created! Go to login.")


# -----------------------------
# SEO DASHBOARD (MAIN APP)
# -----------------------------
def dashboard():

    st.sidebar.title(f"Welcome {st.session_state.user}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    st.title("🚀 SEO Intelligence Dashboard")

    uploaded_file = st.file_uploader("Upload GSC CSV", type=["csv"])

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.write("### 📄 Data Preview")
        st.dataframe(df)

        results = []

        for _, row in df.iterrows():

            clicks = float(row.get("Clicks", 0))
            impressions = float(row.get("Impressions", 0))
            ctr = float(str(row.get("CTR", 0)).replace("%", ""))
            position = float(row.get("Position", 0))

            score = 0
            actions = []

            if impressions > 1000 and ctr < 2:
                score += 40
                actions.append("Improve CTR (title/meta)")

            if position > 10:
                score += 30
                actions.append("Improve ranking content")

            if clicks < 10:
                score += 20
                actions.append("Expand content")

            priority = "LOW 🟢"
            if score >= 60:
                priority = "HIGH 🔴"
            elif score >= 30:
                priority = "MEDIUM 🟠"

            results.append({
                "Page": row.get("Top pages", "Unknown"),
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Priority": priority,
                "Recommendations": " | ".join(actions)
            })

        st.write("### 📊 SEO Insights")
        st.dataframe(pd.DataFrame(results), use_container_width=True)


# -----------------------------
# APP ROUTER
# -----------------------------
def main():

    menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

    if st.session_state.logged_in:
        dashboard()
    else:
        if menu == "Login":
            login_page()
        else:
            signup_page()


main()