import requests
import re
import streamlit as st
from g4f.client import Client
from g4f.Provider import DarkAI

# Function to generate text using the g4f client
def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        provider=DarkAI
    )
    return response.choices[0].message.content

# Function to replace assistant tags and unwanted characters
def replace_assistant(strin):
    e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
    e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
    return e.strip()

# Function to send prompt and get response
def send(prompt):
    print('generating')
    print(prompt)
    for i in range(0, 10):
        try:
            system_prompt = f"""Write website article text based on provided data. Make it very brief. 2-3 sentences. Response with {st.session_state.gen_lang} language only. """
            full_prompt = f"{system_prompt}\n{prompt}"
            full_response = generate_text(full_prompt)
            print(full_response)
            return full_response
        except Exception as e:
            print(e)
            pass
    return "Error"

if 'lang' not in st.session_state:
    st.session_state.lang = 'ru'

# Streamlit app
if __name__ == "__main__":
    st.title("Text Generator")
    user_prompt = st.text_input("Enter your text prompt:")
    if st.button("Generate"):
        generated_text = send(user_prompt)
        st.write(generated_text)