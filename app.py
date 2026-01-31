import streamlit as st
from groq import Groq

# 1. Konfiguracija strani
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# 2. Inicializacija Groq klienta
if "GROQ_API_KEY" not in st.secrets:
    st.error("Manjka GROQ_API_KEY v Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 GymGator Pomočnik")

# 3. Nastavitev sistemskih navodil (specializacija)
system_prompt = {
    "role": "system",
    "content": "Ti si GymGator pomočnik, strokovnjak za fitnes in zdravo prehrano. Odgovarjaj izključno v slovenščini. Bodi motivacijski in prijazen. Če te kdo vpraša kaj, kar ni povezano s športom ali prehrano, vljudno odgovori, da si specializiran le za GymGator področje."
}

# 4. Spomin klepeta
if "messages" not in st.session_state:
    st.session_state.messages = []

# Prikaz zgodovine
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Vnos uporabnika
if prompt := st.chat_input("Kako vam lahko GymGator pomaga?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generiranje odgovora preko Groq (Uporabljamo NOVEJŠI model Llama 3.1)
    try:
        chat_completion = client.chat.completions.create(
            messages=[system_prompt] + st.session_state.messages,
            model="llama-3.1-8b-instant",  # TA MODEL JE AKTIVEN IN DELUJE
        )
        
        response_text = chat_completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        st.error(f"Prišlo je do napake pri povezavi z Groq strežnikom: {e}")
