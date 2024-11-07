import streamlit as st

st.set_page_config(layout="wide")

# Define translations
translations = {
    'en': {
        'language_selection': "Language selection",
        'to_be_implemented': "To be implemented ...",
        'navigation': "Navigation",
        'pages': "Pages: ",
        'guides': "Guides",
        'user_manual_us': "User manual (UK/US)",
        'user_manual_ru': "Руководство (RU)"
    },
    'ru': {
        'language_selection': "Выбор языка",
        'to_be_implemented': "Будет реализовано ...",
        'navigation': "Навигация",
        'pages': "Страницы: ",
        'guides': "Руководства",
        'user_manual_us': "Руководство пользователя (UK/US)",
        'user_manual_ru': "Руководство (RU)"
    },
    'de': {
        'language_selection': "Sprachauswahl",
        'to_be_implemented': "Wird implementiert ...",
        'navigation': "Navigation",
        'pages': "Seiten: ",
        'guides': "Anleitungen",
        'user_manual_us': "Benutzerhandbuch (UK/US)",
        'user_manual_ru': "Ratgeber (RU)"
    }
}

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
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'  # Default language

st.session_state["hf_token"] = st.secrets.hf_token
st.session_state["px_token"] = st.secrets.px_token

style = """
<style>
    div[role='radiogroup'] > label > div:first-of-type {
        display: none;
    }

    div[role='radiogroup'] > label {
        display: block;
        padding: 5px;
        color: inherit;
    }

    div[role='radiogroup'] > label:hover {
        background-color: transparent;
        color: #FF4B4B;
    }

    div[role='radiogroup'] > label.selected {
        color: #FF4B4B !important;
        background-color: transparent;
        border: none;
        background: red !important;
    }

    div[role='radiogroup'] > label {
        cursor: pointer;
    }
</style>
"""
st.markdown(style, unsafe_allow_html=True)

# Define paths to the pages
PAGE_PATHS = {
    "About us ℹ️": "welcome_page.py",
    "Account 👤": "login.py",
    "Settings ⚙️": "config.py",
    "Generate ✨": "interface.py",
    "Build 🛠️": "construct.py",
    "Edit 👨‍💻": "editor.py"
}

def load_page(path):
    with open(path, 'r') as file:
        page_code = file.read()
    exec(page_code, globals())

def main():
    st.sidebar.title(translations[st.session_state.lang]['language_selection'])
    st.session_state.lang = st.sidebar.selectbox('Select Language', ['en', 'ru', 'de'], index=['en', 'ru', 'de'].index(st.session_state.lang), key="randomkey")
    st.sidebar.divider()
    st.sidebar.title(translations[st.session_state.lang]['navigation'])
    selection = st.sidebar.radio(translations[st.session_state.lang]['pages'], list(PAGE_PATHS.keys()))

    st.sidebar.divider()
    
    st.sidebar.title(translations[st.session_state.lang]['guides'])
    st.sidebar.link_button(label=translations[st.session_state.lang]['user_manual_us'], url="https://github.com/Wafflelover404/WebWizz/blob/main/ExtraFiles/guides/en.md")
    st.sidebar.link_button(label=translations[st.session_state.lang]['user_manual_ru'], url="https://github.com/Wafflelover404/WebWizz/blob/main/ExtraFiles/guides/ru.md")

    # Load and display the selected page
    page_path = PAGE_PATHS[selection]
    load_page(page_path)

if __name__ == "__main__":
    main()