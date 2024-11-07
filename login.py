import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import os
import json
import bcrypt

# Define translations
translations = {
    'en': {
        'authentication': "Authentication",
        'create_new_account': "Create new account",
        'login_existing_account': "Login to existing account",
        'create_unique_username': "Create a unique username",
        'create_password': "Create a password",
        'password_short_warning': "Your password is shorter than 8 symbols.",
        'create_account_button': "Create account",
        'username_occupied_error': "The username is occupied.",
        'account_created_success': "Account created successfully!",
        'provide_username_password_error': "Please provide both a username and a password.",
        'username': "Username",
        'password': "Password",
        'login_button': "Login",
        'logged_in_success': "Logged in successfully!",
        'invalid_username_password_error': "Invalid username or password.",
        'my_projects': "My projects",
        'current_account': "Current account: {account}",
        'add_files_manually': "Add files manually",
        'upload_file': "Upload file",
        'write_file_manually': "Write file manually",
        'upload_your_html_file': "Upload your html file here.",
        'uploaded_file_name': "Uploaded file name: {filename}",
        'file_content': "File content:",
        'add_to_database': "Add to database",
        'enter_data_manually': "Enter data manually.",
        'filename': "Filename",
        'content': "Content",
        'existing_projects': "Existing projects",
        'no_files_found': "No files found for this user.",
        'export': "Export",
        'download_started': "Download started !",
        'edit': "Edit",
        'open_in_code_editor': "Open this file in code editor",
        'opened_in_web_editor': "Opened in Web Editor !"
    },
    'ru': {
        'authentication': "Аутентификация",
        'create_new_account': "Создать новый аккаунт",
        'login_existing_account': "Войти в существующий аккаунт",
        'create_unique_username': "Создайте уникальное имя пользователя",
        'create_password': "Создайте пароль",
        'password_short_warning': "Ваш пароль короче 8 символов.",
        'create_account_button': "Создать аккаунт",
        'username_occupied_error': "Имя пользователя занято.",
        'account_created_success': "Аккаунт успешно создан!",
        'provide_username_password_error': "Пожалуйста, предоставьте и имя пользователя, и пароль.",
        'username': "Имя пользователя",
        'password': "Пароль",
        'login_button': "Войти",
        'logged_in_success': "Успешный вход!",
        'invalid_username_password_error': "Неверное имя пользователя или пароль.",
        'my_projects': "Мои проекты",
        'current_account': "Текущий аккаунт: {account}",
        'add_files_manually': "Добавить файлы вручную",
        'upload_file': "Загрузить файл",
        'write_file_manually': "Написать файл вручную",
        'upload_your_html_file': "Загрузите ваш html файл здесь.",
        'uploaded_file_name': "Имя загруженного файла: {filename}",
        'file_content': "Содержимое файла:",
        'add_to_database': "Добавить в базу данных",
        'enter_data_manually': "Введите данные вручную.",
        'filename': "Имя файла",
        'content': "Содержимое",
        'existing_projects': "Существующие проекты",
        'no_files_found': "Файлы для этого пользователя не найдены.",
        'export': "Экспорт",
        'download_started': "Загрузка началась !",
        'edit': "Редактировать",
        'open_in_code_editor': "Открыть этот файл в редакторе кода",
        'opened_in_web_editor': "Открыто в веб-редакторе !"
    },
    'de': {
        'authentication': "Authentifizierung",
        'create_new_account': "Neues Konto erstellen",
        'login_existing_account': "In bestehendes Konto einloggen",
        'create_unique_username': "Erstellen Sie einen eindeutigen Benutzernamen",
        'create_password': "Erstellen Sie ein Passwort",
        'password_short_warning': "Ihr Passwort ist kürzer als 8 Zeichen.",
        'create_account_button': "Konto erstellen",
        'username_occupied_error': "Der Benutzername ist besetzt.",
        'account_created_success': "Konto erfolgreich erstellt!",
        'provide_username_password_error': "Bitte geben Sie sowohl einen Benutzernamen als auch ein Passwort an.",
        'username': "Benutzername",
        'password': "Passwort",
        'login_button': "Einloggen",
        'logged_in_success': "Erfolgreich eingeloggt!",
        'invalid_username_password_error': "Ungültiger Benutzername oder Passwort.",
        'my_projects': "Meine Projekte",
        'current_account': "Aktuelles Konto: {account}",
        'add_files_manually': "Dateien manuell hinzufügen",
        'upload_file': "Datei hochladen",
        'write_file_manually': "Datei manuell schreiben",
        'upload_your_html_file': "Laden Sie Ihre HTML-Datei hier hoch.",
        'uploaded_file_name': "Hochgeladener Dateiname: {filename}",
        'file_content': "Dateiinhalt:",
        'add_to_database': "Zur Datenbank hinzufügen",
        'enter_data_manually': "Daten manuell eingeben.",
        'filename': "Dateiname",
        'content': "Inhalt",
        'existing_projects': "Bestehende Projekte",
        'no_files_found': "Keine Dateien für diesen Benutzer gefunden.",
        'export': "Exportieren",
        'download_started': "Der Download wurde gestartet !",
        'edit': "Bearbeiten",
        'open_in_code_editor': "Diese Datei im Code-Editor öffnen",
        'opened_in_web_editor': "Im Web-Editor geöffnet !"
    }
}

