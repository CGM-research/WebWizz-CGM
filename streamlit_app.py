import streamlit as st
st.set_page_config(layout="wide")

# Initialize session state with default values if they don't exist
if 'hf_token' not in st.session_state:
    st.session_state.hf_token = ""
if 'px_token' not in st.session_state:
    st.session_state.px_token = ""
if 'context' not in st.session_state:
    st.session_state.context = False
if 'db_path' not in st.session_state:
    st.session_state.db_path = './Data/DB/app.db'
if 'account' not in st.session_state:
    st.session_state.account = ""
if 'account_id' not in st.session_state:
    st.session_state.account_id = ""
if 'change' not in st.session_state:
    st.session_state.change = True

st.session_state["hf_token"] = st.secrets["hf_token"]
st.session_state["px_token"] = st.secrets["px_token"]

# Define paths to the pages
PAGE_PATHS = {
    "Welcome page !": "welcome_page.py",
    "Login": "login.py",
    "Configure": "config.py",
    "Generate a template": "interface.py",
    "Build a template": "construct.py",
    "Edit page": "editor.py"
}

def load_page(path):
    if path:
        with open(path, 'r') as file:
            page_code = file.read()
        exec(page_code, globals())

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Pages:", list(PAGE_PATHS.keys()))

    # Custom CSS styles for selected and non-selected options
    for key in PAGE_PATHS.keys():
        color = '#FF4B4B' if key == selection else 'inherit'
        style = f"""
        <style>
            div[role='radiogroup'] > label > div:first-of-type {{
                display: none;
            }}
            div[role='radiogroup'] > label:has(input[value='{key}']) {{
                color: {color} !important;
                cursor: pointer;
            }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)

    if selection:  # Only load page if an option is selected
        page_path = PAGE_PATHS[selection]
        load_page(page_path)

if __name__ == "__main__":
    main()