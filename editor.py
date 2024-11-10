import json
import streamlit as st
from code_editor import code_editor
import base64
import sqlite3
import streamlit.components.v1 as components
import requests
from login import get_user_id_by_username
from login import get_file_ids_by_user_id
from login import get_file_data_as_json
import difflib
import re

# Define translations
translations = {
    'en': {
        'welcome_title': "Welcome to our WebIDE !",
        'welcome_description': "A simple website editor",
        'choose_html_file': "Choose your HTML file.",
        'use_generator': "Use generator, constructor",
        'create_new_file': "Create new file",
        'login_to_load': "Login to load project from account",
        'no_files_found': "No files found for this user.",
        'settings': "Settings",
        'height_format': "height format:",
        'min_max_lines': "min-max lines:",
        'lang': "lang:",
        'theme': "theme:",
        'shortcuts': "shortcuts:",
        'focus': "focus",
        'wrap': "wrap",
        'save': "Save",
        'download': "Download",
        'ai_coder': "AI coder",
        'code_result': "Code result",
        'enter_filename': "Enter filename",
        'export': "Export",
        'download_started': "Download started!",
        'submit': "Submit",
        'login_to_save': "Login to save your files.",
        'verstkedit_ai_test': "WebWizz Ai test.",
        'ask_assistant': "Ask the assistant any coding-related questions. The assistant has your code as context for your request.",
        'code_context': "Code context",
        'code_context_help': "Tick the checkbox to let Ai use your code as additional data.",
        'send': "Send",
        'edit': "Edit",
        'assistant_code_preview': "Assistant's code preview",
        'user_code_preview': "Source code",
        'code_changes': "Code changes",
        'diff_result': "Diff Result",
        'page_preview': "Page preview",
        'file_content': "File content:",
        'opened_in_web_editor': "Opened in Web Editor !"
    },
    'ru': {
        'welcome_title': "Добро пожаловать в наш WebIDE !",
        'welcome_description': "Простой редактор веб-сайтов",
        'choose_html_file': "Выберите ваш HTML файл.",
        'use_generator': "Используйте генератор, конструктор",
        'create_new_file': "Создать новый файл",
        'login_to_load': "Войдите, чтобы загрузить проект из аккаунта",
        'no_files_found': "Файлы для этого пользователя не найдены.",
        'settings': "Настройки",
        'height_format': "формат высоты:",
        'min_max_lines': "минимум-максимум строк:",
        'lang': "язык:",
        'theme': "тема:",
        'shortcuts': "сочетания клавиш:",
        'focus': "фокус",
        'wrap': "перенос",
        'save': "Сохранить",
        'download': "Скачать",
        'ai_coder': "AI кодер",
        'code_result': "Результат кода",
        'enter_filename': "Введите имя файла",
        'export': "Экспорт",
        'download_started': "Загрузка началась!",
        'submit': "Отправить",
        'login_to_save': "Войдите, чтобы сохранить ваши файлы.",
        'verstkedit_ai_test': "Тест WebWizz Ai.",
        'ask_assistant': "Задайте помощнику любые вопросы, связанные с кодированием. Помощник использует ваш код в качестве контекста для вашего запроса.",
        'code_context': "Контекст кода",
        'code_context_help': "Установите флажок, чтобы позволить Ai использовать ваш код в качестве дополнительных данных.",
        'send': "Отправить",
        'edit': "Редактировать",
        'assistant_code_preview': "Предпросмотр кода помощника",
        'user_code_preview': "Исходный код",
        'code_changes': "Изменения кода",
        'diff_result': "Результат сравнения",
        'page_preview': "Предпросмотр страницы",
        'file_content': "Содержимое файла:",
        'opened_in_web_editor': "Открыто в веб-редакторе !"
    },
    'de': {
        'welcome_title': "Willkommen in unserem WebIDE !",
        'welcome_description': "Ein einfacher Website-Editor",
        'choose_html_file': "Wählen Sie Ihre HTML-Datei.",
        'use_generator': "Verwenden Sie den Generator, den Konstruktor",
        'create_new_file': "Neue Datei erstellen",
        'login_to_load': "Melden Sie sich an, um das Projekt aus dem Konto zu laden",
        'no_files_found': "Keine Dateien für diesen Benutzer gefunden.",
        'settings': "Einstellungen",
        'height_format': "Höhenformat:",
        'min_max_lines': "min-max Zeilen:",
        'lang': "Sprache:",
        'theme': "Thema:",
        'shortcuts': "Tastenkombinationen:",
        'focus': "Fokus",
        'wrap': "Umbruch",
        'save': "Speichern",
        'download': "Herunterladen",
        'ai_coder': "AI-Coder",
        'code_result': "Code-Ergebnis",
        'enter_filename': "Geben Sie den Dateinamen ein",
        'export': "Exportieren",
        'download_started': "Der Download wurde gestartet!",
        'submit': "Senden",
        'login_to_save': "Melden Sie sich an, um Ihre Dateien zu speichern.",
        'verstkedit_ai_test': "WebWizz Ai-Test.",
        'ask_assistant': "Stellen Sie dem Assistenten alle kodierungsbezogenen Fragen. Der Assistent verwendet Ihren Code als Kontext für Ihre Anfrage.",
        'code_context': "Code-Kontext",
        'code_context_help': "Aktivieren Sie das Kontrollkästchen, um dem Ai die Verwendung Ihres Codes als zusätzliche Daten zu ermöglichen.",
        'send': "Senden",
        'edit': "Bearbeiten",
        'assistant_code_preview': "Vorschau des Assistenten-Codes",
        'user_code_preview': "Quellcode",
        'code_changes': "Codeänderungen",
        'diff_result': "Diff-Ergebnis",
        'page_preview': "Seitenvorschau",
        'file_content': "Dateiinhalt:",
        'opened_in_web_editor': "Im Web-Editor geöffnet !"
    }
}

