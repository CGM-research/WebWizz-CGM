import streamlit as st

# Assuming the translations dictionary is already defined as shown in the previous response

translations = {
    'en': {
        'configure_everything_here': "Configure everything here",
        'privacy_message': "Don't worry, we respect your privacy 🤫",
        'privacy_help': "All tokens are stored locally in session and accessible by user only.",
        'use_public_tokens': "Use public tokens",
        'use_public_tokens_help': "Uncheck to use your own tokens. Your own tokens give better performance.",
        'configure_your_tokens': "Configure your tokens",
        'configure_your_tokens_help': "User Access Tokens are the preferred way to authenticate an application or notebook to Hugging Face services. You can manage your access tokens in your settings.",
        'configure_huggingface_token': "Configure your <a href=https://huggingface.co/settings/tokens>HuggingFace token</a>.",
        'enter_huggingface_token': "Enter your HuggingFace token 🤗",
        'configure_pixabay_token': "Configure your <a href=https://pixabay.com/api/docs/>Pixabay token</a>.",
        'enter_pixabay_token': "Enter your Pixabay token 🖼️",
        'code_editor_settings': "Code editor settings",
        'ai_code_context': "AI code context",
        'ai_code_context_help': "Tick the checkbox to let VerstkaEdit AI assistant see your code.",
    },
    'ru': {
        'configure_everything_here': "Настройте все здесь",
        'privacy_message': "Не волнуйтесь, мы уважаем вашу конфиденциальность 🤫",
        'privacy_help': "Все токены хранятся локально в сессии и доступны только пользователю.",
        'use_public_tokens': "Использовать публичные токены",
        'use_public_tokens_help': "Снимите флажок, чтобы использовать свои собственные токены. Ваши собственные токены обеспечивают лучшую производительность.",
        'configure_your_tokens': "Настройте свои токены",
        'configure_your_tokens_help': "Токены доступа пользователя являются предпочтительным способом аутентификации приложения или блокнота в сервисах Hugging Face. Вы можете управлять своими токенами доступа в настройках.",
        'configure_huggingface_token': "Настройте ваш <a href=https://huggingface.co/settings/tokens>HuggingFace токен</a>.",
        'enter_huggingface_token': "Введите ваш HuggingFace токен 🤗",
        'configure_pixabay_token': "Настройте ваш <a href=https://pixabay.com/api/docs/>Pixabay токен</a>.",
        'enter_pixabay_token': "Введите ваш Pixabay токен 🖼️",
        'code_editor_settings': "Настройки редактора кода",
        'ai_code_context': "Контекст кода AI",
        'ai_code_context_help': "Установите флажок, чтобы позволить помощнику VerstkaEdit AI видеть ваш код.",
    },
    'de': {
        'configure_everything_here': "Konfigurieren Sie alles hier",
        'privacy_message': "Keine Sorge, wir respektieren Ihre Privatsphäre 🤫",
        'privacy_help': "Alle Tokens werden lokal in der Sitzung gespeichert und sind nur dem Benutzer zugänglich.",
        'use_public_tokens': "Öffentliche Tokens verwenden",
        'use_public_tokens_help': "Deaktivieren Sie das Kontrollkästchen, um Ihre eigenen Tokens zu verwenden. Ihre eigenen Tokens bieten eine bessere Leistung.",
        'configure_your_tokens': "Konfigurieren Sie Ihre Tokens",
        'configure_your_tokens_help': "Benutzerzugriffstokens sind die bevorzugte Methode zur Authentifizierung einer Anwendung oder eines Notebooks bei Hugging Face-Diensten. Sie können Ihre Zugriffstokens in Ihren Einstellungen verwalten.",
        'configure_huggingface_token': "Konfigurieren Sie Ihr <a href=https://huggingface.co/settings/tokens>HuggingFace-Token</a>.",
        'enter_huggingface_token': "Geben Sie Ihr HuggingFace-Token ein 🤗",
        'configure_pixabay_token': "Konfigurieren Sie Ihr <a href=https://pixabay.com/api/docs/>Pixabay-Token</a>.",
        'enter_pixabay_token': "Geben Sie Ihr Pixabay-Token ein 🖼️",
        'code_editor_settings': "Code-Editor-Einstellungen",
        'ai_code_context': "AI-Code-Kontext",
        'ai_code_context_help': "Aktivieren Sie das Kontrollkästchen, damit der VerstkaEdit AI-Assistent Ihren Code sehen kann.",
    }
}

st.title(translations[st.session_state.lang]['configure_everything_here'])

st.markdown(translations[st.session_state.lang]['privacy_message'], help=translations[st.session_state.lang]['privacy_help'])
st.divider()
st.session_state.change = st.checkbox(translations[st.session_state.lang]['use_public_tokens'], help=translations[st.session_state.lang]['use_public_tokens_help'], value=True)

if not st.session_state.change:
    st.session_state["hf_token"] = ""
    st.session_state["px_token"] = ""
    
    st.header(translations[st.session_state.lang]['configure_your_tokens'], help=translations[st.session_state.lang]['configure_your_tokens_help'])

    st.markdown(translations[st.session_state.lang]['configure_huggingface_token'], unsafe_allow_html=True)
    hf = st.text_input(translations[st.session_state.lang]['enter_huggingface_token'], value=st.session_state.get("hf_token", ""))
    if hf:
        st.session_state["hf_token"] = hf

    st.markdown(translations[st.session_state.lang]['configure_pixabay_token'], unsafe_allow_html=True)
    px = st.text_input(translations[st.session_state.lang]['enter_pixabay_token'], value=st.session_state.get("px_token", ""))
    if px:
        st.session_state["px_token"] = px
    st.divider()
else:
    st.session_state["hf_token"] = st.secrets.hf_token
    st.session_state["px_token"] = st.secrets.px_token
    st.divider()

st.header(translations[st.session_state.lang]['code_editor_settings'])
ctxt = st.checkbox(translations[st.session_state.lang]['ai_code_context'], help=translations[st.session_state.lang]['ai_code_context_help'], value=st.session_state.get("context", False))
if 'context' not in st.session_state:
    st.session_state["context"] = ctxt
else:
    st.session_state["context"] = ctxt