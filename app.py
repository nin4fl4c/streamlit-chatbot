import streamlit as st
from openai import OpenAI  # Ali katera druga knjižnica, ki jo uporabljaš

# Nastavitve strani (barve se nastavljajo v .streamlit/config.toml, a tukaj nastavimo naslov)
st.set_page_config(page_title="Moj Chatbot", layout="centered")

# Povezava do API ključa iz Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Inicializacija spomina (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Ti si specializiran pomočnik za [TVOJA TEMA]. Odgovarjaj izključno v slovenščini. Če vprašanje ni povezano s temo, vljudno zavrni odgovor."}
    ]

# Prikaz zgodovine klepeta
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Vnos uporabnika
if prompt := st.chat_input("Kako vam lahko pomagam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Odgovor chatbota
    with st.chat_message("assistant"):
        # Tukaj dodaš klic na API (npr. OpenAI) z uporabo st.session_state.messages
        # ... koda za generiranje odgovora ...
        response = "Tukaj bo generiran odgovor v slovenščini."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})