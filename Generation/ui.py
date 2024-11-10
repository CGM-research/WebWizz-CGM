import streamlit as st

st.set_page_config(
    page_title='page1',
    page_icon='📋',
    layout='wide',
    initial_sidebar_state='collapsed'
)

#sidebar_style = """
#    <style>
#        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
#            width: 700px;
#        }
#        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
#            width: 700px;
#            margin-left: -700px;
#        }
#    </style>
#"""


with st.sidebar.title("Additional questions"):
    st.write("No questions yet")

st.title("WebWizz HTML generation engine")

