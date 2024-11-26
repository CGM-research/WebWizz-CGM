import streamlit as st
import streamlit.components.v1 as components
import os
import sqlite3
import text_writer
import get_image_topic
from search_image import get_image_urls
import random

# Define translations
translations = {
    'en': {
        'title': "Generate websites with ease !",
        'description': "An open-source Website generation engine",
        'warning': "Make sure to configure your keys",
        'company_name_label': "Enter the page topic",
        'company_description_label': "Enter the page description",
        'generate_button': "Generate",
        'error_keys': "Configure you access keys at 'configure' page",
        'download_tab': "Download",
        'save_tab': "Save",
        'edit_tab': "Edit",
        'enter_filename': "Enter filename",
        'export_button': "Export",
        'download_success': "Download started!",
        'submit_button': "Submit",
        'save_success': "File added to the database with file_id: {file_id}",
        'save_success_login': "Saved to your account. Visit the login page to see.",
        'login_error': "Login to save to account",
        'edit_button': "Edit",
        'edit_help': "Open this file in code editor",
        'edit_success': "Opened in Web Editor!",
        'Select Language': 'Select Language',
        'gen_lang': "Generation language select",
    },
    'ru': {
        'title': "Генерируйте веб-сайты легко !",
        'description': "Открытый движок для генерации веб-сайтов",
        'warning': "Убедитесь, что вы настроили свои ключи",
        'company_name_label': "Введите тему страницы",
        'company_description_label': "Введите описание страницы",
        'generate_button': "Сгенерировать",
        'error_keys': "Настройте ваши ключи на странице 'настройки'",
        'download_tab': "Скачать",
        'save_tab': "Сохранить",
        'edit_tab': "Редактировать",
        'enter_filename': "Введите имя файла",
        'export_button': "Экспорт",
        'download_success': "Загрузка началась!",
        'submit_button': "Отправить",
        'save_success': "Файл добавлен в базу данных с file_id: {file_id}",
        'save_success_login': "Сохранено в ваш аккаунт. Посетите страницу входа, чтобы увидеть.",
        'login_error': "Войдите, чтобы сохранить в аккаунт",
        'edit_button': "Редактировать",
        'edit_help': "Открыть этот файл в редакторе кода",
        'edit_success': "Открыто в веб-редакторе!",
        'gen_lang': "Выбор языка генерации",
    },
    'de': {
        'title': "Webseiten einfach generieren !",
        'description': "Ein Open-Source-Webseitengenerator",
        'warning': "Stellen Sie sicher, dass Sie Ihre Schlüssel konfiguriert haben",
        'company_name_label': "Geben Sie das Seiten-Thema ein",
        'company_description_label': "Geben Sie die Seitenbeschreibung ein",
        'generate_button': "Generieren",
        'error_keys': "Konfigurieren Sie Ihre Zugriffsschlüssel auf der 'Konfigurations'-Seite",
        'download_tab': "Herunterladen",
        'save_tab': "Speichern",
        'edit_tab': "Bearbeiten",
        'enter_filename': "Geben Sie den Dateinamen ein",
        'export_button': "Exportieren",
        'download_success': "Der Download wurde gestartet!",
        'submit_button': "Senden",
        'save_success': "Datei wurde in der Datenbank mit file_id: {file_id} hinzugefügt",
        'save_success_login': "Gespeichert in Ihrem Konto. Besuchen Sie die Anmeldeseite, um es zu sehen.",
        'login_error': "Melden Sie sich an, um im Konto zu speichern",
        'edit_button': "Bearbeiten",
        'edit_help': "Öffnen Sie diese Datei im Code-Editor",
        'edit_success': "Im Web-Editor geöffnet!",
        'gen_lang': "Generation Sprachauswahl",
    }
}

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = ""
if 'edited_content' not in st.session_state:
    st.session_state.edited_content = ""
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""

ready = False

def replace_text(old_text, new_text):
    path = "output.html"
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()
        if old_text in html_content:
            html_content = html_content.replace(old_text, new_text)
            with open(path, "w", encoding="utf-8") as output_file:
                output_file.write(html_content)
            print(f"Replaced placeholders in '{path}'")
        else:
            print(f"The text '{old_text}' was not found in the file '{path}' - FATAL ERROR")
            
