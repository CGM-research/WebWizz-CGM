import streamlit as st
import streamlit.components.v1 as components
import json
from code_editor import code_editor
import base64
import sqlite3
import requests
import difflib
import re
from g4f.client import Client
from g4f.Provider import DarkAI

if 'display' not in st.session_state:
    st.session_state.display = True 

def getcode (text):
    pattern = r'```(.*?)```' 
    matches = re.findall(pattern, text, re.DOTALL) 
    return matches

def load_main():
    page_shop, edit = st.tabs(["Page shop", "Edit code"])
    with edit:
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
                'verstkedit_ai_test': "WebWizz Ai test. (β)",
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
                'verstkedit_ai_test': "Тест WebWizz Ai. (β)",
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
                'verstkedit_ai_test': "WebWizz Ai-Test. (β)",
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
        if 'lang' not in st.session_state:
            st.session_state.lang = 'en'

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

        #st.title(translations[st.session_state.lang]['welcome_title'])
        #st.markdown(translations[st.session_state.lang]['welcome_description'])

        upload, load = st.columns([3, 3])
        with st.expander(translations[st.session_state.lang]['settings'], expanded=True):
            col_a, col_b, col_c, col_cb = st.columns([6,11,3,3])
            col_c.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)
            col_cb.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)

            height_type = col_a.selectbox(translations[st.session_state.lang]['height_format'], ["min-max lines"])
            if height_type == "min-max lines":
                st.session_state.height = col_b.slider(translations[st.session_state.lang]['min_max_lines'], 1, 50, st.session_state.height)

            col_d, col_e, col_f = st.columns([1,1,1])
            st.session_state.language = col_d.selectbox(translations[st.session_state.lang]['lang'], mode_list, index=mode_list.index(st.session_state.language))
            st.session_state.theme = col_e.selectbox(translations[st.session_state.lang]['theme'], ["default", "light", "dark", "contrast"], index=["default", "light", "dark", "contrast"].index(st.session_state.theme))
            st.session_state.shortcuts = col_f.selectbox(translations[st.session_state.lang]['shortcuts'], ["emacs", "vim", "vscode", "sublime"], index=["emacs", "vim", "vscode", "sublime"].index(st.session_state.shortcuts))
            st.session_state.focus = col_c.checkbox(translations[st.session_state.lang]['focus'], st.session_state.focus)
            st.session_state.wrap = col_cb.checkbox(translations[st.session_state.lang]['wrap'], st.session_state.wrap)
            
        # Render code editor
        ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
        response_dict = code_editor(code=st.session_state.edited_content, height=st.session_state.height, lang=st.session_state.language, theme=st.session_state.theme, shortcuts=st.session_state.shortcuts, focus=st.session_state.focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": st.session_state.wrap}, allow_reset=True, key="code_editor_demo")    

        filename = st.text_input(label=translations[st.session_state.lang]['enter_filename'], key='filename2')
        if st.download_button(
            label=translations[st.session_state.lang]['export'],
            data=st.session_state.edited_content,
            file_name=filename,
            key="Download"
        ):
            st.success(translations[st.session_state.lang]['download_started'])
        
        # Code Result Tab (conditionally rendered)
        if 'response_dict' in locals() and response_dict.get('type') == "submit":
            st.session_state.display = True

def load_chat():
    # Function to generate text using the g4f client
    def generate_text(prompt):
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            provider=DarkAI
        )
        return response.choices[0].message.content

    # Function to send prompt and get response
    def send(prompt):
        print('generating')
        print(prompt)
        for i in range(0, 10):
            try:
                system_prompt = f"""You are an HTML coding expert. Response with HTML and CSS code only, using user's code if provided. Always respond with full code (User code and yours combined). Always add css ! Always respond with one code, which includes both html and css. Generate some text for website (Lorem ipsum), to make it look filled. ALWAYS Keep the format: Horizontal topbar, body, footer"""
                full_prompt = f"{system_prompt}\n{st.session_state.edited_content}\n{prompt}\n{st.session_state['preferences']}"
                full_response = generate_text(full_prompt)
                print(full_response)
                return full_response
            except Exception as e:
                print(e)
                pass
        return "Error"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun with tabs for each Q-A pair
    if st.session_state.messages:
        chat_expander = st.expander("Chat History")
        with chat_expander:
            for idx in range(0, len(st.session_state.messages), 2):
                if idx+1 < len(st.session_state.messages):
                    tabs = st.tabs([f"Q{idx//2 + 1}", f"A{idx//2 + 1}"])
                    with tabs[0]:
                        with st.chat_message("user"):
                            st.markdown(f"**Question {idx//2 + 1}:**")
                            st.markdown(st.session_state.messages[idx]["content"])
                    with tabs[1]:
                        with st.chat_message("assistant"):
                            st.markdown(f"**Answer {idx//2 + 1}:**")
                            st.markdown(st.session_state.messages[idx + 1]["content"])

    if prompt := st.chat_input("Page prompt"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.status("AI is responding"):
            response = send(prompt)

        with st.chat_message("assistant"):
            t1, t2 = st.tabs(["Code", "Explanation"])
            with t1:
                resp = st.markdown(response)
                # Capture the response content
                resp_content = response
            with t2:
                # Pass the captured content to getcode
                code = st.code(getcode(resp_content))
        st.session_state.messages.append({"role": "assistant", "content": response})

if "box_wid" not in st.session_state:
    st.session_state.box_wid = 40

with st.sidebar:
    st.divider()
    st.title("Additional questions")
    
    # Function to collect user preferences and save to session state
    def save_preferences(preferences):
        st.session_state['preferences'] = preferences

    # Initialize an empty dictionary to store preferences
    preferences = {}

    # Layout selection
    layout = st.selectbox(
        "Select Layout Style",
        ["", "Fixed-width", "Fluid/Responsive"]
    )
    if layout:
        preferences["Layout Style"] = layout

    # Navigation style
    navigation = st.selectbox(
        "Select Navigation Style",
        ["", "Horizontal", "Vertical", "Sticky/Fixed", "Scrollable"]
    )
    if navigation:
        preferences["Navigation Style"] = navigation

    # Color scheme
    color_scheme = st.pills(
        "Choose Color Scheme",
        ["Light", "Dark", "Custom"]
    )
    if color_scheme:
        preferences["Color Scheme"] = color_scheme
        if color_scheme == "Custom":
            color = st.text_area(label="Describe color scheme")
            st.color_picker(label="RGB color picker", help="Doesn't apply automatically !")

    # Typography
    typography = st.selectbox(
        "Select Typography Style",
        ["", "Serif", "Sans-serif", "Custom Fonts", "Standard Web-safe Fonts"]
    )
    if typography:
        preferences["Typography"] = typography

    # Imagery and Media
    imagery = st.selectbox(
        "Imagery Preferences",
        ["", "Full-width Images", "Contained Images", "Background Images", "Solid Colors", "Icons/Illustrations"]
    )
    if imagery:
        preferences["Imagery"] = imagery

    # CSS Frameworks
    css_framework = st.selectbox(
        "CSS Framework Preference",
        ["", "Bootstrap", "Foundation", "Bulma", "Custom CSS"]
    )
    if css_framework:
        preferences["CSS Framework"] = css_framework

    # Grid System
    grid_system = st.selectbox(
        "Preferred Grid System",
        ["", "Flexbox", "CSS Grid", "Other"]
    )
    if grid_system:
        preferences["Grid System"] = grid_system

    # Animations and Interactions
    animations = st.multiselect(
        "Select Animations and Interactions",
        ["CSS Animations", "JavaScript Interactions", "Hover Effects", "Scrolling Animations", "Transitions"]
    )
    if animations:
        preferences["Animations and Interactions"] = animations

    # Form styles
    form_styles = st.selectbox(
        "Form Element Styles",
        ["", "Standard", "Rounded Corners", "Sharp Corners", "Flat Design", "Gradients/Shadows"]
    )
    if form_styles:
        preferences["Form Styles"] = form_styles

    # Accessibility
    accessibility = st.selectbox(
        "Accessibility Features",
        ["", "Standard", "High Contrast", "Keyboard Navigation", "Screen Reader Compatible"]
    )
    if accessibility:
        preferences["Accessibility"] = accessibility

    # Responsive design
    responsive_design = st.selectbox(
        "Responsive Design Approach",
        ["", "Mobile-first", "Desktop-first"]
    )
    if responsive_design:
        preferences["Responsive Design"] = responsive_design
        
    additional_data = st.text_area(label="Additional preferences")
    
    if additional_data:
        preferences["Additional Preferences"] = additional_data

    # Save preferences when button is clicked
    if st.button("Save Preferences"):
        save_preferences(preferences)
        st.success("Preferences saved successfully!")

    # Display current configuration
    if st.button("Display Current Configuration"):
        if 'preferences' in st.session_state:
            st.json(st.session_state['preferences'])
        else:
            st.warning("No preferences saved yet!")




st.title("WebWizz generation engine")
st.session_state.box_wid = st.slider(label="Resize page", label_visibility="collapsed", min_value=0, max_value=50, value=st.session_state.box_wid, help="Resize page")

if st.session_state.box_wid == 50:
    with st.container(border=True, height=750):
        load_main()

elif st.session_state.box_wid == 0:
    with st.container(border=True, height=750):
        load_chat()


else:
    main, chat = st.columns([st.session_state.box_wid, 50 - st.session_state.box_wid])

    with main:
        with st.container(border=True, height=750):
            load_main()

    with chat:
        with st.container(border=True, height=750):
            load_chat()
            
st.write("<~~ Configure page here")
if st.checkbox(label="Toogle to preview page"):
    st.divider()
    components.html(st.session_state.edited_content)