# Initialize session state variables
if 'uploaded_file_content' not in st.session_state:
    st.session_state.uploaded_file_content = ""
if 'height' not in st.session_state:
    st.session_state.height = [19, 22]
if 'language' not in st.session_state:
    st.session_state.language = "html"
if 'theme' not in st.session_state:
    st.session_state.theme = "default"
if 'shortcuts' not in st.session_state:
    st.session_state.shortcuts = "vscode"
if 'focus' not in st.session_state:
    st.session_state.focus = True
if 'wrap' not in st.session_state:
    st.session_state.wrap = True
if 'edited_content' not in st.session_state:
    st.session_state.edited_content = ""
if 'account' not in st.session_state:
    st.session_state.account = ""
if 'show_ai_coder' not in st.session_state:
    st.session_state.show_ai_coder = False

def find_between(s, first, last):
    try:
        start = s.find(first) + len(first)
        end = s.find(last, start)
        return s[start:end]
    except ValueError:
        return ""

# Load custom buttons and CSS
with open('resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)
with open('resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)
with open('resources/example_code_editor_css.scss') as css_file:
    css_text = css_file.read()

# Construct component props dictionary
comp_props = {"css": css_text, "globalCSS": ":root {\n  --streamlit-dark-font-family: monospace;\n}"}

mode_list = ["abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "bibtex", "c9search", "c_cpp", "cirru", "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", "io", "ion", "jack", "jade", "java", "javascript", "jexl", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", "kotlin", "latex", "latte", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mips", "mixal", "mushcode", "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "partiql", "pascal", "perl", "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", "properties", "protobuf", "puppet", "python", "qml", "r", "raku", "razor", "rdoc", "red", "redshift", "rhtml", "robot", "rst", "ruby", "rust", "sac", "sass", "scad", "scala", "scheme", "scrypt", "scss", "sh", "sjs", "slim", "smarty", "smithy", "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml", "zeek"]

btns = custom_buttons_alt

st.title(translations[st.session_state.lang]['welcome_title'])
st.markdown(translations[st.session_state.lang]['welcome_description'])

upload, load = st.columns([3, 3])

with upload:
    with st.container(border=True, height=350):
        uploaded_file = st.file_uploader(label=translations[st.session_state.lang]['choose_html_file'], label_visibility="collapsed")
        st.subheader(translations[st.session_state.lang]['use_generator'])
        st.subheader(translations[st.session_state.lang]['create_new_file'])
        if st.button(translations[st.session_state.lang]['create_new_file']):
            st.session_state.edited_content = ""
        

with load:
    with st.container(border=True, height=350):
        if st.session_state.account:
            with sqlite3.connect(st.session_state.db_path) as db:
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
                                st.write(f"**Filename**: {file_json['filename']}")
                                st.write(translations[st.session_state.lang]['file_content'])
                                with st.expander("View source code"):
                                    st.code(file_json["content"], line_numbers=True)
                                if st.button(label=translations[st.session_state.lang]['edit'], key=f"{file_id}_export"):
                                    st.session_state.edited_content = file_json["content"]
                                    st.success(translations[st.session_state.lang]['opened_in_web_editor'])
                    else:
                        st.write(translations[st.session_state.lang]['no_files_found'])
        else:
            st.warning(translations[st.session_state.lang]['login_to_load'])

if uploaded_file != None:
    st.session_state.uploaded_file_content = uploaded_file.read().decode('utf-8')
    st.session_state.edited_content = st.session_state.uploaded_file_content

if st.session_state.edited_content != None:
    bytes_data = st.session_state.edited_content
    st.write("filename:", uploaded_file.name if uploaded_file else "Not defined")

    st.write("")
    with st.expander(translations[st.session_state.lang]['settings'], expanded=True):
        col_a, col_b, col_c, col_cb = st.columns([6,11,3,3])
        col_c.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)
        col_cb.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)

        height_type = col_a.selectbox(translations[st.session_state.lang]['height_format'], ["min-max lines"])
        if height_type == "min-max lines":
            st.session_state.height = col_b.slider(translations[st.session_state.lang]['min_max_lines'], 1, 40, st.session_state.height)

        col_d, col_e, col_f = st.columns([1,1,1])
        st.session_state.language = col_d.selectbox(translations[st.session_state.lang]['lang'], mode_list, index=mode_list.index(st.session_state.language))
        st.session_state.theme = col_e.selectbox(translations[st.session_state.lang]['theme'], ["default", "light", "dark", "contrast"], index=["default", "light", "dark", "contrast"].index(st.session_state.theme))
        st.session_state.shortcuts = col_f.selectbox(translations[st.session_state.lang]['shortcuts'], ["emacs", "vim", "vscode", "sublime"], index=["emacs", "vim", "vscode", "sublime"].index(st.session_state.shortcuts))
        st.session_state.focus = col_c.checkbox(translations[st.session_state.lang]['focus'], st.session_state.focus)
        st.session_state.wrap = col_cb.checkbox(translations[st.session_state.lang]['wrap'], st.session_state.wrap)
        
        # Render code editor
        ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
        response_dict = code_editor(bytes_data, height=st.session_state.height, lang=st.session_state.language, theme=st.session_state.theme, shortcuts=st.session_state.shortcuts, focus=st.session_state.focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": st.session_state.wrap}, allow_reset=True, key="code_editor_demo")    

        # Initial tabs
        tabs = [translations[st.session_state.lang]['save'], translations[st.session_state.lang]['download'], translations[st.session_state.lang]['ai_coder'], translations[st.session_state.lang]['code_result']]

        # Create tabs
        tab_objects = st.tabs(tabs)

        # Assign tabs to variables
        tab_save = tab_objects[tabs.index(translations[st.session_state.lang]['save'])]
        tab_download = tab_objects[tabs.index(translations[st.session_state.lang]['download'])]
        tab_ai_coder = tab_objects[tabs.index(translations[st.session_state.lang]['ai_coder'])]
        tab_code_result = tab_objects[tabs.index(translations[st.session_state.lang]['code_result'])]
            
        # Save Tab
        with tab_download:
            filename = st.text_input(label=translations[st.session_state.lang]['enter_filename'], key='filename2')
            if st.download_button(
                label=translations[st.session_state.lang]['export'],
                data=st.session_state.get('edited_content', ''),
                file_name=filename,
                key="Download"
            ):
                st.success(translations[st.session_state.lang]['download_started'])
            
            # Download Tab
            with tab_save:
                if st.session_state.get('account', ''):
                    filename = st.text_input(label=translations[st.session_state.lang]['enter_filename'], key='filename1')
                    if st.button(label=translations[st.session_state.lang]['submit']):
                        with sqlite3.connect(st.session_state.db_path) as db:
                            cursor = db.cursor()
                            cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, st.session_state.get('edited_content', '')))
                            file_id = cursor.lastrowid
                            cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (st.session_state.account_id, file_id))
                            db.commit()
                            st.success(f"File added to the database with file_id: {file_id}")
                            st.success("Saved to your account. Visit the login page to see.")
                else:
                    st.error(translations[st.session_state.lang]['login_to_save'])
                    
        with tab_ai_coder:
            # This code is a merge of assistant.py and compare.py, using both 

            context = False

            diff_result = ""
            st.header(translations[st.session_state.lang]['verstkedit_ai_test'])
            UserCode = st.session_state.edited_content

            css = st.markdown("""
            <style>
                .st-da st-db st-dc st-f3 st-gp st-gq st-gr st-gs st-gt st-gu st-hc st-cc st-bb st-he st-gx st-gy st-gz st-h0 st-eu st-h1 st-fi st-h2 st-c3 st-c4 st-c5 st-c6 st-h3 st-h4 st-h5 st-h6 st-c7 st-c8 st-c9 st-ca st-h7 st-h8 st-h9 st-ha {
                    width: 100%;
                }

                .st-emotion-cache-15hul6a ef3psqc12 {
                    width: 100%;
                }       
            </style>
            """, unsafe_allow_html=True)

            def st_codemirror_diff(left, right, opts, key=None): # This function is used to compare Ai-written code with user's one.
                    # Generate a diff using difflib
                    diff = difflib.unified_diff(
                        left.splitlines(keepends=True),
                        right.splitlines(keepends=True),
                        fromfile='Left',
                        tofile='Right',
                    )
                    diff_result = ''.join(diff)
                    return diff_result

            opts = { # Options for difference
                "mode": "python",
                "theme": "default",
            }

            hf_token = st.session_state.get("hf_token", "") # replace with your HuggingFace API key

            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1/v1/chat/completions"
            headers = {"Authorization": f"Bearer {hf_token}"}

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            def replace_assistant(strin):
                e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
                e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
                return e.strip()

            def send(prompt):
                print('generating')
                print(prompt)
                for i in range(0, 10):
                    try:
                        promptd = [{'role': 'system', 'content':""" Assistants helps user with his coding tasks. Assistant can only respond with code.
                            """}, {'role': 'user', 'content': f'{prompt}'}]
                        response = query({
                        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                            "messages": promptd,
                            "max_tokens": 8000,
                            'stream': False
                        })
                        print(response['choices'][0]['message']['content'])
                        full_response = response['choices'][0]['message']['content']
                        return full_response
                        break
                    except Exception as e:
                        print(e)
                        pass
                return "Error"

            # Here starts the streamlit interface for Ai assistant
            if 'hf_token' not in st.session_state:
                st.session_state.hf_token = ""

            st.markdown(translations[st.session_state.lang]['ask_assistant'])
            context = st.checkbox(translations[st.session_state.lang]['code_context'], help=translations[st.session_state.lang]['code_context_help'])    
            request = st.text_area(label="", label_visibility="collapsed")
            if context:
                request = f"""
                    User's request: {request}

                    User's code: {UserCode}
                """
            else:
                request = f"""
                    User's request: {request}
                """
            
            pt1, pt2 = st.columns(2)
            
            with pt1:
                if st.button(translations[st.session_state.lang]['send']):
                    response = send(request)
                    if response != "Error":
                        print("Text writing successfully!", response)
                        t1 ,t2, t3 = st.tabs([translations[st.session_state.lang]['assistant_code_preview'], translations[st.session_state.lang]['user_code_preview'], translations[st.session_state.lang]['code_changes']])
                        response = find_between(response, "```", "```")
                        
                        with t1:
                            st.components.v1.html(response, height=750)
                            
                        with t2:
                            st.code(response)
                            
                        with t3:
                            # Display the difference result between user's code and ai's
                            diff_result = st_codemirror_diff(UserCode, response, opts)
                            
                    else:
                        print("An error occurred while communicating with TextAi.")
                
            #with pt2:
            #    if response != "":
            #        if st.button(translations[st.session_state.lang]['edit']):
            #            st.session_state.edited_content = response
            #            
        if diff_result != None and diff_result != "":
            st.subheader(translations[st.session_state.lang]['diff_result'])
            st.code(diff_result, language='diff')
            st.header(translations[st.session_state.lang]['page_preview'])
            st.components.v1.html(response)
        
        # Code Result Tab (conditionally rendered)
        if 'response_dict' in locals() and response_dict.get('type') == "submit":
            with tab_code_result:
                st.header(translations[st.session_state.lang]['page_preview'])
                st.components.v1.html(response_dict['text'], height=750)
                st.session_state.edited_content = response_dict['text']