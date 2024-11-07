import streamlit as st

# Define translations
translations = {
    'en': {
        'title': "Welcome to *WebWizz* ! :wave:",
        'subheader': "A simple website editor with cool functions of generating web-pages powered by AI algorithms",
        'markdown1': "This project is built with <a href='https://streamlit.io/'>Streamlit :crown:</a> and <a href='https://huggingface.co/'>HuggingFace :hugging_face:</a>.",
        'markdown2': "You are welcome in our <a href='https://t.me/webwizzcom'>Telegram channel</a> !",
        'markdown3': "Also checkout <a href='https://t.me/ezcodebot'>EzCode bot</a> and <a href='https://t.me/learnezcode'>EzCode telegram channel</a>!"
    },
    'ru': {
        'title': "Добро пожаловать в *WebWizz* ! :wave:",
        'subheader': "Простой редактор веб-сайтов с крутыми функциями генерации веб-страниц на основе алгоритмов искусственного интеллекта",
        'markdown1': "Этот проект создан с использованием <a href='https://streamlit.io/'>Streamlit :crown:</a> и <a href='https://huggingface.co/'>HuggingFace :hugging_face:</a>.",
        'markdown2': "Добро пожаловать в наш <a href='https://t.me/webwizzcom'>Telegram канал</a> !",
        'markdown3': "Также загляните в <a href='https://t.me/ezcodebot'>EzCode бот</a> и <a href='https://t.me/learnezcode'>Telegram канал EzCode</a>!"
    },
    'de': {
        'title': "Willkommen bei *WebWizz* ! :wave:",
        'subheader': "Ein einfacher Website-Editor mit coolen Funktionen zur Generierung von Webseiten, unterstützt von KI-Algorithmen",
        'markdown1': "Dieses Projekt wurde mit <a href='https://streamlit.io/'>Streamlit :crown:</a> und <a href='https://huggingface.co/'>HuggingFace :hugging_face:</a> erstellt.",
        'markdown2': "Willkommen in unserem <a href='https://t.me/webwizzcom'>Telegram-Kanal</a> !",
        'markdown3': "Schauen Sie sich auch <a href='https://t.me/ezcodebot'>EzCode bot</a> und <a href='https://t.me/learnezcode'>EzCode Telegram-Kanal</a> an!"
    }
}

# Use translations
st.title(translations[st.session_state.lang]['title'])
st.subheader(translations[st.session_state.lang]['subheader'])
st.markdown(translations[st.session_state.lang]['markdown1'], unsafe_allow_html=True)
st.markdown(translations[st.session_state.lang]['markdown2'], unsafe_allow_html=True)
st.divider()
st.markdown(translations[st.session_state.lang]['markdown3'], unsafe_allow_html=True)
st.divider()
with st.container(border=False):
    st.image(image="ExtraFiles/jointg.png", width=640)