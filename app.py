import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEO SaaS MVP", layout="wide")

# -----------------------------
# SESSION INIT
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
# DEBUG (optional - remove later)
# -----------------------------
# st.write(st.session_state.users)


# -----------------------------
# CLEAN NUMBER
# -----------------------------
def clean_number(v):
    try:
        if pd.isna(v):
            return 0
        return float(str(v).replace("%", "").strip())
    except:
        return 0


# -----------------------------
# SEO ENGINE
# -----------------------------
def analyze(clicks, impressions, ctr, position):

    score = 0
    actions = []

    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve title/meta (CTR issue)")

    if position > 10:
        score += 30
        actions.append("Improve content depth")

    if clicks < 10:
        score += 20
        actions.append("Expand content")

    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# LOGIN
# -----------------------------
def login():

    st.title("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):

        users = st.session_state.users

        # DEBUG HELP
        # st.write("Users:", users)

        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful ✔")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


# -----------------------------
# SIGNUP (FIXED)
# -----------------------------
def signup():

    st.title("🆕 Sign Up")

    new_user = st.text_input("Create Username", key="signup_user")
    new_pass = st.text_input("Create Password", type="password", key="signup_pass")

    if st.button("Create Account"):

        # IMPORTANT: always read latest state
        users = st.session_state.users.copy()

        if new_user in users:
            st.error("User already exists")
            return

        if new_user.strip() == "" or new_pass.strip() == "":
            st.warning("Please fill all fields")
            return

        # SAVE USER PROPERLY
        users[new_user] = new_pass
        st.session_state.users = users

        st.success("Account created ✔ Now login")


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():

    st.sidebar.title(f"👋 {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    st.title("🚀 SEO Dashboard")

    file = st.file_uploader("Upload GSC CSV", type=["csv"])

    if file:

        df = pd.read_csv(file)
        st.dataframe(df, use_container_width=True)

        results = []

        for _, row in df.iterrows():

            clicks = clean_number(row.get("Clicks", 0))
            impressions = clean_number(row.get("Impressions", 0))
            ctr = clean_number(row.get("CTR", 0))
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

        out = pd.DataFrame(results)

        st.subheader("📊 SEO Insights")
        st.dataframe(out, use_container_width=True)

        st.download_button(
            "📥 Download Report",
            out.to_csv(index=False),
            "seo_report.csv",
            mime="text/csv"
        )


# -----------------------------
# ROUTER
# -----------------------------
def main():

    if st.session_state.logged_in:
        dashboard()
    else:
        menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

        if menu == "Login":
            login()
        else:
            signup()


main()
