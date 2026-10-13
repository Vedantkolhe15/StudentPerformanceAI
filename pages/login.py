import streamlit as st


st.set_page_config(
    page_title="Login - Student Performance AI",
    page_icon="🔐",
    layout="centered"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .login-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-top: 30px;
    }

    .login-subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------

st.markdown(
    '<div class="login-title">🔐 Student Performance AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="login-subtitle">'
    'Academic Analytics & Performance Management System'
    '</div>',
    unsafe_allow_html=True
)


with st.form("login_form"):

    username = st.text_input(
        "👤 Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter password"
    )

    login_button = st.form_submit_button(
        "🔐 Login",
        width="stretch"
    )


if login_button:

    if username == "admin" and password == "admin123":

        st.success(
            "Login successful! Welcome Admin."
        )

        st.session_state["logged_in"] = True
        st.session_state["username"] = username

        st.info(
            "You can now access the Student Performance AI dashboard."
        )

    else:

        st.error(
            "❌ Invalid username or password."
        )


st.markdown("---")

st.caption(
    "Demo Login: Username = admin | Password = admin123"
)