# Create a header for the app
st.header(translations[st.session_state.lang]['authentication'])

# Create tabs for different login methods
tab1, tab2 = st.tabs([translations[st.session_state.lang]['create_new_account'], translations[st.session_state.lang]['login_existing_account']])

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = ""

# Initialize session state
if 'account_id' not in st.session_state:
    st.session_state.account_id = ""

# Debugging function
def debug_print(message):
    st.text(message)

# Access via st.secrets dictionary
salt = st.secrets["salt"].encode('utf-8')  # Convert salt to bytes

def hash_it_quick(password):
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 

    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt)

    # Return result 
    return hash

# Function to check if username exists
def username_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

# Function to verify login credentials
def verify_login(cursor, username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hashed_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)
    return False

def get_user_id_by_username(cursor, username):
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_file_ids_by_user_id(cursor, user_id):
    cursor.execute("SELECT file_id FROM user_files WHERE user_id = ?", (user_id,))
    result = cursor.fetchall()
    return [row[0] for row in result] if result else []

def get_file_data_as_json(cursor, file_id):
    cursor.execute("SELECT filename, source FROM files WHERE file_id = ?", (file_id,))
    result = cursor.fetchone()
    
    if result:
        file_data = {
            "file_id": file_id,
            "filename": result[0],
            "content": result[1].decode('utf-8') if isinstance(result[1], bytes) else result[1]
        }
        return json.dumps(file_data, indent=4)
    else:
        return json.dumps({"error": "File not found"}, indent=4)

# Ensure the database directory exists
db_path = st.session_state.db_path
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Initialize session state
if 'db_path' not in st.session_state:
    st.session_state.db_path = db_path

