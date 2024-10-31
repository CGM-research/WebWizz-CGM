import streamlit as st

st.title("Welcome to *WebWizz* ! :wave:")
st.subheader("A simple website editor with cool functions of generating web-pages powered by AI algorithms")
st.markdown("This project is built with <a href='https://streamlit.io/'>Streamlit :crown:</a> and <a href='https://huggingface.co/'>HuggingFace :hugging_face:</a>.", unsafe_allow_html=True)
st.markdown("You are welcome in our <a href='https://t.me/webwizzcom'>Telegram channel</a> !", unsafe_allow_html=True)
st.divider()
st.markdown("Also checkout <a href='https://t.me/ezcodebot'>EzCode bot</a> and <a href='https://t.me/learnezcode'>EzCode telegram channel</a>!", unsafe_allow_html=True)
st.divider()
with st.container(border=False):
    st.image(image="ExtraFiles/jointg.png", width=640)

