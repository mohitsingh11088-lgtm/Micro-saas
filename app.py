import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SEO SaaS MVP",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "admin123",
        "seo": "seo123"
    }


# -----------------------------
# CLEAN NUMBER
# -----------------------------
def clean_number(value):
    try:
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            value = value.replace("%", "").strip()
        return float(value)
    except:
        return 0


# -----------------------------
# SEO ANALYSIS ENGINE
# -----------------------------
def analyze(clicks, impressions, ctr, position):

    score = 0
    actions = []

    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve title & meta (low CTR)")

    if position > 10:
        score += 30
        actions.append("Improve content depth & SEO structure")

    if clicks < 10:
        score += 20
        actions.append("Expand content + add FAQs")

    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():

    st.title("🔐 Login to SEO SaaS")

    with st.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            users = st.session_state.users

            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful ✔")
                st.rerun()
            else:
                st.error("Invalid credentials")


# -----------------------------
# SIGNUP PAGE
# -----------------------------
def signup_page():

    st.title("🆕 Create Account")

    with st.container():
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Sign Up"):

            if new_user in st.session_state.users:
                st.error("User already exists")
            elif new_user == "" or new_pass == "":
                st.warning("Fill all fields")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created! Go to login.")


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():

    st.sidebar.title(f"👋 Welcome {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    st.title("🚀 SEO Intelligence Dashboard")
    st.caption("Upload GSC CSV and get insights")

    uploaded_file = st.file_uploader("Upload Google Search Console CSV", type=["csv"])

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Raw Data Preview")
        st.dataframe(df, use_container_width=True)

        results = []

        for _, row in df.iterrows():

            clicks = clean_number(row.get("Clicks", 0))
            impressions = clean_number(row.get("Impressions", 0))
            ctr = clean_number(str(row.get("CTR", 0)).replace("%", ""))
            position = clean_number(row.get("Position", 0))

            priority, actions = analyze(clicks, impressions, ctr, position)

            results.append({
                "Page": row.get("Top pages", "Unknown"),
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Priority": priority,
                "Recommendations": " | ".join(actions)
            })

        st.subheader("📊 SEO Insights")

        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True
        )

        st.download_button(
            "📥 Download Report",
            pd.DataFrame(results).to_csv(index=False),
            "seo_report.csv",
            mime="text/csv"
        )


# -----------------------------
# MAIN APP ROUTER
# -----------------------------
def main():

    if st.session_state.logged_in:
        dashboard()
    else:
        menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

        if menu == "Login":
            login_page()
        else:
            signup_page()


main()
