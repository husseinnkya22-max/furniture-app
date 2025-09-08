import streamlit as st

st.set_page_config(page_title='Furniture database system', page_icon='🛢️')

# --- Initialize login state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()  # rerun to go back to login form

# --- Login form ---
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    username = st.text_input("Name:", key="username_input")
    password = st.text_input("Password:", type="password", key="password_input")
    
    if st.button("Login"):
        if username == "Test" and password == "123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("⚠ Oops! Wrong credentials")

# --- Content after login ---
if st.session_state.logged_in:
    # Navigation pages
    create_page = st.Page('create.py', title='Create new entry', icon='➕')
    access_page = st.Page('access.py', title='Access database', icon='📋')
    
    # Add Sign Out button in sidebar (or navigation)
    with st.sidebar:
        if st.button("🚪 Sign Out"):
            logout()

    pg = st.navigation([create_page, access_page])
    pg.run()