# Create or connect to the database and create tables
def initialize_database(db_path):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                source TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_files (
                user_id INTEGER,
                file_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(file_id) REFERENCES files(file_id),
                PRIMARY KEY(user_id, file_id)
            )
        """)
        db.commit()

initialize_database(db_path)

# Create new account tab
with tab1:
    st.subheader(translations[st.session_state.lang]['create_new_account'])
    create_username = st.text_input(translations[st.session_state.lang]['create_unique_username'], key="create_username")
    create_password = st.text_input(translations[st.session_state.lang]['create_password'], type="password", key="create_password")
    
    if len(create_password) < 8 and create_password != "":
        st.warning(translations[st.session_state.lang]['password_short_warning'])
    
    if st.button(translations[st.session_state.lang]['create_account_button']):
        if create_username and create_password:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if username_exists(cursor, create_username):
                    st.error(translations[st.session_state.lang]['username_occupied_error'])
                else:
                    hashed_password = hash_it_quick(create_password)
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (create_username, hashed_password))
                    st.success(translations[st.session_state.lang]['account_created_success'])
                    st.session_state.account = create_username
                    st.session_state.account_id = get_user_id_by_username(cursor, st.session_state.account)
                    debug_print(f"User: {create_username}, ID: {get_user_id_by_username(cursor, st.session_state.account)} added to the database.")
                    db.commit()
        else:
            st.error(translations[st.session_state.lang]['provide_username_password_error'])

# Login to existing account tab
with tab2:
    st.subheader(translations[st.session_state.lang]['login_existing_account'])
    login_username = st.text_input(translations[st.session_state.lang]['username'], key="login_username")
    login_password = st.text_input(translations[st.session_state.lang]['password'], type="password", key="login_password")
    
    if st.button(translations[st.session_state.lang]['login_button']):
        if login_username and login_password:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if verify_login(cursor, login_username, login_password):
                    st.success(translations[st.session_state.lang]['logged_in_success'])
                    st.session_state.account = login_username
                    st.session_state.account_id = get_user_id_by_username(cursor, st.session_state.account)
                else:
                    st.error(translations[st.session_state.lang]['invalid_username_password_error'])
        else:
            st.error(translations[st.session_state.lang]['provide_username_password_error'])

# Hide Streamlit's default footer and menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.divider()

if st.session_state.account:
    st.header(translations[st.session_state.lang]['my_projects'])
    st.write(translations[st.session_state.lang]['current_account'].format(account=st.session_state.account))

    with st.expander(translations[st.session_state.lang]['add_files_manually']):
        tab1, tab2 = st.tabs([translations[st.session_state.lang]['upload_file'], translations[st.session_state.lang]['write_file_manually']])
        
        # Tab 1: Upload a file
        with tab1:
            uploaded_file = st.file_uploader(label=translations[st.session_state.lang]['upload_your_html_file'])
            if uploaded_file is not None:
                # Read file content
                file_content = uploaded_file.getvalue()
                # Get filename
                filename = uploaded_file.name
                st.write(translations[st.session_state.lang]['uploaded_file_name'].format(filename=filename))
                st.write(translations[st.session_state.lang]['file_content'])
                st.write(file_content)
                if st.button(translations[st.session_state.lang]['add_to_database'], key="upload_button"):
                    with sqlite3.connect(db_path) as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, file_content))
                        file_id = cursor.lastrowid
                        cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (get_user_id_by_username(cursor, st.session_state.account), file_id))
                        db.commit()
                        st.success(f"File added to the database with file_id: {file_id}")
        
        # Tab 2: Write file manually
        with tab2:
            st.write(translations[st.session_state.lang]['enter_data_manually'])
            filename = st.text_input(translations[st.session_state.lang]['filename'], key="manual_filename")
            filecont = st.text_area(translations[st.session_state.lang]['content'], key="manual_content")
            
            if st.button(translations[st.session_state.lang]['add_to_database'], key="manual_button"):
                if filename and filecont:
                     with sqlite3.connect(db_path) as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, filecont))
                        file_id = cursor.lastrowid
                        cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (get_user_id_by_username(cursor, st.session_state.account), file_id))
                        db.commit()
                        st.success(f"File added to the database with file_id: {file_id}")

    with st.expander(translations[st.session_state.lang]['existing_projects']):
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            user_id = get_user_id_by_username(cursor, st.session_state.account)
            file_ids = get_file_ids_by_user_id(cursor, user_id)
            
            if file_ids:
                # Create tabs for each file ID
                tabs = [f"File ID: {file_id}" for file_id in file_ids]
                selected_tab = st.tabs(tabs)
                
                for file_id, tab_name in zip(file_ids, tabs):
                    with selected_tab[tabs.index(tab_name)]:
                        file_json_str = get_file_data_as_json(cursor, file_id)
                        file_json = json.loads(file_json_str)  # Parse the JSON string into a dictionary
                        st.write(f"**File ID**: {file_id}")
                        st.write(f"**Filename**: {file_json['filename']}")
                        st.write(translations[st.session_state.lang]['file_content'])
                        st.code(file_json["content"], line_numbers=True)
                        btn1, btn2 = st.columns(2)
                        with btn1:
                            # Create a button for downloading the file
                            if st.download_button(
                                    label=translations[st.session_state.lang]['export'],
                                    data=file_json["content"],
                                    file_name=file_json['filename'],
                                    key=f"Download from bd{file_id}"
                                ):
                                st.success(translations[st.session_state.lang]['download_started'])
                        with btn2:
                            if st.button(label=translations[st.session_state.lang]['edit'], help=translations[st.session_state.lang]['open_in_code_editor'], key=f"{file_id}_export"):
                                st.session_state.edited_content = file_json["content"]
                                st.success(translations[st.session_state.lang]['opened_in_web_editor'])
            else:
                st.write(translations[st.session_state.lang]['no_files_found'])