st.title(translations[st.session_state.lang]['title'])
st.write(translations[st.session_state.lang]['description'])
st.write(translations[st.session_state.lang]['gen_lang'])
st.session_state.gen_lang = st.selectbox(label='',label_visibility='collapsed', options=['en', 'ru', 'de'], index=['en', 'ru', 'de'].index(st.session_state.lang), key="randomkey1")
st.session_state.gen_lang = st.session_state.lang
if st.session_state["hf_token"] == "" or st.session_state["px_token"] == "":
    st.warning(translations[st.session_state.lang]['warning'])

# Initialize session state variables
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'company_description' not in st.session_state:
    st.session_state.company_description = ""

# Create an input field for the company names
company_name = st.text_input(translations[st.session_state.lang]['company_name_label'], value=st.session_state.company_name)

# Create an input field for the company description
company_description = st.text_area(translations[st.session_state.lang]['company_description_label'], value=st.session_state.company_description)

# Create a button
if st.button(translations[st.session_state.lang]['generate_button']):

    if st.session_state["hf_token"] == "" or st.session_state["px_token"] == "":
        st.error(translations[st.session_state.lang]['error_keys'])
    else:
        ready = False
        # When pressed, the field content will be written to the session state variables
        st.session_state.company_name = company_name
        st.session_state.company_description = company_description

        open("output.html", 'w').close()

        if (company_name and company_description):

            os.system("python3 merge.py")  # Merge HTML files to get started"

            topic = f'{company_name} - {company_description}'

            try:
                response = text_writer.send(topic)
                if response != "Error":
                    print("Text writing successfully!", response)

                    # Emplace company text and name
                    replace_text("&Company-name&", company_name)
                    replace_text("&Company-description&", response)

                else:
                    print("An error occurred while communicating with TextAi.")
            except Exception as e:
                print(f"An error occurred: {e}")

            try:
                response = get_image_topic.send(topic)
                if response != "Error":
                    imgurl_horizontal = random.choice(get_image_urls(response, "horizontal"))
                    imgurl_vertical = random.choice(get_image_urls(response, "vertical"))
                    replace_text("&Vertical-image&", imgurl_vertical)
                    replace_text("&Horizontal-image&", imgurl_horizontal)
                    print("Vertical image URL:", imgurl_vertical)
                    print("Horizontal image URL:", imgurl_horizontal)
                else:
                    print("An error occurred while communicating with TextAi.")
            except Exception as e:
                print(f"An error occurred: {e}")

            print("All processes have completed successfully, and all changes have been written to the HTML code.")

            with open('output.html', 'r') as f:
                html_string = f.read()
                st.session_state.generated_html = html_string

if st.session_state.generated_html:
    components.html(st.session_state.generated_html, height=750)

    tab_download, tab_save, tab_edit = st.tabs([translations[st.session_state.lang]['download_tab'], translations[st.session_state.lang]['save_tab'], translations[st.session_state.lang]['edit_tab']])

    # Save Tab
    with tab_download:
        filename = st.text_input(label=translations[st.session_state.lang]['enter_filename'], key='filename2')
        if st.download_button(
            label=translations[st.session_state.lang]['export_button'],
            data=st.session_state.generated_html,
            file_name=filename,
            key="Download"
        ):
            st.success(translations[st.session_state.lang]['download_success'])

    # Download Tab
    with tab_save:
        if st.session_state.get('account', ''):
            filename = st.text_input(label=translations[st.session_state.lang]['enter_filename'], key='filename1')
            if st.button(label=translations[st.session_state.lang]['submit_button']):
                with sqlite3.connect(st.session_state.db_path) as db:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, st.session_state.generated_html))
                    file_id = cursor.lastrowid
                    cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (st.session_state.account_id, file_id))
                    db.commit()
                    st.success(translations[st.session_state.lang]['save_success'].format(file_id=file_id))
                    st.success(translations[st.session_state.lang]['save_success_login'])
        else:
            st.error(translations[st.session_state.lang]['login_error'])

    with tab_edit:
        if st.button(label=translations[st.session_state.lang]['edit_button'], help=translations[st.session_state.lang]['edit_help']):
            st.session_state.edited_content = st.session_state.generated_html
            st.success(translations[st.session_state.lang]['edit_success'])